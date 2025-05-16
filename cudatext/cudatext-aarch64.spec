%global         full_name cudatext
%global         app_name CudaText
%global         variant qt5
%global         arch %arm64
%global         debug_package %{nil}

Name:           cudatext-%{arch}
Version:        1.223.6.0
Release:        1%{?dist}
Summary:        Cross-platform text and code editor

License:        MPL-2.0
URL:            https://cudatext.github.io/

Source0:        https://sourceforge.net/projects/cudatext/files/release/%{version}/%{full_name}-linux-%{variant}-%{arch}-%{version}.tar.xz
Source1:        https://github.com/Alexey-T/CudaText/raw/refs/heads/master/setup/debfiles/%{full_name}.desktop
Source2:        %{full_name}

ExclusiveArch:  %arm64

%description
CudaText is a cross-platform text editor, written in Object Pascal.
It is open source project and can be used free of charge, even for business.
It starts quite fast: ~0.3 sec with ~30 plugins, on Linux on CPU Intel Core i3 3GHz.
It is extensible by Python add-ons: plugins, linters, code tree parsers, external tools.
Syntax parser is feature-rich, from EControl engine.

%prep
%setup -q -n ./%{full_name}

%install
# Remove the build root
%__rm -rf %{buildroot}

# Start installing the application to the build root (while also creating another build root)
%__install -d %{buildroot}{/opt/%{app_name},%{_bindir},%{_datadir}/{applications,cudatext}}
%__install -d %{buildroot}%{_datadir}/icons/hicolor/512x512/apps

# CudaText requires the `data`, `py` and `settings_default` directories to be in
# `/usr/share/cudatext` in order to be considered non-portable
%__mv ./{data,py,settings_default} %{buildroot}%{_datadir}/cudatext

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}

# Install the desktop file
%__install -D -m 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__install -D -m 0755 %{SOURCE2} -t %{buildroot}%{_bindir}
%__chmod +x %{buildroot}%{_bindir}/%{full_name}

# Install application icon
%__install -D -m 0644 %{buildroot}/opt/%{app_name}/icons/%{full_name}-512.png -t %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{full_name}.png

%files
/opt/%{app_name}
%{_bindir}/%{full_name}
%{_datadir}/cudatext
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/512x512/apps/%{full_name}.png
%license ./readme/license.%{app_name}.txt

%changelog
* Fri May 09 2025 FlawlessCasual17 <07e5297d5b@c0x0.com> - 1.223.6.0-1
- Beginning of initial RPM packaging for Cudatext version 1.223.6.0
