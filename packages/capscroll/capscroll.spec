%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __spec_install_post %nil
%global         app_id %{app_name}.Desktop
%global         app_name CapScroll
%global         debug_package %nil

Name:           %(v='%{app_name}'; echo "${v,,}")
Version:        1.3.0
Release:        1%{?dist}
Summary:        Linux scrolling screenshot and region capture tool

License:        MIT
URL:            https://github.com/netcrawlerr/%{app_name}

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  dotnet-sdk-10.0
Requires:       libicu libX11

Recommends:     ydotool

%description
CapScroll is a %summary
built with .NET and Avalonia.


%prep
%autosetup -n ./%{app_name}-%{version}


%build
export DOTNET_NOLOGO=true
export DOTNET_CLI_TELEMETRY_OPTOUT=true

DESKTOP_PROJ='./src/%{app_id}/%{app_id}.csproj'
dotnet restore "$DESKTOP_PROJ"
dotnet publish "$DESKTOP_PROJ" \
  -c Release \
  -r linux-x64 \
  --self-contained true \
  '-p:PublishSingleFile=true' \
  '-p:PublishTrimmed=false' \
  '-p:DebugType=None' \
  '-p:DebugSymbols=false'


%install
PROJ_DIR='./src/%{app_id}'
RELEASE_DIR="$PROJ_DIR/bin/Release/net10.0/linux-x64/publish"

# Create needed directories
install -d %{buildroot}{/opt/%{app_name},%{_bindir}}

# Copy all application files to
# the application directory
cp -a "$RELEASE_DIR"/* %{buildroot}/opt/%{app_name}

# Symlink the application bin
ln -sv /opt/%{app_name}/%{app_id} \
  %{buildroot}%{_bindir}/%{name}

# Install the desktop file
CONTENT="$(cat << DESKTOP
[Desktop Entry]
Type=Application
Name=%app_name
Comment=%summary
Exec=%name
Icon=%{_iconsdir}/hicolor/512x512/%{name}.png
Terminal=false
Categories=Graphics;Utility
DESKTOP
)"
install -Dm 0644 /dev/stdin \
  %{buildroot}%{_datadir}/applications/%{app_id}.desktop <<< "$CONTENT"

# Install the application icon
install -Dm 0644 "$PROJ_DIR/Assets/Images/logo.png" \
  %{buildroot}%{_iconsdir}/hicolor/512x512/%{name}.png


%files
%{_bindir}/{%{app_id},%{name}}
/opt/%{app_name}
%{_datadir}/applications/%{app_id}.desktop
%{_iconsdir}/hicolor/512x512/%{name}.png
%license ./LICENSE
%doc ./README.md


%changelog
%autochangelog
