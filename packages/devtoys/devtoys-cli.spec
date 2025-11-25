%global         __provides_exclude_from ^/opt/%{name}/.*$
%global         __requires_exclude_from ^/opt/%{name}/.*$
%global         __spec_install_post %{nil}
%global         __os_install_post %{_dbpath}/brp-compress
%global         fullname devtoys
%global         debug_package %{nil}

Name:           devtoys-cli
Version:        2.0.8.0
Release:        1%{?dist}
Summary:        A Swiss Army knife for developers. (CLI version)

License:        MIT
URL:            https://devtoys.app/

Source0:        https://github.com/DevToys-app/DevToys/releases/download/v%{version}/%{fullname}.cli_linux_x64_portable.zip

Requires:       dotnet-host

ExclusiveArch:  x86_64

%description
DevToys helps with daily development tasks by offering a
bundle of tiny tools designed to do quick, specific tiny tasks.
No need to use many untrustworthy websites to simply decode a
text or compress an image. With Smart Detection, the app
intuitively selects the best tool for the data on your clipboard.

%prep
%setup -q -c -n %{name}-%{version}

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create a new build root
%__install -d %{buildroot}{/opt/%{name},%{_bindir},%{_datadir}/applications}

# Copy all the application files to application directory
%__cp -a . %{buildroot}/opt/%{name}

# Create a symlink to the executable
%__ln -s /opt/%{name}/DevToys.CLI %{buildroot}%{_bindir}/DevToys

%files
/opt/%{name}
%{_bindir}/DevToys
%license ./LICENSE.md

%changelog
%autochangelog
