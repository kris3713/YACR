# Generic name of the package without vendor branding
%global         gen_name bitmask-vpn
%global         git_url https://0xacab.org/leap/bitmask-vpn
%global         debug_package %{nil}

Name:           riseup-vpn
Version:        0.25.8
Release:        1%{?dist}
Summary:        Easy, fast, and secure VPN service from riseup.net

License:        GPL-3.0-only
URL:            https://riseup.net/en/vpn

Source0:        %{git_url}/-/archive/%{version}/%{gen_name}-%{version}.tar.gz

BuildRequires:  git gawk python3 gcc libgcc cmake golang openvpn-devel
BuildRequires:  qt6-qtbase qt6-qtbase-devel qt6-qtbase-gui qt6-qttools
BuildRequires:  qt6-qttools-devel qt6-qtsvg-devel qt-devel qt6-qtdeclarative-devel
Requires:       python3 openvpn

ExclusiveArch:  x86_64

%description
Easy, fast, and secure VPN service from riseup.net.

The service does not require a user account, keep logs, or track you in any
way. The service is paid for entirely by donations from users.


%prep
%setup -q -n ./%{gen_name}-%{version}
# Using git makes the build unreproducible, but `make vendor` will fail without it
git init &> /dev/null
git remote add origin %{git_url}.git &> /dev/null
git fetch --tags &> /dev/null
git checkout -fb %{version} %{version}


%build
# Ensure the vendor is "riseup"
export PROVIDER='riseup'
make vendor
make relink_vendor

# Build the application
export LRELEASE="%{_libdir}/qt6/bin/lrelease" RELEASE='yes'
export QMAKE='qmake6'
%make_build


%install
# Create important directories in the buildroot
install -d %{buildroot}{%{_bindir},%{_datadir}/{applications,polkit-1/actions}}
install -d %{buildroot}%{_iconsdir}/hicolor/{256x256,scalable}/apps

# Install the desktop file
DESKTOP_FILE=./branding/templates/debian/app.desktop-template
sed -i -e 's/${applicationName}/RiseupVPN/' \
  -e 's/${binaryName}/%{name}/' \
  -e 's/${name}/%{name}/' \
  "$DESKTOP_FILE"
install -Dm 0644 "$DESKTOP_FILE" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install the application binaries
install -Dm 0755 ./build/qt/release/%{name} -t %{buildroot}%{_bindir}
install -Dm 0755 ./pkg/pickle/helpers/bitmask-root -t %{buildroot}%{_bindir}

# Install the application policykit file
install -Dm 0644 ./pkg/pickle/helpers/se.leap.bitmask.policy -t %{buildroot}%{_datadir}/polkit-1/actions

# Install application icons
install -Dm 0644 ./providers/riseup/assets/icon.png \
  %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{name}.png
install -Dm 0644 ./providers/riseup/assets/icon.svg \
  %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

%post
/usr/bin/%{name} --install-helpers


%files
%{_bindir}/%{name}
%{_bindir}/bitmask-root
%{_datadir}/applications/%{name}.desktop
%{_datadir}/polkit-1/actions/se.leap.bitmask.policy
%{_iconsdir}/hicolor/256x256/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%license ./LICENSE


%changelog
%autochangelog
