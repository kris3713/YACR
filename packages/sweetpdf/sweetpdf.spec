%global         app_id org.%{name}.%{app_name}
%global         app_name SweetPDF
%global         debug_package %nil

Name:           %(v="%{app_name}"; echo "${v,,}")
Version:        1.1.2
Release:        1%{?dist}
Summary:        All-in-one open source PDF editor

License:        AGPL-3.0
URL:            https://github.com/foisalislambd/%{app_name}

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc-c++ cmake ninja-build qt6-qtbase-devel
BuildRequires:  qt6-qtsvg-devel mupdf-devel tesseract-devel
BuildRequires:  leptonica-devel sqlite-devel ghostscript
Requires:       mupdf tesseract

%description
%summary.
Annotate, edit, OCR, merge, redact & encrypt locally.
No upload, no account. Qt 6 + MuPDF.


%prep
%autosetup -n ./%{app_name}-%{version}


%build
%cmake -DCMAKE_BUILD_TYPE=Release -DSWEETPDF_VERSION=%version
%cmake_build


%install
%cmake_install


%files
%{_bindir}/%{name}
%{_datadir}/applications/%{app_id}.desktop
%{_iconsdir}/hicolor/*/apps/%{app_id}.png
%{_metainfodir}/%{app_id}.metainfo.xml
%license ./LICENSE
%doc ./{CHANGELOG,README,SECURITY}.md


%changelog
%autochangelog

