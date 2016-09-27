# This makefile should be called from the topmost bitmask folder
#
bundle: bundle_clean
	pyinstaller -y pkg/pyinst/app.spec
	cp $(VIRTUAL_ENV)/lib/python2.7/site-packages/_scrypt.so $(DIST)
	cp src/leap/bitmask/core/bitmaskd.tac $(DIST)
	mkdir $(DIST)/leap
	cp -r $(VIRTUAL_ENV)/lib/python2.7/site-packages/leap/bitmask_js/  $(DIST)/leap
	mv $(DIST) _bundlelib && mkdir $(DIST_VERSION) && mv _bundlelib $(DIST_VERSION)/lib
	cd pkg/launcher && make
	cp pkg/launcher/bitmask $(DIST_VERSION)

bundle_tar:
	cd dist/ && tar cvzf Bitmask.$(NEXT_VERSION).tar.gz bitmask-$(NEXT_VERSION)

bundle_sign:
	gpg2 -a --sign --detach-sign dist/Bitmask.$(NEXT_VERSION).tar.gz 

bundle_upload:
	rsync --rsh='ssh' -avztlpog --progress --partial dist/Bitmask.$(NEXT_VERSION).* salmon.leap.se:./

bundle_clean:
	rm -rf dist build

