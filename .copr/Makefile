srpm:
	dnf group install -y rpm-development-tools development-tools
	rpmbuild -bs ./packages/atuin/atuin.spec \
		--define "_srcrpmdir $(outdir)"
    # --define "_sourcedir $(PWD)"
