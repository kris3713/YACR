%global         __provides_exclude_from ^/opt/%{full_name}/.*$
%global         __requires_exclude_from ^/opt/%{full_name}/.*$
%global         real_name Figma-Linux
%global         full_name %(echo %real_name | tr '[:upper:]' '[:lower:]')
%global         debug_package %{nil}

Name:           %{full_name}-arm64
Version:        0.11.5
Release:        1%{?dist}
Summary:        %{real_name} is an unofficial Electron-based Figma desktop app for Linux.

License:        GPL-2.0
URL:            https://github.com/%{real_name}/%{full_name}

Source0:        %{url}/releases/download/v%{version}/%{full_name}_%{version}_linux_arm64.zip
Source1:        https://raw.githubusercontent.com/%{real_name}/%{full_name}/master/resources/%{full_name}.desktop

ExclusiveArch:  %arm64

%description
%summary


%prep
%setup -q -c -n ./%{full_name}


%install
# Setup the buildroot
install -d %{buildroot}{/opt/%{full_name},%{_bindir},%{_datadir}/applications}

sizes=(
  '24x24' '36x36' '48x48' '64x64' '72x72' '96x96'
  '128x128' '192x192' '256x256' '384x384' '512x512'
)
for size in "${sizes[@]}"; do
  install -d "%{buildroot}%{_iconsdir}/hicolor/$size/apps"
done
install -d %{buildroot}%{_iconsdir}/hicolor/scalable/apps

# Remove unneeded files in the build directory
rm -r ./{usr,lib,AppRun} ./*.sh

# Copy the application files to the application directory
cp -a . %{buildroot}/opt/%{full_name}

# Install the desktop file
install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Create a symlink to the application binary
ln -s /opt/%{full_name}/%{full_name} %{buildroot}%{_bindir}

# Install application icons
for size in "${sizes[@]}"; do
  install -Dm 0644 "./icons/$size.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{name}.png"
done
install -Dm 0644 ./icons/scalable.svg \
  %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.png

# Remove unneeded files in the application directory
rm -r %{buildroot}/opt/%{full_name}/icons


%files
/opt/%{full_name}
%{_bindir}/%{full_name}
%{_datadir}/applications/%{full_name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png


%changelog
%autochangelog
