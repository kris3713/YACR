%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         git_url https://github.com/%{app_name}/%{app_name}
%global         app_name StreamNook
%global         debug_package %nil

Name:           %(v="%{app_name}"; echo "${v,,}")
# TODO: Update this to the latest version the moment the
# TODO: developer announces better Linux support
Version:        8.7.1
Release:        1%{?dist}
Summary:        A native desktop client for Twitch, YouTube, Kick, and TikTok

License:        PolyForm-Noncommercial-1.0.0 AND LicenseRef-StreamNook-Additional-Permissions
URL:            https://%{name}.app/

Source0:        %{git_url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  nodejs nodejs-npm rustup gcc-c++ openssl-devel libsoup3-devel
BuildRequires:  javascriptcoregtk4.1-devel webkit2gtk4.1-devel alsa-lib-devel
BuildRequires:  gtk3-devel libayatana-appindicator-gtk3-devel libxdo-devel

# To avoid having syslog-ng as a dependency; required
# libraries (shared objects) will need to be manually listed.
Requires:       openssl-libs glib2 gtk3 gdk-pixbuf2 libgcc systemd-libs
Requires:       zlib-ng-compat libffi pango cairo harfbuzz fontconfig
Requires:       fribidi atk libepoxy libXi at-spi2-atk libcloudproviders
Requires:       libtinysparql libwayland-client libXfixes libxkbcommon
Requires:       libwayland-cursor libwayland-egl libXext libXcursor
Requires:       libXdamage libXcomposite libXrandr libXinerama
Requires:       glycin-libs libmount libselinux pcre2 libthai libpng
Requires:       freetype libXrender libxcb pixman graphite2 libxml2
Requires:       at-spi2-core json-glib sqlite-libs lcms2 libseccomp
Requires:       libblkid libdatrie libbrotli bzip2-libs libXau xz-libs

ExclusiveArch:  x86_64

%description
%summary.
Multi-stream grid, standalone chat, and every emote provider in one place.


%prep
%autosetup -n ./%{app_name}-%{version}


%build
export npm_config_cache="$(realpath ./.node_cache)"
export RUSTUP_HOME="$(realpath ./.rustup)"
export CARGO_HOME="$(realpath ./.cargo)"

# Initialize rustup
rustup-init -y --no-modify-path \
  --default-toolchain stable
export PATH="$PATH:$CARGO_HOME/bin"

env NODE_ENV='dev' npm install

export TWITCH_WEB_CLIENT_ID='kimne78kx3ncx6brgo4mv6wki5h1ko'
export TWITCH_APP_CLIENT_ID='1qgws7yzcp21g5ledlzffw3lmqdvie'
export TWITCH_ANDROID_CLIENT_ID='kd1unb4b3q4t58fwlpcbzcbnm76a8fp'
export TWITCH_APP_CLIENT_SECRET="$TWITCH_APP_CLIENT_ID"
env NODE_ENV='production' \
  npm run tauri build -- \
    --no-bundle \
    --target x86_64-unknown-linux-gnu \
    -- "-j$(nproc)"


%install
RELEASE_DIR='./src-tauri/target/x86_64-unknown-linux-gnu/release'

%if "%{version}" == "8.7.1"
# Install the application binary
install -Dm 0755 "$RELEASE_DIR/%{app_name}" -t %{buildroot}%{_bindir}
%else
install -d %{buildroot}{/opt/%{app_name},%{_bindir}}

# Copy all the application files to the application dir
cp -a "$RELEASE_DIR/build"/{*.so*,*.pak,locales,icudtl.dat,vk_swiftshader_icd.json} \
  %{buildroot}/opt/%{app_name}/
cp -a "$RELEASE_DIR/build"/{chrome-sandbox,v8_context_snapshot.bin,CREDITS.html} \
  %{buildroot}/opt/%{app_name}/
cp -a "$RELEASE_DIR/%{app_name}" \
  %{buildroot}/opt/%{app_name}/

# Symlink the application binary
ln -sv /opt/%{app_name}/%{app_name} %{buildroot}%{_bindir}
%endif

# Install the desktop file
CONTENT="$(cat << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=%app_name
Comment=%summary
Exec=%app_name
StartupWMClass=%app_name
Icon=%app_name
Terminal=false
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
ICONS_DIR='./src-tauri/icons'

# Reorganize icon names
mv -v "$ICONS_DIR/${std_sizes[1]}@2x.png" "$ICONS_DIR/${std_sizes[2]}.png"
mv -v "$ICONS_DIR/icon.png" "$ICONS_DIR/${std_sizes[3]}.png"
mv -v "$ICONS_DIR/StoreLogo.png" "$ICONS_DIR/Square${nstd_sizes[2]}Logo.png"

# Install the application icons
for size in "${std_sizes[@]}"; do
  install -Dm 0644 "$ICONS_DIR/$size.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{app_name}.png"
done
for size in "${nstd_sizes[@]}"; do
  install -Dm 0644 "$ICONS_DIR/Square${size}Logo.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$size/apps/%{app_name}.png"
done
install -Dm 0644 "$ICONS_DIR/icon.svg" \
  %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{app_name}.svg


%files
%{_bindir}/%{app_name}
%if "%{version}" != "8.7.1"
/opt/%{app_name}
%endif
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{app_name}.*
%license ./LICENSE
%doc ./{CHANGELOG,README}.md ./docs/plugins


%changelog
%autochangelog
