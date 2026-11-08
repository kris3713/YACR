%global         app_id io.github.%{maintainer}.system-monitoring-center
%global         maintainer hakandundar34coding
%global         debug_package %nil

Name:           system-monitoring-center
Version:        3.4.1
Release:        1%{?dist}
Summary:        Multi-featured system monitor

License:        GPL-3.0
URL:            https://github.com/%{maintainer}/%{name}

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  meson ninja-build gettext gtk3-devel
BuildRequires:  hwdata-devel dmidecode util-linux
BuildRequires:  pkgconfig pkgconfig(python3)
BuildRequires:  python3-cairo python3-tkinter
BuildRequires:  python3-pillow python3-pillow-tk
BuildRequires:  desktop-file-utils

BuildArch:      noarch

Requires:       hwdata dmidecode util-linux
Requires:       python3-cairo python3-tkinter
Requires:       python3-pillow python3-pillow-tk
Requires:       desktop-file-utils

%description
Provides information about CPU/RAM/Disk/Network/GPU performance, sensors,
processes, users, storage, startup programs, services, environment
variables and system.


%prep
%autosetup -n ./%{name}-%{version}


%build
%meson
%meson_build


%install
%meson_install


%files
%{_bindir}/%{name}
%{_datadir}/applications/%{app_id}.desktop
%{_iconsdir}/hicolor/*
%{_datadir}/appdata/%{app_id}.appdata.xml
%{_datadir}/%{name}
%{_datadir}/locale
%{_mandir}/man1


%changelog
%autochangelog
