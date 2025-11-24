%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         app_name Bitwarden
%global         debug_package %{nil}

Name:           bitwarden
Version:        2025.11.1
Release:        1%{?dist}
Summary:        A secure and free password manager for all of your devices.

License:        GPL-3.0
URL:            https://bitwarden.com

# Not bothering trying to build from source, keep getting too much build errors
# related to rust.
Source0:        https://github.com/%{name}/clients/releases/download/desktop-v%{version}/%{app_name}-%{version}-amd64.deb

BuildRequires:  dpkg

ExclusiveArch:  x86_64

%description
%{summary}

%prep
dpkg -x %{SOURCE0} .

%install
# Create the new build root
%__install -d %{buildroot}{%{_bindir},/opt,%{_datadir}/applications}
for size in '16x16' '32x32' '64x64' '128x128' '256x256' '512x512' '1024x1024'; do
  %__install -d "%{buildroot}%{_iconsdir}/hicolor/$size/apps"
done

# Copy the application files to the application directory
%__cp -a ./opt/%{app_name} %{buildroot}/opt

# Ensure chrome-sandbox has the correct permissions
%__chmod 4755 %{buildroot}/opt/%{app_name}/chrome-sandbox

# Create a symbolic link to the application binary
%__ln_s /opt/%{app_name}/%{name} -t %{buildroot}%{_bindir}

# Install the desktop file
%__install -Dm 0644 .%{_datadir}/applications/%{name}.desktop -t %{buildroot}%{_datadir}/applications

# Install the application icons
for size in '16x16' '32x32' '64x64' '128x128' '256x256' '512x512' '1024x1024'; do
  %__install -Dm 0644 ".%{_iconsdir}/hicolor/$size/apps/%{name}.png" -t "%{buildroot}%{_iconsdir}/hicolor/$size/apps"
done

%files
%{_bindir}/%{name}
/opt/%{app_name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%doc .%{_datadir}/doc/%{name}
