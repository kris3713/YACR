set -e

echo '----- Installing Python packages -----'

if ! command -v pip &> /dev/null; then
  #shellcheck disable=SC2016
  echo '`pip` not found, please install it first'
  exit 1
elif ! command -v python &> /dev/null; then
  #shellcheck disable=SC2016
  echo '`python` not found, please install it first'
  exit 1
fi

# The reason for installing uv from pip is
# because it provides the latest version, unlike nixpkgs
echo '> pip install uv --user'
pip install uv --user

if ! command -v uv &> /dev/null; then
  #shellcheck disable=SC2016
  echo '`uv` not found, please install it first'
  exit 1
fi

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

echo '----- Updating package versions -----'

for i in 'fd' 'sd' 'rg' 'fish'; do
  if ! command -v $i &> /dev/null; then
    #shellcheck disable=SC2016
    echo "\`$i\` not found, please install it first"
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
