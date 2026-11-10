# Created by pyp2rpm-3.3.10
%global         alt_pypi_name python3-%{srcname}
%global         pypi_name %name
%global         srcname box

%define         underscore_name %(echo %name | tr '-' '_')

Name:           python-%{srcname}
Version:        8.0.0
Release:        1%{?dist}
Summary:        Advanced Python dictionaries with dot notation access

License:        MIT
URL:            https://github.com/cdgriffith/Box

Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{underscore_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  pkgconfig pkgconfig(python)
BuildRequires:  python3dist(msgpack)
BuildRequires:  python3dist(pyyaml)
BuildRequires:  python3dist(ruamel-yaml)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(toml)
BuildRequires:  python3dist(tomli-w)
BuildRequires:  python3dist(pip)

%description
Box will automatically make otherwise inaccessible
keys safe to access as an attribute.

%package -n     %{alt_pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide %{alt_pypi_name}}

%description -n %{alt_pypi_name}
Box will automatically make otherwise inaccessible
keys safe to access as an attribute.


%prep
%autosetup -n ./%{underscore_name}-%{version}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files '%{srcname}'


%check
%_pyproject_check_import_allow_no_modules -t


%files -n %{alt_pypi_name} -f %pyproject_files
%license ./LICENSE
%doc ./{AUTHORS,CHANGES,README}.rst

%changelog
%autochangelog
