# Created by pyp2rpm-3.3.10
%global         alt_pypi_name python3-%{srcname}
%global         pypi_name %name
%global         pypi_version 8.0.0
%global         srcname box

%define         underscore_name %(echo %name | tr '-' '_')

Name:           python-%{srcname}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Advanced Python dictionaries with dot notation access

License:        MIT
URL:            https://github.com/cdgriffith/Box

Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{underscore_name}-%{pypi_version}.tar.gz

BuildArch:      noarch

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

Requires:       python3dist(msgpack)
Requires:       python3dist(pyyaml)
Requires:       python3dist(ruamel-yaml)
Requires:       python3dist(toml)
Requires:       python3dist(tomli-w)
Requires:       python3dist(pip)

%description -n %{alt_pypi_name}
Box will automatically make otherwise inaccessible
keys safe to access as an attribute.


%prep
%autosetup -n %{underscore_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf ./%{pypi_name}.egg-info


%build
%pyproject_wheel


%install
%pyproject_install


%check
%nil


%files -n %{alt_pypi_name}
%license ./LICENSE
%doc ./README.rst
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{underscore_name}-%{pypi_version}.dist-info
# %%{python3_sitelib}/%%{underscore_name}-%%{pypi_version}-py%%{python3_version}.egg-info

%changelog
%autochangelog
