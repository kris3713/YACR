%global         __brp_check_rpaths %nil
# The reason for this is to avoid the "broken rpath" error

%global         __provides_exclude_from ^/opt/%{name}/.*$
%global         __requires_exclude_from ^/opt/%{name}/.*$
%global         url_part https://download.jetbrains.com/toolbox
%global         debug_package %nil

%ifarch x86_64
%global         src_number 0
%else
%global         src_number 1
%endif

Name:           jetbrains-toolbox
Version:        3.9.1.89198
Release:        1%{?dist}
Summary:        Manage your JetBrains IDEs and Tools the easy way

License:        Freeware (https://www.jetbrains.com/legal/)
URL:            https://www.jetbrains.com/toolbox-app/

Source0:        %{url_part}/%{name}-%{version}.tar.gz
Source1:        %{url_part}/%{name}-%{version}-arm64.tar.gz
Source2:        %{name}.svg

Obsoletes:      %{name}-arm64 = 3.9.1.89198-%{release}

%description
%{summary}


%prep
%autosetup -T -b %src_number -n ./%{name}-%{version}/bin


%install
# Create a new build root
install -d %{buildroot}{/opt/%{name},%{_bindir}}

# Copy all the application files to the appilcation directory
cp -a ./* %{buildroot}/opt/%{name}
install -Dm 0644 %SOURCE2 \
  %{buildroot}/opt/%{name}/toolbox.svg

# Remove unnecessary files from the application directory
rm %{buildroot}/opt/%{name}/%{name}.desktop

# Create a symlink to the application binary
ln -sv /opt/%{name}/%{name} %{buildroot}%{_bindir}

# Install the desktop file
install -Dm 0644 ./%{name}.desktop \
  -t %{buildroot}%{_datadir}/applications

# Install the application icon
install -Dm 0644 %SOURCE2 \
  -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps


%post
DESKTOP_FILE="$SUDO_HOME/.local/share/applications/%{name}.desktop"
# Check if the desktop file does not already exist
if [ ! -f "$DESKTOP_FILE" ]; then
  # Prevent JetBrains Toolbox from creating a desktop file in $HOME/.local/share/applications
  ln -sfv /dev/null "$DESKTOP_FILE"
fi

# Check if the output of `readlink -f` is not equal to /dev/null
if [ "$(readlink -f "$DESKTOP_FILE")" != /dev/null ]; then
  # Prevent JetBrains Toolbox from creating a desktop file in $HOME/.local/share/applications
  ln -sfv /dev/null "$DESKTOP_FILE"
fi


%postun
if [ -f "$SUDO_HOME/.local/share/applications/%{name}.desktop" ]; then
  rm "$SUDO_HOME/.local/share/applications/%{name}.desktop"
fi


%files
/opt/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg


%changelog
%autochangelog
