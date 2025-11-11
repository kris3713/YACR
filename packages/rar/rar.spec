%global         debug_package %{nil}
%global         version_no_dots 712

Name:           rar
Version:        7.12
Release:        1%{?dist}
Summary:        Utility for RAR archives

License:        Custom (See license.txt)
URL:            https://www.rarlab.com/

Source0:        https://www.rarlab.com/rar/rarlinux-x64-%{version_no_dots}.tar.gz
# Thank you Debian/Ubuntu mantainers for the unrar man page
Source1:        https://manpages.ubuntu.com/manpages.gz/questing/man1/unrar-nonfree.1.gz#/unrar.1.gz

BuildRequires:  perl

ExclusiveArch:  x86_64

Provides:       un%{name}(%{_arch}) = %{version}-%{release}

%description
%{summary}. This package also includes the `unrar` utility.

%prep
%setup -q -n ./%{name}

%build
# This script is taken from the Nix script for the rar pkg
# https://github.com/NixOS/nixpkgs/blob/b6a8526db03f735b89dd5ff348f53f752e7ddc8e/pkgs/by-name/ra/rar/package.nix#L47
# Create man pages with perl and pod2man using rar.txt
%__perl -0777 -i -pe 's/ ([\w .-]+\n) ~+\n/=head1 \U$1/g' ./%{name}.txt
%__perl -0777 -i -pe 's/ (Copyrights)/=head1 \U$1/g;' ./%{name}.txt
%__mv ./%{name}.txt ./%{name}.1.pod
pod2man -c "RAR User's Manual" -n 'RAR' -r "%{name} ${version}" -s 1 ./%{name}.1.pod > ./%{name}.1

# Compress the man page
%__gzip -9 -c ./%{name}.1 > ./%{name}.1.gz
%__rm ./%{name}.1 # Remove the uncompressed man page

%install
# Create directories in the build root
%__install -d %{buildroot}{%{_bindir},/usr/lib,%{_mandir}/man1,/etc}

# Install the application binaries
%__install -Dm 0755 ./%{name} -t %{buildroot}%{_bindir}
%__install -Dm 0755 ./un%{name} -t %{buildroot}%{_bindir}

# Install the application libraries
%__install -Dm 0644 ./default.sfx -t %{buildroot}/usr/lib

# Install the man pages
%__install -Dm 0644 ./%{name}.1.gz -t %{buildroot}%{_mandir}/man1
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_mandir}/man1

# Install the list of data to /etc
%__install -Dm 0644 ./%{name}files.lst -t %{buildroot}/etc

%files
%{_bindir}/%{name}
%{_bindir}/un%{name}
/usr/lib/default.sfx
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/un%{name}.1.gz
/etc/rarfiles.lst
%license ./acknow.txt ./license.txt
