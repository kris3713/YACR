%global         app_name FastFlix
%global         pypi_name python-%name
%global         srcname %(v="%{app_name}"; echo "${v,,}")
%global         debug_package %nil

Name:           %srcname
Version:        6.3.2
Release:        1%{?dist}
Summary:        %{app_name} is a handy GUI for encoding videos.

License:        MIT
URL:            https://%{name}.org/

Source0:        https://github.com/cdgriffith/%{app_name}/archive/refs/tags/%{version}.tar.gz

BuildRequires:  gcc pyproject-rpm-macros desktop-file-utils
BuildRequires:  gettext pkgconfig pkgconfig(python3)
BuildRequires:  python3dist(platformdirs) python3dist(chardet)
BuildRequires:  python3dist(colorama) python3dist(coloredlogs)
BuildRequires:  python3dist(iso639-lang) python3dist(mistune)
BuildRequires:  python3dist(packaging) python3dist(pathvalidate)
BuildRequires:  python3dist(psutil) python3dist(pydantic)
BuildRequires:  python3dist(pyside6) python3dist(python-box[all])
BuildRequires:  python3dist(requests) python3dist(setuptools)
BuildRequires:  python3dist(ffmpeg-normalize) python3dist(reusables)
BuildRequires:  python3dist(pgsrip) python3dist(pytesseract)
BuildRequires:  python3dist(babelfish) python3dist(cleanit)
BuildRequires:  python3dist(trakit) python3dist(opencv-python)
BuildRequires:  python3dist(pysrt) python3dist(pip)
BuildRequires:  python3dist(setuptools-scm[toml])
BuildRequires:  python3dist(wheel) python3dist(chardet)
BuildRequires:  python3dist(mistune) python3dist(pathvalidate)
BuildRequires:  python3dist(psutil)
BuildRequires:  icoutils

Recommends: tesseract mkvtoolnix

%description
%app_name is a free GUI for H.264, HEVC and AV1 hardware and software encoding!


%prep
%autosetup -n ./%{app_name}-%{version}


# %%generate_buildrequires
# %%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files '%{name}'

# Install the desktop file
CONTENT="$(cat << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=%app_name
Comment=%summary
GenericName=Video Encoder
Exec=%name
StartupWMClass=%name
Icon=%name
Terminal=false
MimeType=inode/directory
Categories=Audio;AudioVideo;Video;AudioVideoEditing
DESKTOP
)"
install -Dm 0644 /dev/stdin \
  %{buildroot}%{_datadir}/applications/%{name}.desktop <<< "$CONTENT"

# Install the application icon
icotool ./%{name}/data/icon.ico \
  --extract --index=1 -o ./%{name}.png
install -Dm 0644 ./%{name}.png \
  -t %{buildroot}%{_iconsdir}/hicolor/256x256/apps


%files -f %{pyproject_files}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/256x256/apps/%{name}.png
%doc ./README.md
%license ./LICENSE


%changelog
%autochangelog
