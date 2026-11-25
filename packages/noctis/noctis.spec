%ifarch x86_64
%define         rel_type linux-x64
%else
%define         rel_type linux-arm64
%endif

%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/runtimes/.*$
%global         __spec_install_post %nil
%global         app_name Noctis
%global         debug_package %nil

Name:           %(echo %app_name | tr '[:upper:]' '[:lower:]')
Version:        1.7.2
Release:        1%{?dist}
Summary:        A music player that respects what's yours. Zero tracking, total control

License:        GPL-2.0-or-later
URL:            https://%{name}app.cc/

Source0:        https://github.com/heartached/%{app_name}/archive/refs/tags/v%{version}.tar.gz

Requires:       vlc-libs gtk-update-icon-cache
BuildRequires:  dotnet-sdk-10.0 vlc-devel

%description
%{summary}. Gapless playback, synced lyrics and full theming.
No account to make, no telemetry to switch off.

%prep
%autosetup -n ./%{app_name}-%{version}

%build
export NUGET_PACKAGES="$(realpath ./.nuget_cache)"
export DOTNET_NOLOGO=true
export DOTNET_CLI_TELEMETRY_OPTOUT=true

dotnet restore ./src/%{app_name}/%{app_name}.csproj
dotnet publish ./src/%{app_name}/%{app_name}.csproj \
  -c Release \
  -r %{rel_type} \
  --self-contained \
  '-p:PublishSingleFile=true' \
  '-p:DebugType=None' \
  '-p:DebugSymbols=false' \
  -o ./app

%install
# Remove unneeded runtime libraries
for glob_exp in 'win*' 'macos*'; do
  find ./app/runtimes \
    -type d \
    -name "$glob_exp" \
    -exec rm -rv '{}' +
done

# Copy the application files to the application directory
install -d %{buildroot}/opt/%{app_name}
cp -a ./app/* %{buildroot}/opt/%{app_name}

# Install the desktop file
CONTENT="$(cat << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=%app_name
Comment=%summary
Exec=%app_name
Icon=%name
Categories=Audio;Player;Music
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
