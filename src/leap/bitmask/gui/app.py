# -*- coding: utf-8 -*-
# app.py
# Copyright (C) 2016 LEAP Encryption Acess Project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Main entrypoint for the Bitmask Qt GUI.
It just launches a wekbit browser that runs the local web-ui served by bitmaskd
when the web service is running.
"""

import os
import platform
import signal
import sys

from functools import partial
from multiprocessing import Process

from leap.bitmask.core.launcher import run_bitmaskd, pid
from leap.bitmask.gui import app_rc
from leap.common.config import get_path_prefix


if platform.system() == 'Windows':
    from multiprocessing import freeze_support
    from PySide import QtCore, QtGui
    from PySide import QtWebKit
    from PySide.QtGui import QDialog
    from PySide.QtGui import QApplication
    from PySide.QtWebKit import QWebView, QGraphicsWebView
    from PySide.QtCore import QSize
else:
    from PyQt5 import QtCore, QtGui
    from PyQt5 import QtWebKit
    from PyQt5.QtCore import QSize
    from PyQt5.QtCore import QObject, pyqtSlot
    from PyQt5.QtWidgets import QDialog
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWebKitWidgets import QWebView
    from PyQt5.QtWebKit import QWebSettings


BITMASK_URI = 'http://localhost:7070/'
PIXELATED_URI = 'http://localhost:9090/'

IS_WIN = platform.system() == "Windows"
DEBUG = os.environ.get("DEBUG", False)

qApp = None
bitmaskd = None


class BrowserWindow(QWebView):
    def __init__(self, *args, **kw):
        url = kw.pop('url', None)
        first = False
        if not url:
            url = "http://localhost:7070"
            path = os.path.join(get_path_prefix(), 'leap', 'authtoken')
            token = open(path).read().strip()
            url += '#' + token
            first = True
        self.url = url
        self.closing = False

        super(QWebView, self).__init__(*args, **kw)
        self.bitmask_browser = NewPageConnector(self) if first else None
        self.loadPage(self.url)

    def loadPage(self, web_page):
        self.settings().setAttribute(
            QWebSettings.DeveloperExtrasEnabled, True)

        if os.environ.get('DEBUG'):
            self.inspector = QWebInspector(self)
            self.inspector.setPage(self.page())
            self.inspector.show()

        if os.path.isabs(web_page):
            web_page = os.path.relpath(web_page)

        url = QtCore.QUrl(web_page)
        self.frame = self.page().mainFrame()
        self.frame.addToJavaScriptWindowObject(
            "bitmaskBrowser", self.bitmask_browser)
        self.load(url)

    def shutdown(self, *args):
        if self.closing:
            return
        self.closing = True
        global bitmaskd
        bitmaskd.join()
        if os.path.isfile(pid):
            with open(pid) as f:
                pidno = int(f.read())
            print('[bitmask] terminating bitmaskd...')
            os.kill(pidno, signal.SIGTERM)
        print('[bitmask] shutting down gui...')
        try:
            self.stop()
            try:
                global pixbrowser
                pixbrowser.stop()
                del pixbrowser
            except:
                pass
            QtCore.QTimer.singleShot(0, qApp.deleteLater)

        except Exception as ex:
            print('exception catched: %r' % ex)
            sys.exit(1)


pixbrowser = None


class NewPageConnector(QObject):

    @pyqtSlot()
    def openPixelated(self):
        global pixbrowser
        pixbrowser = BrowserWindow(url=PIXELATED_URI)
        pixbrowser.show()


def _handle_kill(*args, **kw):
    win = kw.get('win')
    if win:
        QtCore.QTimer.singleShot(0, win.close)
    global pixbrowser
    if pixbrowser:
        QtCore.QTimer.singleShot(0, pixbrowser.close)


def launch_gui():
    global qApp
    global bitmaskd

    if IS_WIN:
        freeze_support()
    bitmaskd = Process(target=run_bitmaskd)
    bitmaskd.start()

    qApp = QApplication([])
    browser = BrowserWindow(None)

    qApp.setQuitOnLastWindowClosed(True)
    qApp.lastWindowClosed.connect(browser.shutdown)

    signal.signal(
        signal.SIGINT,
        partial(_handle_kill, win=browser))

    # Avoid code to get stuck inside c++ loop, returning control
    # to python land.
    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(500)

    browser.show()
    sys.exit(qApp.exec_())


def start_app():
    from leap.bitmask.util import STANDALONE
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

    # Allow the frozen binary in the bundle double as the cli entrypoint
    # Why have only a user interface when you can have two?

    if platform.system() == 'Windows':
        # In windows, there are some args added to the invocation
        # by PyInstaller, I guess...
        MIN_ARGS = 3
    else:
        MIN_ARGS = 1

    # DEBUG ====================================
    if STANDALONE and len(sys.argv) > MIN_ARGS:
        from leap.bitmask.cli import bitmask_cli
        return bitmask_cli.main()
    launch_gui()


if __name__ == "__main__":
    start_app()
