%global         python_name python3-click
%global         pypi_name click

%global         _description %{expand:
click is a Python package for creating beautiful command line
interfaces in a composable way with as little amount of code as necessary.
It's the "Command Line Interface Creation Kit".  It's highly configurable but
comes with good defaults out of the box.}

Name:           python-%{pypi_name}
Epoch:          1
Version:        8.5.1
Release:        1%{?dist}
Summary:        Simple wrapper around optparse for powerful command line utilities

License:        BSD-3-Clause
URL:            https://github.com/pallets/%{pypi_name}

Source0:        %pypi_source

BuildArch:      noarch

BuildRequires:  pkgconfig pkgconfig(python)
BuildRequires:  python3dist(flit-core)

# This is required for test_echo_via_pager, but it should also be considered a
# hard runtime dependency; see the implementation of
# click._termui_impl._pager_contextmanager(), which uses less unconditionally
# (for regular terminals, when the PAGER environment variable is not set).
BuildRequires:  less

%description %_description


%package -n     %python_name
Summary:        %summary

Requires:       less

%description -n %python_name %_description


%prep
%autosetup -n ./%{pypi_name}-%{version} -p1


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-g tests}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files --assert-license %pypi_name


%check
%pyproject_check_import
%if %{with tests}
%pytest -rs
%endif


%files -n %python_name -f %pyproject_files
%license ./LICENSE.txt
%doc ./{CHANGES,README}.md


%changelog
%autochangelog
