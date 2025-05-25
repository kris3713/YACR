# Generic name of the package without vendor branding
%global         gen_name bitmask-vpn
%global         git_url https://0xacab.org/leap/bitmask-vpn
%global         debug_package %{nil}

Name:           riseup-vpn
Version:        0.24.10
Release:        1%{?dist}
Summary:        Easy, fast, and secure VPN service from riseup.net.

License:        GPL-3.0-only
URL:            https://riseup.net/en/vpn

Source0:        %{git_url}/-/archive/%{version}/%{gen_name}-%{version}.tar.gz
Source1:        %{name}.desktop

BuildRequires:  git gawk python3 gcc libgcc cmake golang openvpn-devel qt6-qtbase qt6-qtbase-devel
BuildRequires:  qt6-qtbase-gui qt6-qttools qt6-qttools-devel qt6-qtsvg-devel qt-devel qt6-qtdeclarative-devel
Requires:       openvpn qt6-qtbase qt6-qttools

ExclusiveArch:  x86_64

%description
Easy, fast, and secure VPN service from riseup.net.

The service does not require a user account, keep logs, or track you in any
way. The service is paid for entirely by donations from users.

%prep
%setup -q -n ./%{gen_name}-%{version}
# Using git makes the build unreproducible, but `make vendor` will fail without it
%__git init &> /dev/null
%__git remote add origin %{git_url}.git &> /dev/null
%__git fetch --tags &> /dev/null
%__git checkout -fb %{version} %{version}

%build
# Ensure the vendor is "riseup"
export PROVIDER='riseup'
%__make vendor
%__make relink_vendor

# Build the application
env LRELEASE="%{_libdir}/qt6/bin/lrelease" RELEASE='yes' %__make build &> /dev/null

# Cleanup user-created environmental variables
unset PROVIDER

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create a new build root (along with other directories)
%__install -d %{buildroot}{%{_bindir},%{_datadir}/{applications,polkit-1/actions}}
%__install -d %{buildroot}%{_iconsdir}/hicolor/{256x256,scalable}/apps

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application binaries
%__install -Dm 0755 ./build/qt/release/%{name} -t %{buildroot}%{_bindir}
%__install -Dm 0755 ./pkg/pickle/helpers/bitmask-root -t %{buildroot}%{_bindir}

# Install the application policykit file
%__install -Dm 0644 ./pkg/pickle/helpers/se.leap.bitmask.policy -t %{buildroot}%{_datadir}/polkit-1/actions

# Install application icons
%__install -Dm 0644 ./providers/riseup/assets/icon.png %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{name}.png
%__install -Dm 0644 ./providers/riseup/assets/icon.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

%files
%{_bindir}/%{name}
%{_bindir}/bitmask-root
%{_datadir}/applications/%{name}.desktop
%{_datadir}/polkit-1/actions/se.leap.bitmask.policy
%{_iconsdir}/hicolor/256x256/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%license ./LICENSE
