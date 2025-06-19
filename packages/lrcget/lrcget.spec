%global         app_name LRCGET
%global         debug_package %{nil}

Name:           lrcget
Version:        0.9.3
Release:        1%{?dist}
Summary:        Utility for mass-downloading LRC synced lyrics for your offline music library.

License:        MIT
URL:            https://github.com/tranxuanthang/lrcget

Source0:        https://github.com/tranxuanthang/lrcget/archive/refs/tags/0.9.3.tar.gz
Source1:        %{name}.desktop

BuildRequires:  nodejs-npm rust cargo openssl-devel libsoup3-devel
BuildRequires:  javascriptcoregtk4.1-devel webkit2gtk4.1-devel alsa-lib-devel

%description
Utility for mass-downloading LRC synced lyrics for your offline music library.

LRCGET will scan every files in your chosen directory for music files,
then and try to download lyrics to a LRC files having the same name and save
them to the same directory as your music files.

LRCGET is the official client of LRCLIB service.

%prep
%setup -q -n ./%{name}-%{version}

%build
npm install
npm run tauri build -- --no-bundle

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},%{_datadir}/applications}
%__install -d %{buildroot}%{_iconsdir}/hicolor/{32x32,44x44,128x128,256x256,512x512}/apps

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__install -Dm 0755 ./src-tauri/target/release/%{app_name} -t %{buildroot}%{_bindir}

# Install the application icons
%__install -Dm 0644 ./src-tauri/icons/{32x32,128x128}.png %{buildroot}%{_iconsdir}/hicolor/{32x32,128x128}/apps/%{app_name}.png
%__install -Dm 0644 ./src-tauri/icons/Square44x44Logo.png %{buildroot}%{_iconsdir}/hicolor/44x44/apps/%{app_name}.png
%__install -Dm 0644 ./src-tauri/icons/128x128@2x.png %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{app_name}.png
%__install -Dm 0644 ./src-tauri/icons/icon.png %{buildroot}%{_iconsdir}/hicolor/512x512/apps/%{app_name}.png

%files
%{_bindir}/%{app_name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/44x44/apps/%{name}.png
%{_iconsdir}/hicolor/128x128/apps/%{name}.png
%{_iconsdir}/hicolor/256x256/apps/%{name}.png
%{_iconsdir}/hicolor/512x512/apps/%{name}.png
%license ./LICENSE
