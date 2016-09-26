# -*- coding: utf-8 -*-
# launcher.py
# Copyright (C) 2016 LEAP
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
Run bitmask daemon.
"""
from os.path import join, abspath
from sys import argv

from twisted.scripts.twistd import run

from leap.bitmask.util import here
from leap.bitmask import core
from leap.bitmask.core import flags
from leap.common.config import get_path_prefix

pid = abspath(join(get_path_prefix(), 'leap', 'bitmaskd.pid'))


def run_bitmaskd():
    # TODO --- configure where to put the logs... (get --logfile, --logdir
    # from the bitmask_cli
    for (index, arg) in enumerate(argv):
        if arg == '--backend':
            flags.BACKEND = argv[index + 1]
    argv[1:] = [
        '-y', join(here(core), "bitmaskd.tac"),
        '--pidfile', pid,
        '--umask=0022',
    ]
    print '[+] launching bitmaskd...'
    run()


if __name__ == "__main__":
    run_bitmaskd()
