%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         app_name Bitwarden
%global         debug_package %{nil}

%define         git_url https://github.com/%{name}/clients

Name:           %(echo %app_name | tr '[:upper:]' '[:lower:]')
Version:        2026.1.0
Release:        1%{?dist}
Summary:        A secure and free password manager for all of your devices.

License:        GPL-3.0
URL:            https://%{name}.com

Source0:        %{git_url}/archive/refs/tags/desktop-v%{version}.tar.gz

BuildRequires:  electron nodejs nodejs-npm rustup gcc gcc-c++
BuildRequires:  libsecret-devel glib2-devel atk-devel
BuildRequires:  at-spi2-atk-devel gtk3-devel libxcrypt-compat

ExclusiveArch:  x86_64

%description
%{summary}


%prep
%autosetup -n ./clients-desktop-v%{version}


%build
%if %{?fedora} >= 44
  mkdir -v ./extra_bin
  ln -sv $(command -v node-22) ./extra_bin/node
  ln -sv $(command -v npm-22) ./extra_bin/npm
  export PATH="$PATH:$(realpath ./extra_bin)"
%endif

# Ensure nodejs does not download
# an electron executable.
export ELECTRON_SKIP_BINARY_DOWNLOAD=1
export ELECTRON_OVERRIDE_DIST_PATH='%{_libdir}/electron'

# Ensure npm/electron/cargo/rustup stores
# it's config in a relative location.
export npm_config_cache="$(realpath ./.node_cache)"
export ELECTRON_CACHE="$(realpath ./.electron_cache)"
export ELECTRON_BUILDER_CACHE="$(realpath ./.electron_builder_cache)"
export CARGO_HOME="$(realpath ./.cargo)"
export RUSTUP_HOME="$(realpath ./.rustup)"

# Change where npm stores its
# user and global config
export NPM_CONFIG_USERCONFIG="$(realpath ./user_npmrc)"
export NPM_CONFIG_GLOBALCONFIG="$(realpath ./npmrc)"
touch ./user_npmrc ./npmrc

# Clean install all node dependencies
env NODE_ENV='dev' npm ci --loglevel=error

# Ensure rustup uses the nightly
# toolchain by default.
export RUSTUP_TOOLCHAIN='nightly'

# Install rustup, install rust nightly,
# and add cargo bin to PATH
rustup-init -y --no-modify-path \
  --default-toolchain $RUSTUP_TOOLCHAIN
export PATH="$PATH:$CARGO_HOME/bin"

# Build the native modules
export NODE_ENV='production'
pushd ./apps/desktop/desktop_native/napi

# Using extra arguments that will be
# passed to cargo from napi cli
BUILD_TARGET='x86_64-unknown-linux-gnu'
npm run build -- --release \
  --target $BUILD_TARGET -- "-j$(nproc)"

pushd ..

npm run build -- --release \
  --target $BUILD_TARGET

# Build the application
pushd ..

npm run build -- --release \
  --target $BUILD_TARGET
npm run 'pack:dir' -- --linux --x64 \
  "-c.electronDist=$ELECTRON_OVERRIDE_DIST_PATH" \
  "-c.electronVersion=$(cat $ELECTRON_OVERRIDE_DIST_PATH/version)"

popd


%install
# Create the new build root
install -d %{buildroot}{%{_bindir},/opt/%{app_name},%{_datadir}/applications}

sizes=('16x16' '32x32' '64x64' '128x128' '256x256' '512x512' '1024x1024')
for size in "${sizes[@]}"; do
  install -d "%{buildroot}%{_iconsdir}/hicolor/$size/apps"
done

DESKTOP_APP_DIR='./apps/desktop'
BUILD_DIR="$DESKTOP_APP_DIR/dist/linux-unpacked"
RESOURCES_DIR="$DESKTOP_APP_DIR/resources"

# Copy the application files to the application directory
cp -a "$BUILD_DIR"/* %{buildroot}/opt/%{app_name}

# Ensure chrome-sandbox has the correct permissions
chmod -v 4755 %{buildroot}/opt/%{app_name}/chrome-sandbox

# Create a symbolic link to the application binary
ln -s /opt/%{app_name}/%{name} %{buildroot}%{_bindir}

# Install the desktop file
install -Dm 0644 "$RESOURCES_DIR/com.%{name}.desktop.desktop" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -i -e 's/com.%{name}.desktop/%{name}/' \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install the application icons
for size in "${sizes[@]}"; do
  install -Dm 0644 "$RESOURCES_DIR/icons/$size.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{name}.png"
done

# Differentiate between README.md in root dir and apps/desktop/
mv -v ./apps/desktop/README.md ./apps/desktop/README_desktop.md


%files
%{_bindir}/%{name}
/opt/%{app_name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%license ./LICENSE*.txt
%doc ./{README,SECURITY}.md ./apps/desktop/README_desktop.md


%changelog
%autochangelog
