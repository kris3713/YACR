%global         __brp_mangle_shebangs %{nil}
%global         __requires_exclude_from ^%{_bindir}/generate-domains-blocklist$
%global         debug_package %{nil}

Name:           dnscrypt-proxy
Version:        2.1.14
Release:        1%{?dist}
Summary:        Flexible DNS proxy, with support for encrypted DNS protocols

License:        ISC
URL:            https://github.com/DNSCrypt/dnscrypt-proxy

Source0:        %{url}/archive/refs/tags/%{version}.tar.gz
Patch0:         %{name}.custom_config.patch

BuildRequires:  systemd-rpm-macros golang
# Optionally needed for the `generate-domains-blocklist` script
Recommends:     python3

%description
A flexible DNS proxy, with support for modern encrypted DNS protocols such as
DNSCrypt v2 and DNS-over-HTTP/2.

Features:

 - DNS traffic encryption and authentication. Supports DNS-over-HTTPS (DoH)
 and DNSCrypt.
 - DNSSEC compatible
 - DNS query monitoring, with separate log files for regular and suspicious
 queries
 - Pattern-based local blocking of DNS names and IP addresses
 - Time-based filtering, with a flexible weekly schedule
 - Transparent redirection of specific domains to specific resolvers
 - DNS caching, to reduce latency and improve privacy
 - Local IPv6 blocking to reduce latency on IPv4-only networks
 - Load balancing: pick a set of resolvers, dnscrypt-proxy will automatically
 measure and keep track of their speed, and balance the traffic across the
 fastest available ones.
 - Cloaking: like a HOSTS file on steroids, that can return preconfigured
 addresses for specific names, or resolve and return the IP address of other
 names. This can be used for local development as well as to enforce safe
 search results on Google, Yahoo and Bing.
 - Automatic background updates of resolvers lists
 - Can force outgoing connections to use TCP; useful with tunnels such as Tor.

%prep
%setup -q -n ./%{name}-%{version}
%__patch -Np1 -i %{PATCH0}

%build
cd ./%{name}
go build '-ldflags=-s -w' -mod vendor -o ../bin/%{name}
cd ..

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},/etc/%{name},%{_unitdir}}

# Install the application binary
%__install -Dm 0755 ./bin/%{name} -t %{buildroot}%{_bindir}

# Modify the python helper script, then install it
%__sed -ie 's/#! /#!/' ./utils/generate-domains-blocklist/generate-domains-blocklist.py
%__install -Dm 0755 ./utils/generate-domains-blocklist/generate-domains-blocklist.py \
  %{buildroot}%{_bindir}/generate-domains-blocklist

# Installing required config files
%__install -Dm 0644 ./dnscrypt-proxy/example-dnscrypt-proxy.toml %{buildroot}/etc/%{name}/dnscrypt-proxy.toml
%__install -Dm 0644 ./dnscrypt-proxy/example-allowed-ips.txt %{buildroot}/etc/%{name}/allowed-ips.txt
%__install -Dm 0644 ./dnscrypt-proxy/example-allowed-names.txt  %{buildroot}/etc/%{name}/allowed-names.txt
%__install -Dm 0644 ./dnscrypt-proxy/example-blocked-ips.txt  %{buildroot}/etc/%{name}/blocked-ips.txt
%__install -Dm 0644 ./dnscrypt-proxy/example-blocked-names.txt  %{buildroot}/etc/%{name}/blocked-names.txt
%__install -Dm 0644 ./dnscrypt-proxy/example-captive-portals.txt  %{buildroot}/etc/%{name}/captive-portals.txt
%__install -Dm 0644 ./dnscrypt-proxy/example-cloaking-rules.txt  %{buildroot}/etc/%{name}/cloaking-rules.txt
%__install -Dm 0644 ./dnscrypt-proxy/example-forwarding-rules.txt  %{buildroot}/etc/%{name}/forwarding-rules.txt

%post
dnscrypt-proxy -service uninstall
dnscrypt-proxy -service install -config /etc/%{name}/%{name}.toml
echo "dnscrypt-proxy service has been installed to '/etc/systemd/system/dnscrypt-proxy.service'"
echo -e "\ndnscrypt-proxy configuration files can be found in the '/etc/%{name}' directory"

%preun
if [ $1 -eq 0 ]; then
  dnscrypt-proxy -service stop
  dnscrypt-proxy -service uninstall
  echo "'/etc/systemd/system/dnscrypt-proxy.service' was removed"
  echo 'Reloading systemd daemon...'
  systemctl daemon-reload
fi

# %postun
# dnscrypt-proxy -service stop
# rm -rfv /etc/systemd/system/dnscrypt-proxy.service
# %systemd_postun_with_restart dnscrypt-proxy.service
#
# %posttrans
# dnscrypt-proxy -service stop
# rm -rfv /etc/systemd/system/dnscrypt-proxy.service

%files
%{_bindir}/%{name}
%{_bindir}/generate-domains-blocklist
%dir /etc/%{name}/
%config(noreplace) /etc/%{name}/%{name}.toml
%config(noreplace) /etc/%{name}/*.txt
%ghost %config(noreplace) /etc/%{name}/blacklist.txt
%ghost %config(noreplace) /etc/%{name}/whitelist.txt
%ghost /var/cache/%{name}
%license ./LICENSE
%doc ./README.md ./ChangeLog ./utils/generate-domains-blocklist
