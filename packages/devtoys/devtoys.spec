%define         git_url https://github.com/DevToys-app/DevToys

%global         __provides_exclude_from ^/opt/%{name}/.*$
%global         __requires_exclude_from ^/opt/%{name}/.*$
%global         __spec_install_post %{nil}
%global         __os_install_post %{_dbpath}/brp-compress
%global         fullname devtoys
%global         debug_package %{nil}

Name:           devtoys
Version:        2.0.8.0
Release:        1%{?dist}
Summary:        A Swiss Army knife for developers.

License:        MIT
URL:            https://devtoys.app/

Source0:        %{git_url}/releases/download/v%{version}/%{fullname}_linux_x64_portable.zip
Source1:        %{name}.desktop
Source2:        %{git_url}/raw/refs/tags/v%{version}/assets/logo/Windows-Linux/Preview/Icon-Windows-Linux-Preview.svg#/%{fullname}.svg
Source3:        %{git_url}/raw/refs/tags/v%{version}/assets/logo/Windows-Linux/Preview/Icon-Windows-Linux-Preview.png#/%{fullname}.png

Requires:      dotnet-host webkitgtk6.0

ExclusiveArch:  x86_64

%description
DevToys helps with daily development tasks by offering a
bundle of tiny tools designed to do quick, specific tiny tasks.
No need to use many untrustworthy websites to simply decode a
text or compress an image. With Smart Detection, the app
intuitively selects the best tool for the data on your clipboard.

%prep
%setup -q -c -n ./%{name}-%{version}

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create a new build root
%__install -d %{buildroot}{/opt/%{name},%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_iconsdir}/hicolor/{scalable,512x512}/apps

# Copy all the application files to application directory
%__cp -a . %{buildroot}/opt/%{name}

# Install the destkop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Create a symlink to the executable
%__ln -s /opt/%{name}/DevToys.Linux %{buildroot}%{_bindir}

# Install the application icons
%__install -Dm 0644 %{SOURCE2} -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps
%__install -Dm 0644 %{SOURCE3} -t %{buildroot}%{_iconsdir}/hicolor/512x512/apps

%files
/opt/%{name}
%{_bindir}/DevToys.Linux
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{fullname}.svg
%{_iconsdir}/hicolor/512x512/apps/%{fullname}.png
%license ./LICENSE.md
