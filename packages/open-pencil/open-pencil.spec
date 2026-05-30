%global         appname OpenPencil
%global         debug_package %{nil}

%ifarch x86_64
%global         build_target x86_64-unknown-linux-gnu
%else
%global         build_target aarch64-unknown-linux-gnu
%endif

%define         git_url https://github.com/%{name}/%{name}

Name:           open-pencil
Version:        0.13.2
Release:        1%{?dist}
Summary:        AI-native design editor. Open-source Figma alternative.

License:        MIT
URL:            https://%(echo %appname | tr '[:upper:]' '[:lower:]').dev/

Source0:        %{git_url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  nodejs bun-bin rust cargo openssl-devel libsoup3-devel
BuildRequires:  javascriptcoregtk4.1-devel webkit2gtk4.1-devel alsa-lib-devel
BuildRequires:  gtk3-devel libayatana-appindicator-gtk3-devel librsvg2-devel
BuildRequires:  pkgconf-pkg-config pkgconf perl-FindBin perl-IPC-Cmd perl

# ExclusiveArch:  x86_64

%description
Open-Source Design Editor.
Opens Figma files. Built-in AI. Fully programmable.
Also a toolkit for building custom editors.


%prep
%autosetup -n ./%{name}-%{version}


%build
%if %{?fedora} >= 44
  mkdir -v ./extra_bin
  ln -sv $(command -v node-22) ./extra_bin/node
  export PATH="$PATH:$(realpath ./extra_bin)"
%endif

export BUN_INSTALL_CACHE_DIR="$(realpath ./.bun_cache)"
export BUN_INSTALL_GLOBAL_DIR="$(realpath ./.bun_global)"
export DO_NOT_TRACK=1
export CARGO_HOME="$(realpath ./.cargo)"

env NODE_ENV='dev' bun install
env NODE_ENV='production' bun run tauri build \
  --no-bundle \
  --target %build_target \
  -- "-j$(nproc)"


%install
# Setup buildroot
install -d %{buildroot}{%{_bindir},%{_datadir}/applications}

# Install the application binary
install -Dm 0755 ./desktop/target/%{build_target}/release/%{appname} \
  -t %{buildroot}%{_bindir}

std_sizes=('32x32' '128x128' '256x256' '512x512')
for size in "${std_sizes[@]}"; do
  install -d "%{buildroot}%{_iconsdir}/hicolor/$size/apps"
done
nstd_sizes=('30x30' '44x44' '89x89' '107x107' '150x150')
for size in "${nstd_sizes[@]}"; do
  install -d "%{buildroot}%{_iconsdir}/hicolor/$size/apps"
done

# Install the desktop file
install -Dm 0644 /dev/stdin %{buildroot}%{_datadir}/applications/%{appname}.desktop << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=%{appname}
Comment=%{summary}
Exec=%{appname} %U
Icon=%{name}
Terminal=false
DESKTOP

# For later use
ICONS_DIR='./desktop/icons'

# Reorganize icon names
mv -v "$ICONS_DIR/${std_sizes[1]}@2x.png" "$ICONS_DIR/${std_sizes[2]}.png"
mv -v "$ICONS_DIR/icon.png" "$ICONS_DIR/${std_sizes[3]}.png"

# install the application icons
for size in "${std_sizes[@]}"; do
  install -Dm 0644 "$ICONS_DIR/$size.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{name}.png"
done
for size in "${nstd_sizes[@]}"; do
  install -Dm 0644 "$ICONS_DIR/Square${size}Logo.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{name}.png"
done


%files
%{_bindir}/%{appname}
%{_datadir}/applications/%{appname}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%license ./LICENSE
%doc ./{README,SECURITY}.md


%changelog
%autochangelog
