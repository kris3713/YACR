%global         full_name rename-my-tv-series
%global         application_name RenameMyTVSeries
%global         debug_package %{nil}

Name:           rename-my-tv-series
Version:        2.0.10
Release:        2%{?dist}
Summary:        Rename My TV Series 2

License:        Freeware
URL:            https://www.tweaking4all.com/home-theatre/rename-my-tv-series-v2/

Source0:        https://www.tweaking4all.com/downloads/video/RenameMyTVSeries-2.0.10-Linux64bit.tar.gz
Source1:        %{full_name}.desktop

ExclusiveArch:  x86_64

Requires:       openssl-devel, libsq3-devel

%description
Rename My TV Series is a utility designed to help you rename your TV series
episodes based on information from TheTVDB.com. It supports various naming
formats and can help organize your media files.

%prep
%setup -q -c -n ./%{full_name}

%install

# Remove the build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{full_name},%{_bindir},%{_datadir}/applications,%{_datadir}/icons/hicolor/128x128/apps,%{_datadir}/icons/hicolor/64x64/apps,%{_datadir}/icons/hicolor/48x48/apps,%{_datadir}/icons/hicolor/32x32/apps,%{_datadir}/icons/hicolor/16x16/apps}

# Copy the application files to the build root
%__cp -r * %{buildroot}/opt/%{full_name}

# Install the desktop file
%__install -D -m 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__install -D -m 0755 %{buildroot}/opt/%{full_name}/%{application_name} -t %{buildroot}%{_bindir}

%__ln_s ../../../../../../opt/%{full_name}/icons/16x16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%__ln_s ../../../../../../opt/%{full_name}/icons/32x32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%__ln_s ../../../../../../opt/%{full_name}/icons/48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%__ln_s ../../../../../../opt/%{full_name}/icons/64x64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%__ln_s ../../../../../../opt/%{full_name}/icons/128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png

%files
/opt/%{full_name}
%{_bindir}/%{application_name}
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png

%changelog
* Wed May 14 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 2.0.10-3
- Removed some unnecessary commands from the spec file

* Fri May 09 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 2.0.10-2
- Changed the prep and install sections

* Tue Apr 22 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 2.0.10-1
- Initial RPM packaging of version 2.0.10
