%global         app_id org.%{name}.%{app_name}
%global         app_id fr.%{maintainer}.%{app_name}
%global         maintainer morfredus
%global         app_name AntRenamerQt
%global         alt_name %%(echo %name | sed -e 's/-//')
%global         debug_package %nil

%ifarch x86_64
%global         preset linux
%else
%global         preset linux-arm64
%endif

Name:           ant-renamer-qt
Version:        3.3.1
Release:        1%{?dist}
Summary:        C++/Qt 6 port of Ant Renamer 2.13 (originally Delphi 7, GPL v2 or later)

License:        GPL-2.0-or-later
URL:            https://%{maintainer}.fr/%{name}-en/

Source0:        https://github.com/%{maintainer}/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc-c++ cmake ninja-build
BuildRequires:  pkgconfig pkgconfig(Qt6)

%description
Batch file renaming: replace, insert, move, delete,
enumerate, change case, regular expressions, names
from a list, file date, MP3 tags (ID3v1/v2),
EXIF / IPTC / XMP, EPUB metadata. Also: filter the
list by date, time of the day and size, and put the
shooting date of photos back as their modification
date (with safeguards).


%prep
%autosetup -n ./%{name}-%{version}


%build
%cmake --preset %preset -DCMAKE_BUILD_TYPE=Release
%cmake_build --preset %preset


%install
%cmake_install


%files
%{_bindir}/%{alt_name}
%{_datadir}/applications/%{alt_name}.desktop
%{_iconsdir}/hicolor/*/apps/%{alt_name}.*
%{_metainfodir}/%{app_id}.metainfo.xml
%{_datadir}/%{alt_name}
%license ./LICENSE
%doc ./{CHANGELOG,README*,SECURITY*}.md ./docs


%changelog
%autochangelog

