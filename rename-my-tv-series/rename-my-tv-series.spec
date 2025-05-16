%global         full_name rename-my-tv-series
%global         application_name RenameMyTVSeries
%global         version 3.10
%global         debug_package %{nil}

Name:           rename-my-tv-series
Version:        2.0.10
Release:        1%{?dist}
Summary:        Rename My TV Series 2

License:        Freeware
URL:            https://www.tweaking4all.com/home-theatre/rename-my-tv-series-v2/

Source0:        https://www.tweaking4all.com/downloads/video/%{application_name}-%{version}-Linux64bit.tar.gz
Source1:        %{full_name}.desktop

ExclusiveArch:  x86_64

Requires:       openssl-devel libsq3-devel

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
%__install -d %{buildroot}{/opt/%{full_name},%{_bindir},%{_datadir}/applications,%{_datadir}/icons/hicolor/512x512/apps,%{_datadir}/icons/hicolor/256x256/apps,%{_datadir}/icons/hicolor/128x128/apps,%{_datadir}/icons/hicolor/64x64/apps,%{_datadir}/icons/hicolor/48x48/apps,%{_datadir}/icons/hicolor/32x32/apps,%{_datadir}/icons/hicolor/16x16/apps}

# Copy the application files to the build root
%__cp -a . %{buildroot}/opt/%{full_name}

# Install the desktop file
%__install -D -m 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__ln_s %{buildroot}/opt/%{full_name}/%{application_name} %{buildroot}%{_bindir}

# Install application icons
%__install -D -m 0644 %{buildroot}/opt/%{full_name}/icons/16x16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%__install -D -m 0644 %{buildroot}/opt/%{full_name}/icons/32x32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%__install -D -m 0644 %{buildroot}/opt/%{full_name}/icons/64x64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%__install -D -m 0644 %{buildroot}/opt/%{full_name}/icons/128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
%__install -D -m 0644 %{buildroot}/opt/%{full_name}/icons/256x256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{full_name}.png
%__install -D -m 0644 %{buildroot}/opt/%{full_name}/icons/512x512.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{full_name}.png

%files
/opt/%{full_name}
%{_bindir}/%{application_name}
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{full_name}.png
%{_datadir}/icons/hicolor/512x512/apps/%{full_name}.png

%changelog
* Tue Apr 22 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 2.0.10-1
- Initial packaging of rename-my-tv-series version 2.0.10
