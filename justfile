# Builds a package in COPR based on it's spec file and/or it's pkg directory
build-to-copr *ARGS:
  ./scripts/build-to-copr {{ARGS}}

# Builds rpm packages safely by executing all the required commands in an ultramarine-linux container.
build-in-container *ARGS:
  ./scripts/build-in-container {{ARGS}}

# Enable/disable webhook-rebuild for a package based on it's spec file and/or it's pkg directory.
change-packages *ARGS:
  ./scripts/change-packages {{ARGS}}

# Removes any leftover residue made by rpmbuild.
wipetree:
  rm -rfv \
    ./build/BUILD/* \
    ./build/SOURCES/* \
    ./build/RPMS/* \
    ./build/SRPMS/* \
    ./build/SPECS/*

# Tests a packages update-script if it exists.
test-update-script pkg_name:
  #!/usr/bin/env sh

  if [ -f ./packages/{{pkg_name}}/update-script ]; then
    ./packages/{{pkg_name}}/update-script
  else
    echo 'update-script for pkg {{pkg_name}} does not exist!'
    exit 1
  fi

# Same as change-packages but only takes two args to afffect multiple packages.
batch-change-packages webhook_rebuild pkg_name: # Best used with cudatext
  fd -g '{{pkg_name}}*.spec' --exec \
    just --justfile {{justfile()}} \
    change-packages {{webhook_rebuild}} {{pkg_name}} '{/.}'
