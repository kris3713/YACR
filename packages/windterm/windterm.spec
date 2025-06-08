%global         __brp_check_rpaths %{nil}
# The reason for this is to avoid the "broken rpath" error
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
Source1:        %{full_name}.desktop
Source2:        %{full_name}

ExclusiveArch:  x86_64

Requires:       qt5-qtbase qt5-qttools

%description
A professional cross-platform SSH/Sftp/Shell/Telnet/Tmux/Serial terminal.

You may need to use the following command to give the application permissions to create the `profiles.config` file:

chown -R $USER:$USER /opt/%{app_name}

%prep
%setup -q -n ./%{app_name}_%{version}

%install
# Remove build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{app_name},%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary (might use a BASH script wrapper if this doesn't work)
%__install -Dm 0755 %{SOURCE2} -t %{buildroot}%{_bindir}

# Install application icons
%__install -Dm 0644 %{buildroot}/opt/%{app_name}/%{full_name}.png -t %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps

%post
# Inform the user that they may have to use chown if they want the application to create the `profiles.config` file
echo "You may need to use the following command to give the application permissions to create the `profiles.config` file:"
echo ""
echo "chown -R \$USER:\$USER /opt/%{app_name}"

%files
/opt/%{app_name}
%{_bindir}/%{full_name}
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/1024x1024/apps/%{full_name}.png
%license ./license.txt
