%global         app_name Parabolic
%global         git_url https://github.com/NickvisionApps/Parabolic
%global         debug_package %{nil}

Name:           parabolic
Version:\s+8.1.42025.5.5
Release:        1%{?dist}
Summary:        Download web video and audio

License:        GPL-3.0
URL:            %{git_url}

Source0:        %{git_url}/archive/refs/tags/%{version}.tar.gz

BuildRequires:  cmake vcpkg boost boost-devel boost-date-time gtest gtest-devel
BuildRequires:  qt6-qtbase qt6-qtbase-devel qt6-qtbase-gui qt6-qttools
BuildRequires:  qt6-qttools-devel qt6-qtsvg-devel qt-devel qt6-qtdeclarative-devel

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
# Install the libnick dependency
export VCPKG_ROOT="%{_builddir}/vcpkg"
export VCPKG_DEFAULT_TRIPLET='x64-linux'
vcpkg install libnick

# Build the application
cd ./build
cmake .. "-DCMAKE_BUILD_TYPE=Release" "-DUI_PLATFORM=qt"
cmake --build .
cd ..

%install


%files
%license add-license-file-here
%doc add-docs-here
