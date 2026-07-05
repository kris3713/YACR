%global         app_name BleachBit
%global         app_id org.%{name}.%{app_name}
%global         debug_package %nil

%define         fedoraproject_src https://src.fedoraproject.org/rpms/%{name}/raw/rawhide/f

Name:           %(echo %app_name | tr '[:upper:]' '[:lower:]')
Version:        6.0.0
Release:        2%{?dist}
Summary:        Remove sensitive data and free up disk space

License:        GPL-3.0-or-later
URL:            https://www.%{name}.org/
Source:         https://github.com/%{name}/%{name}/archive/refs/tags/v%{version}.tar.gz

Patch0:         %{fedoraproject_src}/no_update.patch
# https://github.com/bleachbit/bleachbit/issues/950
Patch1:         %{fedoraproject_src}/disable_policykit.patch

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  make
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-hatchling
BuildRequires:  python3-installer
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-psutil
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  pkgconfig(systemd)

Requires:       gtk3
Requires:       python3-chardet
Requires:       python3-gobject
Requires:       python3-psutil


%description
Delete traces of your computer activity and other junk files to free
disk space and maintain privacy.

With BleachBit, you can free cache, delete cookies, clear Internet
history, shred temporary files, delete logs, and discard junk you didn't
know was there. Designed for Linux and Windows systems, it wipes clean
thousands of applications including Firefox, Internet Explorer, Adobe
Flash, Google Chrome, Opera, Safari, and many more. Beyond simply
deleting files, BleachBit includes advanced features such as shredding
files to prevent recovery, wiping free disk space to hide traces of
files deleted by other applications, and cleaning Web browser profiles
to make them run faster.


%prep
%autosetup -p1 -n ./%{name}-%{version}

# Disable update notifications, since package will be updated by DNF or Packagekit.
sed 's/online_update_notification_enabled = True/online_update_notification_enabled = False/g' \
  --in-place ./%{name}/__init__.py
# These get installed to %%{_datadir} as non-executable files, and so shouldn't need a shebang at all.
find ./bleachbit/  -type f  -iname '*.py'  -exec sed --regexp-extended '1s|^#! ?/.+$||g' --in-place '{}' +
# Replace any remaining env shebangs, or shebangs calling unversioned or unnecessarily specifically versioned Python, with plain python3.
find ./  -type f  -iname '*.py' -exec \
  sed --regexp-extended '1s|^#! ?%{_bindir}/env python3?$|#!%{_bindir}/python3|g' \
  --in-place '{}' +
find ./  -type f  -iname '*.py' -exec \
  sed --regexp-extended '1s|^#! ?%{_bindir}/python[[:digit:][:punct:]]*$|#!%{_bindir}/python3|g' \
  --in-place '{}' +


%build
%pyproject_wheel

make -C po local
# Remove Windows-specific functionality.
%make_build delete_windows_files


%install
%make_install prefix=%{_prefix}

desktop-file-install --dir=%{buildroot}%{_datadir}/applications/ \
  ./%{app_id}.desktop
install -Dm 0644 ./%{app_id}.metainfo.xml \
  -t %{buildroot}%{_metainfodir}

%find_lang %{name}


%files -f %{name}.lang
%doc ./README* ./doc
%license ./COPYING
%{_bindir}/%{name}
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_metainfodir}/%{app_id}.metainfo.xml


%changelog
%autochangelog
