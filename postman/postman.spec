%global         full_name postman
%global         application_name Postman
%global         debug_package %{nil}

Name:           postman
Version:        11.45.2
Release:        1%{?dist}
Summary:        Postman - Platform for building and using APIs

License:        Freeware
URL:            https://www.postman.com/

Source0:        https://dl.pstmn.io/download/latest/linux_64#/postman-linux-x64.tar.gz
Source1:        %{full_name}.desktop

ExclusiveArch:  x86_64

%description
Postman is an API platform for building and using APIs.
Postman simplifies each step of the API lifecycle and
streamlines collaboration so you can create better APIs faster.

%prep
%setup -q -n ./%{application_name}/app

%install
# Remove the build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{full_name},%{_bindir},%{_datadir}/applications,%{_datadir}/icons/hicolor/128x128/apps}

# Copy the application files to the build root
%__cp -a . %{buildroot}/opt/%{full_name}

# Change filemode to prevent "permission denied" error
%__chmod 755 %{buildroot}/opt/%{full_name}/chrome_crashpad_handler

# Install the desktop file
%__install -D -m 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__ln_s /opt/%{full_name}/%{full_name} %{buildroot}%{_bindir}

# Install application icon
%__install -D -m 0644 %{buildroot}/opt/%{full_name}/icons/icon_128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png

%files
/opt/%{full_name}
%{_bindir}/%{full_name}
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png

%changelog
* Fri May 09 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 11.45.2-1
- Beginning of initial RPM packaging for Postman version 11.45.2
