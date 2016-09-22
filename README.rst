Bitmask
=======================================

*Your internet encryption toolkit*

.. image:: https://badge.fury.io/py/leap.bitmask.svg
    :target: http://badge.fury.io/py/leap.bitmask
.. image:: https://img.shields.io/badge/IRC-leap-blue.svg
   :target: http://webchat.freenode.net/?channels=%23leap&uio=d4
   :alt: IRC
.. image:: https://img.shields.io/badge/IRC-bitmask_(es)-blue.svg
   :target: http://webchat.freenode.net/?channels=%23bitmask-es&uio=d4
   :alt: IRC-es


**Bitmask** is the client for the services offered by `the LEAP Platform`_. It
contains a command-line interface and a multiplatform desktop client. It can be
also used as a set of libraries to communicate with the different services from
third party applications.

It is written in python using `Twisted`_  and licensed under the `GPL3`_. The
Graphical User Interface is written in html+js and uses `PyQt5`_ for serving the
application.

.. _`the LEAP Platform`: https://github.com/leapcode/leap_platform
.. _`Twisted`: https://twistedmatrix.com
.. _`PyQt5`: https://pypi.python.org/pypi/PyQt5
.. _`GPL3`: http://www.gnu.org/licenses/gpl.txt

Package under development!
---------------------------------------

This is a unified repo that has merged the following packages, previously isolated, under the leap namespace:

bonafide, mail, keymanager, bitmask.

The previous Qt client has been deprecated (bitmask version 0.8.2, still
available at the http://github.com/leapcode/bitmask_client repo).

Note that this repo still doesn't have support for VPN: its porting will
follow soon.

Read the Docs!
---------------------------------------

The latest documentation about Bitmask is available at `LEAP`_.

.. _`LEAP`: https://leap.se/en/docs/client

Bugs
=======================================

Please report any bugs `in our bug tracker`_.

.. _`in our bug tracker`: https://leap.se/code/projects/report-issues


Development
=======================================

Running Tests
---------------------------------------

You need tox to run the tests. If you don't have it in your system yet::

  pip install tox

And then run all the tests::

  tox


Hacking
----------------------------------

In order to run bitmask in a development environment, you must activate a
virtualenv and install the various packages using 'pip install -e'. This
installs python packages as links to the source code, so that your code
changes are immediately reflected in the packages installed in the virtualenv.

All this is done for you with the Makefile. For example, if you want to
develop for the encrypted mail service::

  virtualenv venv
  source venv/bin/activate
  make dev-mail

If you want to develop for the gui client too, you have to have
installed the python2 bindings for Qt5 in your system (in debian: ``apt
install python-pyqt5  python-pyqt5.qtwebkit``). After ensuring this, you can
do::

  make dev-all

Note: even though the UI is in javascript. Qt is used to create a webview
window.

hacking on the javascript UI
+++++++++++++++++++++++++++++++++++++++

The above instructions will install a python package that contains a pre-
bundled version of the javascript UI.

If you want to hack on the javascript UI, then it needs to be able to update the
javascript bundle whenever a javascript or CSS source file changes.

First, install the javascript prerequisites:

  sudo apt install nodejs npm nodejs-legacy

Next, run ``dev-install``:

  source venv/bin/activate    # if not already activated
  cd ui
  make dev-install            # install JS user interface as a python package in "develop" mode.
  node run watch              # continually rebuild javascript bundle when source files change.

For more information, see ``ui/README.md``.

cross-testing
+++++++++++++++++++++++++++++++++++++++

If you are developing against a non-published branch of ``leap.common`` or
``leap.soledad``, run instead::

  tox -e py27-dev

This expects ``leap_common`` and ``soledad`` repos to be checked out in the
parent folder.


License
=======================================

.. image:: https://raw.github.com/leapcode/bitmask_client/develop/docs/user/gpl.png

Bitmask is released under the terms of the `GNU GPL version 3`_ or later.

.. _`GNU GPL version 3`: http://www.gnu.org/licenses/gpl.txt
