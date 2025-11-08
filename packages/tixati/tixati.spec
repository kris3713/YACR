%global         __requires_exclude_from ^%{_bindir}/%{name}$
%global         debug_package %{nil}

Name:           tixati
Version:        3.39
Release:        1%{?dist}
Summary:        Tixati is a peer-to-peer file sharing program that uses the popular BitTorrent protocol

License:        Freeware
URL:            https://tixati.com/

Source0:        https://download.tixati.com/%{name}-%{version}-1.x86_64.manualinstall.tar.gz
Source1:        %{url}favicon.png#/%{name}.png
Source2:        %{url}tixati_eula.txt

Requires:       gtk3 dbus-glib

ExclusiveArch:  x86_64

%description
%{summary}

%prep
%setup -q -n ./%{name}-%{version}-1.x86_64.manualinstall

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_iconsdir}/hicolor/{48x48,64x64}/apps

# Install the application binary
%__install -Dm 0755 ./%{name} -t %{buildroot}%{_bindir}

# Install the desktop file
%__install -Dm 0644 ./%{name}.desktop -t %{buildroot}%{_datadir}/applications

# Install the application icons
%__install -Dm 0644 ./%{name}.png -t %{buildroot}%{_iconsdir}/hicolor/48x48/apps
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_iconsdir}/hicolor/64x64/apps

# Copy the tixati eula to the current directory
%__cp %{SOURCE2} .

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%license ./tixati_eula.txt
%doc ./README.txt
