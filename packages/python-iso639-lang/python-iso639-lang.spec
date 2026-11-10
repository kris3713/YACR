%global         alt_name %(v="%{srcname}"; echo "${v/-lang/}")
%global         underscore_name %(echo %srcname | tr '-' '_')
%global         alt_pypi_name python3-%{srcname}
%global         pypi_name %name
%global         srcname iso639-lang

Name:           python-%{srcname}
Version:        2.6.3
Release:        1%{?dist}
Summary:        A fast, comprehensive, ISO 639 library.

License:        MIT
URL:            https://github.com/LBeaudoux/%{alt_name}

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

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
%autosetup -n ./%{alt_name}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %alt_name


%check
%_pyproject_check_import_allow_no_modules -t


%files -n %{alt_pypi_name} -f %{pyproject_files}
%doc ./README.md
%license ./LICENSE.txt

%changelog
%autochangelog

