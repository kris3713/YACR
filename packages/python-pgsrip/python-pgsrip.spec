%global         alt_pypi_name python3-%{srcname}
%global         pypi_name %name
%global         srcname pgsrip

%global         common_description %{expand:
Convert image-based Blu-ray subtitles (PGS) in .mkv,
.mks, and .sup files to text .srt files, with OCR.
}

Name:           python-%{srcname}
Version:        0.3.0
Release:        1%{?dist}
Summary:        Rip your PGS subtitles

License:        MIT
URL:            https://github.com/ratoaq2/%{srcname}

Source0:        %pypi_source

BuildArch:      noarch

BuildRequires:  pkgconfig pkgconfig(python)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(hatchling)
BuildRequires:  python3dist(appdirs)
BuildRequires:  python3dist(babelfish)
BuildRequires:  python3dist(cleanit)
BuildRequires:  python3dist(click)
BuildRequires:  python3dist(numpy)
BuildRequires:  python3dist(opencv-python)
BuildRequires:  python3dist(pysrt)
BuildRequires:  python3dist(pytesseract)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(trakit)

%description %common_description


%package -n     %srcname
Summary:        %summary
%{?python_provide:%python_provide %{alt_pypi_name}}

%description -n %srcname %common_description

%pyproject_extras_subpkg -n %srcname rapidocr

%prep
%autosetup -n ./%{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires


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
