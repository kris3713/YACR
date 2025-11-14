%global         __brp_check_rpaths %{nil}
# The reason for this is to avoid the "broken rpath" error

%define         git_url https://github.com/Losses/rune

%global         __provides_exclude_from ^/opt/%{name}/.*$
%global         __requires_exclude_from ^/opt/%{name}/.*$
%global         pkg_arch amd64
%global         debug_package %{nil}

Name:           rune-player
Version:        1.1.0
Release:        1%{?dist}
Summary:        The audio player that blends classic design with modern technology

License:        MPL-2.0
URL:            %{git_url}

Source0:        %{git_url}/releases/download/v%{version}/Rune-v%{version}-linux-%{pkg_arch}.zip

BuildRequires:  fd-find

ExclusiveArch:  x86_64

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
%__rm -r %{buildroot}/opt/%{name}/assets

# Install the desktop file
%__install -Dm 0644 ./assets/rune.desktop -t %{buildroot}%{_datadir}/applications

# Create a symlink to the application binary
%__ln_s /opt/%{name}/rune %{buildroot}%{_bindir}

# Install the application metainfo file
%__install -Dm 0644 ./assets/rune.metainfo.xml -t %{buildroot}%{_metainfodir}

# Copy the application icons to the icon directory
%__cp -a ./assets/icons/* %{buildroot}%{_iconsdir}/hicolor
fd -e spec . %{buildroot}%{_iconsdir}/hicolor --exec %__chmod 0644 {}

%files
/opt/%{name}
%{_bindir}/rune
%{_datadir}/applications/rune.desktop
%{_metainfodir}/rune.metainfo.xml
%{_iconsdir}/hicolor/*
