%global         git_url https://github.com/JanDeDobbeleer/%{name}
%global         debug_package %{nil}

%ifarch x86_64
%global         go_arch amd64
%else
%global         go_arch arm64
%endif

Name:           oh-my-posh
Version:        28.5.1
Release:        1%{?dist}
Summary:        The most customisable and low-latency cross platform/shell prompt renderer

License:        MIT
URL:            https://ohmyposh.dev/

Source0:        %{git_url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  git golang

%description
%summary


%prep
%autosetup -n ./%{name}-%{version}


%build
if [ $(rpm -E %fedora) -gt 42 ]; then
  export GOEXPERIMENT='greenteagc,jsonv2'
else
  sed -i -e 's/go 1.25.5/go 1.24.10/' ./src/go.mod
fi

export CGO_ENABLED=0
export GOOS='linux'
export GOARCH='%{go_arch}'

pushd ./src

go mod tidy
go build \
  -trimpath \
  -buildmode pie \
  -modcacherw \
  -o ../bin/%{name} \
  -ldflags '-s -w'

popd


%install
install -d %{buildroot}{%{_bindir},%{_datadir}/%{name}}

# Copy the themes directory into /usr/share/oh-my-posh
cp -a ./themes %{buildroot}%{_datadir}/%{name}/

# Install the executable
install -Dm 0755 ./bin/%{name} -t %{buildroot}%{_bindir}


%files
%{_bindir}/oh-my-posh
%{_datadir}/%{name}/themes
%license ./COPYING
%doc ./README.md ./SECURITY.md

%changelog
%autochangelog
