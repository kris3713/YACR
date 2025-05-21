%global         full_name figma-linux
%global         arch arm64
%global         debug_package %{nil}

Name:           figma-linux-arm64
Version:        0.11.5
Release:        1%{?dist}
Summary:        Figma-linux is an unofficial Electron-based Figma desktop app for Linux.

License:        GPL-2.0
URL:            https://github.com/Figma-Linux/figma-linux

Source0:        https://github.com/Figma-Linux/figma-linux/releases/download/v%{version}/%{full_name}_%{version}_linux_%{arch}.zip
Source1:        https://raw.githubusercontent.com/Figma-Linux/figma-linux/master/resources/%{full_name}.desktop

ExclusiveArch:  %arm64

# Requires:       # Might use this later

%description
Figma is the first interface design tool based in the browser, making it easier for teams to create software.

%prep
%setup -q -c -n ./%{full_name}

%install
# Remove the build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{full_name},%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_datadir}/icons/hicolor/{24x24,36x36,48x48,64x64,72x72,96x96}/apps
%__install -d %{buildroot}%{_datadir}/icons/hicolor/{128x128,192x192,256x256,384x384,512x512}/apps

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{full_name}

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__ln_s /opt/%{full_name}/%{full_name} -t %{buildroot}%{_bindir}

# Install application icons
%__install -Dm 0644 %{buildroot}/opt/%{full_name}/icons/24x24.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{full_name}.png
%__install -Dm 0644 %{buildroot}/opt/%{full_name}/icons/36x36.png %{buildroot}%{_datadir}/icons/hicolor/36x36/apps/%{full_name}.png
%__install -Dm 0644 %{buildroot}/opt/%{full_name}/icons/48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%__install -Dm 0644 %{buildroot}/opt/%{full_name}/icons/64x64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%__install -Dm 0644 %{buildroot}/opt/%{full_name}/icons/72x72.png %{buildroot}%{_datadir}/icons/hicolor/72x72/apps/%{full_name}.png
%__install -Dm 0644 %{buildroot}/opt/%{full_name}/icons/96x96.png %{buildroot}%{_datadir}/icons/hicolor/96x96/apps/%{full_name}.png
%__install -Dm 0644 %{buildroot}/opt/%{full_name}/icons/128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
%__install -Dm 0644 %{buildroot}/opt/%{full_name}/icons/192x192.png %{buildroot}%{_datadir}/icons/hicolor/192x192/apps/%{full_name}.png
%__install -Dm 0644 %{buildroot}/opt/%{full_name}/icons/256x256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{full_name}.png
%__install -Dm 0644 %{buildroot}/opt/%{full_name}/icons/384x384.png %{buildroot}%{_datadir}/icons/hicolor/384x384/apps/%{full_name}.png
%__install -Dm 0644 %{buildroot}/opt/%{full_name}/icons/512x512.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{full_name}.png

%files
/opt/%{full_name}
%{_bindir}/%{full_name}
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/24x24/apps/%{full_name}.png
%{_datadir}/icons/hicolor/36x36/apps/%{full_name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%{_datadir}/icons/hicolor/72x72/apps/%{full_name}.png
%{_datadir}/icons/hicolor/96x96/apps/%{full_name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
%{_datadir}/icons/hicolor/192x192/apps/%{full_name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{full_name}.png
%{_datadir}/icons/hicolor/384x384/apps/%{full_name}.png
%{_datadir}/icons/hicolor/512x512/apps/%{full_name}.png
