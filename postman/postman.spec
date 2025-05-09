%global         full_name postman
%global         application_name Postman
%global         debug_package %{nil}

Name:           postman
Version:        11.44.0
Release:        1%{?dist}
Summary:        Postman - Platform for building and using APIs

License:        Freeware
URL:            https://www.postman.com/

Source0:        https://dl.pstmn.io/download/latest/linux_64
Source1:        %{full_name}.desktop

%description
Postman is an API platform for building and using APIs.
Postman simplifies each step of the API lifecycle and
streamlines collaboration so you can create better APIs faster.

%prep
ls -laR .
%__rm ./%{application_name}/%{application_name}
%__chmod 755 ./%{application_name}/app/chrome_crashpad_handler
%setup -n ./%{application_name}/app
ls -laR .

%install
ls -laR .

# Remove the build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{final_name},%{_bindir},%{_datadir}/applications,%{_datadir}/icons/hicolor/128x128/apps

# Copy the application files to the build root
%__cp -r * %{buildroot}/opt/%{final_name}

# Install the desktop file
%__install -D -m 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__install -D -m 0755 %{buildroot}/opt/%{final_name}/%{application_name} -t %{buildroot}%{_bindir}

%__ln_s ../../../../../../opt/%{final_name}/icons/icon_128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png

ls -laR .

%files
%license add-license-file-here
%doc add-docs-here



%changelog
* Fri May 09 2025 FlawlessCasual17 <07e5297d5b@c0x0.com>
- 
