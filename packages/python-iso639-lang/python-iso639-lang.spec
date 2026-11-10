%global         underscore_name %(echo %srcname | tr '-' '_')
%global         alt_pypi_name python3-%{srcname}
%global         pypi_name %name
%global         pypi_version 2.6.3
%global         srcname iso639-lang


Name:           python-%{srcname}
Version:        %pypi_version
Release:        1%{?dist}
Summary:        A fast, comprehensive, ISO 639 library.

License:        Apache-2.0
URL:            https://github.com/RapidAI/%{repo_name}

Source:         https://files.pythonhosted.org/packages/source/i/%{srcname}/%{underscore_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  pkgconfig pkgconfig(python)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(pip)

%description
%srcname handles the ISO 639 code for individual languages and language groups.


%package -n     %{alt_pypi_name}
Summary:        %summary

%description -n %{alt_pypi_name}
%srcname handles the ISO 639 code for individual languages and language groups.


%prep
%autosetup -n ./%{underscore_name}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files '*iso639*'


%check
%_pyproject_check_import_allow_no_modules -t


%files -n %{alt_pypi_name} -f %{pyproject_files}
%doc ./README.md
%license ./LICENSE.txt

%changelog
%autochangelog

