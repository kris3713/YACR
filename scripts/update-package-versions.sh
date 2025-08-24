echo '----- Installing Python packages -----'
echo '> pip install uv'
pip install uv
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
echo '---------------------------------------'
echo '---------------------------------------'

for i in $(fd 'update-script' .); do
  chmod +x $i
  echo "Executing $i"; $i
  chmod -x $i
  echo '---------------------------------------'
  echo '---------------------------------------'
done
