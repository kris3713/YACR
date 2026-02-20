%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         app_name Kuro
%global         debug_package %nil

Name:           %(echo %app_name | tr '[:upper:]' '[:lower:]')
Version:        9.1.3
Release:        2%{?dist}
Summary:        An elegant Microsoft ToDo desktop client for Linux (a fork of Ao)

License:        MIT
URL:            https://github.com/davidsmorais/%{name}

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  electron nodejs yarnpkg

ExclusiveArch:  x86_64

%description
%app_name is an unofficial, featureful, open source,
community-driven, free Microsoft To-Do app for Linux


%prep
%autosetup -n ./%{name}-%{version}


%build
%if %{?fedora} >= 44
  mkdir -v ./extra_bin
  ln -sv $(command -v node-22) ./extra_bin/node
  export PATH="$PATH:$(realpath ./extra_bin)"
%endif

# Ensure nodejs does not download
# an electron executable.
export ELECTRON_SKIP_BINARY_DOWNLOAD=1
export ELECTRON_OVERRIDE_DIST_PATH='%{_libdir}/electron'

# Ensure yarn (or npm if ever used) stores it's
# config in a relative location
export npm_config_cache="$(realpath ./.yarn_cache)"
export ELECTRON_CACHE="$(realpath ./.electron_cache)"
export ELECTRON_BUILDER_CACHE="$(realpath ./.electron_builder_cache)"
export YARN_CACHE_FOLDER="$npm_config_cache"
export YARN_GLOBAL_FOLDER="$(realpath ./.yarn_config)"

# Clean install all node dependencies
env NODE_ENV='dev' yarn install

# Build the application
export NODE_ENV='production'
yarn run release --linux --x64 --dir \
  "-c.electronDist=$ELECTRON_OVERRIDE_DIST_PATH" \
  "-c.electronVersion=$(cat $ELECTRON_OVERRIDE_DIST_PATH/version)"


%install
# Create the new build root
install -d %{buildroot}{%{_bindir},/opt/%{app_name},%{_datadir}/applications}

sizes=(
  '16x16' '24x24' '32x32' '48x48' '64x64'
  '128x128' '256x256' '512x512' '1024x1024'
)
for size in "${sizes[@]}"; do
  install -d "%{buildroot}%{_iconsdir}/hicolor/$size/apps"
done

# Copy the application files to the application directory
cp -a ./dist/linux-unpacked/* %{buildroot}/opt/%{app_name}

# Create a symbolic link to the application binary
ln -s /opt/%{app_name}/%{name}-desktop -t %{buildroot}%{_bindir}

# Install the desktop file
CONTENT="$(cat << 'DESKTOP'
[Desktop Entry]
Name=%app_name
Exec=%name
Terminal=false
Type=Application
Icon=%name
StartupWMClass=%app_name
Comment=%app_name is an unofficial, featureful Microsoft ToDo desktop client for Linux (a fork of Ao).
Categories=Office
DESKTOP
)"
install -Dm 0644 /dev/stdin %{buildroot}%{_datadir}/applications/%{name}.desktop <<< "$CONTENT"

# Install the application icons
for size in "${sizes[@]}"; do
  install -Dm 0644 "./build/icons/png/$size.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{name}.png"
done


%files
%{_bindir}/%{name}-desktop
/opt/%{app_name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%license ./license.md
%doc ./{readme.md,docs/devlog.md}


%changelog
%autochangelog
