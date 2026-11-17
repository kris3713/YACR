%global        app_name %%(v='%{name}'; v="$(echo "${v^}" | tr -d '-')"; echo "${v^^m}")
%global        debug_package %nil

Name:           tux-manager
Version:        1.1.0
Release:        1%{?dist}
Summary:        A Linux system monitor inspired by the Windows Task Manager.

License:        GPL-3.0-or-later
URL:            https://github.com/benapetr/%{app_name}

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  qt6-qtbase-devel qt6-linguist pkgconf-pkg-config ImageMagick

%description
%summary


%prep
%autosetup -n ./%{app_name}-%{version}


%build
mkdir -pv ./build
cd ./build
qmake6 ../src
%make_build


%install
install -Dm 0755 ./build/%{name} %{buildroot}%{_bindir}/%{name}

CONTENT="$(cat << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=Tux Manager
Comment=%summary
Exec=%name
Icon=%name
Categories=System;Monitor
Terminal=false
DESKTOP
)"
install -Dm 0644 /dev/stdin \
  %{buildroot}%{_datadir}/applications/%{name}.desktop <<< "$CONTENT"

SIZES=('16x16' '32x32' '48x48' '64x64' '128x128' '256x256')
ICONS_DIR='./app_icons'
mkdir -v "$ICONS_DIR"
magick ./src/tux_manager_256.ico ./%{name}.png
mv -v ./%{name}-0.png "$ICONS_DIR/${SIZES[5]}.png"
mv -v ./%{name}-1.png "$ICONS_DIR/${SIZES[4]}.png"
mv -v ./%{name}-2.png "$ICONS_DIR/${SIZES[3]}.png"
mv -v ./%{name}-3.png "$ICONS_DIR/${SIZES[2]}.png"
mv -v ./%{name}-4.png "$ICONS_DIR/${SIZES[1]}.png"
mv -v ./%{name}-5.png "$ICONS_DIR/${SIZES[0]}.png"

for size in "${SIZES[@]}"; do
  install -Dm 0644 "$ICONS_DIR/$size.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/%{name}.png"
done
install -Dm644 ./src/tux_manager_icon.svg \
  %{buildroot}%{_iconsdir}/hicolor/scalable/%{name}.svg


%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/%{name}.*
%license ./LICENSE
%doc ./README.md

%changelog
%autochangelog
