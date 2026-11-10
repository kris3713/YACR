%global         python_name python3-%{pypi_name}
%global         pypi_name pyinstaller
%global         debug_package %nil

Name:           python-%{pypi_name}
Version:        6.22.3
Release:        1%{?dist}
Summary:        Bundle a Python application and all its dependencies into a single package
License:        GPL-2.0-only
URL:            https://www.%{pypi_name}.org

Source:         %pypi_source

BuildRequires:  gcc binutils
BuildRequires:  pkgconfig pkgconfig(zlib) pkgconfig(python)
BuildRequires:  python3dist(hatchling)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(altgraph)
BuildRequires:  python3dist(pyinstaller-hooks-contrib)

%description
PyInstaller bundles a Python application and all its dependencies into a single
package. The user can run the packaged app without installing a Python
interpreter or any modules.

%package -n %python_name
Summary:        Bundle a Python application and all its dependencies into a single package
Recommends:     upx

%description -n %python_name
PyInstaller bundles a Python application and all its dependencies into a single
package. The user can run the packaged app without installing a Python
interpreter or any modules.

%prep
%autosetup -n ./%{pypi_name}-%{version}

# Force build of bootloader
rm -r ./PyInstaller/bootloader

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files PyInstaller

%files -n %python_name -f %pyproject_files
%doc ./README.rst ./doc/{CHANGES,CREDITS}.rst
%license ./COPYING.txt
%{_bindir}/pyi-archive_viewer
%{_bindir}/pyi-bindepend
%{_bindir}/pyi-grab_version
%{_bindir}/pyi-makespec
%{_bindir}/pyi-set_version
%{_bindir}/%{pypi_name}

%changelog
%autochangelog
