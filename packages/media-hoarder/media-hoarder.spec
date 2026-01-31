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

# Needed for creating a non-portable variant
Patch0:         package.json_diff.patch

BuildRequires:  git mise
Requires:       mediainfo

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
git remote add origin %{git_url}.git
git fetch --tags -q
git checkout -fb 'v%{version}' 'v%{version}'
# Apply the patch
%autopatch


%build
# Change the node cache dir to avoid errors in COPR's cloud environment
export npm_config_cache="$(readlink -f ./.node_cache)"

# Setup mise, and install nodejs
export MISE_GLOBAL_CONFIG_FILE=''
export MISE_CACHE_DIR="$(realpath ./.mise_cache)"
export MISE_DATA_DIR="$(realpath ./.mise_data)"
mise install node@14.17.5
NODE_PATH="$(mise where node@14.17.5)"

# Add the executables to the PATH
export PATH="$PATH:$NODE_PATH/bin"

# # Change prefix for npm
# npm config set prefix "$NODE_PATH"

# Install the dependencies
env NODE_ENV='dev' npm install

# Update the `caniuse-lite` database
export NODE_ENV='production'
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
