%global         full_name windterm
%global         app_name WindTerm
%global         debug_package %{nil}

Name:           windterm
Version:        2.7.0
Release:        1%{?dist}
Summary:        A professional cross-platform SSH/Sftp/Shell/Telnet/Tmux/Serial terminal.

License:        MIT, Apache-2.0, LGPL-2.1-or-later, BSD-2-Clause (or BSD-3-Clause)
URL:            https://github.com/kingToolbox/WindTerm

Source0:        https://github.com/kingToolbox/WindTerm/releases/download/%{version}/%{app_name}_%{version}_Linux_Portable_x86_64.zip

ExclusiveArch:  x86_64

Requires:       qt5-qtbase qt5-qttools

%description
A professional cross-platform SSH/Sftp/Shell/Telnet/Tmux/Serial terminal.

%prep
%setup -q -n ./%{app_name}_%{version}

%install
# Remove build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{app_name},%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps

# Compress the `lib` directory to avoid the "broken rpath" error
%__tar -cf ./lib.tar ./lib
%__xz -6 ./lib.tar -c > ./lib.tar.xz
%__rm -r ./lib.tar ./lib

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}

# Install the desktop file
%__mv %{buildroot}/opt/%{app_name}/%{full_name}.desktop %{buildroot}%{_datadir}/applications
%__chmod 0644 %{buildroot}%{_datadir}/applications/%{full_name}.desktop

# Install the application binary (might use a BASH script wrapper if this doesn't work)
%__chmod +x %{buildroot}/opt/%{app_name}/%{app_name}
%__ln_s /opt/%{app_name}/%{app_name} %{buildroot}%{_bindir}/%{full_name}

# Install application icons
%__install -D -m 0644 %{buildroot}/opt/%{app_name}/%{full_name}.png -t %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps

%post
if [ -e /opt/%{app_name}/lib.tar.xz ]; then
  # Create the `lib` directory
  %__mkdir_p /opt/%{app_name}/lib
  # Uncompress the `lib.tar.xz` file
  %__tar -xf /opt/%{app_name}/lib.tar.xz "--strip-components=2" -C /opt/%{app_name}/lib
  # Remove the `lib.tar.xz` file
  %__rm /opt/%{app_name}/lib.tar.xz
fi

%postun
if [ -e /opt/%{app_name}/lib ]; then
  # Remove the `lib` directory
  %__rm /opt/%{app_name}/lib
fi

%files
/opt/%{app_name}
%{_bindir}/%{full_name}
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/1024x1024/apps/%{full_name}.png
%license ./license.txt

%changelog
* Sun May 18 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 2.7.0-1
- Inital packaging of WindTerm version 2.7.0
