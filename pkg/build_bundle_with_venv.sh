#!/bin/bash
###########################################################
# Build a Bitmask bundle inside a fresh virtualenv.
# To be run by Gitlab Runner,
# will produce an artifact for each build.
###########################################################
virtualenv venv
source venv/bin/activate
$VIRTUAL_ENV/bin/pip install -U pyinstaller==3.1 packaging
$VIRTUAL_ENV/bin/pip install zope.interface zope.proxy

# For the Bitmask 0.9.5 bundles.
#$VIRTUAL_ENV/bin/pip install -U leap.soledad.common==0.9.3
#$VIRTUAL_ENV/bin/pip install -U leap.soledad.client==0.9.3

# CHANGE THIS IF YOU WANT A DIFFERENT BRANCH CHECKED OUT FOR COMMON/SOLEDAD --------------------
$VIRTUAL_ENV/bin/pip install -U leap.soledad.common --find-links https://devpi.net/kali/dev 
$VIRTUAL_ENV/bin/pip install -U leap.soledad.client --find-links https://devpi.net/kali/dev 
# ----------------------------------------------------------------------------------------------

# XXX hack for the namespace package not being properly handled by pyinstaller
touch $VIRTUAL_ENV/lib/python2.7/site-packages/zope/__init__.py
touch $VIRTUAL_ENV/lib/python2.7/site-packages/leap/soledad/__init__.py

make dev-all

$VIRTUAL_ENV/bin/pip uninstall leap.bitmask
$VIRTUAL_ENV/bin/pip install .

# install pixelated from kali dev repo until assets get packaged.
pip install pixelated_www pixelated_user_agent --find-links https://devpi.net/kali/dev

make bundle
make bundle_gpg
