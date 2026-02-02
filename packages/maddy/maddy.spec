%global         debug_package %nil

Name:           maddy
Version:        1.6.0
Release:        1%{?dist}
Summary:        C++ Markdown to HTML header-only parser library

License:        MIT
URL:            https://github.com/progsource/%{name}

Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

BuildRequires:  gcc gcc-c++ ninja-build cmake cmake-rpm-macros

%description
%name is a C++ Markdown to HTML header-only parser library.

%prep
%autosetup -n ./%{name}-%{version}



%package devel
Summary: Development files for %name
Provides: %{name}-static = %{?epoch:%{epoch}:}%{version}-%{release}
%description devel
%{summary}.


%build
%cmake -DCMAKE_BUILD_TYPE=Release
# %%cmake_build


%install
%cmake_install


%files
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%license ./LICENSE
%doc ./{README.md,AUTHORS} ./docs


%changelog
%autochangelog
