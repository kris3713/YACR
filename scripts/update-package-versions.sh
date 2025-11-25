set -e

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

source "$SCRIPT_DIR/setup-python-env.sh"

BOLD_GREEN='\e[1;32m'

echo -e "${BOLD_GREEN}Updating package versions...$RESET"

for i in 'fd' 'sd' 'rg' 'fish'; do
  if ! command -v $i &> /dev/null; then
    #shellcheck disable=SC2016
    echo -e "${BOLD_RED}ERROR: ${RESET}${RED}\`$i\` not found, please install it first$RESET"
    exit 1
  fi
done

for i in $(fd 'update-script' .); do
  echo '---------------------------------------'
  echo "Executing $i"; "$i"
  echo '---------------------------------------'
done
