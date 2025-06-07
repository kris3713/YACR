%global         pkg_arch arm64
%global         git_url https://github.com/Losses/rune
%global         real_version 1.1.0
%global         debug_package %{nil}

Name:           rune-player
Version:        1.1.0
Release:        1%{?dist}
Summary:        The audio player that blends classic design with modern technology

License:        MPL-2.0
URL:            %{git_url}

Source0:        %{git_url}/releases/download/v%{real_version}/Rune-v%{real_version}-linux-%{pkg_arch}.zip

ExclusiveArch:  %arm64

%description
Rune Player is a music player that offers audio analysis and recommendation features.
It introduces a new, modern music management paradigm to enhance your experience with cross-platform support.

%prep
%setup -q -c -n ./Rune-v%{version}

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},/opt/%{name},%{_datadir}/applications,%{_iconsdir}/hicolor,%{_metainfodir}}

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{name}

# Install the desktop file
%__install -Dm 0644 %{buildroot}/opt/%{name}/assets/rune.desktop -t %{buildroot}%{_datadir}/applications

# Create a symlink to the application binary
%__ln_s %{buildroot}/opt/%{name}/rune %{buildroot}%{_bindir}

# Install the application metainfo file
%__install -Dm 0644 %{buildroot}/opt/%{name}/assets/rune.metainfo.xml -t %{buildroot}%{_metainfodir}

# Copy the application icons to the icon directory
%__chmod -R 0644 %{buildroot}/opt/%{name}/assets/icons
%__cp -a %{buildroot}/opt/%{name}/assets/icons/* %{buildroot}%{_iconsdir}/hicolor

# Remove the assets directory
%__rm -r %{buildroot}/opt/%{name}/assets

%files
/opt/%{name}
%{_bindir}/rune
%{_datadir}/applications/rune.desktop
%{_metainfodir}/rune.metainfo.xml
%{_iconsdir}/hicolor/*
