%global         __python %python3
%global         debug_package %nil

Name:           superlight
Version:        1.0.2
Release:        1%{?dist}
Summary:        System Monitor for Linux desktops

License:        GPL-3.0-only
URL:            https://github.com/xapp-project/%{name}

Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

BuildRequires:  meson ninja-build gettext flatpak-libs
BuildRequires:  pkgconfig gtk3-devel upower-libs
BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-gobject python3-cairo
BuildRequires:  python3-setproctitle
BuildRequires:  python3-xapp

BuildArch:      noarch

Requires:       upower xapp-symbolic-icons
Requires:       python3-gobject python3-cairo
Requires:       python3-setproctitle
Requires:       python3-xapp

%description
%summary


%prep
%autosetup -n ./%{name}-%{version}


%build
%meson
%meson_build


%install
%meson_install


%files
%{_bindir}/%{name}
%{python3_sitelib}/%{name}
%{_datadir}/applications/org.x.%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/glib-2.0/schemas/org.x.%{name}.gschema.xml
%license ./LICENSES/*
%doc ./README.md

%changelog
%autochangelog
