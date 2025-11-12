set -e

source ./setup-python-env.sh

echo -e "${BOLD_YELLOW}Updating package versions...$RESET"

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
