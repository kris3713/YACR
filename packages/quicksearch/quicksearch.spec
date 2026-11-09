%global         app_id com.%{maintainer}.%{name}
%global         maintainer karsttech
%global         altname quick_search
%global         debug_package %nil

%define         git_url https://code.%{maintainer}.com/jeremy/%{altname}
%ifarch x86_64
%define         build_target x86_64-unknown-linux-gnu
%else
%define         build_target aarch64-unknown-linux-gnu
%endif

Name:           %(echo %altname | sed 's/_//')
Version:        1.2.1
Release:        1%{?dist}
Summary:        Find any file on your computer, as fast as you can type

License:        GPL-3.0-or-later
URL:            https://%{name}.%{maintainer}.com/

Source0:        %{git_url}/archive/v%{version}.tar.gz

BuildRequires:  gcc rust cargo openssl-devel perl
BuildRequires:  libX11-devel libX11-xcb libxcb-devel libXcursor-devel
BuildRequires:  libXi-devel libXrender-devel glibc-devel libgcc
BuildRequires:  libxkbcommon-devel libxkbcommon-x11-devel libwayland-client
BuildRequires:  libwayland-egl libglvnd-egl libglvnd-glx

# Taken from the website
%description
QuickSearch helps you find important files quickly and easily.
It indexes the folders you choose, names and text contents, and
shows ranked results with every keystroke. It's free, open source,
and yours to keep.


%prep
%autosetup -n ./%{altname}


%build
export CARGO_HOME="$(realpath ./.cargo)"

cargo build "-j$(nproc)" --profile release --target %build_target

# Generate a LICENSE file for all cargo dependencies
cargo tree --workspace --edges 'no-build,no-dev,no-proc-macro' \
  --no-dedupe --prefix none \
  --format '{l}: {p}' |
    sed -e "s: ($(pwd)[^)]*)::g" -e 's: / :/:g' -e 's:/: OR :g' |
      sort -u > ./LICENSE.dependencies

%install
# Install the binaries
for bin in '%{name}' '%{name}-cli'; do
  install -Dm 0755 "./target/%{build_target}/release/$bin" \
    -t %{buildroot}%{_bindir}
done

# Install desktop file
install -Dm 0644 ./packaging/%{name}.desktop \
  -t %{buildroot}%{_datadir}/applications

# Install the application icons
ICONS_DIR='./crates/quicksearch-gui/assets/icons'
install -Dm 0644 "$ICONS_DIR/%{name}_icon.svg" \
  %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
sizes=('256' '128' '64' '48' '32' '24' '22' '16')
for size in "${sizes[@]}"; do
  dirname="${size}x${size}"
  install -Dm 0644 "$ICONS_DIR/%{name}-${size}.png" \
    "%{buildroot}%{_iconsdir}/hicolor/$dirname/apps/%{name}.png"
done

# Install metainfo files
install -Dm 0644 ./packaging/%{app_id}.metainfo.xml \
  -t %{buildroot}%{_metainfodir}

# Install man pages
for man_page in '%{name}' '%{name}-cli'; do
  install -Dm 0644 "./packaging/$man_page.1" \
    -t %{buildroot}%{_mandir}/man1
done


%files
%{_bindir}/{%{name},%{name}-cli}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_metainfodir}/%{app_id}.metainfo.xml
%{_mandir}/man1/*
%license ./{LICENSE,LICENSE.dependencies}
%doc ./README.md


%changelog
%autochangelog
