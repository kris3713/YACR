%global         fullname youtube-dl-gui
%global         py_name youtube_dl_gui
%global         __python %python3
%global         __requires_exclude_from ^%{python_sitelib}/.*$
%global         debug_package %{nil}

Name:           yt-dlg
Version:        1.8.5
Release:        1%{?dist}
Summary:        GUI for youtube-dl

License:        Unlicense
URL:            https://oleksis.github.io/youtube-dl-gui/

Source0:        https://github.com/oleksis/youtube-dl-gui/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}.desktop

BuildRequires:  make libxcrypt-compat fdupes open-sans-fonts gettext python3 python3-devel
BuildRequires:  python3-polib python3-pypubsub python3-wxpython4 python3-setuptools
Requires:       python3 python3-polib python3-pypubsub python3-wxpython4 python3-setuptools
Recommends:     yt-dlp ffmpeg

%description
A front-end GUI for the popular youtube-dl written in wxPython.

%prep
%setup -q -n ./%{fullname}-%{version}

%build
# For whatever reason, this has to be executed twice or find_lang fails
for _ in {1..2}; do
  %py3_build -- -- build_trans no_updates
done

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},%{_datadir}/{applications,pixmaps},%{_mandir}/man1}
%__install -d %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64,128x128,256x256}/apps
%__install -d %{buildroot}%{python_sitelib}/{%{py_name},yt_dlg-%{version}-py%{python_version}.egg-info}

%py3_install
%__cp -a ./%{py_name}/data/pixmaps/* %{buildroot}%{_datadir}/pixmaps
%find_lang youtube_dl_gui

# Install desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

cat << EOF > README.install
This application downloads the last youtube-dl on ~/.config/yt-dlg
EOF
%__chmod a+r README.install

%__sed -i 's/pyinstaller<=5.6.2,>=3.6//g' \
  %{buildroot}%{python3_sitelib}/yt_dlg-%{version}-py%{python3_version}.egg-info/requires.txt

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{fullname}.1*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps
%{_iconsdir}/hicolor/16x16/apps/%{fullname}.png
%{_iconsdir}/hicolor/32x32/apps/%{fullname}.png
%{_iconsdir}/hicolor/48x48/apps/%{fullname}.png
%{_iconsdir}/hicolor/64x64/apps/%{fullname}.png
%{_iconsdir}/hicolor/128x128/apps/%{fullname}.png
%{_iconsdir}/hicolor/256x256/apps/%{fullname}.png
%{python_sitelib}/%{py_name}
%{python_sitelib}/yt_dlg-%{version}-py%{python_version}.egg-info
%license ./LICENSE

%changelog
%autochangelog
