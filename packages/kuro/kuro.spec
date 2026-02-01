%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         app_name Kuro
%global         debug_package %nil

Name:           %(echo %app_name | tr '[:upper:]' '[:lower:]')
Version:        9.1.1
Release:        1%{?dist}
Summary:        A secure and free password manager for all of your devices.

License:        MIT
URL:            https://github.com/davidsmorais/%{name}

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}.desktop

BuildRequires:  nodejs yarnpkg
# BuildRequires:  libsecret-devel glib2-devel atk-devel
# BuildRequires:  at-spi2-atk-devel gtk3-devel libxcrypt-compat

ExclusiveArch:  x86_64

%description
%{summary}


%prep
%autosetup -n ./%{name}-%{version}


%build
%if %{?fedora} >= 44
  mkdir -v ./extra_bin
  ln -sv $(command -v node-22) ./extra_bin/node
  export PATH="$PATH:$(realpath ./extra_bin)"
%endif

export npm_config_cache="$(realpath ./.yarn_cache)"
export YARN_CACHE_FOLDER="$npm_config_cache"
export YARN_CONFIG_FOLDER="$(realpath ./.yarn_config)"

# Clean install all node dependencies
env NODE_ENV='dev' yarn install

# Build the application
export NODE_ENV='production'
yarn icons
yarn exec electron-builder -- \
  --linux --x64 --dir -p always


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
ln -s /opt/%{app_name}/%{name} -t %{buildroot}%{_bindir}

# Install the desktop file
install -Dm 0644 %SOURCE1 \
  -t %{buildroot}%{_datadir}/applications

# Install the application icons
for size in "${sizes[@]}"; do
  install -Dm 0644 "./build/icons/png/$size.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{name}.png"
done


%files
%{_bindir}/%{name}
/opt/%{app_name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%license ./license.md
%doc ./{readme.md,docs/devlog.md}


%changelog
%autochangelog
