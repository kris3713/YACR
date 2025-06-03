%global         major 7
%global         full_name Stacher%{major}
%global         app_name %{name}%{major}
%global         debug_package %{nil}

Name:           stacher
Version:        7.0.19
Release:        1%{?dist}
Summary:        A modern GUI for yt-dlp (and other youtube-dl forks)

License:        Freeware
URL:            https://stacher.io/

Source0:        https://s7-releases.stacher-cloud.com/s%{major}-releases/stacher%{major}_%{version}_amd64.deb

BuildRequires:  dpkg
Requires:       yt-dlp ffmpeg

ExclusiveArch:  x86_64

%description
Stacher is a frontend GUI for the youtube-dl (or yt-dlp) command line tool.
It is designed to be simple, easy to use, and powerful.

%prep
dpkg -x %{SOURCE0} .

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},/opt/%{name},pixmaps,%{_datadir}/applications}
%__install -d %{buildroot}%{_iconsdir}/hicolor/256x256/apps

# Copy the application files to the application directory
%__cp -a ./usr/lib/%{app_name}/* %{buildroot}/opt/%{name}

# Install the desktop file
%__install -Dm 0644 ./usr/share/applications/%{app_name}.desktop -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__ln -s /opt/%{name}/%{full_name} %{buildroot}%{_bindir}/%{app_name}

# Install the application icon
%__install -Dm 0644 ./usr/share/pixmaps/%{app_name}.png -t %{buildroot}%{_iconsdir}/hicolor/256x256/apps

# Install the application pixmap
%__install -Dm 0644 ./usr/share/pixmaps/%{app_name}.png -t %{buildroot}%{_datadir}/pixmaps

%files
/opt/%{name}
%{_bindir}/%{app_name}
%{_datadir}/applications/%{app_name}.desktop
%{_datadir}/pixmaps/%{app_name}.png
%{_iconsdir}/hicolor/256x256/apps/%{app_name}.png
