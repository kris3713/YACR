%global         app_id org.%{maintainer}.%{app_name}
%global         app_name Picard
%global         maintainer musicbrainz
%global         forgeurl https://github.com/%{maintainer}/%{name}
%global         commit b4cfdb02dbe808e7ac73a34760aaf382e8d837f6
%global         debug_package %nil

Name:           %(v="%{app_name}"; echo "${v,}")
Version:        3.0.4
Summary:        MusicBrainz-based audio tagger
%if 0%{?buildtag:1}
%forgemeta
%global         build_id %(echo '%{buildtag}' | sed 's/^\\.copr//')
Release:        %autorelease -s %{build_id}
%else
Release:        %autorelease
%forgemeta
%endif

License:        GPL-2.0-or-later
URL:            https://%{name}.musicbrainz.org/

Source0:        %{forgesource}

BuildRequires:  gcc pyproject-rpm-macros desktop-file-utils
BuildRequires:  gettext pkgconfig pkgconfig(python3)
BuildRequires:  python3dist(discid) python3dist(markdown)
BuildRequires:  python3dist(mutagen) python3dist(pygit2)
BuildRequires:  python3dist(pyjwt) python3dist(pip)
BuildRequires:  python3dist(pyqt6) python3dist(tomlkit)
BuildRequires:  python3-setuptools
Recommends:     rsgain

%if 0%{?rhel}
ExcludeArch:    ppc64
%endif

%description
Picard is an audio tagging application using data from the MusicBrainz
database. The tagger is album or release oriented, rather than
track-oriented.


%prep
%forgeautosetup

sed -i 's/"PyJWT~=2\.12"/"PyJWT~=2.0"/' ./pyproject.toml


%build
export PICARD_DISABLE_AUTOUPDATE=1
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files %{name}

desktop-file-install \
  --delete-original --remove-category="Application"   \
  --dir=%{buildroot}%{_datadir}/applications      \
  %{buildroot}%{_datadir}/applications/*


%files -f %{pyproject_files}
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_datadir}/applications/%{app_id}.desktop
%{_iconsdir}/hicolor/*/apps/%{app_id}.*
%{_metainfodir}/%{app_id}.appdata.xml
%doc ./{AUTHORS.txt,README.md}
%license ./COPYING.txt


%changelog
%autochangelog
