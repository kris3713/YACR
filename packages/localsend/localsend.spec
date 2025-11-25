%global         __brp_check_rpaths %{nil}
# The reason for this is to avoid the "broken rpath" error

%define         git_url https://github.com/localsend/localsend

%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         fullname localsend
%global         realname localsend_app
%global         app_name LocalSend
%global         debug_package %{nil}

Name:           %{fullname}
Version:        1.17.0
Release:        1%{?dist}
Summary:        An open source cross-platform alternative to AirDrop

License:        Apache-2.0
URL:            https://localsend.org/

Source0:        %{git_url}/releases/download/v%{version}/%{app_name}-%{version}-linux-x86-64.tar.gz
Source1:        %{fullname}.desktop
Source2:        %{git_url}/raw/refs/tags/v%{version}/app/assets/img/logo-32.png
Source3:        %{git_url}/raw/refs/tags/v%{version}/app/assets/img/logo-128.png
Source4:        %{git_url}/raw/refs/tags/v%{version}/app/assets/img/logo-256.png
Source5:        %{git_url}/raw/refs/tags/v%{version}/app/assets/img/logo-512.png

ExclusiveArch:  x86_64

%description
LocalSend is a free, open-source app that allows you to securely share files and messages
with nearby devices over your local network without needing an internet connection.

%prep
%setup -q -c -n ./%{name}-%{version}

%install
export QA_RPATHS=$[ 0x0002 | 0x0010 ]
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},/opt/%{app_name},%{_datadir}/applications}
%__install -d %{buildroot}%{_iconsdir}/hicolor/{32x32,128x128,256x256,512x512}/apps}

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}

# Create a symlink to the application binary
%__ln_s /opt/%{app_name}/%{realname} %{buildroot}%{_bindir}

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application icons
%__install -Dm 0644 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{realname}.png
%__install -Dm 0644 %{SOURCE3} %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{realname}.png
%__install -Dm 0644 %{SOURCE4} %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{realname}.png
%__install -Dm 0644 %{SOURCE5} %{buildroot}%{_iconsdir}/hicolor/512x512/apps/%{realname}.png

%files
/opt/%{app_name}
%{_bindir}/%{realname}
%{_datadir}/applications/%{fullname}.desktop
%{_iconsdir}/hicolor/32x32/apps/%{realname}.png
%{_iconsdir}/hicolor/128x128/apps/%{realname}.png
%{_iconsdir}/hicolor/256x256/apps/%{realname}.png
%{_iconsdir}/hicolor/512x512/apps/%{realname}.png

%changelog
%autochangelog
