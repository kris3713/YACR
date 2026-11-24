%global         __provides_exclude_from ^/usr/lib/%{alt_name}/.*$
%global         __requires_exclude_from ^/usr/lib/%{alt_name}/.*$
%global         alt_name Open PDF Studio
%global         app_id org.openaec.OpenPdfStudio
%global         debug_package %nil

Name:           open-pdf-studio
Version:        2026.48.5
Release:        1%{?dist}
Summary:        An open source PDF viewer/editor with it's own blazing fast rust engine

License:        LGPL-3.0-or-later AND GPL-3.0-only
URL:            https://open-aec.com/%{name}/

Source0:        https://github.com/OpenAEC-Foundation/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  nodejs nodejs-npm rustup gcc-c++ openssl-devel libsoup3-devel
BuildRequires:  javascriptcoregtk4.1-devel webkit2gtk4.1-devel alsa-lib-devel
BuildRequires:  gtk3-devel libayatana-appindicator-gtk3-devel libxdo-devel
BuildRequires:  cmake turbojpeg-devel leptonica-devel tesseract-devel patchelf

ExclusiveArch:  x86_64

%description
A free, open-source PDF editor for people
who work with drawings: markup, measuring
to scale, revision compare and CAD import


%prep
%autosetup -n ./%{name}-%{version}/%{name}

# Compiling the bundled Tesseract/Leptonica sources
# for tesseract-rs always fails. This is a workaround
# to force tesseract-rs into using the system-installed
# tesseract and leptonica libs
sed -i ./src-tauri/Cargo.toml \
  -e 's/"build-tesseract"/"build-tesseract", "use-system-tesseract"/'

%build
export npm_config_cache="$(realpath ./.node_cache)"
export RUSTUP_HOME="$(realpath ./.rustup)"
export CARGO_HOME="$(realpath ./.cargo)"

# Install rustup to ensure latest rust toolchain
rustup-init -y --no-modify-path \
  --default-toolchain stable
export PATH="$PATH:$CARGO_HOME/bin"

env NODE_ENV='dev' npm install
env NODE_ENV='production' npm run 'tauri:build' -- \
  --no-bundle \
  --target x86_64-unknown-linux-gnu \
  -- "-j$(nproc)"


%install
# Install the application binaries
RELEASE_DIR='../target/x86_64-unknown-linux-gnu/release'
install -Dm 0755 "$RELEASE_DIR/%{name}" \
  -t %{buildroot}%{_bindir}
install -Dm 0755 "$RELEASE_DIR/build/pdfium-worker" \
  -t %{buildroot}%{_bindir}

install -d '%{buildroot}/usr/lib/%{alt_name}'
LIB_FILES=('fonts' 'kaders' 'onderhoeken' 'tessdata'
'file-icon.ico' 'libpdfium.so')
for lib_file in "${LIB_FILES[@]}"; do
  cp -rv "$RELEASE_DIR/build/$lib_file" \
    '%{buildroot}/usr/lib/%{alt_name}'
done

# Install the desktop file
install -Dm 0644 ../flatpak/%{app_id}.desktop \
  -t %{buildroot}%{_datadir}/applications

# Install the metainfo file
install -Dm 0644 ../flatpak/%{app_id}.metainfo.xml \
  -t %{buildroot}%{_metainfodir}

# For later use
std_sizes=('32x32' '128x128' '256x256' '512x512')
nstd_sizes=(
  '30x30' '44x44' '50x50' '89x89' '107x107'
  '142x142' '150x150' '284x284' '310x310'
)
ICONS_DIR='./src-tauri/icons'

# Reorganize icon names
mv -v "$ICONS_DIR/${std_sizes[1]}@2x.png" "$ICONS_DIR/${std_sizes[2]}.png"
mv -v "$ICONS_DIR/icon.png" "$ICONS_DIR/${std_sizes[3]}.png"
mv -v "$ICONS_DIR/StoreLogo.png" "$ICONS_DIR/Square${nstd_sizes[2]}Logo.png"

# install the application icons
for size in "${std_sizes[@]}"; do
  install -Dm 0644 "$ICONS_DIR/$size.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{app_id}.png"
done
for size in "${nstd_sizes[@]}"; do
  install -Dm 0644 "$ICONS_DIR/Square${size}Logo.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{app_id}.png"
done


%files
%{_bindir}/{%{name},pdfium-worker}
"/usr/lib/%{alt_name}"
%{_datadir}/applications/%{app_id}.desktop
%{_metainfodir}/%{app_id}.metainfo.xml
%{_iconsdir}/hicolor/*/apps/%{app_id}.png
%license ../{{LICENSE,LICENSING.md}.md,GPL-3.0.txt}
%doc ../README.md


%changelog
%autochangelog
