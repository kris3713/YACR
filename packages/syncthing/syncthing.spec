%global         debug_package %{nil}
%global         goipath github.com/syncthing/syncthing
%global         tag v%{version}%{?rcnum:-rc.%{rcnum}}

Name:           syncthing
Summary:        Continuous File Synchronization
Version:        2.0.11
Release:        1%{?dist}
# syncthing (MPL-2.0) bundles
# - angular, bootstrap, daterangepicker, fancytree, jQuery, moment (MIT),
# - HumanizeDuration (MIT OR Unlicense),
# - ForkAwesome (MIT, OFL-1.1, CC-BY-3.0), and
# - a number of go packages (Apache-2.0, BSD-2-Clause, BSD-2-Clause-Views, BSD-3-Clause, ISC, MIT, MPL-2.0)
License:        MPL-2.0 AND Apache-2.0 AND BSD-2-Clause AND BSD-2-Clause-Views AND BSD-3-Clause AND CC-BY-3.0 AND ISC AND MIT AND OFL-1.1 AND (Apache-2.0 OR MIT) AND (MIT OR Unlicense)

URL:            https://syncthing.net
# use official release tarball (contains vendored dependencies)
Source0:        %{gourl}/releases/download/%{tag}/%{name}-source-%{tag}.tar.gz

BuildRequires:  desktop-file-utils systemd-rpm-macros
%gometa -f

Requires:       hicolor-icon-theme

# assets in gui/default/vendor/*
Provides:       bundled(angular) = 1.3.20
Provides:       bundled(angular-dirPagination) = 759009c
Provides:       bundled(angular-sanitize) = 1.3.20
Provides:       bundled(angular-translate) = 2.9.0.1
Provides:       bundled(angular-translate-loader-static-files) = 2.11.0
Provides:       bundled(bootstrap) = 3.3.6
Provides:       bundled(daterangepicker) = 3.1
Provides:       bundled(ForkAwesome) = 1.2.0
Provides:       bundled(HumanizeDuration.js)
Provides:       bundled(jquery) = 2.2.2
Provides:       bundled(jquery-fancytree) = 2.38.0
Provides:       bundled(jquery-ui) = 1.12.1
Provides:       bundled(moment) = 2.19.4

# automatically generated Provides for bundled go dependencies
# manually check licenses for new deps and update License tag if necessary
# generate with "./vendor2provides.py path/to/vendor/modules.txt"

