%global         __requires_exclude_from ^/opt/%{app_name}/.*\.so.*$
%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude ^libcef\.so$
%global         git_url https://github.com/%{app_name}/%{app_name}
%global         app_name StreamNook
%global         debug_package %nil

Name:           %(v="%{app_name}"; echo "${v,,}")
Version:        8.9.1
Release:        1%{?dist}
Summary:        A native desktop client for Twitch, YouTube, Kick, and TikTok

License:        MIT
URL:            https://%{name}.app/

Source0:        %{git_url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  nodejs nodejs-npm rust cargo openssl-devel libsoup3-devel
BuildRequires:  javascriptcoregtk4.1-devel webkit2gtk4.1-devel alsa-lib-devel
BuildRequires:  gtk3-devel libayatana-appindicator-gtk3-devel libxdo-devel

%description
%summary.
Multi-stream grid, standalone chat, and every emote provider in one place.


%prep
%autosetup -n ./%{app_name}-%{version}


%build
export npm_config_cache="$(realpath ./.node_cache)"
export CARGO_HOME="$(realpath ./.cargo)"

env NODE_ENV='dev' npm install

export TWITCH_WEB_CLIENT_ID='kimne78kx3ncx6brgo4mv6wki5h1ko' \
  TWITCH_APP_CLIENT_ID='1qgws7yzcp21g5ledlzffw3lmqdvie' \
  TWITCH_ANDROID_CLIENT_ID='kd1unb4b3q4t58fwlpcbzcbnm76a8fp'
env TWITCH_APP_CLIENT_SECRET="$TWITCH_APP_CLIENT_ID" \
  NODE_ENV='production' \
  npm run tauri build -- \
    --no-bundle \
    --target x86_64-unknown-linux-gnu \
    -- "-j$(nproc)"


%install
install -d %{buildroot}{/opt/%{app_name},%{_bindir}}

# Copy all the application files to the application dir
RELEASE_DIR='./src-tauri/target/x86_64-unknown-linux-gnu/release'
cp -av "$RELEASE_DIR"/{*.so*,*.pak,locales,icudtl.dat,vk_swiftshader_icd.json} \
  %{buildroot}/opt/%{app_name}/
cp -av "$RELEASE_DIR"/{chrome-sandbox,%{app_name},v8_context_snapshot.bin} \
  %{buildroot}/opt/%{app_name}/
cp -av "$RELEASE_DIR/CREDITS.html" %{buildroot}/opt/%{app_name}/

# Symlink the application binary
ln -sv /opt/%{app_name}/%{app_name} %{buildroot}%{_bindir}

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
/opt/%{app_name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{app_name}.*
%license ./LICENSE
%doc ./README.md


%changelog
%autochangelog
