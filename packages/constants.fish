# just in case sourcing the environment variables from bash isn't enough
set -l script_dir (status dirname)
source "$script_dir/../scripts/.venv/bin/activate.fish"

# A regex for capturing alpha-numeric versions with extra characters
set -gx ALPHA_NUM_VERSION_REGEX_EXTRA '([\\w]+.*)'

# A regex for capturing alpha-numeric versions
set -gx ALPHA_NUM_VERSION_REGEX '([\\w.]+)'

# A regex for capturing numeric versions
set -gx VERSION_REGEX '([\\d.]+)'
