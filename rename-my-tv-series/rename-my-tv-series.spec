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
ls -laR .
%setup -q -n .

%install
%__rm -rf %{buildroot}

%__install -d %{buildroot}{/opt/%{application_name},%{_bindir},%{_datadir}/applications,%{_datadir}/icons/hicolor/128x128/apps,%{_datadir}/icons/hicolor/64x64/apps,%{_datadir}/icons/hicolor/48x48/apps,%{_datadir}/icons/hicolor/32x32/apps,%{_datadir}/icons/hicolor/16x16/apps}

%__cp -r * %{buildroot}/opt/%{application_name}

%__install -D -m 0644 %{SOURCE0} -t %{buildroot}%{_datadir}/applications

%__install -D -m 0444 %{SOURCE1} -t %{buildroot}/opt/%{application_name}/distribution

%__ln_s ../../../../../../opt/%{application_name}/16x16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%__ln_s ../../../../../../opt/%{application_name}/32x32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%__ln_s ../../../../../../opt/%{application_name}/48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%__ln_s ../../../../../../opt/%{application_name}/64x64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%__ln_s ../../../../../../opt/%{application_name}/128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png

ls -laR .

%files
%{_optdir}/%{application_name}
%{_bindir}/%{application_name}
%{_datadir}/applications/rename-my-tv-series.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png

%changelog
* Tue Apr 22 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 2.0.10-1
- Initial RPM packaging of version 2.0.10
