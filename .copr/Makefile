srpm:
	dnf install -y git rpmdevtools
	spectool --define "_sourcedir $(PWD)" --sourcedir -g "$(spec)"
	rpmbuild -bs "$(spec)" \
		--define "_srcrpmdir $(outdir)" \
		--define "_sourcedir $(PWD)"
