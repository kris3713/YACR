%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         fullname postman
%global         app_name Postman
%global         real_version 11.75.6
%global         debug_package %{nil}

Name:           %{fullname}-arm64
# Postman sometimes likes to include a hypen in the version number,
# which is not allowed in RPM version numbers. This is a workaround for that.
Version:        %(echo %{real_version} | tr '-' '~')
Release:        1%{?dist}
Summary:        Postman - Platform for building and using APIs (arm64 variant)

License:        Freeware
URL:            https://www.postman.com/

Source0:        https://dl.pstmn.io/download/version/%{real_version}/linuxarm64#/%{fullname}-%{version}-linux-arm64.tar.gz
Source1:        %{fullname}.desktop

ExclusiveArch:  %arm64

%description
Postman is an API platform for building and using APIs.
Postman simplifies each step of the API lifecycle and
streamlines collaboration so you can create better APIs faster.

%prep
%setup -q -n ./%{app_name}/app

%install
# Remove the build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{app_name},%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_datadir}/icons/hicolor/128x128/apps

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}

# Change filemode to prevent "permission denied" error
%__chmod 0755 %{buildroot}/opt/%{app_name}/chrome_crashpad_handler

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Create a symlink to the application binary
%__ln_s /opt/%{app_name}/%{fullname} %{buildroot}%{_bindir}

# Install application icon
%__install -Dm 0644 ./resources/app/assets/icon.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{fullname}.png

%files
/opt/%{app_name}
%{_bindir}/%{fullname}
%{_datadir}/applications/%{fullname}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{fullname}.png

%changelog
%autochangelog
