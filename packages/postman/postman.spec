%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         url_part https://dl.pstmn.io/download/version/%{real_version}
%global         app_name Postman
%global         real_version 12.37.3
%global         debug_package %{nil}

%ifarch x86_64
%global         src_number 0
%else
%global         src_number 1
%endif

Name:           %(v='%{app_name}'; echo "${v,,}")
# Postman sometimes likes to include a hypen in the version number,
# which is not allowed in RPM version numbers. This is a workaround for that.
Version:        %(echo %real_version | tr '-' '~')
Release:        1%{?dist}
Summary:        Postman - Platform for building and using APIs

License:        Freeware
URL:            https://www.postman.com/

Source0:        %{url_part}/linux64#/%{name}-%{version}-linux-x64.tar.gz
Source1:        %{url_part}/linuxarm64#/%{name}-%{version}-linux-arm64.tar.gz
Source2:        %{name}.desktop

Obsoletes:      %{name}-arm64 = 12.37.3-%{release}

%description
Postman is an API platform for building and using APIs.
Postman simplifies each step of the API lifecycle and
streamlines collaboration so you can create better APIs faster.

%prep
%autosetup -T -b %src_number -n ./%{app_name}/app

%install
# Start installing the application to the build root (while also creating another build root)
install -d %{buildroot}{/opt/%{app_name},%{_bindir}}

# Copy the application files to the application directory
cp -a ./* %{buildroot}/opt/%{app_name}

# Change filemode to prevent "permission denied" error
chmod -v 0755 %{buildroot}/opt/%{app_name}/chrome_crashpad_handler

# Install the desktop file
install -Dm 0644 %SOURCE2 -t %{buildroot}%{_datadir}/applications

# Create a symlink to the application binary
ln -sv /opt/%{app_name}/%{name} %{buildroot}%{_bindir}

# Install application icon
install -Dm 0644 ./resources/app/assets/icon.png \
  %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

%files
/opt/%{app_name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/128x128/apps/%{name}.png

%changelog
%autochangelog
