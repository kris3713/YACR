%global         __provides_exclude_from ^/opt/%{name}/.*$
%global         __requires_exclude_from ^/opt/%{name}/.*$
%global         debug_package %{nil}

Name:           streamlink-twitch-gui
Version:        2.5.3
Release:        1%{?dist}
Summary:        A multi platform Twitch.tv browser for Streamlink

License:        MIT
URL:            https://streamlink.github.io/streamlink-twitch-gui/

Source0:        https://github.com/streamlink/streamlink-twitch-gui/releases/download/v2.5.3/streamlink-twitch-gui-v2.5.3-linux64.tar.gz
Source1:        %{name}.desktop

ExclusiveArch:  x86_64

%description
A multi platform Twitch.tv browser for Streamlink.
Browse Twitch.tv and watch streams in your video player of choice.
A graphical user interface on top of the Streamlink command line interface.
Built with NW.js, a web application platform powered by Chromium and Node.js.

%prep
%setup -q -n %{name}

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create a new build root
%__install -d %{buildroot}{/opt/%{name},%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64,128x128,256x256}/apps

# Copr the application files to the application directory
%__cp -a . %{buildroot}/opt/%{name}

# Remove unnecessary scripts
%__rm %{buildroot}/opt/%{name}/*.sh

# Change filemode
%__chmod 0755 %{buildroot}/opt/%{name}/{chrome_crashpad_handler,%{name}}

# Install the application binary
%__ln_s /opt/%{name}/%{name} %{buildroot}%{_bindir}

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application icons
%__install -Dm 0644 ./icons/icon-16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%__install -Dm 0644 ./icons/icon-32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%__install -Dm 0644 ./icons/icon-48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%__install -Dm 0644 ./icons/icon-64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%__install -Dm 0644 ./icons/icon-128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png
%__install -Dm 0644 ./icons/icon-256.png %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{name}.png

%files
/opt/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%{_iconsdir}/hicolor/128x128/apps/%{name}.png
%{_iconsdir}/hicolor/256x256/apps/%{name}.png
%license ./LICENSE.txt
