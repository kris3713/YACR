%ifarch x86_64
%define         rel_type linux-x64
%else
%define         rel_type linux-arm64
%endif

%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         __spec_install_post %nil
%global         app_name Noctis
%global         debug_package %nil

Name:           %(echo %app_name | tr '[:upper:]' '[:lower:]')
Version:        1.6.5
Release:        1%{?dist}
Summary:        A music player that respects what's yours. Zero tracking, total control

License:        GPL-2.0-or-later
URL:            https://noctisapp.cc/

Source0:        https://github.com/heartached/%{app_name}/archive/refs/tags/v%{version}.tar.gz

Requires:       vlc-libs
BuildRequires:  dotnet-sdk-10.0 vlc-devel

%description
%{summary}. Gapless playback, synced lyrics and full theming.
No account to make, no telemetry to switch off.

%prep
%autosetup -n ./%{app_name}-%{version}

%build
env DOTNET_NOLOGO=true DOTNET_CLI_TELEMETRY_OPTOUT=true \
  dotnet publish ./src/%{app_name}/%{app_name}.csproj -c Release -r %{rel_type} \
  --self-contained '-p:DebugType=None' '-p:DebugSymbols=false' \
  -o ./app

%install
# Copy the application files to the application directory
install -d %{buildroot}/opt/%{app_name}
cp -a ./app/* %{buildroot}/opt/%{app_name}

# Install the desktop file
CONTENT="$(cat << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=Noctis
Comment=A music player that respects what's yours
Exec=Noctis
Icon=noctis
Categories=AudioVideo;Audio;Player
Terminal=false
DESKTOP
)"
install -Dm 0644 /dev/stdin \
  %{buildroot}%{_datadir}/applications/%{name}.desktop <<< "$CONTENT"

# Create a symlink to the application binary
install -d %{buildroot}%{_bindir}
ln -sv /opt/%{app_name}/%{app_name} -t %{buildroot}%{_bindir}

# Install the application icons
install -Dm 0644 ./website/src/assets/logo-mark.svg \
  %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
sizes=('512' '192' '48' '32')
for size in "${sizes[@]}"; do
  dirname="${size}x${size}"
  if [ -f "./website/public/icons/icon-${size}.png" ]; then
    install -Dm 0644 "./website/public/icons/icon-${size}.png" \
      "%{buildroot}%{_iconsdir}/hicolor/$dirname/apps/%{name}.png"
  else
    install -Dm 0644 "./website/public/icons/favicon-${size}.png" \
      "%{buildroot}%{_iconsdir}/hicolor/$dirname/apps/%{name}.png"
  fi
done

%post
gtk-update-icon-cache %{_iconsdir}/hicolor -f

%files
/opt/%{app_name}
%{_bindir}/%{app_name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*
%license ./LICENSE

%changelog
%autochangelog
