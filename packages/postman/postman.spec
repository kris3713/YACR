%global         app_name Postman
%global         real_version 11.47.1
%global         debug_package %{nil}

Name:           postman
Version:        11.47.1
Release:        1%{?dist}
Summary:        Postman - Platform for building and using APIs

License:        Freeware
URL:            https://www.postman.com/

Source0:        https://dl.pstmn.io/download/version/%{real_version}/linux64#/postman-linux-x64.tar.gz
Source1:        cudatext.desktop
Source2:        cudatext

ExclusiveArch:  x86_64

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
%__chmod 755 %{buildroot}/opt/%{app_name}/chrome_crashpad_handler

# Install the desktop file
%__install -D -m 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__install -D -m 0755 %{SOURCE2} -t %{buildroot}%{_bindir}
%__chmod +x %{buildroot}%{_bindir}/cudatext

# Install application icon
%__install -D -m 0644 ./icons/icon_128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/cudatext.png

%files
/opt/%{app_name}
%{_bindir}/cudatext
%{_datadir}/applications/cudatext.desktop
%{_datadir}/icons/hicolor/128x128/apps/cudatext.png
