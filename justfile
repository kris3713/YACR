# Builds a package in COPR based on it's spec file and/or it's pkg directory
build-to-copr *ARGS:
  ./scripts/build-to-copr {{ARGS}}

# Builds rpm packages safely by executing all the required commands in an ultramarine-linux container.
build-in-container *ARGS:
  ./scripts/build-in-container {{ARGS}}

# Enable/disable webhook-rebuild for a package based on it's spec file and/or it's pkg directory
change-packages *ARGS:
  ./scripts/change-packages {{ARGS}}
