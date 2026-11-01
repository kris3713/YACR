%global         __brp_check_rpaths %nil
# The reason for this is to avoid the "broken rpath" error

%global         __provides_exclude_from ^/opt/%{name}/.*$
%global         __requires_exclude_from ^/opt/%{name}/.*$
%global         app_id com.edde746.%{name}
%global         debug_package %nil

Name:           plezy
Version:        2.25.0
Release:        1%{?dist}
Summary:        Modern cross-platform Plex, Jellyfin and Emby client

License:        GPL-3.0
URL:            https://%{name}.app/

Source0:        https://github.com/edde746/%{name}/archive/refs/tags/%{version}.tar.gz

# `flutter` is provided by `mise`
BuildRequires:  mise
BuildRequires:  git cmake clang ninja-build glib2-devel gtk3-devel
BuildRequires:  mpv-devel libcurl-devel libevdev-devel java-25-openjdk-devel
Requires:       glib2 gtk3 mpv-libs libcurl libevdev

ExclusiveArch:  x86_64

%description
A modern client for Plex, Jellyfin, and Emby on desktop, mobile, and TV.
Built with Flutter for native performance and a clean interface.


%prep
%autosetup -n ./%{name}-%{version}


%build
# Setup mise, and install flutter
export MISE_GLOBAL_CONFIG_FILE=''
export MISE_CACHE_DIR="$(realpath ./.mise_cache)"
export MISE_DATA_DIR="$(realpath ./.mise_data)"
export PUB_CACHE="$(realpath ./.pub-cache)"
mise install 'vfox:mise-plugins/vfox-flutter@latest'

# Modify $PATH
export PATH="$(mise where 'vfox:mise-plugins/vfox-flutter@latest')/bin:$PATH"

# Build the application
unset CFLAGS CXXFLAGS
real_dir="$(dirname "$(readlink -f "$(command -v javac)")")"
export JAVA_HOME="$(dirname "$real_dir")"
flutter --no-version-check pub get
flutter --no-version-check build linux --release -v


%install
# Create the new build root
install -d %{buildroot}{%{_bindir},/opt/%{name}}

# Copy the application files to the application directory
cp -a ./build/linux/x64/release/bundle/* %{buildroot}/opt/%{name}

# Install the shell script wrapper to the application directory
linux_packaging='./linux/packaging'
install -Dm 0755 "$linux_packaging/%{name}.sh" \
  -t %{buildroot}/opt/%{name}

# Create a symlink to the application binary
ln -s /opt/%{name}/%{name}.sh %{buildroot}%{_bindir}/%{name}

# Install the desktop file
install -Dm 0644 "$linux_packaging/%{app_id}.desktop" \
  -t %{buildroot}%{_datadir}/applications

# Install the application metainfo file
install -Dm 0644 "$linux_packaging/flatpak/%{app_id}.metainfo.xml" \
  -t %{buildroot}%{_metainfodir}

# Install the application icons
install -Dm 0644 ./assets/%{name}.svg \
  -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps
install -Dm 0644 ./assets/%{name}.png \
  -t %{buildroot}%{_iconsdir}/hicolor/1024x1024/apps


%files
/opt/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{app_id}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_metainfodir}/%{app_id}.metainfo.xml
%license ./LICENSE


%changelog
%autochangelog
