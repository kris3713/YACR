%global         full_name rename-my-tv-series

Name:           rename-my-tv-series
Version:        2.0.10
Release:        1%{?dist}
Summary:        Rename My TV Series 2

License:        Freeware
URL:            https://www.tweaking4all.com/home-theatre/rename-my-tv-series-v2/
Source0:        https://www.tweaking4all.com/downloads/video/RenameMyTVSeries-2.0.10-Linux64bit.tar.gz

ExclusiveArch:  x86_64

Requires:       openssl-devel
Requires:       libsq3-devel

%description
Rename My TV Series is a utility designed to help you rename your TV series
episodes based on information from TheTVDB.com. It supports various naming
formats and can help organize your media files.

%prep
# Unpack the tarball gzip archive
%setup -q -n RenameMyTVSeries-2.0.10-Linux64bit
%autosetup

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/

install -m 755 RenameMyTVSeries %{buildroot}%{_bindir}/

# Install the desktop file (assuming it's in the extracted directory)
# If the desktop file has a different name, update 'RenameMyTVSeries.desktop'
if [ -f RenameMyTVSeries.desktop ]; then
    install -m 644 RenameMyTVSeries.desktop %{buildroot}%{_datadir}/applications/
fi

%files
%{_bindir}/RenameMyTVSeries
%if commentators == "RenameMyTVSeries.desktop"
%{_datadir}/applications/RenameMyTVSeries.desktop
%endif

%changelog
* Tue Apr 22 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 2.0.10-1
- Initial RPM packaging of version 2.0.10
