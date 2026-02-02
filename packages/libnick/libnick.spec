%global         debug_package %nil

Name:           libnick
Version:        2025.10.0
Release:        1%{?dist}
Summary:        A cross-platform base for native Nickvision applications

License:        MIT
URL:            https://github.com/NickvisionApps/%{name}

Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

BuildRequires:  gcc gcc-c++ ninja-build cmake cmake-rpm-macros
BuildRequires:  maddy boost-devel boost-json cpr-devel gettext-libs
BuildRequires:  gtest-devel libsecret-devel sqlcipher-devel
Requires:       maddy

%description
%name provides Nickvision apps with a common set of cross-platform
APIs for managing system and desktop app functionality such as
network management, taskbar icons, translations, app updates, and more.

%prep
%autosetup -n ./%{name}-%{version}


# %%package devel
# Summary: Development files for %%name
# Provides: %%{name}-static = %%{?epoch:%%{epoch}:}%%{version}-%%{release}
# %%description devel
# %%{summary}.


%build
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build


%install
%cmake_install


%files
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%{_libdir}/lib%{name}.so*
%{_libdir}/pkgconfig/%{name}.pc
%license ./COPYING
%doc ./{README.md} ./manual


%changelog
%autochangelog
