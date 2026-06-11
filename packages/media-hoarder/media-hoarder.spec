%global         debug_package %nil
%global         app_name Media-Hoarder
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         git_url https://github.com/theMK2k/%{app_name}
%global         ws_name %(v="%{app_name}"; echo "${v/-/ }")

Name:           %(echo %app_name | tr '[:upper:]' '[:lower:]')
Version:        1.5.4
Release:        1%{?dist}
Summary:        %ws_name - THE media frontend for data hoarders and movie lovers

License:        Freeware (See LICENSE.md)
URL:            https://media.hoarder.software/

Source0:        %{git_url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  mise
Requires:       mediainfo

# Currently, the application is only available for 64bit platforms
ExclusiveArch:  x86_64

%description
%ws_name is THE frontend for your Movie and TV Series collection if you love metadata, filter abilities and easy management.

Features:

- Automatically scans your movies and tv series (local or NAS, you define the source paths)
- Gathers metadata using mediainfo and imdb.com
- Provides a frontend to browse your collection and play your media (running the media player of your choice, e.g. VLC)

%prep
%autosetup -n ./%{app_name}-%{version}


%build
# Change the node cache dir
export npm_config_cache="$(readlink -f ./.node_cache)"

# Change the electron cache dir
export ELECTRON_CACHE="$(realpath ./.electron_cache)"
export ELECTRON_BUILDER_CACHE="$(realpath ./.electron_builder_cache)"

# Setup mise, and install nodejs
export MISE_GLOBAL_CONFIG_FILE=''
export MISE_CACHE_DIR="$(realpath ./.mise_cache)"
export MISE_DATA_DIR="$(realpath ./.mise_data)"
mise install node@24
NODE_PATH="$(mise where node@24)"

# Add the executables to the PATH
export PATH="$PATH:$NODE_PATH/bin"

# Update the caniuse-lite database
npx -y update-browserslist-db@latest
./fetch-easylist.sh

# Install the dependencies
env NODE_ENV='dev' npm install

# Set NODE_ENV to production
export NODE_ENV='production'

# Build the appplication
node set-portable --portable=false
npx -y electron-vite build
npx -y electron-builder build --linux --dir --x64


%install
# Create important dirs in the buildroot
install -d %{buildroot}{/opt/%{app_name},%{_bindir},%{_datadir}/applications}

sizes=(
  '16x16' '24x24'
  '32x32' '48x48'
  '64x64' '128x128'
  '180x180' '192x192'
  '256x256' '512x512'
  '1024x1024'
)
for size in "${sizes[@]}"; do
  install -d "%{buildroot}%{_iconsdir}/hicolor/$size/apps"
done

# Copy the application files to the application directory
cp -a ./dist/linux-unpacked/* %{buildroot}/opt/%{app_name}

# Create a symbolic link to the application executable
ln -s /opt/%{app_name}/%{name} -t %{buildroot}%{_bindir}

# Install the application desktop file
CONTENT="$(cat << 'DESKTOP'
[Desktop Entry]
Name=%ws_name
Exec=%name
Terminal=false
Type=Application
Icon=%name
StartupWMClass=%ws_name
Comment=%summary
Categories=AudioVideo
DESKTOP
)"
install -Dm 0644 /dev/stdin %{buildroot}%{_datadir}/applications/%{name}.desktop <<< "$CONTENT"

# Install the application icons
install -Dm 0644 ./icon/mh1/mh1.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

for size in "${sizes[@]}"; do
  install -Dm 0644 "./build/icons/$size.png" "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{name}.png"
done


%files
/opt/%{app_name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*
%license ./LICENSE.md
%doc ./README.md


%changelog
%autochangelog
