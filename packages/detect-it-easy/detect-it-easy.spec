%global         app_id io.github.%{maintainer}.%{name}
%global         maintainer horsicq
%global         app_name die
%global         debug_package %nil

%define         uppercase_app_name %(v="%{app_name}"; echo "${v^^}")
%define         git_url https://github.com/%{maintainer}/%{uppercase_app_name}-engine

Name:           detect-it-easy
Version:        4.0.0
Release:        1%{?dist}
Summary:        Program for determining types of files

License:        MIT
URL:            https://horsicq.github.io/#%{name}%{app_name}

Source0:        %{git_url}/releases/download/%{version}/%{app_name}_sourcecode_%{version}.tar.gz

BuildRequires:  gcc-c++ cmake qt5-qtbase qt5-qtbase-devel
BuildRequires:  qt5-qtbase-gui qt5-qtscript-devel qt5-qttools-devel
BuildRequires:  qt5-qtsvg-devel qt-devel qtchooser
BuildRequires:  qt5-linguist

%description
Detect It Easy (DiE) is a powerful tool for file type identification,
popular among malware analysts, cybersecurity experts, and reverse engineers
worldwide. Supporting both signature-based and heuristic analysis, DiE
enables efficient file inspections across a broad range of platforms,
including Windows, Linux, and MacOS. Its adaptable, script-driven
detection architecture makes it one of the most versatile tools in
the field, with a comprehensive list of supported OS images.


%prep
%autosetup -n ./%{app_name}_sourcecode_%{version}


%build
# The maintainer forgot to add `lrelease` to the PATH
export PATH="$PATH:%{_libdir}/qt5/bin"

%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build


%install
%cmake_install


%files
%{_bindir}/%{app_name}
%{_bindir}/%{app_name}c
%{_bindir}/%{app_name}l
%{_bindir}/%{app_name}-update
%{_libdir}/%{app_name}
/usr/lib/%{app_name}
%{_datadir}/applications/%{app_name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{app_id}.png
%{_metainfodir}/%{app_id}.metainfo.xml
%{_docdir}/DetectItEasy


%changelog
%autochangelog
