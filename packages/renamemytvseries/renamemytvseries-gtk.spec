%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         fullname renamemytvseries
%global         app_name RenameMyTVSeries
%global         debug_package %{nil}

Name:           %{fullname}-gtk
Version:        2.3.5
Release:        1%{?dist}
Summary:        Rename My TV Series 2 (GTK version)

License:        Freeware
URL:            https://www.tweaking4all.com/home-theatre/rename-my-tv-series-v2/

Source0:        https://www.tweaking4all.com/downloads/video/%{app_name}-%{version}-GTK-Linux-x64-shared-ffmpeg.tar.xz
Source1:        %{fullname}.desktop

ExclusiveArch:  x86_64

Requires:       openssl-devel libsq3-devel
Recommends:     ffmpeg

Conflicts:      %{fullname}-qt

%description
Rename My TV Series is a utility designed to help you rename your TV series
episodes based on information from TheTVDB.com. It supports various naming
formats and can help organize your media files.

%prep
%setup -q -c -n ./%{name}

%install
# Remove the build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{app_name},%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64,128x128,256x256,512x512}/apps

# Copy the application files to the build root
%__cp -a . %{buildroot}/opt/%{app_name}

# Remove problematic files
%__rm %{buildroot}/opt/%{app_name}/{ffmpeg,ffprobe,%{app_name}.desktop,readme.txt}

# Install the desktop file
%__install -D -m 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__ln_s /opt/%{app_name}/%{app_name} %{buildroot}%{_bindir}

# Install application icons
%__install -D -m 0644 ./icons/16x16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{app_name}.png
%__install -D -m 0644 ./icons/32x32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{app_name}.png
%__install -D -m 0644 ./icons/64x64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{app_name}.png
%__install -D -m 0644 ./icons/128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{app_name}.png
%__install -D -m 0644 ./icons/256x256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{app_name}.png
%__install -D -m 0644 ./icons/512x512.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{app_name}.png

%files
/opt/%{app_name}
%{_bindir}/%{app_name}
%{_datadir}/applications/%{fullname}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{app_name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{app_name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{app_name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{app_name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{app_name}.png
%{_datadir}/icons/hicolor/512x512/apps/%{app_name}.png
