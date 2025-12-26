%global         debug_package %{nil}

Name:           catnap
Version:        1.1.1
Release:        1%{?dist}
Summary:        A highly customizable systemfetch written in nim

License:        MIT
URL:            https://github.com/iinsertNameHere/%{name}

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

# The nim package is from terrapkg
BuildRequires:  nim
BuildRequires:  gzip curl
Requires:       curl pcre usbutils glx-utils

%description
Catnap (originally known as Catnip) is as a playful,
simple system-information concatenation tool using nim.
It is quite customizable and has possibilities to
alter the names and colors of the statistics.


%prep
%autosetup -n ./%{name}-%{version}


%build
# All is needed to build the catnap executable
nim release


%install
# Create important directories in the buildroot
install -d %{buildroot}{%{_bindir},/etc/%{name},%{_mandir}/{man1,man5}}

# Install the executable
install -Dm 0755 ./bin/%{name} -t %{buildroot}%{_bindir}

# Copy the config files
cp -a ./config/* %{buildroot}/etc/%{name}/

# Install the manpages
install -Dm 0644 ./docs/%{name}.1 -t %{buildroot}%{_mandir}/man1
install -Dm 0644 ./docs/%{name}.5 -t %{buildroot}%{_mandir}/man5

%post
if ! [ -d "$SUDO_HOME/.config/%{name}" ]; then
  mkdir -p "$SUDO_HOME/.config/%{name}"
  mv -a /etc/%{name}/* "$SUDO_HOME/.config/%{name}/"
fi


%files
%{_bindir}/%{name}
%{_mandir}/*
%config(noreplace) /etc/%{name}/*
%license ./LICENSE
%doc ./CHANGELOG.md


%changelog
%autochangelog
