%global         __brp_check_rpaths %{nil}
# The reason for this is to avoid the "broken rpath" error
%global         __provides_exclude_from ^/opt/%{fullname}/.*$
%global         __requires_exclude_from ^/opt/%{fullname}/.*$
%global         fullname jetbrains-toolbox
%global         debug_package %{nil}

Name:           %{fullname}-arm64
Version:        3.1.0.62320
Release:        1%{?dist}
Summary:        Manage your JetBrains IDEs and Tools the easy way

License:        Freeware (https://www.jetbrains.com/legal/)
URL:            https://www.jetbrains.com/toolbox-app/

Source0:        https://download.jetbrains.com/toolbox/%{fullname}-%{version}-arm64.tar.gz
Source1:        %{fullname}.svg

ExclusiveArch:  %arm64

%description
%{summary}

%prep
%setup -q -n ./%{fullname}-%{version}/bin

%install
# Remove the old buildroot
%__rm -rf %{buildroot}

# Create a new build root
%__install -d %{buildroot}{/opt/%{fullname},%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_iconsdir}/hicolor/scalable/apps

# Copy all the application files to the appilcation directory
%__cp -a . %{buildroot}/opt/%{fullname}
%__install -Dm 0644 %{SOURCE1} %{buildroot}/opt/%{fullname}/toolbox.svg

# Remove unnecessary files from the application directory
%__rm %{buildroot}/opt/%{fullname}/%{fullname}.desktop

# Create a symlink to the application binary
%__ln_s /opt/%{fullname}/%{fullname} %{buildroot}%{_bindir}

# Install the desktop file
%__install -Dm 0644 ./%{fullname}.desktop -t %{buildroot}%{_datadir}/applications

# Install the application icon
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps

%post
# Prevent JetBrains Toolbox from creating a desktop file in $HOME/.local/share/applications
%__ln_s /dev/null "$SUDO_HOME/.local/share/applications/%{fullname}.desktop"

%postun
if [ -f "$SUDO_HOME/.local/share/applications/%{fullname}.desktop" ]; then
  %__rm "$SUDO_HOME/.local/share/applications/%{fullname}.desktop"
fi

%files
/opt/%{fullname}
%{_bindir}/%{fullname}
%{_datadir}/applications/%{fullname}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{fullname}.svg
