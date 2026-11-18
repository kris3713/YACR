# Builds a package in COPR based on it's spec file and/or it's pkg directory
build-to-copr *ARGS:
  ./scripts/build-to-copr {{ARGS}}

# Builds rpm packages safely by executing all the required commands in an ultramarine-linux container.
build-in-container *ARGS:
  ./scripts/build-in-container {{ARGS}}

# Enable/disable webhook-rebuild for a package based on it's spec file and/or it's pkg directory
change-packages *ARGS:
  ./scripts/change-packages {{ARGS}}

# Tests a packages update-script if it exists
test-update-script pkg_name:
  #!/usr/bin/env sh

  set -x

  if [ -f ./packages/{{pkg_name}}/update-script ]; then
    ./packages/{{pkg_name}}/update-script
  else
    echo 'update-script for pkg {{pkg_name}} does not exist!'
    exit 1
  fi
