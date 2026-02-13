# rpmbuild keeps adding this non-existant requirement
%global         __requires_exclude liblttng-ust.*

%global         project %{org}.%{real_name}.GNOME
%global         org %%(str="$(echo %app_id | cut '-d.' -f2)"; echo "${str^}")
%global         app_id org.nickvision.tubeconverter
%global         real_name Parabolic
%global         debug_package %nil

%ifarch x86_64
%global         rel_type linux-x64
%else
%global         rel_type linux-arm64
%endif

Name:           %(echo %real_name | tr '[:upper:]' '[:lower:]')
Version:        2026.2.2
Release:        1%{?dist}
Summary:        Download web video and audio.

License:        MIT
URL:            https://github.com/NickvisionApps/%{real_name}

Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

Patch0:         fix_chmod_cmd.patch

BuildRequires:  dotnet-sdk-10.0 blueprint-compiler
BuildRequires:  gtk4-devel libadwaita-devel
BuildRequires:  libsecret-devel gettext-devel
Requires:       libsecret gnome-keyring python3
# yt-dlp is not in needed in "Requires"
# as parabolic (or tubeconverter) downloads
# and maintains its own version.

%description
%summary

  * A powerful yt-dlp frontend
  * Supports downloading videos in multiple formats (mp4, webm, mp3, opus, flac, and wav)
  * Run multiple downloads at a time
  * Supports downloading metadata and video subtitles


%prep
%autosetup -p1 -n ./%{real_name}-%{version}


%build
export NUGET_PACKAGES="$(realpath ./.nuget_cache)"
export DOTNET_NOLOGO='true'
export DOTNET_CLI_TELEMETRY_OPTOUT='true'

dotnet publish -c Release -r %rel_type \
  --self-contained --ucr -v m \
  '-p:PublishReadyToRun=true' \
  '-p:DebugType=None' '-p:DebugSymbols=false' \
  ./%{project}/%{project}.csproj

ln -sv ./%{project}/bin/Release/net10.0/%{rel_type}/publish ./build


%install
RESRCS='./resources'
LINUX_RESRCS="$RESRCS/linux"
APP_DIR='/opt/%{real_name}'
DESKTOP_FILE='%{buildroot}%{_datadir}/applications/%{app_id}.desktop'
SERVICE_FILE='%{buildroot}%{_datadir}/dbus-1/services/%{app_id}.service'
METADATA_FILE='%{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml'

# Setup buildroot
install -d %{buildroot}{"$APP_DIR",%{_bindir},%{_datadir}/applications}
install -d %{buildroot}{%{_datadir}/dbus-1/services,%{_metainfodir}}

# Copy application files to application directory
cp -a ./build/* "%{buildroot}$APP_DIR"

# Create symlinks to the application executable
ln -sv "$APP_DIR/%{project}" %{buildroot}%{_bindir}/%{app_id}
ln -sv ./%{app_id} %{buildroot}%{_bindir}/%{name}

# Install desktop file
install -Dm 0644 "$LINUX_RESRCS/%{app_id}.desktop.in" "$DESKTOP_FILE"
sed -i 's|@APP_ID@|%{app_id}|' "$DESKTOP_FILE"
sed -i 's|@LIB_DIR@/@OUTPUT_NAME@|%{app_id}|' "$DESKTOP_FILE"

# Install service file
install -Dm 0644 "$LINUX_RESRCS/%{app_id}.service.in" "$SERVICE_FILE"
sed -i 's|@APP_ID@|%{app_id}|' "$SERVICE_FILE"
sed -i "s|@LIB_DIR@/@OUTPUT_NAME@|%{app_id}|" "$SERVICE_FILE"

# Install metadata file
install -Dm 0644 "$LINUX_RESRCS/%{app_id}.metainfo.xml" "$METADATA_FILE"

# Copy icons
SCALABLE_ICON_DIR="%{buildroot}%{_iconsdir}/hicolor/scalable/apps"
SYMBOLIC_ICON_DIR="%{buildroot}%{_iconsdir}/hicolor/symbolic/apps"
for icon_filepath in "$RESRCS"/%{app_id}{.svg,-devel.svg}; do
  install -Dm 0644 "$icon_filepath" -t "$SCALABLE_ICON_DIR"
done

install -Dm 0644 "$RESRCS/%{app_id}-symbolic.svg" -t "$SYMBOLIC_ICON_DIR"


%files
%{_bindir}/%{app_id}
%{_bindir}/%{name}
/opt/%{real_name}
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/dbus-1/services/%{app_id}.service
%{_metainfodir}/%{app_id}.metainfo.xml
%{_iconsdir}/hicolor/*/apps/*.svg
%license ./{LICENSE,License.rtf}
%doc ./README.md


%changelog
%autochangelog
