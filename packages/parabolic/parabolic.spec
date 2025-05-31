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

BuildRequires:  git python3-pip python3-jinja2 perl ninja-build libstdc++-devel wget
BuildRequires:  autoconf-archive autoconf flex libtool gawk cmake bison libcurl-devel
BuildRequires:  blueprint-compiler libxml++-devel gtk4-devel gtk4-devel-tools libadwaita-devel
BuildRequires:  libsecret-devel boost-devel boost-date-time gtest-devel desktop-file-utils yelp
Requires:       desktop-file-utils

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
BASE_URL='https://raw.githubusercontent.com/FlawlessCasual17/YACR'
curl -s "$BASE_URL/refs/heads/master/scripts/install-vcpkg" -o ./install-vcpkg
%__chmod +x ./install-vcpkg
./install-vcpkg &> /dev/null
%__rm -f ./install-vcpkg

# Set environmental variables
export VCPKG_ROOT="%{_builddir}/vcpkg"
%__mkdir_p "$VCPKG_ROOT"
export VCPKG_DEFAULT_TRIPLET='x64-linux'

# Install the required c++ libraries
%{vcpkg} install libnick &> /dev/null

# Build the application
%__mkdir build && cd ./build
%__cmake .. '-DCMAKE_BUILD_TYPE=Release' '-DUI_PLATFORM=gnome' "-Dlibnick_DIR=$VCPKG_ROOT/installed/x64-linux/share/libnick"
%__cmake --build .
cd ..

%install


%files
%license add-license-file-here
%doc add-docs-here
