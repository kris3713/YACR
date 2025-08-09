%global         __brp_check_rpaths %{nil}
# The reason for this is to avoid the "broken rpath" error

%define         sed_script 's/opt.backgroundBrush = {}/opt.backgroundBrush = Qt::NoBrush/g'
%define         libvgm_sha1 0833b26bcda4fce9d870a22f2adb8e0cd525be22

%global         __spec_install_post %{nil}
%global         __os_install_post %{_dbpath}/brp-compress
%global         app_name org.fooyin.fooyin
%global         debug_package %{nil}

Name:           fooyin
Version:        0.8.1
Release:        1%{?dist}
Summary:        A customisable music player inspired by foobar2000

License:        GPL-3.0-or-later
URL:            https://www.fooyin.org/

Source0:        https://github.com/fooyin/fooyin/archive/refs/tags/v%{version}.tar.gz
Source1:        https://github.com/ValleyBell/libvgm/archive/%{libvgm_sha1}.tar.gz#/libvgm-%{libvgm_sha1}.tar.gz

BuildRequires:  fd-find cmake ninja-build glib2-devel libxkbcommon-x11-devel libxkbcommon-devel
BuildRequires:  alsa-lib-devel qt6-qtbase-devel qt6-qtsvg-devel qt6-qttools-devel libavdevice-free-devel
BuildRequires:  libavcodec-free-devel libavformat-free-devel libavutil-free-devel libswresample-free-devel
BuildRequires:  taglib-devel kdsingleapplication-qt6-devel libicu-devel pipewire-devel libsndfile-devel
BuildRequires:  SDL2-devel libopenmpt-devel game-music-emu-devel libarchive-devel libebur128-devel
Requires:       qt6-qtbase qt6-qttools libicu74

ExclusiveArch:  x86_64

%description
fooyin is a music player built around customisation. It provides
a variety of widgets to help you manage and play your local collection.
It's highly extensible with a plugin system and includes FooScript,
a scripting language for advanced configuration of widgets.
A layout editing mode enables the entire user interface to be customised,
starting from a blank slate or a preset layout.

%prep
%setup -q -n ./%{name}-%{version}

%build
# Unpack libvgm (Need since tarballs don't retain refrences to other git repositories)
%__tar -xf %{SOURCE1} '--strip-components=1' -C ./3rdparty/libvgm

# Generate build environment
%__mkdir build
%__cmake -S . -G Ninja -B ./build '-DCMAKE_BUILD_TYPE=Release'

# Manually correct some issues present in some source code files before building
%__sed -i -e %{sed_script} ./src/gui/{dirbrowser/dirdelegate,librarytree/librarytreedelegate}.cpp
%__sed -i -e %{sed_script} ./src/gui/playlist/organiser/playlistorganiserdelegate.cpp

# Build the application
%__cmake --build ./build "-j$(nproc)" &> /dev/null

%install
export QA_RPATHS=$[ 0x0002 | 0x0010 ]
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},%{_libdir}/%{name},%{_datadir}/%{name}/translations,%{_datadir}/applications}
%__install -d %{buildroot}%{_iconsdir}/hicolor/{16x16,22x22,32x32,48x48,64x64,128x128,256x256,512x512,scalable}/apps
%__install -d %{buildroot}%{_sysconfdir}/ld.so.conf.d

# Make sure the shared libraries are discoverable
echo "%{_libdir}/%{name}" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

# Install the desktop file
%__install -Dm 0644 ./dist/linux/%{app_name}.desktop.in %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install the application binary
%__install -Dm 0755 ./build/run/bin/%{name} -t %{buildroot}%{_bindir}

# Install the libraries required by the application
fd . ./build/run/lib64/%{name} -t symlink --exec %__rm {}
%__cp -a ./build/run/lib64/%{name}/* %{buildroot}%{_libdir}/%{name}

# Install the application icons
%__install -Dm 0644 ./data/icons/16-%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{app_name}.png
%__install -Dm 0644 ./data/icons/22-%{name}.png %{buildroot}%{_iconsdir}/hicolor/22x22/apps/%{app_name}.png
%__install -Dm 0644 ./data/icons/32-%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{app_name}.png
%__install -Dm 0644 ./data/icons/48-%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{app_name}.png
%__install -Dm 0644 ./data/icons/64-%{name}.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{app_name}.png
%__install -Dm 0644 ./data/icons/128-%{name}.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{app_name}.png
%__install -Dm 0644 ./data/icons/256-%{name}.png %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{app_name}.png
%__install -Dm 0644 ./data/icons/512-%{name}.png %{buildroot}%{_iconsdir}/hicolor/512x512/apps/%{app_name}.png
%__install -Dm 0644 ./data/icons/sc-%{name}.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{app_name}.svg

# Install the application metainfo file
%__install -Dm 0644 ./dist/linux/%{app_name}.metainfo.xml -t %{buildroot}%{_metainfodir}

# Copy the translation files
%__cp -a ./build/data/*.qm %{buildroot}%{_datadir}/%{name}/translations

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/16x16/apps/%{app_name}.png
%{_iconsdir}/hicolor/22x22/apps/%{app_name}.png
%{_iconsdir}/hicolor/32x32/apps/%{app_name}.png
%{_iconsdir}/hicolor/48x48/apps/%{app_name}.png
%{_iconsdir}/hicolor/64x64/apps/%{app_name}.png
%{_iconsdir}/hicolor/128x128/apps/%{app_name}.png
%{_iconsdir}/hicolor/256x256/apps/%{app_name}.png
%{_iconsdir}/hicolor/512x512/apps/%{app_name}.png
%{_iconsdir}/hicolor/scalable/apps/%{app_name}.svg
%{_metainfodir}/%{app_name}.metainfo.xml
%{_datadir}/%{name}/translations
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}.conf
%license ./COPYING
