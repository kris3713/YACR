%global         real_name Picocrypt-NG
%global         debug_package %nil

Name:           %(echo %real_name | tr '[:upper:]' '[:lower:]')
Version:        2.05
Release:        1%{?dist}
Summary:        A very small, very simple, yet very secure encryption tool

License:        GPL-3.0
URL:            https://github.com/%{real_name}/%{real_name}

Source0:        %{url}/archive/refs/tags/%{version}.tar.gz
Source1:        %{name}.desktop

BuildRequires:  golang git gcc gcc-c++ xorg-x11-server-devel gtk3-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel libXxf86vm-devel

ExclusiveArch:  x86_64

%description
Picocrypt (New Generation) is a very small (hence Pico), very simple, yet very secure encryption tool
that you can use to protect your files. It's designed to be the go-to tool for file encryption,
with a focus on security, simplicity, and reliability. Picocrypt uses the secure XChaCha20 cipher
and the Argon2id key derivation function to provide a high level of security.

%prep
%setup -q -n ./%{real_name}-%{version}


%build
export CGO_ENABLED=1 GOOS='linux' GOARCH='amd64'

pushd ./src

go build \
  -ldflags '-s -w -linkmode=external' \
  -buildmode pie \
  -o %{name} \
  ./cmd/picocrypt/main.go

popd


%install
# Create important directories in the buildroot
install -d %{buildroot}{%{_bindir},%{_datadir}/applications,%{_iconsdir}/hicolor/scalable/apps}

# Install the application binary
install -Dm 0755 ./src/%{name} -t %{buildroot}%{_bindir}

# Install the desktop file
install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application icon
install -Dm 0644 ./images/key.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg


%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%license ./LICENSE
%doc ./src/README.md ./Changelog.md ./Internals.md ./README.md ./rec.md

%changelog
%autochangelog
