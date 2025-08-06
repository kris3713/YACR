%global         __brp_check_rpaths %{nil}
# The reason for this is to avoid the "broken rpath" error
%global         __provides_exclude_from ^/opt/%{fullname}/.*$
%global         __requires_exclude_from ^/opt/%{fullname}/.*$
%global         fullname jetbrains-toolbox
%global         debug_package %{nil}

Name:           %{fullname}
Version:        2.8.0.51430
Release:        1%{?dist}
Summary:        Manage your JetBrains IDEs and Tools the easy way

License:        Freeware (https://www.jetbrains.com/legal/)
URL:            https://www.jetbrains.com/toolbox-app/

Source0:        https://download.jetbrains.com/toolbox/%{fullname}-%{version}.tar.gz
Source1:        %{fullname}.svg
Source2:        %{fullname}

ExclusiveArch:  x86_64

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
%__install -Dm 0644 %{SOURCE1} %{buildroot}/opt/%{fullname}/icon.svg

# Remove unnecessary files from the application directory
%__rm %{buildroot}/opt/%{fullname}/%{fullname}.desktop

# Install the shell wrapper script for the application binary
%__install -Dm 0755 %{SOURCE2} %{buildroot}%{_bindir}

# Install the desktop file
%__install -Dm 0644 ./%{fullname}.desktop -t %{buildroot}%{_datadir}/applications

# Install the application icon
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps

%files
/opt/%{fullname}
%{_bindir}/%{fullname}
%{_datadir}/applications/%{fullname}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{fullname}.svg
