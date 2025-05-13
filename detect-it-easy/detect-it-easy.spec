Name:           detect-it-easy
Version:        3.1.0
Release:        1%{?dist}
Summary:        Program for determining types of files for Windows, Linux and MacOS

License:        MIT
URL:            https://horsicq.github.io/#detect-it-easydie

Source0:        https://github.com/horsicq/DIE-engine/archive/refs/tags/3.10.tar.gz
Source1:        https://raw.githubusercontent.com/horsicq/DIE-engine/refs/heads/master/LINUX/io.github.horsicq.detect-it-easy.desktop#/detect-it-easy.desktop

BuildRequires:  qt5-qtbase qt5-qtbase-gui qt5-qtscript-devel qt5-qttools-devel qt5-qtsvg-devel git gettext diffstat doxygen patch patchutils systemtap
# Requires:       # Add required packages here

%description
Detect It Easy (DiE) is a powerful tool for file type identification,
popular among malware analysts, cybersecurity experts, and reverse engineers
worldwide. Supporting both signature-based and heuristic analysis, DiE
enables efficient file inspections across a broad range of platforms,
including Windows, Linux, and MacOS. Its adaptable, script-driven
detection architecture makes it one of the most versatile tools in
the field, with a comprehensive list of supported OS images.

%prep
%autosetup


%build
%configure
%make_build


%install
%make_install


%files
%license add-license-file-here
%doc add-docs-here



%changelog
* Tue May 13 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 3.1.0-1
- Inital packaging of detect-it-easy
