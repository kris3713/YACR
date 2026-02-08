%global         lib_name lib%{name}
%global         app_id org.nickvision.tubeconverter
%global         real_name Parabolic
%global         debug_package %nil

Name:           %(echo %real_name | tr '[:upper:]' '[:lower:]')
Version:        2026.2.1
Release:        1%{?dist}
Summary:        Download web video and audio.

License:        MIT
URL:            https://github.com/NickvisionApps/%{real_name}

Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

BuildRequires:  gcc gcc-c++ ninja-build cmake
BuildRequires:  cmake-rpm-macros libnick boost-devel
BuildRequires:  boost-date-time cpr-devel blueprint-compiler
BuildRequires:  gtk4-devel libadwaita-devel libxml++50-devel
BuildRequires:  libsecret-devel sqlcipher-devel yelp-tools patchelf
Requires:       libsecret gnome-keyring python3 %lib_name
# yt-dlp is not in needed in "Requires"
# as parabolic (or tubeconverter) downloads
# and maintains its own version.

%description
%summary

  * A powerful yt-dlp frontend
  * Supports downloading videos in multiple formats (mp4, webm, mp3, opus, flac, and wav)
  * Run multiple downloads at a time
  * Supports downloading metadata and video subtitles


%package -n %lib_name
Summary:        Core libraries required by %{name}.
Provides:       lib%{lib_name}.so()(%{_arch}) = %{version}-%{release}
%description -n %lib_name
%{summary}


%prep
%autosetup -n ./%{real_name}-%{version}


%build
# Setup and build the application
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build

# Name of the compiled executable
EXE_FILE='%{app_id}.gnome'
EXE_FILEPATH="./redhat-linux-build/$EXE_FILE/$EXE_FILE"

# Patch the broken rpath
patchelf --print-rpath "$EXE_FILEPATH"
patchelf --debug \
  --set-rpath %{_libdir}/%{lib_name} \
  "$EXE_FILEPATH"
patchelf --print-rpath "$EXE_FILEPATH"


%install
# Install Parabolic
%cmake_install
ln -s ./%{app_id} %{buildroot}%{_bindir}/%{name}
ln -s ./%{app_id} %{buildroot}%{_bindir}/tubeconverter

# Install libparabolic
install -d %{buildroot}%{_libdir}/%{lib_name}
cp -a ./redhat-linux-build/%{lib_name}/* \
  %{buildroot}%{_libdir}/%{lib_name}


%files
%{_bindir}/%{name}
%{_bindir}/%{app_id}
%{_bindir}/tubeconverter
%{_libdir}/%{app_id}
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/help/*/parabolic/*
%{_metainfodir}/%{app_id}.metainfo.xml
/usr/share/dbus-1/services/%{app_id}.service
%{_iconsdir}/hicolor/*/apps/*.svg
%license ./{COPYING,License.rtf}
%doc ./README.md ./docs


%files -n %lib_name
%{_libdir}/%{lib_name}


%changelog
%autochangelog
