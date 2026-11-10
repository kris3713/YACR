%global         python_name  python3-%{pypi_name}
%global         pypi_name jsonschema

%global         common_description %{expand:
jsonschema is an implementation of JSON Schema for Python (supporting
2.7+, including Python 3).

 - Full support for Draft 7, Draft 6, Draft 4 and Draft 3
 - Lazy validation that can iteratively report all validation errors.
 - Small and extensible
 - Programmatic querying of which properties or items failed validation.}

Name:           python-%{pypi_name}
Summary:        Implementation of JSON Schema validation for Python
Version:        4.26.0
Release:        %autorelease
License:        MIT
URL:            https://github.com/Julian/jsonschema
Source0:        %{pypi_source}

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  pkgconfig pkgconfig(python)
BuildRequires:  python3dist(hatch-fancy-pypi-readme)
BuildRequires:  python3dist(hatch-vcs)
BuildRequires:  python3dist(hatchling)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(jsonpath-ng)
BuildRequires:  python3dist(jsonschema-specifications)
BuildRequires:  python3dist(referencing)
BuildRequires:  python3dist(rpds-py)

# test requirements
%bcond tests %{undefined rhel}

%if %{with tests}
# For “trial-3”
BuildRequires:  python3dist(twisted)
%endif

%description %{common_description}


%package -n     %python_name
Summary:        %{summary}
%{?python_provide:%python_provide %{alt_pypi_name}}

%description -n %python_name %{common_description}

%pyproject_extras_subpkg -n %python_name format format-nongpl


%prep
%autosetup -n ./%{pypi_name}-%{version} -p1

# Requires a checkout of the JSON-Schema-Test-Suite
# https://github.com/json-schema-org/JSON-Schema-Test-Suite
rm ./%{pypi_name}/tests/test_%{pypi_name}_test_suite.py

# Test dependency on (python-)virtue would only be required if we used nox to
# run the tests.
sed -i -e 's|"virtue",||' ./pyproject.toml

%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-g test}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}


%check
%pyproject_check_import -e '*.benchmarks*' -e '*.tests*'
%if %{with tests}
%{py3_test_envvars} trial-3 %{pypi_name}
%endif

%files -n %python_name -f %{pyproject_files}
%license ./COPYING ./json/LICENSE
%doc ./README.rst
%{_bindir}/jsonschema

%changelog
%autochangelog
