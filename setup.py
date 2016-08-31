"""
Setup file for leap.bitmask
"""
from setuptools import setup, find_packages
import versioneer

# This requirements list is curated by hand. Here we can specify ranges.
requirements =  [
    "twisted",
    "colorama"]


trove_classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: End Users/Desktop",
    ("License :: OSI Approved :: GNU General "
     "Public License v3 or later (GPLv3+)"),
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Topic :: Communications",
    'Topic :: Communications :: Email',
    "Topic :: Security",
    'Topic :: Security :: Cryptography',
    "Topic :: Utilities"
]

DOWNLOAD_BASE = ('https://github.com/leapcode/bitmask-dev/'
                 'archive/%s.tar.gz')

VERSION = versioneer.get_version()
DOWNLOAD_URL = DOWNLOAD_BASE % VERSION



gui_launcher = 'bitmask=leap.bitmask.gui.app:start_app'
bitmask_cli = 'bitmaskctl=leap.bitmask.cli.bitmask_cli:main'
bitmaskd = 'bitmaskd=leap.bitmask.core.launcher:run_bitmaskd'


setup(
    name='leap.bitmask',
    version=VERSION,
    cmdclass = versioneer.get_cmdclass(),
    url='https://leap.se/',
    download_url=DOWNLOAD_URL,
    license='GPLv3+',
    author='The LEAP Encryption Access Project',
    author_email='info@leap.se',
    maintainer='Kali Kaneko',
    maintainer_email='kali@leap.se',
    description=("The Internet Encryption Toolkit: "
                 "Encrypted Internet Proxy and Encrypted Mail."),
    long_description = open('README.rst').read(),
    classifiers=trove_classifiers,
    namespace_packages=["leap"],
    package_dir={'': 'src'},
    package_data={'': ['*.pem']},
    packages=find_packages('src'),
    install_requires=requirements,
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'console_scripts': [gui_launcher, bitmask_cli, bitmaskd]
    },
)
