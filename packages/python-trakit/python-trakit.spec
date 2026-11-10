# Copied from the openSUSE package of the same name
%global         alt_pypi_name python3-%{srcname}
%global         pypi_name %name
%global         pypi_version 0.4.0
%global         srcname trakit

Name:           python-%{srcname}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Guess additional information from track titles

License:        MIT
URL:            https://github.com/ratoaq2/%{srcname}

Source0:        %{pypi_source %{srcname}}

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  pkgconfig pkgconfig(python)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(babelfish)
BuildRequires:  python3dist(rebulk)
BuildRequires:  python3dist(hatchling)

%description
TrakIt is a track name parser created to solve a common, yet very specific
problem, that is vagueness in metadata information.


%package -n     %{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide %{alt_pypi_name}}

%description -n %{srcname}
TrakIt is a track name parser created to solve a common, yet very specific
problem, that is vagueness in metadata information.


%prep
%autosetup -n ./%{srcname}-%{version}
# Remove bundled egg-info
rm -rf ./%{pypi_name}.egg-info


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files '%{srcname}'


%check
%_pyproject_check_import_allow_no_modules -t


%files -n %{srcname} -f %{pyproject_files}
%{_bindir}/%{srcname}
%license ./LICENSE
%doc ./README.md


%changelog
%autochangelog
