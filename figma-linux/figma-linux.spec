%global         full_name figma-linux
%global         debug_package %{nil}

Name:           figma-linux
Version:        0.11.5
Release:        1%{?dist}
Summary:        Figma-linux is an unofficial Electron-based Figma desktop app for Linux.

License:        GPL-2.0
URL:            https://github.com/Figma-Linux/figma-linux

Source0:        https://github.com/Figma-Linux/%{name}/releases/download/v%{version}/%{full_name}-%{version}.zip
Source1:        https://raw.githubusercontent.com/ChugunovRoman/%{full_name}/master/resources/%{full_name}.desktop
Source2:        https://raw.githubusercontent.com/ChugunovRoman/%{full_name}/master/resources/icons/24x24.png
Source3:        https://raw.githubusercontent.com/ChugunovRoman/%{full_name}/master/resources/icons/36x36.png
Source4:        https://raw.githubusercontent.com/ChugunovRoman/%{full_name}/master/resources/icons/48x48.png
Source5:        https://raw.githubusercontent.com/ChugunovRoman/%{full_name}/master/resources/icons/64x64.png
Source6:        https://raw.githubusercontent.com/ChugunovRoman/%{full_name}/master/resources/icons/72x72.png
Source7:        https://raw.githubusercontent.com/ChugunovRoman/%{full_name}/master/resources/icons/96x96.png
Source8:        https://raw.githubusercontent.com/ChugunovRoman/%{full_name}/master/resources/icons/128x128.png
Source9:        https://raw.githubusercontent.com/ChugunovRoman/%{full_name}/master/resources/icons/192x192.png
Source10:       https://raw.githubusercontent.com/ChugunovRoman/%{full_name}/master/resources/icons/256x256.png
Source11:       https://raw.githubusercontent.com/ChugunovRoman/%{full_name}/master/resources/icons/384x384.png
Source12:       https://raw.githubusercontent.com/ChugunovRoman/%{full_name}/master/resources/icons/512x512.png
# Source13:       %{full_name}

# Requires:       # Might use this later

%description
Figma is the first interface design tool based in the browser, making it easier for teams to create software.

%prep
%setup -q -c -n ./%{full_name}

%install
# Remove the build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{full_name},%{_datadir}/applications}
%__install -d %{buildroot}%{_datadir}/icons/hicolor/{24x24,36x36,48x48,64x64,72x72,96x96}/apps
%__install -d %{buildroot}%{_datadir}/icons/hicolor/{128x128,192x192,256x256,384x384,512x512}/apps

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{full_name}

# Install the desktop file
%__install -Dm 0644 %{SOURCE13} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__ln_s /opt/%{full_name}/%{full_name} %{buildroot}%{_bindir}

# Install application icons
%__install -Dm 0644 %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{full_name}.png
%__install -Dm 0644 %{SOURCE3} %{buildroot}%{_datadir}/icons/hicolor/36x36/apps/%{full_name}.png
%__install -Dm 0644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%__install -Dm 0644 %{SOURCE5} %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%__install -Dm 0644 %{SOURCE6} %{buildroot}%{_datadir}/icons/hicolor/72x72/apps/%{full_name}.png
%__install -Dm 0644 %{SOURCE7} %{buildroot}%{_datadir}/icons/hicolor/96x96/apps/%{full_name}.png
%__install -Dm 0644 %{SOURCE8} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
%__install -Dm 0644 %{SOURCE9} %{buildroot}%{_datadir}/icons/hicolor/192x192/apps/%{full_name}.png
%__install -Dm 0644 %{SOURCE10} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{full_name}.png
%__install -Dm 0644 %{SOURCE11} %{buildroot}%{_datadir}/icons/hicolor/384x384/apps/%{full_name}.png
%__install -Dm 0644 %{SOURCE12} %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{full_name}.png

%files
/opt/figma-linux/
%{_datadir}/applications/figma-linux.desktop
%{_datadir}/icons/hicolor/24x24/apps/figma-linux.png
%{_datadir}/icons/hicolor/36x36/apps/figma-linux.png
%{_datadir}/icons/hicolor/48x48/apps/figma-linux.png
%{_datadir}/icons/hicolor/64x64/apps/figma-linux.png
%{_datadir}/icons/hicolor/72x72/apps/figma-linux.png
%{_datadir}/icons/hicolor/96x96/apps/figma-linux.png
%{_datadir}/icons/hicolor/128x128/apps/figma-linux.png
%{_datadir}/icons/hicolor/192x192/apps/figma-linux.png
%{_datadir}/icons/hicolor/256x256/apps/figma-linux.png
%{_datadir}/icons/hicolor/384x384/apps/figma-linux.png
%{_datadir}/icons/hicolor/512x512/apps/figma-linux.png
