%global         __brp_check_rpaths %{nil}
# The reason for this is to avoid the "broken rpath" error

%define         rel_url https://github.com/alexmercerind2/harmonoid-releases

%global         __provides_exclude_from ^/opt/%{name}/.*$
%global         __requires_exclude_from ^/opt/%{name}/.*$
%global         debug_package %{nil}

Name:           harmonoid
Version:        0.3.16
Release:        1%{?dist}
Summary:        Plays & manages your music library. Looks beautiful & juicy.

# No need to include the PolyForm-Strict-1.0.0 license as were are not compiling from source
License:        Freeware/Custom (See LICENSE.txt)
URL:            https://harmonoid.com/

Source0:        %{rel_url}/releases/download/v%{version}/harmonoid-linux-x86_64.tar.gz
Source1:        %{rel_url}/raw/refs/heads/main/LICENSE.txt

BuildRequires:  fd-find
Requires:       mpv mpv-libs (ffmpeg-devel or ffmpeg-free-devel)

ExclusiveArch:  x86_64

%description
Plays & manages your music library. Looks beautiful & juicy.

Features:

* Performant media library & tag reader.
* Material Design 3 & 2.
* Light & dark themes.
* Gapless playback.
* Speed adjustment.
* Pitch adjustment.
* Volume boost.
* Portable.
* Discord RPC integration.
* mpv backend.
* Lyrics (LRC, tags & online).
* Playlists.
* Multiple artist & genre support.
* Fallback cover support. e.g. cover.jpg, Folder.jpg etc.
* Small installer (≈ 35 MB) & low RAM usage (≈ 150 MB).
* Excellent backward compatibility. Android 5.0 or higher. macOS 10.9 or higher. Windows 7 or higher.
* Cross-platform (macOS, Windows, GNU/Linux & Android).
* Notification.MediaStyle for Android.
* D-Bus MPRIS controls for GNU/Linux.
* MPNowPlayingInfoCenter for macOS.
* System Media Transport Controls & Taskbar Thumbnail Toolbar for Windows.

%prep
%setup -q -n ./usr/share

%install
export QA_RPATHS=$[ 0x0002 | 0x0010 ]
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},/opt/%{name},%{_datadir}/applications,%{_iconsdir}/hicolor,%{_metainfodir}}

# Copy the application files to the application directory
%__cp -a ./%{name}/* %{buildroot}/opt/%{name}

# Install the desktop file
%__install -Dm 0644 ./applications/%{name}.desktop -t %{buildroot}%{_datadir}/applications

# Create a symlink to the application binary
%__ln_s /opt/%{name}/%{name} %{buildroot}%{_bindir}

# Install the application icons
%__cp -a ./icons/hicolor/* %{buildroot}%{_iconsdir}/hicolor
fd -e spec . %{buildroot}%{_iconsdir}/hicolor --exec %__chmod 0644 {}

# Install the application metainfo file
%__install -Dm 0644 ./metainfo/%{name}.appdata.xml -t %{buildroot}%{_metainfodir}

# Copy the license file
%__cp -a %{SOURCE1} .

%files
/opt/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*
%{_metainfodir}/%{name}.appdata.xml
%license ./LICENSE.txt

%changelog
%autochangelog
