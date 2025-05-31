%define         vcpkg ./vcpkg/vcpkg
%global         app_name Parabolic
%global         git_url https://github.com/NickvisionApps/Parabolic
%global         debug_package %{nil}

Name:           parabolic
Version:        2025.5.5
Release:        1%{?dist}
Summary:        Download web video and audio

License:        GPL-3.0
URL:            %{git_url}

Source0:        %{git_url}/archive/refs/tags/%{version}.tar.gz

# parabolic dependencies
BuildRequires:  qt6-qtbase-devel qt6-qtbase-gui qt6-qttools-devel
BuildRequires:  qt6-qtsvg-devel qt-devel qt6-qtdeclarative-devel
# vcpkg dependencies
BuildRequires:  git python3-pip python3-jinja2 perl ninja-build libstdc++-devel
BuildRequires:  wget autoconf-archive flex gcc-c++ autoconf libtool gawk
BuildRequires:  cmake bison boost-devel boost-date-time gtest-devel
BuildRequires:  libxkbcommon-devel mesa-libEGL-devel xcb-util-cursor-devel
BuildRequires:  xcb-util-wm-devel xcb-util-renderutil-devel xcb-util-keysyms-devel
BuildRequires:  xcb-util-image-devel xcb-util-devel

Recommends:     ffmpeg yt-dlp

ExclusiveArch:  x86_64

%description
Download web video and audio

* A basic yt-dlp frontend
* Supports downloading videos in multiple formats (mp4, webm, mp3, opus, flac, and wav)
* Run multiple downloads at a time
* Supports downloading metadata and video subtitles

%prep
%setup -q -n ./%{app_name}-%{version}

%build
# Install vcpkg
BASE_URL='https://gist.githubusercontent.com/FlawlessCasual17/2ac42388ee357363bbae41567391778d'
curl -s "$BASE_URL/raw/417c5ba672ce217b13626363ea3de0efbb257b6f/install-vcpkg" -o ./install-vcpkg
chmod +x ./install-vcpkg
./install-vcpkg &> /dev/null

# Set environmental variables
if [ -z "$VCPKG_ROOT" ]; then
  export VCPKG_ROOT="%{_builddir}/vcpkg"
fi
%__mkdir_p "$VCPKG_ROOT"
export VCPKG_DEFAULT_TRIPLET='x64-linux'

# Install the required c++ libraries
%{vcpkg} install libnick qtbase qlementine qlementine-icons &> /dev/null

# Build the application
cd ./build
%__cmake .. '-DCMAKE_BUILD_TYPE=Release' '-DUI_PLATFORM=qt'
%__cmake --build .
cd ..

%install


%files
%license add-license-file-here
%doc add-docs-here
