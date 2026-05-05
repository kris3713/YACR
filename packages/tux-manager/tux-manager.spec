%global        app_name %%(v='%{name}'; v="$(echo "${v^}" | tr -d '-')"; echo "${v^^m}")
%global        debug_package %nil

Name:           tux-manager
Version:        1.0.6
Release:        1%{?dist}
Summary:        A Linux system monitor inspired by the Windows Task Manager.

License:        GPL-3.0-or-later
URL:            https://github.com/benapetr/%{app_name}
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  qt6-qtbase-devel pkgconf-pkg-config

%description
%summary


%prep
%autosetup -n ./%{app_name}-%{version}


%build
mkdir -pv ./release
pushd ./src
qmake6 ./%{app_name}.pro -o ../release/Makefile
popd
%make_build -C ./release


%install
# rm -rf %{buildroot}
install -Dm 0755 ./release/tux-manager %{buildroot}%{_bindir}/%{name}

install -Dm 0644 /dev/stdin %{buildroot}%{_datadir}/applications/%{name}.desktop << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=Tux Manager
Comment=Linux system monitor inspired by Windows Task Manager
Exec=%name
Icon=/usr/share/pixmaps/%{name}-icon.svg
Categories=System;Monitor
Terminal=false
DESKTOP

install -Dm644 ./src/tux_manager_icon.svg %{buildroot}%{_datadir}/pixmaps/%{name}-icon.svg


%files
%license ./LICENSE
%doc ./README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}-icon.svg


%changelog
%autochangelog
