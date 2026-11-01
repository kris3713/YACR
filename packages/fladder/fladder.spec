%global         __brp_check_rpaths %nil
# The reason for this is to avoid the "broken rpath" error

%global         __provides_exclude_from ^/opt/%{name}/.*$
%global         __requires_exclude_from ^/opt/%{name}/.*$
%global         app_id nl.jknaapen.%{name}
%global         app_name Fladder
%global         debug_package %nil

Name:           %(echo %app_name | tr '[:upper:]' '[:lower:]')
Version:        0.11.1
Release:        1%{?dist}
Summary:        A cross-platform Jellyfin Frontend built on top of Flutter.

License:        GPL-3.0
URL:            https://github.com/DonutWare/%{app_name}

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

# `flutter` is provided by `mise`
BuildRequires:  mise
BuildRequires:  git cmake clang ninja-build glib2-devel gtk3-devel
BuildRequires:  mpv-devel libcurl-devel libevdev-devel
BuildRequires:  jq
Requires:       glib2 gtk3 mpv-libs libcurl libevdev

ExclusiveArch:  x86_64

%description
%summary


%prep
%autosetup -n ./%{app_name}-%{version}


%build
# Get required flutter version from .fvmrc
flutter_version="$(jq '.flutter' ./.fvmrc -r)"

# Setup mise, and install flutter
export MISE_GLOBAL_CONFIG_FILE=''
export MISE_CACHE_DIR="$(realpath ./.mise_cache)"
export MISE_DATA_DIR="$(realpath ./.mise_data)"
export PUB_CACHE="$(realpath ./.pub-cache)"
mise install "vfox:mise-plugins/vfox-flutter@$flutter_version"

# Modify $PATH
export PATH="$(mise where "vfox:mise-plugins/vfox-flutter@$flutter_version")/bin:$PATH"

# Build the application
unset CFLAGS CXXFLAGS LDFLAGS
flutter --no-version-check pub get
flutter --no-version-check gen-l10n
flutter --no-version-check build linux --release -v


%install
# Create the new build root
install -d %{buildroot}{%{_bindir},/opt/%{name}}

# Copy the application files to the application directory
cp -a ./build/linux/x64/release/bundle/* %{buildroot}/opt/%{name}

# Create a symlink to the application binary
ln -s /opt/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

# Install the desktop file
CONTENT="$(cat << 'DESKTOP'
[Desktop Entry]
Name=%app_name
StartupWMClass=%app_id
Comment=A Simple Jellyfin Frontend built on top of Flutter.
Exec=%name %%u
Icon=%app_id
Terminal=false
Type=Application
Categories=AudioVideo;Video;Player;Jellyfin
MimeType=x-scheme-handler/fladder
DESKTOP
)"
install -Dm 0644 /dev/stdin \
  %{buildroot}%{_datadir}/applications/%{app_name}.desktop <<< "$CONTENT"

# Install the application icons
install -Dm 0644 ./icons/%{name}_icon.svg \
  %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{app_id}.svg
install -Dm 0644 ./icons/production/%{name}_icon_512.png \
  %{buildroot}%{_iconsdir}/hicolor/512x512/apps/%{app_id}.png
install -Dm 0644 ./icons/production/%{name}_icon_desktop.png \
  %{buildroot}%{_iconsdir}/hicolor/1024x1030/apps/%{app_id}.png

# Install the application metainfo file
install -Dm 0644 ./flatpak/%{app_id}.metainfo.xml \
  -t %{buildroot}%{_metainfodir}


%files
/opt/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{app_name}.desktop
%{_iconsdir}/hicolor/*/apps/%{app_id}.*
%{_metainfodir}/%{app_id}.metainfo.xml
%license ./LICENSE


%changelog
%autochangelog
