%global         debug_package %{nil}

Name:           qman
Version:        1.5.1
Release:        1%{?dist}
Summary:        A more modern manual page viewer for our terminals
License:        BSD-2-Clause

URL:            https://github.com/plp13/%{name}
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc meson python3dist(cogapp) pkgconfig(liblzma) pkgconfig(ncursesw)
BuildRequires:  pkgconfig(inih) pkgconfig(zlib) pkgconfig(bzip2) pkgconfig(cunit)
Requires:       man groff-base

%description
Qman is a modern, interactive manual page viewer for our terminals. It strives
to be easy to use for anyone familiar with the man(1) command, and also to be
fast and tiny, so that it can be used everywhere.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%check
%meson_test

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/doc/%{name}/config/README.md
%{_datadir}/doc/%{name}/doc/*.md
%doc ./README.md
%license ./LICENSE
%dir %{_sysconfdir}/xdg/qman/
%dir %{_sysconfdir}/xdg/qman/themes/
%config(noreplace) %{_sysconfdir}/xdg/qman/qman.conf
%config(noreplace) %{_sysconfdir}/xdg/qman/themes/*.conf
