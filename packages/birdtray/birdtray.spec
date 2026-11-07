%global         app_id com.%{company_name}.%{app_name}
%global         company_name ulduzsoft
%global         app_name Birdtray
%global         debug_package %nil

Name:           %(echo %app_name | tr '[:upper:]' '[:lower:]')
Version:        1.11.4
Release:        1%{?dist}
Summary:        %app_name is a free system tray notification for new mail for Thunderbird.

License:        GPL-3.0
URL:            https://github.com/gyunaev/%{name}

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc-c++ cmake pkgconfig
%if "%version" > "1.11.4"
BuildRequires:  pkgconfig(Qt6Widgets) pkgconfig(Qt6Core) pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6Network) pkgconfig(Qt6Svg) pkgconfig(Qt6Linguist)
BuildRequires:  pkgconfig(sqlite3) pkgconfig(x11)
%else
BuildRequires:  pkgconfig(Qt5Widgets) pkgconfig(Qt5Core) pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network) pkgconfig(Qt5Svg) pkgconfig(sqlite3)
BuildRequires:  pkgconfig(x11) pkgconfig(Qt5X11Extras)
BuildRequires:  qt5-linguist
%endif

%description
%summary


%prep
%autosetup -n ./%{name}-%{version}


%build
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build


%install
%cmake_install


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :


%files
%{_bindir}/%{name}
%{_datadir}/applications/%{app_id}.desktop
%{_iconsdir}/hicolor/*/apps/%{app_id}.*
%{_metainfodir}/%{app_id}.appdata.xml
%{_datadir}/%{company_name}/birdtray/translations/*.qm
%license ./LICENSE.txt

%changelog
%autochangelog
