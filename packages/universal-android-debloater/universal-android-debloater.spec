%global         alt uad
%global         gui_name %{alt}-ng
%global         debug_package %nil

%ifarch x86_64
%define         build_target x86_64-unknown-linux-gnu
%else
%define         build_target aarch64-unknown-linux-gnu
%endif

Name:           universal-android-debloater
Version:        1.3.1
Release:        1%{?dist}
Summary:        Cross-platform GUI written in Rust using ADB to debloat non-rooted Android devices

License:        GPL-3.0-only
URL:            https://github.com/Universal-Debloater-Alliance/%{name}-next-generation

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc rustup icoutils
Requires:       android-tools

%description
%summary.
Improve your privacy, the security and battery life of your device.


%package        cli
Summary:        Cross-platform CLI written in Rust using ADB to debloat non-rooted Android devices

%description    cli
%summary.
Improve your privacy, the security and battery life of your device.


%prep
%autosetup -n ./%{name}-next-generation-%{version}


%build
# Setup rustup and cargo
export RUSTUP_HOME="$(realpath ./.rustup)"
export CARGO_HOME="$(realpath ./.cargo)"

# Install rustup to ensure latest rust toolchain
rustup-init -y --no-modify-path \
  --default-toolchain stable
export PATH="$PATH:$CARGO_HOME/bin"

# Build uad-gui and uad-cli
cargo build "-j$(nproc)" --release \
  --target %build_target \
  -p %{alt}-gui \
  -p %{alt}-cli

# # Generate a clean dependency graph
# cargo tree --workspace --edges 'no-build,no-dev,no-proc-macro' \
#   --no-dedupe --prefix none \
#   --format '# {l}' |
#     sed -e "s: / :/:g" -e "s:/: OR :g" |
#       sort -u

# Generate a LICENSE file for all cargo dependencies
cargo tree --workspace --edges 'no-build,no-dev,no-proc-macro' \
  --no-dedupe --prefix none \
  --format '{l}: {p}' |
    sed -e "s: ($(pwd)[^)]*)::g" -e 's: / :/:g' -e 's:/: OR :g' |
      sort -u > ./LICENSE.dependencies


%install
# install uad-gui
install -Dm 0755 ./target/%{build_target}/release/%{gui_name} \
  -t %{buildroot}%{_bindir}

# install uad-cli
install -Dm 0755 ./target/%{build_target}/release/%{alt} \
  -t %{buildroot}%{_bindir}

# Install the desktop file
CONTENT="$(cat << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=Universal Android Debloater Next Generation
Comment=ADB GUI for debloating non-rooted Android devices
Exec=%{gui_name}
StartupWMClass=%{gui_name}
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
DESKTOP
)"
install -Dm 0644 /dev/stdin \
  %{buildroot}%{_datadir}/applications/%{gui_name}.desktop <<< "$CONTENT"

# Install application icons
ICONS_DIR='./app_icons'
mkdir -v "$ICONS_DIR"
ICO_FILE='./resources/assets/icon.ico'
icotool "$ICO_FILE" --extract \
  --index=1 -o "$ICONS_DIR/16x16.png"
icotool "$ICO_FILE" --extract \
  --index=2 -o "$ICONS_DIR/24x24.png"
icotool "$ICO_FILE" --extract \
  --index=3 -o "$ICONS_DIR/32x32.png"
icotool "$ICO_FILE" --extract \
  --index=4 -o "$ICONS_DIR/48x48.png"
icotool "$ICO_FILE" --extract \
  --index=5 -o "$ICONS_DIR/64x64.png"
icotool "$ICO_FILE" --extract \
  --index=6 -o "$ICONS_DIR/96x96.png"
icotool "$ICO_FILE" --extract \
  --index=7 -o "$ICONS_DIR/128x128.png"
icotool "$ICO_FILE" --extract \
  --index=8 -o "$ICONS_DIR/256x256.png"

for icon in "$ICONS_DIR"/*; do
  dir_name="$(basename -s '.png' "$icon")"
  install -Dm 0644 "$icon" \
    "%{buildroot}%{_iconsdir}/hicolor/$dir_name/%{gui_name}.png"
done

install -d %{buildroot}%{_datadir}/pixmaps
ln -sv %{_iconsdir}/hicolor/256x256/%{gui_name} \
  %{buildroot}%{_datadir}/pixmaps/%{name}.png

%files
%{_bindir}/%{gui_name}
%{_datadir}/applications/%{gui_name}.desktop
%{_iconsdir}/hicolor
%{_datadir}/pixmaps/%{name}.png
%license ./LICENSE ./LICENSE.dependencies
%doc ./README.md


%files          cli
%{_bindir}/%{alt}
%license ./LICENSE ./LICENSE.dependencies
%doc ./README.md


%changelog
%autochangelog
