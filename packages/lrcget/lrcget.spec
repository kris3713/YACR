%global         app_name LRCGET
%global         debug_package %{nil}

Name:           %(echo %app_name | tr '[:upper:]' '[:lower:]')
Version:        1.0.2
Release:        1%{?dist}
Summary:        Utility for mass-downloading LRC synced lyrics for your offline music library.

License:        MIT
URL:            https://github.com/tranxuanthang/%{name}

Source0:        %{url}/archive/refs/tags/%{version}.tar.gz
Source1:        %{name}.desktop

BuildRequires:  nodejs nodejs-npm rust cargo openssl-devel libsoup3-devel
BuildRequires:  javascriptcoregtk4.1-devel webkit2gtk4.1-devel alsa-lib-devel

ExclusiveArch:  x86_64

%description
Utility for mass-downloading LRC synced lyrics for your offline music library.

%app_name will scan every files in your chosen directory for music files,
then and try to download lyrics to a LRC files having the same name and save
them to the same directory as your music files.

%app_name is the official client of LRCLIB service.


%prep
%autosetup -n ./%{name}-%{version}


%build
%if %{?fedora} >= 44
  mkdir -v ./extra_bin
  ln -sv $(command -v node-22) ./extra_bin/node
  ln -sv $(command -v npm-22) ./extra_bin/npm
  export PATH="$PATH:$(realpath ./extra_bin)"
%endif

export npm_config_cache="$(realpath ./.node_cache)"
export CARGO_HOME="$(realpath ./.cargo)"

env NODE_ENV='dev' npm install
env NODE_ENV='production' npm run tauri build -- \
  --no-bundle \
  --target x86_64-unknown-linux-gnu \
  -- --release


%install
# Setup buildroot
install -d %{buildroot}{%{_bindir},%{_datadir}/applications}
install -d %{buildroot}%{_iconsdir}/hicolor/{32x32,44x44,128x128}/apps
install -d %{buildroot}%{_iconsdir}/hicolor/{256x256,512x512}/apps

# Install the desktop file
install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary
install -Dm 0755 ./src-tauri/target/release/%{app_name} \
  -t %{buildroot}%{_bindir}

# Install the application icons
install -Dm 0644 ./src-tauri/icons/32x32.png \
  %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{app_name}.png
install -Dm 0644 ./src-tauri/icons/Square44x44Logo.png \
  %{buildroot}%{_iconsdir}/hicolor/44x44/apps/%{app_name}.png
install -Dm 0644 ./src-tauri/icons/128x128.png \
  %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{app_name}.png
install -Dm 0644 ./src-tauri/icons/128x128@2x.png \
  %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{app_name}.png
install -Dm 0644 ./src-tauri/icons/icon.png \
  %{buildroot}%{_iconsdir}/hicolor/512x512/apps/%{app_name}.png


%files
%{_bindir}/%{app_name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{app_name}.png
%license ./LICENSE
%doc ./README.md


%changelog
%autochangelog
