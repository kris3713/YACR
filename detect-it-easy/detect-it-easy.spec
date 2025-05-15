%global         full_name detect-it-easy
%global         application_name die
%global         debug_package %{nil}

Name:           detect-it-easy
Version:        3.10
Release:        1%{?dist}
Summary:        Program for determining types of files for Windows, Linux, and MacOS

License:        MIT
URL:            https://horsicq.github.io/#detect-it-easydie

Source0:        https://github.com/horsicq/DIE-engine/releases/download/%{version}/die_sourcecode_%{version}.tar.gz

BuildRequires:  cmake qt5-qtbase qt5-qtbase-gui qt5-qtscript-devel qt5-qttools-devel qt5-qtsvg-devel qt-devel git systemtap qtchooser
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
%setup -q -n ./die_sourcecode_%{version}

%build
# Generate build configuration files tailored for the host system
%__chmod a+x ./configure
./configure
%__chmod a-x ./configure
# Build the application binaries
%__make -j4 &> /dev/null

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create a new build root (along with other directories)
%__install -d %{buildroot}{%{_bindir},%{_datadir}/applications,%{_datadir}/icons/hicolor/256x256/apps,%{_datadir}/icons/hicolor/64x64/apps,%{_datadir}/icons/hicolor/48x48/apps,%{_datadir}/icons/hicolor/32x32/apps,%{_datadir}/icons/hicolor/16x16/apps}

# Install the application binarys
%__install -D -m 0755 ./build/release/die -t %{buildroot}%{_bindir}
%__install -D -m 0755 ./build/release/diec -t %{buildroot}%{_bindir}
%__install -D -m 0755 ./build/release/diel -t %{buildroot}%{_bindir}

# Change the directory to ./LINUX
cd ./LINUX

# Install the desktop file
%__install -D -m 0644 ./%{application_name}.desktop -t %{buildroot}%{_datadir}/applications

# Install application icons
%__ln_s ./hicolor/16x16/apps/%{full_name}.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps
%__ln_s ./hicolor/32x32/apps/%{full_name}.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
%__ln_s ./hicolor/48x48/apps/%{full_name}.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
%__ln_s ./hicolor/64x64/apps/%{full_name}.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
%__ln_s ./hicolor/256x256/apps/%{full_name}.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps

# Change the directory back to the root
cd ..

%files
%{_bindir}/die
%{_bindir}/diec
%{_bindir}/diel
%{_datadir}/applications/%{application_name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{full_name}.png
%license LICENSE

%changelog
* Wed May 14 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 3.1.0-1
- Inital packaging of detect-it-easy version 3.1.0
