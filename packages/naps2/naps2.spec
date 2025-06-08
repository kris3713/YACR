%define         n2 dotnet run --project NAPS2.Tools --

%ifarch x86_64
%define         rel_dir linux-x64
%else
%define         rel_dir linux-arm64
%endif

%global         full_name com.naps2.Naps2
%global         __requires_exclude_from ^/opt/NAPS2/.*$
%global         debug_package %{nil}
%global         __spec_install_post %{nil}
%global         __os_install_post %{_dbpath}/brp-compress

Name:           naps2
Version:        8.1.4
Release:        1%{?dist}
Summary:        Scan documents to PDF and more, as simply as possible.

License:        GPL-2.0-or-later
URL:            https://www.naps2.com/

Source0:        https://github.com/cyanfish/naps2/archive/refs/tags/v%{version}.tar.gz
Source1:        naps2

BuildRequires:  dotnet-sdk-9.0 liberation-fonts-all google-noto-fonts-common google-noto-sans-cjk-vf-fonts
Requires:       dotnet-host dotnet-runtime-9.0

%description
NAPS2 allows you to scan from USB (using SANE) and network scanners. Use your chosen settings, or
set up multiple profiles for different devices and configurations. Once you've finished scanning, you can
save, email, or print with only a couple clicks. Save to PDF, TIFF, JPEG, PNG, or other file types.

Easily rotate, crop, and rearrange scanned pages. Adjust brightness, contrast, and apply automatic document
corrections to make your scanned pages look great. Use OCR to add searchable text to your PDFs in any of
over 100 languages. Use batch scanning, advanced profile settings, and an optional CLI to automate tedious
tasks.

%prep
%setup -q -n ./naps2-%{version}

%build
export DOTNET_NOLOGO=true
export DOTNET_CLI_TELEMETRY_OPTOUT=true

%{n2} pkg rpm -p linux --nosign &> /dev/null
%__mkdir ./app

unset DOTNET_NOLOGO
unset DOTNET_CLI_TELEMETRY_OPTOUT

%__tar -cf ./app/publish.tar -C ./NAPS2.App.Gtk/bin/Release/net9/%{rel_dir}/publish .

%install
# Remove the old build directory
%__rm -rf %{buildroot}

# Install the new build directory
%__install -d %{buildroot}{/opt/NAPS2,%{_bindir},%{_datadir}/applications,%{_metainfodir}}
%__install -d %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,44x44,48x48,64x64}/apps
%__install -d %{buildroot}%{_iconsdir}/hicolor/{72x72,96x96,128x128,150x150}/apps

# Copy the application files to the appllication directory
%__tar -xf ./app/publish.tar '--strip-components=1' -C %{buildroot}/opt/NAPS2

# Remove executables from /opt/NAPS2/sosdocsunix.txt
%__chmod -x %{buildroot}/opt/NAPS2/sosdocsunix.txt

# Install the desktop file
%__install -Dm 0644 ./NAPS2.Setup/config/linux/%{full_name}.desktop %{buildroot}%{_datadir}/applications/naps2.desktop

# Install the application metainfo
%__install -Dm 0644 ./NAPS2.Setup/config/linux/%{full_name}.metainfo.xml -t %{buildroot}%{_metainfodir}

# Install the application binary
%__install -Dm 0755 %{SOURCE1} -t %{buildroot}%{_bindir}

# Install the application icons
%__install -Dm 0644 ./NAPS2.Setup/config/windows/msix/Assets/scanner-150.png %{buildroot}%{_iconsdir}/hicolor/150x150/apps/%{full_name}.png
%__install -Dm 0644 ./NAPS2.Lib/Icons/scanner-128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{full_name}.png
%__install -Dm 0644 ./NAPS2.Lib/Icons/scanner-96.png %{buildroot}%{_iconsdir}/hicolor/96x96/apps/%{full_name}.png
%__install -Dm 0644 ./NAPS2.Lib/Icons/scanner-72-rev1.png %{buildroot}%{_iconsdir}/hicolor/72x72/apps/%{full_name}.png
%__install -Dm 0644 ./NAPS2.Lib/Icons/scanner-64-rev1.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{full_name}.png
%__install -Dm 0644 ./NAPS2.Lib/Icons/scanner-48-rev1.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{full_name}.png
%__install -Dm 0644 ./NAPS2.Lib/Icons/scanner-32-rev1.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{full_name}.png
%__install -Dm 0644 ./NAPS2.Lib/Icons/scanner-16-rev1.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{full_name}.png

%files
/opt/NAPS2
%{_bindir}/naps2
%{_datadir}/applications/naps2.desktop
%{_iconsdir}/hicolor/150x150/apps/%{full_name}.png
%{_iconsdir}/hicolor/128x128/apps/%{full_name}.png
%{_iconsdir}/hicolor/96x96/apps/%{full_name}.png
%{_iconsdir}/hicolor/72x72/apps/%{full_name}.png
%{_iconsdir}/hicolor/64x64/apps/%{full_name}.png
%{_iconsdir}/hicolor/48x48/apps/%{full_name}.png
%{_iconsdir}/hicolor/32x32/apps/%{full_name}.png
%{_iconsdir}/hicolor/16x16/apps/%{full_name}.png
%{_metainfodir}/%{full_name}.metainfo.xml
%license ./LICENSE
