%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         app_name Bitwarden
%global         debug_package %{nil}

%define         git_url https://github.com/%{name}/clients

Name:           %(echo %app_name | tr '[:upper:]' '[:lower:]')
Version:        2025.12.1
Release:        1%{?dist}
Summary:        A secure and free password manager for all of your devices.

License:        GPL-3.0
URL:            https://%{name}.com

Source0:        %{git_url}/archive/refs/tags/desktop-v%{version}.tar.gz

BuildRequires:  nodejs nodejs-npm rustup git gcc gcc-c++
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


export npm_config_cache="$(realpath ./.node_cache)"
export CARGO_HOME="$(realpath ./.cargo)"
export RUSTUP_HOME="$(realpath ./.rustup)"
export RUSTUP_TOOLCHAIN='nightly'

# Clean install all node dependencies
env NODE_ENV='dev' npm ci --loglevel=error

# Install rustup, add cargo bin to PATH and install
# rust nightly
rustup-init -y \
  --no-modify-path --default-toolchain none
export PATH="$PATH:$CARGO_HOME/bin"
rustup toolchain install nightly
rustup default nightly

# Build the native modules
export NODE_ENV='production'
pushd ./apps/desktop/desktop_native/napi

# Using extra arguments that will be
# passed to cargo from napi cli
npm run build -- \
  --release --target x86_64-unknown-linux-gnu \
  -- "-j$(nproc)"

pushd ..

npm run build -- \
  --release --target x86_64-unknown-linux-gnu

# Build the application
pushd ..

npm run build
npm run 'clean:dist'
npm exec electron-builder -- \
  --linux --x64 --dir -p always

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
ln -s /opt/%{app_name}/%{name} -t %{buildroot}%{_bindir}

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
%doc ./README.md ./apps/desktop/README_desktop.md ./SECURITY.md


%changelog
%autochangelog