# github.com/AudriusButkevicius/recli : MPL-2.0
Provides:       bundled(golang(github.com/AudriusButkevicius/recli)) = d000ce8
# github.com/Azure/azure-sdk-for-go : MIT
Provides:       bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/azcore)) = 1.18.0
Provides:       bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/internal)) = 1.11.1
Provides:       bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/storage/azblob)) = 1.6.1
# github.com/Azure/go-ntlmssp : MIT
Provides:       bundled(golang(github.com/Azure/go-ntlmssp)) = 754e693
# github.com/alecthomas/kong : MIT
Provides:       bundled(golang(github.com/alecthomas/kong)) = 1.11.0
# github.com/aws/aws-sdk-go : Apache-2.0
Provides:       bundled(golang(github.com/aws/aws-sdk-go)) = 1.55.7
# github.com/beorn7/perks : MIT
Provides:       bundled(golang(github.com/beorn7/perks)) = 1.0.1
# github.com/calmh/incontainer : MIT
Provides:       bundled(golang(github.com/calmh/incontainer)) = 1.0.0
# github.com/calmh/xdr : MIT
Provides:       bundled(golang(github.com/calmh/xdr)) = 1.2.0
# github.com/ccding/go-stun : Apache-2.0
Provides:       bundled(golang(github.com/ccding/go-stun)) = 0.1.5
# github.com/cenkalti/backoff : MIT
Provides:       bundled(golang(github.com/cenkalti/backoff/v4)) = 4.3.0
# github.com/certifi/gocertifi : MPL-2.0
Provides:       bundled(golang(github.com/certifi/gocertifi)) = 431795d
# github.com/cespare/xxhash : MIT
Provides:       bundled(golang(github.com/cespare/xxhash/v2)) = 2.3.0
# github.com/chmduquesne/rollinghash : MIT
Provides:       bundled(golang(github.com/chmduquesne/rollinghash)) = 4.0.0+incompatible
# github.com/coreos/go-semver : Apache-2.0
Provides:       bundled(golang(github.com/coreos/go-semver)) = 0.3.1
# github.com/cpuguy83/go-md2man : MIT
Provides:       bundled(golang(github.com/cpuguy83/go-md2man/v2)) = 2.0.5
# github.com/d4l3k/messagediff : MIT
Provides:       bundled(golang(github.com/d4l3k/messagediff)) = 1.2.1
# github.com/davecgh/go-spew : ISC
Provides:       bundled(golang(github.com/davecgh/go-spew)) = 1.1.1
# github.com/ebitengine/purego : Apache-2.0
Provides:       bundled(golang(github.com/ebitengine/purego)) = 0.8.3
# github.com/fsnotify/fsnotify : BSD-3-Clause
Provides:       bundled(golang(github.com/fsnotify/fsnotify)) = 1.7.0
# github.com/getsentry/raven-go : BSD-3-Clause
Provides:       bundled(golang(github.com/getsentry/raven-go)) = 0.2.0
# github.com/go-asn1-ber/asn1-ber : MIT
Provides:       bundled(golang(github.com/go-asn1-ber/asn1-ber)) = 2923003
# github.com/go-ldap/ldap : MIT
Provides:       bundled(golang(github.com/go-ldap/ldap/v3)) = 3.4.11
# github.com/go-ole/go-ole : MIT
Provides:       bundled(golang(github.com/go-ole/go-ole)) = 1.3.0
# github.com/go-task/slim-sprig : MIT
Provides:       bundled(golang(github.com/go-task/slim-sprig/v3)) = 3.0.0
# github.com/gobwas/glob : MIT
Provides:       bundled(golang(github.com/gobwas/glob)) = 0.2.3
# github.com/gofrs/flock : BSD-3-Clause
Provides:       bundled(golang(github.com/gofrs/flock)) = 0.12.1
# github.com/golang/snappy : BSD-3-Clause
Provides:       bundled(golang(github.com/golang/snappy)) = 0.0.4
# github.com/google/pprof : Apache-2.0
Provides:       bundled(golang(github.com/google/pprof)) = 337e5dd
# github.com/google/uuid : BSD-3-Clause
Provides:       bundled(golang(github.com/google/uuid)) = 1.6.0
# github.com/greatroar/blobloom : Apache-2.0
Provides:       bundled(golang(github.com/greatroar/blobloom)) = 0.8.0
# github.com/hashicorp/errwrap : MPL-2.0
Provides:       bundled(golang(github.com/hashicorp/errwrap)) = 1.1.0
# github.com/hashicorp/go-multierror : MPL-2.0
Provides:       bundled(golang(github.com/hashicorp/go-multierror)) = 1.1.1
# github.com/hashicorp/golang-lru : MPL-2.0
Provides:       bundled(golang(github.com/hashicorp/golang-lru/v2)) = 2.0.7
# github.com/jackpal/gateway : BSD-3-Clause
Provides:       bundled(golang(github.com/jackpal/gateway)) = 1.0.16
# github.com/jackpal/go-nat-pmp : Apache-2.0
Provides:       bundled(golang(github.com/jackpal/go-nat-pmp)) = 1.0.2
# github.com/jmespath/go-jmespath : Apache-2.0
Provides:       bundled(golang(github.com/jmespath/go-jmespath)) = 0.4.0
# github.com/julienschmidt/httprouter : BSD-3-Clause
Provides:       bundled(golang(github.com/julienschmidt/httprouter)) = 1.3.0
# github.com/kballard/go-shellquote : MIT
Provides:       bundled(golang(github.com/kballard/go-shellquote)) = 95032a8
# github.com/lufia/plan9stats : BSD-3-Clause
Provides:       bundled(golang(github.com/lufia/plan9stats)) = 873cd01
# github.com/maruel/panicparse : Apache-2.0
Provides:       bundled(golang(github.com/maruel/panicparse/v2)) = 2.5.0
# github.com/maxbrunsfeld/counterfeiter : MIT
Provides:       bundled(golang(github.com/maxbrunsfeld/counterfeiter/v6)) = 6.11.2
# github.com/maxmind/geoipupdate : Apache-2.0 OR MIT
Provides:       bundled(golang(github.com/maxmind/geoipupdate/v6)) = 6.1.0
# github.com/miscreant/miscreant.go : MIT
Provides:       bundled(golang(github.com/miscreant/miscreant.go)) = 26d3763
# github.com/munnerz/goautoneg : BSD-3-Clause
Provides:       bundled(golang(github.com/munnerz/goautoneg)) = a7dc8b6
# github.com/nxadm/tail : MIT
Provides:       bundled(golang(github.com/nxadm/tail)) = 1.4.11
# github.com/onsi/ginkgo : MIT
Provides:       bundled(golang(github.com/onsi/ginkgo/v2)) = 2.23.4
# github.com/oschwald/geoip2-golang : ISC
Provides:       bundled(golang(github.com/oschwald/geoip2-golang)) = 1.11.0
# github.com/oschwald/maxminddb-golang : ISC
Provides:       bundled(golang(github.com/oschwald/maxminddb-golang)) = 1.13.1
# github.com/pierrec/lz4 : BSD-3-Clause
Provides:       bundled(golang(github.com/pierrec/lz4/v4)) = 4.1.22
# github.com/pkg/errors : BSD-2-Clause
Provides:       bundled(golang(github.com/pkg/errors)) = 0.9.1
# github.com/pmezard/go-difflib : BSD-3-Clause
Provides:       bundled(golang(github.com/pmezard/go-difflib)) = 1.0.0
# github.com/posener/complete : MIT
Provides:       bundled(golang(github.com/posener/complete)) = 1.2.3
# github.com/power-devops/perfstat : MIT
Provides:       bundled(golang(github.com/power-devops/perfstat)) = 82ca368
# github.com/prometheus/client_golang : Apache-2.0
Provides:       bundled(golang(github.com/prometheus/client_golang)) = 1.22.0
# github.com/prometheus/client_model : Apache-2.0
Provides:       bundled(golang(github.com/prometheus/client_model)) = 0.6.1
# github.com/prometheus/common : Apache-2.0
Provides:       bundled(golang(github.com/prometheus/common)) = 0.62.0
# github.com/prometheus/procfs : Apache-2.0
Provides:       bundled(golang(github.com/prometheus/procfs)) = 0.15.1
# github.com/puzpuzpuz/xsync : Apache-2.0
Provides:       bundled(golang(github.com/puzpuzpuz/xsync/v3)) = 3.5.1
# github.com/quic-go/quic-go : MIT
Provides:       bundled(golang(github.com/quic-go/quic-go)) = 0.52.0
# github.com/rabbitmq/amqp091-go : BSD-2-Clause
Provides:       bundled(golang(github.com/rabbitmq/amqp091-go)) = 1.10.0
# github.com/rcrowley/go-metrics : BSD-2-Clause-Views
Provides:       bundled(golang(github.com/rcrowley/go-metrics)) = 65e299d
# github.com/riywo/loginshell : MIT
Provides:       bundled(golang(github.com/riywo/loginshell)) = 7d26008
# github.com/russross/blackfriday : BSD-2-Clause
Provides:       bundled(golang(github.com/russross/blackfriday/v2)) = 2.1.0
# github.com/shirou/gopsutil : BSD-3-Clause
Provides:       bundled(golang(github.com/shirou/gopsutil/v4)) = 4.25.4
# github.com/stretchr/objx : MIT
Provides:       bundled(golang(github.com/stretchr/objx)) = 0.5.2
# github.com/stretchr/testify : MIT
Provides:       bundled(golang(github.com/stretchr/testify)) = 1.10.0
# github.com/syncthing/notify : MIT
Provides:       bundled(golang(github.com/syncthing/notify)) = c7027d4
# github.com/syndtr/goleveldb : BSD-2-Clause
Provides:       bundled(golang(github.com/syndtr/goleveldb)) = 126854a
# github.com/thejerf/suture : MIT
Provides:       bundled(golang(github.com/thejerf/suture/v4)) = 4.0.6
# github.com/tklauser/go-sysconf : BSD-3-Clause
Provides:       bundled(golang(github.com/tklauser/go-sysconf)) = 0.3.14
# github.com/tklauser/numcpus : Apache-2.0
Provides:       bundled(golang(github.com/tklauser/numcpus)) = 0.9.0
# github.com/urfave/cli : MIT
Provides:       bundled(golang(github.com/urfave/cli)) = 1.22.16
# github.com/vitrun/qart : Apache-2.0 AND BSD-3-Clause
Provides:       bundled(golang(github.com/vitrun/qart)) = bf64b92
# github.com/willabides/kongplete : MIT
Provides:       bundled(golang(github.com/willabides/kongplete)) = 0.4.0
# github.com/yusufpapurcu/wmi : MIT
Provides:       bundled(golang(github.com/yusufpapurcu/wmi)) = 1.2.4
# go.uber.org/automaxprocs : MIT
Provides:       bundled(golang(go.uber.org/automaxprocs)) = 1.6.0
# go.uber.org/mock : Apache-2.0
Provides:       bundled(golang(go.uber.org/mock)) = 0.5.2
# golang.org/x/crypto : BSD-3-Clause
Provides:       bundled(golang(golang.org/x/crypto)) = 0.38.0
# golang.org/x/mod : BSD-3-Clause
Provides:       bundled(golang(golang.org/x/mod)) = 0.24.0
# golang.org/x/net : BSD-3-Clause
Provides:       bundled(golang(golang.org/x/net)) = 0.40.0
# golang.org/x/sync : BSD-3-Clause
Provides:       bundled(golang(golang.org/x/sync)) = 0.14.0
# golang.org/x/sys : BSD-3-Clause
Provides:       bundled(golang(golang.org/x/sys)) = 0.33.0
# golang.org/x/text : BSD-3-Clause
Provides:       bundled(golang(golang.org/x/text)) = 0.25.0
# golang.org/x/time : BSD-3-Clause
Provides:       bundled(golang(golang.org/x/time)) = 0.11.0
# golang.org/x/tools : BSD-3-Clause
Provides:       bundled(golang(golang.org/x/tools)) = 0.33.0
# google.golang.org/protobuf : BSD-3-Clause
Provides:       bundled(golang(google.golang.org/protobuf)) = 1.36.6
# gopkg.in/yaml.v3 : MIT AND Apache-2.0
Provides:       bundled(golang(gopkg.in/yaml.v3)) = 3.0.1
# sigs.k8s.io/yaml : MIT AND BSD-3-Clause AND (MIT OR Apache-2.0)
Provides:       bundled(golang(sigs.k8s.io/yaml)) = 1.4.0

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
go run ./build.go -no-upgrade -version 'v%{version}' install all

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
  cp -pav "./assets/logo-${size}.png" "%{buildroot}%{_iconsdir}/hicolor/${size}x${size}/apps/syncthing.png"
done

install -Dm 0644 ./assets/logo-only.svg %{buildroot}/%{_iconsdir}/hicolor/scalable/apps/syncthing.svg

# install systemd units
install -Dm 0644 ./etc/linux-systemd/system/syncthing@.service -t %{buildroot}/%{_unitdir}
install -Dm 0644 ./etc/linux-systemd/user/syncthing.service -t %{buildroot}/%{_userunitdir}

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
