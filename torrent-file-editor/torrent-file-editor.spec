%global         full_name torrent-file-editor
%global         debug_package %{nil}

Name:           torrent-file-editor
Version:        1.0.0
Release:        1%{?dist}
Summary:        Cross-platform application intended to create and edit .torrent and uTorrent .dat files.

License:        GPL-3.0
URL:            https://torrent-file-editor.github.io/

Source0:        https://github.com/torrent-file-editor/torrent-file-editor/archive/refs/tags/v%{version}.tar.gz

# NOTE: Only building for Qt6, there are not plans to support Qt5 or lower.
BuildRequires:  cmake qt6-qttools-devel qt6-qt5compat-devel git
# Requires:       # Add required packages here

%description
Cross-platform application intended to create and edit .torrent and uTorrent .dat files.

%prep
%setup -q -n %{full_name}-%{version}

%build
%__mkdir build
cd ./build
# Generate cmake build files
%__cmake -DCMAKE_BUILD_TYPE=Release -DQT6_BUILD=ON ..
# Build the application binary
%__make
cd ..

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create a new build root (along with other directories)
%__install -d %{buildroot}{%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64,128x128,256x256}/apps

# NOTE: Might add an /opt directory if required
# # Copy the application binary to the application directory
# %__cp -a ./build/%{full_name} %{buildroot}/opt/%{full_name}

# Install the application binary
%__install -D -m 0755 ./build/%{full_name} %{buildroot}%{_bindir}

# Install the desktop file
%__install -D -m 0644 ./%{full_name}.desktop %{buildroot}%{_datadir}/applications

# Install application icons
%__install -D -m 0644 ./icons/app_16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%__install -D -m 0644 ./icons/app_32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%__install -D -m 0644 ./icons/app_48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%__install -D -m 0644 ./icons/app_64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%__install -D -m 0644 ./icons/app_128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
%__install -D -m 0644 ./icons/app_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{full_name}.png

%files
%{_bindir}/%{full_name}
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{full_name}.png
%license LICENSE

%changelog
* Fri May 16 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 1.0.0-1
- Initial packaging of torrent-file-editor version 1.0.0
