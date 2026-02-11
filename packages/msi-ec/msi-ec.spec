%global         commit_hash 347dadde05d6bbee7b2f69a5356ec08a469022ae
%global         short_hash %(echo %commit_hash | cut -c '1-7')
%global         pkg_version 0.13
%global         underscore_name %%(echo %name | tr '-' '_')
%global         debug_package %nil

Name:           msi-ec
Version:        %{pkg_version}.git.%{short_hash}
Release:        1%{?dist}
Summary:        Embedded Controller for MSI laptops

License:        GPL-2.0
URL:            https://github.com/jcbmln/%{name}

Source:         %{url}/archive/%{commit_hash}.tar.gz

BuildRequires:  dkms
Requires:       dkms

BuildArch:      noarch

%description
%{summary}


%prep
%autosetup -n ./%{name}-%{commit_hash}


%install
src_dir='%{buildroot}/usr/src/%{underscore_name}-%{pkg_version}'

# Create important directories in the buildroot.
install -d "$src_dir"

# Required files
req_files=('dkms.conf' 'Makefile' '%{name}.c' 'ec_memory_configuration.h')

# Install required files to the src directory
for req_file in "${req_files[@]}"; do
  install -Dm 0644 "./$req_file" -t "$src_dir"
done

# Modify the dkms.conf file in the src directory
sed -e 's/@VERSION/%{pkg_version}/' -i "$src_dir/dkms.conf"


%post
if [ $1 -eq 1 ]; then
  # Change current directory
  pushd /usr/src/%{underscore_name}-%{pkg_version}

  dkms remove %{underscore_name}/%{pkg_version} --all
  rm -f /etc/modules-load.d/%{name}.conf

  # Switch back to the previous directory
  popd

  # Inform the user
  echo 'Make sure to restart the computer afterwards to ensure the driver is properly uninstalled!'
fi

# Change current directory
pushd /usr/src/%{underscore_name}-%{pkg_version}

# Install the msi-ec driver
for action in 'add' 'build' 'install'; do
  dkms $action %{underscore_name}/%{pkg_version}
done
echo '%{name}' > /etc/modules-load.d/%{name}.conf

# Switch back to the previous directory
popd

# Inform the user
echo 'Make sure to restart the computer afterwards to ensure the driver is properly installed!'


%preun
if [ $1 -eq 0 ]; then
  # Change current directory
  pushd /usr/src/%{underscore_name}-%{pkg_version}

  dkms remove %{underscore_name}/%{pkg_version} --all
  rm -f /etc/modules-load.d/%{name}.conf

  # Switch back to the previous directory
  popd

  # Inform the user
  echo 'Make sure to restart the computer afterwards to ensure the driver is properly uninstalled!'
fi


%files
/usr/src/%{underscore_name}-%{pkg_version}
%doc ./README.md
%license ./LICENSE

%changelog
%autochangelog
