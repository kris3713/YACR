# imported from: https://src.fedoraproject.org/rpms/hardinfo2/blob/rawhide/f/hardinfo2.spec
%global         debug_package %nil

%if 0%{?rhel} <= 8
%undefine __cmake_in_source_build
%undefine __cmake3_in_source_build
%endif

Name:           hardinfo2
Version:        2.2.16
Release:        4%{?dist}
Summary:        System Information and Benchmark for Linux Systems

# most of the source code is GPL-2.0-or-later license, except:

# hardinfo2/gg_key_file_parse_string_as_value.c: LGPL-2.1-or-later
# includes/blowfish.h: LGPL-2.1-or-later
# deps/uber-graph/g-ring.c: LGPL-2.1-or-later
# deps/uber-graph/g-ring.h: LGPL-2.1-or-later
# modules/benchmark/blowfish.c: LGPL-2.1-or-later

# hardinfo2/gg_strescape.c: LGPL-2.0-or-later
# hardinfo2/util.c: GPL-2.0-or-later AND LGPL-2.0-or-later
# deps/uber-graph/uber-frame-source.c: LGPL-2.0-or-later
# deps/uber-graph/uber-frame-source.h: LGPL-2.0-or-later
# deps/uber-graph/uber-timeout-interval.c: LGPL-2.0-or-later
# deps/uber-graph/uber-timeout-interval.h: LGPL-2.0-or-later

# deps/uber-graph/uber-graph.c: GPL-3.0-or-later
# deps/uber-graph/uber-graph.h: GPL-3.0-or-later
# deps/uber-graph/uber-heat-map.c: GPL-3.0-or-later
# deps/uber-graph/uber-heat-map.h: GPL-3.0-or-later
# deps/uber-graph/uber-label.c: GPL-3.0-or-later
# deps/uber-graph/uber-label.h: GPL-3.0-or-later
# deps/uber-graph/uber-line-graph.c: GPL-3.0-or-later
# deps/uber-graph/uber-line-graph.h: GPL-3.0-or-later
# deps/uber-graph/uber-range.c: GPL-3.0-or-later
# deps/uber-graph/uber-range.h: GPL-3.0-or-later
# deps/uber-graph/uber-scale.c: GPL-3.0-or-later
# deps/uber-graph/uber-scale.h: GPL-3.0-or-later
# deps/uber-graph/uber-scatter.c: GPL-3.0-or-later
# deps/uber-graph/uber-scatter.h: GPL-3.0-or-later
# deps/uber-graph/uber-window.c: GPL-3.0-or-later
# deps/uber-graph/uber-window.h: GPL-3.0-or-later
# deps/uber-graph/uber.h: GPL-3.0-or-later

# includes/loadgraph.h: LGPL-2.1-only
# shell/loadgraph.c: LGPL-2.1-only

License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.0-or-later AND GPL-3.0-or-later AND LGPL-2.1-only
URL:            https://github.com/%{name}/%{name}
Source0:        %{url}/archive/release-%{version}/%{name}-release-%{version}.tar.gz

BuildRequires:  gcc-c++
%if 0%{?rhel} < 8
BuildRequires:  cmake3
%else
BuildRequires:  cmake
%endif

BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5OpenGL)
BuildRequires:  /usr/bin/glslangValidator
BuildRequires:  /usr/bin/glslc
BuildRequires:  libdecor-devel
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-png)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(gmodule-export-2.0)
%if 0%{?fedora} || 0%{?rhel} >= 10
BuildRequires:  pkgconfig(libsoup-3.0)
%else
BuildRequires:  pkgconfig(libsoup-2.4)
%endif
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  zlib-devel

BuildRequires:  systemd-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
Requires:       sysbench iperf3

%if 0%{?rhel} >= 8 || 0%{?fedora}
Recommends:     lm_sensors
# Recommends:     sysbench
Recommends:     lsscsi
Recommends:     glx-utils
Recommends:     dmidecode
Recommends:     udisks2
Recommends:     xdg-utils
# Recommends:     iperf3
Recommends:     vulkan-tools
%endif

%description
Hardinfo2 is based on hardinfo, which have not been released >10 years.
Hardinfo2 is the reboot that was needed.

Hardinfo2 offers System Information and Benchmark for Linux Systems. It is able
to obtain information from both hardware and basic software. It can benchmark
your system and compare to other machines online.

Features include:
- Report generation (in either HTML or plain text)
- Online Benchmarking - compare your machine against other machines

%prep
%autosetup -n ./%{name}-release-%{version}

%build
%if 0%{?rhel} < 8
%cmake3 -DCMAKE_BUILD_TYPE=Release
%cmake3_build
%else
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build
%endif

%install
%if 0%{?rhel} < 8
%cmake3_install
%else
%cmake_install
%endif

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml

%files -f %{name}.lang
%license LICENSE LICENSE.1 LICENSE.2
%doc README.md
%{_bindir}/%{name}
%{_bindir}/hwinfo2_fetch_sysdata
%{_unitdir}/%{name}.service
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/benchmark.so
%{_libdir}/%{name}/modules/computer.so
%{_libdir}/%{name}/modules/devices.so
%{_libdir}/%{name}/modules/network.so
%{_libdir}/%{name}/modules/qgears2
%{_libdir}/%{name}/modules/vkgears
%{_metainfodir}/org.%{name}.%{name}.metainfo.xml
%{_datadir}/applications/%{name}.desktop
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.ids
%{_datadir}/%{name}/benchmark.data
%{_datadir}/%{name}/*.json
%{_datadir}/%{name}/pixmaps/
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_mandir}/man1/%{name}.1*

%changelog
%autochangelog
