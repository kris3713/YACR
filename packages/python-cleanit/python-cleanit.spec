# Created by pyp2rpm-3.3.10
%global         alt_pypi_name python3-%{srcname}
%global         pypi_name %name
%global         pypi_version 0.5.1
%global         srcname cleanit

Name:           python-%{srcname}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Subtitles extremely clean

License:        Apache-2.0
URL:            https://github.com/ratoaq2/%{srcname}

Source0:        %{pypi_source %{srcname}}

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  pkgconfig pkgconfig(python)
BuildRequires:  python3dist(appdirs)
BuildRequires:  python3dist(babelfish)
BuildRequires:  python3dist(chardet)
BuildRequires:  python3dist(click)
BuildRequires:  python3dist(jsonschema)
BuildRequires:  python3dist(pysrt)
BuildRequires:  python3dist(pyyaml)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(hatchling)

%description
CleanIt is a command line tool that helps you to keep your subtitles clean.
You can specify your own rules to detect entries to be removed or patterns
to be replaced.


%package -n     %{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide %{alt_pypi_name}}

%description -n %{srcname}
CleanIt is a command line tool that helps you to keep your subtitles clean.
You can specify your own rules to detect entries to be removed or patterns
to be replaced.


%prep
%autosetup -n ./%{srcname}-%{pypi_version}


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
