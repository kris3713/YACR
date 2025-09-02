%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         fullname cudatext
%global         app_name CudaText
%global         variant qt5
%global         pkg_arch amd64
%global         debug_package %{nil}

Name:           %{fullname}-%{variant}
Version:        1.227.0.0
Release:        1%{?dist}
Summary:        Cross-platform text and code editor

License:        MPL-2.0
URL:            https://cudatext.github.io/

Source0:        https://sourceforge.net/projects/cudatext/files/release/%{version}/%{fullname}-linux-%{variant}-%{pkg_arch}-%{version}.tar.xz
Source1:        %{fullname}.desktop

BuildRequires:  zlib-ng
Requires:       qt5-qtbase qt5-qttools
Recommends:     python3

ExclusiveArch:  x86_64

Conflicts:      %{fullname}-gtk2 %{fullname} %{fullname}-qt6

%description
CudaText is a cross-platform text editor, written in Object Pascal.
It is open source project and can be used free of charge, even for business.
It starts quite fast: ~0.3 sec with ~30 plugins, on Linux on CPU Intel Core i3 3GHz.
It is extensible by Python add-ons: plugins, linters, code tree parsers, external tools.
Syntax parser is feature-rich, from EControl engine.

%prep
%setup -q -n ./%{fullname}

%install
# Remove the build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{app_name},%{_bindir},%{_datadir}/{applications,cudatext}}
%__install -d %{buildroot}%{_datadir}/icons/hicolor/512x512/apps

# CudaText requires the `data`, `py` and `settings_default` directories to be in
# `/usr/share/cudatext` in order to be considered non-portable
%__mv ./{data,py,settings_default} %{buildroot}%{_datadir}/%{fullname}

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}

# Install the desktop file
%__install -D -m 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Create a symlink to the application binary
%__ln_s /opt/%{app_name}/%{fullname} %{buildroot}%{_bindir}

# Install application icon
%__install -D -m 0644 %{buildroot}/opt/%{app_name}/%{fullname}-512.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps

%files
/opt/%{app_name}
%{_bindir}/%{fullname}
%{_datadir}/%{fullname}
%{_datadir}/applications/%{fullname}.desktop
%{_datadir}/icons/hicolor/512x512/apps/%{fullname}-512.png
%license ./readme/license.%{app_name}.txt
