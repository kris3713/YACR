srpm:
	dnf install -y git rpm-development-tools
	spectool --define "_sourcedir $(PWD)" --sourcedir -g "$(spec)"
	rpmbuild -bs "$(spec)" \
		--define "_srcrpmdir $(outdir)" \
		--define "_sourcedir $(PWD)"
