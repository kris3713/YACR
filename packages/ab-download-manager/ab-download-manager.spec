%global         full_name ab-download-manager
%global         app_name ABDownloadManager
%global         debug_package %{nil}

Name:           ab-download-manager
Version:        1.6.3
Release:        1%{?dist}
Summary:        A Download Manager that speeds up your downloads

License:        Apache-2.0
URL:            https://abdownloadmanager.com/

Source0:        https://github.com/amir1376/ab-download-manager/releases/download/v%{version}/%{app_name}_%{version}_linux_x64.tar.gz
Source1:        %{full_name}.desktop

ExclusiveArch:  x86_64

%description
A Download Manager that speeds up your downloads

Features:

* ⚡️ Faster Download Speed
* ⏰ Queues and Schedulers
* 🌐 Browser Extensions
* 💻 Multiplatform (Windows / Linux / Mac)
* 🌙 Multiple Themes (Dark/Light) with modern UI
* ❤️ Free and Open Source

%prep
%setup -q -n ./%{app_name}

%install
# Remove the old build directory
%__rm -rf %{buildroot}

# Start installing the application to the new build root
%__install -d %{buildroot}{/opt/%{app_name},%{_bindir},%{_datadir}/{applications,icons/hicolor/512x512/apps}}

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__ln_s /opt/%{app_name}/bin/%{app_name} %{buildroot}%{_bindir}

# Install application icon
%__install -Dm 0644 %{buildroot}/opt/%{app_name}/lib/%{app_name}.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps

%files
/opt/%{app_name}
%{_bindir}/%{app_name}
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/512x512/apps/%{app_name}.png
