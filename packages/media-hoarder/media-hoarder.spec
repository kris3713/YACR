%global         debug_package %{nil}
%global         app_name Media-Hoarder
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         git_url https://github.com/theMK2k/%{app_name}

Name:           media-hoarder
Version:        1.4.6
Release:        1%{?dist}
Summary:        %{app_name} - THE media frontend for data hoarders and movie lovers

License:        Freeware (See LICENSE.md)
URL:            https://media.hoarder.software/

Source0:        %{git_url}/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}.desktop
# This is needed since the project has dependencies
# that don't work beyond NodeJS version 14.17.5.
Source2:        https://nodejs.org/dist/v14.17.5/node-v14.17.5-linux-x64.tar.xz

# Needed for creating a non-portable variant
Patch:          package.json_diff.patch

BuildRequires:  git

# Currently, the application is only available for 64bit platforms
ExclusiveArch:  x86_64

%description
%{app_name} is THE frontend for your Movie and TV Series collection if you love metadata, filter abilities and easy management.

Features:

- Automatically scans your movies and tv series (local or NAS, you define the source paths)
- Gathers metadata using mediainfo and imdb.com
- Provides a frontend to browse your collection and play your media (running the media player of your choice, e.g. VLC)

%prep
%setup -q -n ./%{app_name}-%{version}
# Git is needed so the build doesn't fail
git init -q
git remote add origin %{git_url}
git fetch --tags -q
git checkout -fb 'v%{version}' 'v%{version}'
# Apply the patch
%autopatch


%build
# Change the node cache dir to avoid errors in COPR's cloud environment
mkdir -v ./.node_cache
NEW_CACHE_DIR="$(readlink -f ./.node_cache)"
export npm_config_cache="$NEW_CACHE_DIR"

# Unpack the precompiled NodeJS executable binaries
mkdir -v ./node-bin
tar -xJf %{SOURCE2} '--strip-components=1' -C ./node-bin
NODE_PATH="$(readlink -f ./node-bin)"

# Add the executables to the PATH (tmp)
NODE_BIN_PATH="$NODE_PATH/bin"
export PATH="$PATH:$NODE_BIN_PATH"

# Change prefix for npm
npm config set prefix "$NODE_PATH"

# Install the dependencies
npm install

# Update the `caniuse-lite` database
npx --verbose -y browserslist@latest --update-db
# npx --verbose -y update-browserslist-db@latest

# Build the appplication
npm run 'electron:build-linux-non-portable'


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
cp -a ./RELEASE/media-hoarder_linux/* %{buildroot}/opt/%{app_name}

# Create a symbolic link to the application executable
ln -s /opt/%{app_name}/%{name} -t %{buildroot}%{_bindir}

# Install the application desktop file
install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application icons
for size in "${sizes[@]}"; do
  install -Dm 0644 "./build/icons/$size.png" -t "%{buildroot}%{_iconsdir}/hicolor/$size/apps"
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
