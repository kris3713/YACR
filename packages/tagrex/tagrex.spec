%global         debug_package %nil

%ifarch x86_64
%global         build_target x86_64-unknown-linux-gnu
%else
%global         build_target aarch64-unknown-linux-gnu
%endif

Name:           tagrex
Version:        1.5.0
Release:        1%{?dist}
Summary:        A free tag editor for your music library

License:        MIT
URL:            https://github.com/%{name}/%{name}

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  bun-bin rustup gcc openssl-devel libsoup3-devel
BuildRequires:  javascriptcoregtk4.1-devel webkit2gtk4.1-devel
BuildRequires:  gtk3-devel libayatana-appindicator-gtk3-devel
BuildRequires:  librsvg2-devel libxdo-devel alsa-lib-devel

%description
%summary. Edit tags and file names in a table,
see exactly what will change before anything is written, and roll any batch back,
even after a restart. Fill tags from Discogs, MusicBrainz, Beatport, Bandcamp and
Soundeo.


%prep
%autosetup -n ./%{name}-%{version}


%build
# Install rustup to ensure latest rust toolchain
export RUSTUP_HOME="$(realpath ./.rustup)"
export CARGO_HOME="$(realpath ./.cargo)"
rustup-init -y --no-modify-path \
  --default-toolchain stable
export PATH="$PATH:$CARGO_HOME/bin"

env NODE_ENV=production bunx @tauri-apps/cli build \
  --no-bundle \
  --target %build_target \
  -- "-j$(nproc)"


%install
# Install the application binary
install -Dm 0755 ./target/%{build_target}/release/%{name} \
  -t %{buildroot}%{_bindir}

# Install the desktop file
CONTENT="$(cat << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=%name
Comment=Cross-platform audio tag editor
Exec=%name %%F
StartupWMClass=%name
Icon=%name
Terminal=false
MimeType=inode/directory
Categories=AudioVideo;Audio;Music
DESKTOP
)"
install -Dm 0644 /dev/stdin \
  %{buildroot}%{_datadir}/applications/%{name}.desktop <<< "$CONTENT"

# For later use
std_sizes=('32x32' '128x128' '256x256' '512x512')
nstd_sizes=(
  '30x30' '44x44' '50x50' '89x89' '107x107'
  '142x142' '150x150' '284x284' '310x310'
)
ICONS_DIR='./app/icons'

# Reorganize icon names
mv -v "$ICONS_DIR/${std_sizes[1]}@2x.png" "$ICONS_DIR/${std_sizes[2]}.png"
mv -v "$ICONS_DIR/icon.png" "$ICONS_DIR/${std_sizes[3]}.png"
mv -v "$ICONS_DIR/StoreLogo.png" "$ICONS_DIR/Square${nstd_sizes[2]}Logo.png"

# install the application icons
for size in "${std_sizes[@]}"; do
  install -Dm 0644 "$ICONS_DIR/$size.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{name}.png"
done
for size in "${nstd_sizes[@]}"; do
  install -Dm 0644 "$ICONS_DIR/Square${size}Logo.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{name}.png"
done
install -Dm 0644 ./assets/icon.svg \
  %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg


%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*
%license ./LICENSE
%doc ./{README,CHANGELOG}.md


%changelog
%autochangelog
