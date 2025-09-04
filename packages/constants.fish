# A regex for capturing alpha-numeric versions with extra characters
set -gx ALPHA_NUM_VERSION_REGEX_EXTRA '([\\w]+.*)'

# A regex for capturing alpha-numeric versions
set -gx ALPHA_NUM_VERSION_REGEX '([\\w.]+)'

# A regex for capturing numeric versions
set -gx VERSION_REGEX '([\\d.]+)'
