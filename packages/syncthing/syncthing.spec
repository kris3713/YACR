%global         debug_package %{nil}
%global         goipath github.com/syncthing/syncthing
%global         tag v%{version}%{?rcnum:-rc.%{rcnum}}

Name:           syncthing
Summary:        Continuous File Synchronization
Version:        2.0.13
Release:        1%{?dist}
License:        MPL-2.0

%gometa -f

URL:            https://syncthing.net
# use official release tarball (contains vendored dependencies)
Source0:        %{gourl}/releases/download/%{tag}/%{name}-source-%{tag}.tar.gz

BuildRequires:  desktop-file-utils systemd-rpm-macros

%description
Syncthing replaces other file synchronization services with something
open, trustworthy and decentralized. Your data is your data alone and
you deserve to choose where it is stored, if it is shared with some
third party and how it's transmitted over the Internet. Using syncthing,
that control is returned to you.

This package contains the syncthing client binary and systemd services.


%package        tools
Summary:        Continuous File Synchronization (server tools)

%description    tools
Syncthing replaces other file synchronization services with something
open, trustworthy and decentralized. Your data is your data alone and
you deserve to choose where it is stored, if it is shared with some
third party and how it's transmitted over the Internet. Using syncthing,
that control is returned to you.

This package contains the main syncthing server tools:

* `strelaysrv`, the syncthing relay server for indirect
  file transfers between client nodes, and
* `stdiscosrv`, the syncthing discovery server for discovering nodes
  to connect to indirectly over the internet.


%prep
%autosetup -n %{name} -p1


%build
export GOPATH="$(pwd)"
# Got rid of Fedora's dumb gobuild macros because
# they keep causing the build to fail.
go run -v ./build.go -no-upgrade -version 'v%{version}' install all

unset GOPATH


%install
# Create important dirs
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/{man1,man5,man7}
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_iconsdir}/hicolor/scalable/apps
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_userunitdir}

for size in '32x32' '64x64' '128x128' '256x256' '512x512'; do
  install -d "%{buildroot}%{_datadir}/icons/hicolor/$size/apps"
done

# install binaries
install -Dm 0755 ./bin/syncthing -t %{buildroot}%{_bindir}
install -Dm 0755 ./bin/stdiscosrv -t %{buildroot}%{_bindir}
install -Dm 0755 ./bin/strelaysrv -t %{buildroot}%{_bindir}

# install man pages
install -Dm 0644 ./man/syncthing.1 -t %{buildroot}%{_mandir}/man1
install -Dm 0644 ./man/*.5 -t %{buildroot}%{_mandir}/man5
install -Dm 0644 ./man/*.7 -t %{buildroot}%{_mandir}/man7
install -Dm 0644 ./man/stdiscosrv.1 -t %{buildroot}%{_mandir}/man1
install -Dm 0644 ./man/strelaysrv.1 -t %{buildroot}%{_mandir}/man1

# install desktop files and icons
install -Dm 0644 ./etc/linux-desktop/syncthing-start.desktop %{buildroot}/%{_datadir}/applications/
install -Dm 0644 ./etc/linux-desktop/syncthing-ui.desktop %{buildroot}/%{_datadir}/applications/

for size in '32' '64' '128' '256' '512'; do
  install -Dm 0644 "./assets/logo-${size}.png" "%{buildroot}%{_iconsdir}/hicolor/${size}x${size}/apps/syncthing.png"
done

install -Dm 0644 ./assets/logo-only.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/syncthing.svg

# install systemd units
install -Dm 0644 ./etc/linux-systemd/system/syncthing@.service -t %{buildroot}%{_unitdir}
install -Dm 0644 ./etc/linux-systemd/user/syncthing.service -t %{buildroot}%{_userunitdir}

# unmark source files as executable
for i in $(find -name '*.go' -type f -executable -print); do
  chmod 0644 "$i";
done

%post
%systemd_post 'syncthing@.service'
%systemd_user_post syncthing.service

%preun
%systemd_preun 'syncthing@*.service'
%systemd_user_preun syncthing.service

%postun
%systemd_postun_with_restart 'syncthing@*.service'
%systemd_user_postun_with_restart syncthing.service


%files
%{_bindir}/syncthing
%{_datadir}/applications/syncthing*.desktop
%{_iconsdir}/hicolor/*/apps/syncthing.*
%{_mandir}/*/syncthing*
%{_unitdir}/syncthing@.service
%{_userunitdir}/syncthing.service
%license ./LICENSE
%doc ./README.md ./AUTHORS

%files tools
%{_bindir}/stdiscosrv
%{_bindir}/strelaysrv
%{_mandir}/man1/stdiscosrv*
%{_mandir}/man1/strelaysrv*
%license ./LICENSE
%doc ./README.md ./AUTHORS

%changelog
%autochangelog
