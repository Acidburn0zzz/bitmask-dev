from os import makedirs
from os.path import abspath, join, isfile, isdir

from twisted.python import logfile

from leap.common.config import get_path_prefix


def loggerFactory():
    configdir = abspath(join(get_path_prefix(), 'leap'))
    if not isdir(configdir):
        makedirs(configdir)
    log_path = abspath(join(get_path_prefix(), 'leap', 'bitmaskd.log'))
    rotate = isfile(log_path)
    _logfile = logfile.LogFile.fromFullPath(log_path, maxRotatedFiles=5)
    if rotate:
        _logfile.rotate()
    return _logfile
