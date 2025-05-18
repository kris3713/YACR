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

# Requires:

%description
A professional cross-platform SSH/Sftp/Shell/Telnet/Tmux/Serial terminal.

%prep
%setup -q -n ./%{app_name}_%{version}

%install
export QA_RPATHS=$(( 0x0002|0x0010 ))

# Remove build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{app_name},%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}

# Install the desktop file
%__mv %{buildroot}/opt/%{app_name}/%{full_name}.desktop %{buildroot}%{_datadir}/applications
%__chmod 0644 %{buildroot}%{_datadir}/applications/%{full_name}.desktop

# Install the application binary (might use a BASH script wrapper if this doesn't work)
%__ln_s /opt/%{app_name}/%{full_name} %{buildroot}%{_bindir}

# Install application icons
%__install -D -m 0644 %{buildroot}/opt/%{app_name}/%{full_name}.png -t %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps

%files
/opt/%{app_name}
%{_bindir}/%{full_name}
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/1024x1024/apps/%{app_name}.png

%changelog
* Sun May 18 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 2.7.0-1
- Inital packaging of WindTerm version 2.7.0
