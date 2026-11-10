%global         repo_name Reusables
%global         alt_pypi_name python3-%{pypi_name}
%global         pypi_name %(v="%{repo_name}"; echo "${v,}")

%global         common_description %{expand:
The reusables library is a cookbook of python functions and
classes that programmers may find themselves often recreating.
}

Name:           python-%{pypi_name}
Version:        1.0.0
Release:        1%{?dist}
Summary:        Commonly Consumed Code Commodities

License:        MIT
URL:            https://github.com/cdgriffith/%{repo_name}

Source0:        %pypi_source

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  pkgconfig pkgconfig(python)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(wheel)


%description %common_description


%package -n     %alt_pypi_name
Summary:        %summary
%{?python_provide:%python_provide %{alt_pypi_name}}

%description -n %alt_pypi_name %common_description


%prep
%autosetup -n ./%{pypi_name}-%{version}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files '%{pypi_name}'


%check
%_pyproject_check_import_allow_no_modules -t


%files -n %alt_pypi_name -f %pyproject_files
%license ./LICENSE
%doc ./{AUTHORS,CHANGES,README}.rst


%changelog
%autochangelog
