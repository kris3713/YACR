%global pypi_name pyinstaller-hooks-contrib

Name:           python-%{pypi_name}
Version:        2026.10
Release:        1%{?dist}
Summary:        Community maintained hooks for PyInstaller
License:        APL, GPLv2
URL:            https://github.com/pyinstaller/%{pypi_name}
BuildArch:      noarch

Source0:        https://github.com/pyinstaller/%{pypi_name}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3dist(packaging)

%description
What happens when (your?) package doesn't work with PyInstaller? Say you have
data files that you need at runtime? PyInstaller doesn't bundle those. Your
package requires others which PyInstaller can't see? How do you fix that?
In summary, a "hook" file extends PyInstaller to adapt it to the special needs
and methods used by a Python package. The word "hook" is used for two kinds of
files. A runtime hook helps the bootloader to launch an app, setting up the
environment. A package hook (there are several types of those) tells PyInstaller
what to include in the final app - such as the data files and (hidden) imports
mentioned above.

This repository is a collection of hooks for many packages, and allows
PyInstaller to work with these packages seamlessly.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
Requires:       python3dist(setuptools)

%description -n python3-%{pypi_name}

%prep
%autosetup -n %{pypi_name}-%{version}

sed -i '/importlib_metadata/d' setup.cfg

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files _pyinstaller_hooks_contrib

# check not possible. It needs pyinstaller, but pyinstaller needs this package for installation.

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
%autochangelog
