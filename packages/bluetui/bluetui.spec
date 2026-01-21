%global         debug_package %{nil}

%ifarch x86_64
%global         build_target x86_64-unknown-linux-gnu
%else
%global         build_target aarch64-unknown-linux-gnu
%endif

Name:           bluetui
Version:        0.8.1
Release:        1%{?dist}
Summary:        TUI for managing bluetooth on Linux
License:        GPL-3.0-or-later

URL:            https://github.com/pythops/%{name}
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cargo rust dbus-devel pkgconf-pkg-config
Requires:       dbus bluez

%description
TUI for managing bluetooth on Linux


%prep
%autosetup -n ./%{name}-%{version}


%build
export CARGO_HOME="$(realpath ./.cargo)"
cargo build --release --locked --target %build_target

# Generate license documentation
cargo tree --workspace --edges 'no-build,no-dev,no-proc-macro' \
  --no-dedupe --prefix none --format '{l}: {p}' | sort -u > ./LICENSE.dependencies

# cargo tree --workspace --edges 'no-build,no-dev,no-proc-macro' \
#   --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary


%install
# Create important directories in the buildroot
install -d %{buildroot}{%{_bindir},%{_datadir}/applications}

# Install the executable
install -Dm 0755 ./target/%{build_target}/release/%{name} -t %{buildroot}%{_bindir}


%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%doc ./Readme.md
%license ./LICENSE ./LICENSE.dependencies


%changelog
%autochangelog
