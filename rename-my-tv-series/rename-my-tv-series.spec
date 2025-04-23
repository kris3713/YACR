%global         full_name rename-my-tv-series
%global         application_name RenameMyTVSeries
%global         debug_package %{nil}

Name:           rename-my-tv-series
Version:        2.0.10
Release:        1%{?dist}
Summary:        Rename My TV Series 2

License:        Freeware
URL:            https://www.tweaking4all.com/home-theatre/rename-my-tv-series-v2/

Source0:        https://www.tweaking4all.com/downloads/video/RenameMyTVSeries-2.0.10-Linux64bit.tar.gz
Source1:        %{full_name}.desktop
# Source2:        %{full_name}

ExclusiveArch:  x86_64

Requires:       openssl-devel libsq3-devel

%description
Rename My TV Series is a utility designed to help you rename your TV series
episodes based on information from TheTVDB.com. It supports various naming
formats and can help organize your media files.

%prep
%setup -qn %{application_name}-%{version}

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
ls -laR .

install -m 755 RenameMyTVSeries %{buildroot}%{_bindir}/
install -m 644 rename-my-tv-series.desktop %{buildroot}%{_datadir}/applications/

%files
%{_bindir}/RenameMyTVSeries
%{_datadir}/applications/rename-my-tv-series.desktop

%changelog
* Tue Apr 22 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 2.0.10-1
- Initial RPM packaging of version 2.0.10
