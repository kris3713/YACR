%global         app_name jdSystemMonitor
%global         full_name page.codeberg.JakobDev.%{app_name}
%global         debug_package %nil

%define         git_url https://codeberg.org/JakobDev/%{app_name}

Name:           %(echo %app_name | tr '[:upper:]' '[:lower:]')
Version:        2.0
Release:        1%{?dist}
Summary:        Monitor your system

License:        GPL-3.0
URL:            https://jakobdev.codeberg.page/work/app/%{app_name}

Source0:        %{git_url}/archive/%{version}.tar.gz

BuildRequires:  qt6-qtbase-devel qt6-qttools-devel qt-devel
BuildRequires:  qt6-qtdeclarative-devel qt6-qtsvg-devel qt6-qtcharts-devel
BuildRequires:  meson clang ninja-build gettext golang python3 polkit-devel
Requires:       xdg-desktop-portal polkit xdg-dbus-proxy

# This description is taken from the
# README.md document in the git repository
%description
%app_name is an advanced, desktop-independent system
monitor for Linux. Its goal is to provide as much information
about your system as possible, with a focus on process management.


%prep
%autosetup -n ./%{name}


%build
# Remove unneeded build flags from C flags (clang doesn't need them)
export CFLAGS="$(
  echo '%{build_cflags}' |
  sed -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-hardened-cc1;;' \
    -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1;;'
)"
# Remove unneeded build flags from CXX flags (clang doesn't need them)
export CXXFLAGS="$(
  echo '%{build_cxxflags}' |
  sed -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-hardened-cc1;;' \
    -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1;;'
)"

# Force meson to use clang instead of gcc
export CC=clang CXX=clang++

# Setup meson
%meson
# Build the application
%meson_build


%install
# Install the required files to their appropriate locations
%meson_install


%files
%{_bindir}/%{name}
%{_libexecdir}/%{name}-daemon
%{_datadir}/applications/%{full_name}.desktop
%{_iconsdir}/hicolor/*
%{_metainfodir}/%{full_name}.metainfo.xml
%{_datadir}/polkit-1/actions/%{full_name}.policy
%license ./LICENSE
%doc ./README.md


%changelog
%autochangelog
