%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         fullname termora
%global         app_name Termora
%global         debug_package %{nil}

Name:           %{fullname}-aarch64
Version:        1.0.17
Release:        1%{?dist}
Summary:        Termora is cross-platform a terminal emulator and SSH client.

License:        AGPL-3.0,Propietary
URL:            https://www.termora.app/

Source0:        https://github.com/TermoraDev/termora/releases/download/%{version}/termora-%{version}-linux-aarch64.tar.gz
Source1:        %{fullname}.desktop

ExclusiveArch:  %arm64

%description
Termora is cross-platform a terminal emulator and SSH client.
It is developed using Kotlin/JVM and partially implements the XTerm control sequence protocol.

Features:

* 🧬 Cross-platform support
* 🔐 Built-in key manager
* 🖼️ X11 forwarding
* 🧑‍💻 SSH-Agent integration
* 💻 System information display
* 📁 GUI-based SFTP file management
* 📊 Nvidia GPU usage monitoring
* ⚡ Quick command shortcuts

%prep
%setup -q -n ./%{app_name}

%install
# Remove the old build directory
%__rm -rf %{buildroot}

# Start installing the application to the new build root
%__install -d %{buildroot}{/opt/%{app_name},%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_iconsdir}/hicolor/1024x1024/apps

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__ln_s /opt/%{app_name}/bin/%{app_name} %{buildroot}%{_bindir}

# Install application icon
%__install -Dm 0644 ./lib/%{app_name}.png %{buildroot}%{_iconsdir}/hicolor/1024x1024/apps

%files
/opt/%{app_name}
%{_bindir}/%{app_name}
%{_datadir}/applications/%{fullname}.desktop
%{_iconsdir}/hicolor/1024x1024/apps/%{app_name}.png
