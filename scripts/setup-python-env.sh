set -e

RESET='\033[0m'
RED='\033[0;31m'
BOLD_RED='\033[1;31m'
YELLOW='\033[0;33m'
BOLD_YELLOW='\033[1;33m'

echo -e "\n${YELLOW}Setting up Python environment...$RESET"

if ! command -v python &> /dev/null; then
  echo -e "${BOLD_RED}ERROR: ${RESET}${RED}\`python\` not found, please install it first$RESET"
  exit 1
fi

# The reason for installing uv from conda/conda-forge (with Pixi) is because
# it provides the latest version, unlike nixpkgs.
if ! command -v uv &> /dev/null; then
  #shellcheck disable=SC2016
  echo 'eval "$(pixi shell-hook --shell bash)"'
  # Sets up the Pixi environment (which includes the installation of `uv`)
  # and hooks it into our current shell.
  eval "$(pixi shell-hook --shell bash)"
fi

# # The reason for installing uv from pip is because
# # it provides the latest version, unlike nixpkgs.
# if ! command -v uv &> /dev/null; then
#   echo '> pip install uv --user'
#   pip install uv --user
# fi

if [ ! -d './scripts/.venv' ]; then
  echo -e "${BOLD_YELLOW}Installing Python packages...$RESET"
  echo '> cd ./scripts'
  cd ./scripts
  echo '> uv venv'
  uv venv
  echo '> source ./.venv/bin/activate'
  source ./.venv/bin/activate
  echo '> uv pip install -r ./requirements.txt'
  uv pip install -r ./requirements.txt
  echo '> cd ..'
  cd ..
fi
