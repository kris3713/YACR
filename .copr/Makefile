srpm:
	dnf group install -y rpm-development-tools development-tools
	spectool --define "_sourcedir $(PWD)" --sourcedir -g "$(spec)"
	rpmbuild -bs "$(spec)" \
		--define "_srcrpmdir $(outdir)" \
		--define "_sourcedir $(PWD)"
