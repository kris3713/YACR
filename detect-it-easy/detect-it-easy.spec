%global         full_name detect-it-easy
%global         app_name die
%global         debug_package %{nil}

Name:           detect-it-easy
Version:        3.10
Release:        2%{?dist}
Summary:        Program for determining types of files for Windows, Linux, and MacOS

License:        MIT
URL:            https://horsicq.github.io/#detect-it-easydie

Source0:        https://github.com/horsicq/DIE-engine/releases/download/%{version}/die_sourcecode_%{version}.tar.gz

BuildRequires:  cmake qt5-qtbase qt5-qtbase-gui qt5-qtscript-devel qt5-qttools-devel qt5-qtsvg-devel qt-devel git qtchooser
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
# Generate build files
%__mkdir_p build
%__cmake . -B ./build
# Switch to the build directory
cd ./build
# Build the application binaries
%__make -j4 &> /dev/null
# Switch back to the root directory
cd ..

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create a new build root (along with other directories)
%__install -d %{buildroot}{%{_bindir},/lib/die,%{_datadir}/applications}
%__install -d %{buildroot}%{_datadir}/icons/hicolor/{16x16,20x20,24x24,32x32,48x48,256x256}/apps

# Install the application binarys
%__install -D -m 0755 ./build/release/die -t %{buildroot}%{_bindir}
%__install -D -m 0755 ./build/release/diec -t %{buildroot}%{_bindir}
%__install -D -m 0755 ./build/release/diel -t %{buildroot}%{_bindir}

# Copy required libraires for Detect It Easy
%__cp -a ./XStyles/qss %{buildroot}/lib/die
%__cp -a ./XYara/yara_rules %{buildroot}/lib/die
%__cp -a ./XInfoDB/info %{buildroot}/lib/die
%__cp -a ./images %{buildroot}/lib/die
%__cp -a ./Detect-It-Easy/db_custom %{buildroot}/lib/die
%__cp -a ./Detect-It-Easy/db %{buildroot}/lib/die
%__install -D -m 0644 ./signatures/crypto.db -t %{buildroot}/lib/die/signatures

# Change the directory to ./LINUX
cd ./LINUX

# Install the desktop file
%__install -D -m 0644 ./%{app_name}.desktop -t %{buildroot}%{_datadir}/applications

# Install application icons
%__install -D -m 0644 ./hicolor/16x16/apps/%{full_name}.png -t %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%__install -D -m 0644 ./hicolor/20x20/apps/%{full_name}.png -t %{buildroot}%{_datadir}/icons/hicolor/20x20/apps/%{full_name}.png
%__install -D -m 0644 ./hicolor/24x24/apps/%{full_name}.png -t %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{full_name}.png
%__install -D -m 0644 ./hicolor/32x32/apps/%{full_name}.png -t %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%__install -D -m 0644 ./hicolor/48x48/apps/%{full_name}.png -t %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%__install -D -m 0644 ./hicolor/256x256/apps/%{full_name}.png -t %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{full_name}.png

# Change the directory back to the root
cd ..

%files
%{_bindir}/die
%{_bindir}/diec
%{_bindir}/diel
/lib/die
%{_datadir}/applications/%{app_name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%{_datadir}/icons/hicolor/20x20/apps/%{full_name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{full_name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{full_name}.png
%license LICENSE

%changelog
* Thu May 15 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 3.10-2
- Added missing libraries for Detect It Easy

* Wed May 14 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 3.10-1
- Inital packaging of detect-it-easy version 3.10
