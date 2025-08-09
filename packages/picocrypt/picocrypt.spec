%global         debug_package %{nil}

Name:           picocrypt
Version:        2.00
Release:        1%{?dist}
Summary:        A very small, very simple, yet very secure encryption tool

License:        GPL-3.0
URL:            https://github.com/Picocrypt-NG/Picocrypt-NG

Source0:        %{url}/releases/download/%{version}/Picocrypt#/%{name}-gui
Source1:        %{name}.desktop
Source2:        %{url}/raw/refs/tags/%{version}/images/key.svg#/%{name}.svg

ExclusiveArch:  x86_64

%description
Picocrypt is a very small (hence Pico), very simple, yet very secure encryption tool
that you can use to protect your files. It's designed to be the go-to tool for file encryption,
with a focus on security, simplicity, and reliability. Picocrypt uses the secure XChaCha20 cipher
and the Argon2id key derivation function to provide a high level of security.

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},%{_datadir}/applications,%{_iconsdir}/hicolor/scalable/apps}

# Install the application binary
%__install -Dm 0755 %{SOURCE0} -t %{buildroot}%{_bindir}

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application icon
%__install -Dm 0644 %{SOURCE2} -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps

%files
%{_bindir}/%{name}-gui
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
