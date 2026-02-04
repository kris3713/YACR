%global         repo_name %{name}.py
%global         debug_package %nil

%define         date_version 2022.06.23
%define         short_commit 43ac66dbd8

Name:           mantra
Version:        %{date_version}.git.%{short_commit}
Release:        1%{?dist}
Summary:        View online Arch Linux manual pages straight from the terminal.

License:        Unknown
URL:            https://codeberg.org/theooo/%{repo_name}

Source0:        %{url}/archive/%{short_commit}.tar.gz

BuildRequires:  make
Requires:       python3 python3-beautifulsoup4 fzf

BuildArch:      noarch

%description
View online Arch Linux manual pages (from https://man.archlinux.org) from the terminal.


%prep
%autosetup -n ./%{repo_name}


%install
%make_install PREFIX='%{_bindir}'


%files
%{_bindir}/%{name}
%doc ./README.md


%changelog
%autochangelog
