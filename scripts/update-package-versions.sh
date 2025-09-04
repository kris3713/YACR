set -e

BOLD=$(tput bold)
RESET=$(tput sgr0)
RED=$(tput setaf 1)
YELLOW=$(tput setaf 3)

if ! command -v pip &> /dev/null; then
  echo "${BOLD}${RED}ERROR: ${RESET}${RED}\`pip\` not found, please install it first$RESET"
  exit 1
elif ! command -v python &> /dev/null; then
  echo "${BOLD}${RED}ERROR: ${RESET}${RED}\`python\` not found, please install it first$RESET"
  exit 1
fi

# The reason for installing uv from pip is because
# it provides the latest version, unlike nixpkgs
if ! command -v uv &> /dev/null; then
  echo '> pip install uv --user'
  pip install uv --user
fi

if [ ! -d './scripts/.venv' ]; then
  echo "${BOLD}${YELLOW}Installing Python packages...$RESET"
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

echo "${BOLD}${YELLOW}Updating package versions...$RESET"

for i in 'fd' 'sd' 'rg' 'fish'; do
  if ! command -v $i &> /dev/null; then
    #shellcheck disable=SC2016
    echo "${BOLD}${RED}ERROR: ${RESET}${RED}\`$i\` not found, please install it first$RESET"
    exit 1
  fi
done

for i in $(fd 'update-script' .); do
  echo '---------------------------------------'
  #shellcheck disable=SC2086
  chmod +x $i
  echo "Executing $i"; $i
  #shellcheck disable=SC2086
  chmod -x $i
  echo '---------------------------------------'
done
