﻿.. _release:

Bitmask Release Checklist
=========================

CI check
--------
* [ ] Check that all tests are passing!
* [ ] Fix any broken tests.

Version bumps and Tagging
-------------------------
* [ ] Update pkg/next-release
* [ ] Update release-notes.rst in leap.bitmask if needed.
* [ ] Update version in bitmask_client/pkg/linux/bitmask-root if needed.

* [ ] Tag everything. Should be done for the following packages, in order:
* [ ] 1. leap.common
* [ ] 2. leap.keymanager
* [ ] 3. leap.soledad
* [ ] 4. leap.mail
* [ ] 5. leap.bitmask
* [ ] 6. leap.mx

* NOTE: It's assumed that origin is the leap.se repo

* [ ] git fetch origin
* [ ] git tag -l, and see the latest tagged version (unless it's not a minor version bump, in which case, just bump to it)
* [ ] export version: export RELEASE=0.9.0
* [ ] git checkout `release/0.9.x`
- NOTE: the release branch is created when the first release candidate
  is tagged, after that the bugfixes and features that are meant to be
  shipped with the specific version that we are targetting are merged in that branch
* [ ] git checkout -b release/$RELEASE (this is a LOCAL branch, never published).
* [ ] (maybe) cherry-pick specific commits
* [ ] (maybe) add special fixes for this release

* [ ] Review pkg/requirements.pip for everything, update if needed (that's why the order).
  - See whatever has been introduced in changes/VERSION_COMPAT
  - Reset changes/VERSION_COMPAT
  - Bump all the leap-requirements altogether.
* [ ] git commit -am "Update requirements file"

* [ ] Merge changes/next-changelog.rst into the CHANGELOG
  - NOTE: in leap.soledad, 3 sections (common, client, server).
* [ ] reset changes/next-changelog.rst
* [ ] git commit -S -m "[pkg] Update changelog"

* [ ] git tag --sign $RELEASE -m "Tag version $RELEASE"

* If everything went ok, push the changes, and merge back into master&develop:
* [ ] git checkout release/0.9.x && git merge $RELEASE
* [ ] git push origin release/0.9.x
* [ ] git push origin $RELEASE
* [ ] git checkout master && git pull origin master && git merge --no-edit $RELEASE
* [ ] git checkout develop && git merge $RELEASE && git push origin develop

Bundles
-------
* [ ] Build and upload bundles
* [ ] Use 'make pyinst-linux' to build bundles.
* [ ] Sign: make pyinst-sign
* [ ] Upload bundle and signature to downloads.leap.se/client/<os>/Bitmask-<os>-<ver>.(tar.bz2,dmg,zip)
* [ ] make pyinst-upload
* [ ] Update symbolic link for latest upload and signature:
* [ ] ~/public/client/Bitmask-<os>-latest
* [ ] ~/public/client/Bitmask-<os>-latest.asc

TUF: Relese candidate bundles: RC# (skipped for now)
----------------------------------------------------

* [ ] Upload the TUF unstable repo
* [ ] Upload bundle to staging for release-candidate
* [ ] Sign the bundles, move it to client downloads (micah)
* [ ] Update symlinks for -latest
* [ ] Fix all show stoppers

TUF: Stable bundles (skipped for now)
-------------------------------------
* [ ] Upload the TUF Stable Repo to staging
* [ ] Upload bundle to staging for stable
* [ ] move and sign the TUF repo (kwadro)
* [ ] Sign the bundles, move it to client downloads (micah)
* [ ] Update symlinks for -latest
  
Debian packages
---------------
* TBD...

Pypi upload
---------------
* [ ]  python setup.py sdist upload --sign -i kali@leap.se -r pypi

Announcing
---------------
* [ ] Announce (use release-notes.rst)
 * [ ] Mail leap@lists.riseup.net
 * [ ] Twitter
 * [ ] Gnusocial
 * [ ] Post in leap.se
 * [ ] reddit
 * [ ] hackernews
