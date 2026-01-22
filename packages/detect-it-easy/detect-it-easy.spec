%global         app_name die
%global         debug_package %nil

%define         git_url https://github.com/horsicq/DIE-engine

Name:           detect-it-easy
Version:        3.10
Release:        2%{?dist}
Summary:        Program for determining types of files for Windows, Linux, and MacOS

License:        MIT
URL:            https://horsicq.github.io/#detect-it-easy%{app_name}

Source0:        %{git_url}/releases/download/%{version}/%{app_name}_sourcecode_%{version}.tar.gz

BuildRequires:  make clang qt5-qtbase qt5-qtbase-devel
BuildRequires:  qt5-qtbase-gui qt5-qtscript-devel qt5-qttools
BuildRequires:  qt5-qttools-devel qt5-qtsvg-devel qt-devel qtchooser

%description
Detect It Easy (DiE) is a powerful tool for file type identification,
popular among malware analysts, cybersecurity experts, and reverse engineers
worldwide. Supporting both signature-based and heuristic analysis, DiE
enables efficient file inspections across a broad range of platforms,
including Windows, Linux, and MacOS. Its adaptable, script-driven
detection architecture makes it one of the most versatile tools in
the field, with a comprehensive list of supported OS images.


%prep
%setup -q -n ./%{app_name}_sourcecode_%{version}


%build
# Remove unneeded build flags from C flags (clang doesn't need them)
export CFLAGS="$(
  echo '%{build_cflags}' |
  sed -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-hardened-cc1;;' \
    -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1;;'
)"
# Remove unneeded build flags from CXX flags (clang doesn't need them)
export CXXFLAGS="$(
  echo '%{build_cxxflags}' |
  sed -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-hardened-cc1;;' \
    -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1;;'
)"
# Remove unneeded build flags from LD flags (clang doesn't need them)
export LDFLAGS="$(
  echo '%{build_ldflags}' |
  sed -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-hardened-ld;;' \
    -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-hardened-ld-errors;;' \
    -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1;;' \
    -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-package-notes;;'
)"

# Ensure the configure script is executable
chmod 0755 ./configure

# Force make to use clang
export CC=clang CXX=clang++

# Generate build files
%configure

# Build the application binaries
%make_build "CC=$CC" "CXX=$CXX"


%install
# Setup buildroot
install -d %{buildroot}{%{_bindir},/lib/%{app_name}/signatures,%{_datadir}/applications}

for size in '16x16' '20x20' '24x24' '32x32' '48x48' '256x256'; do
  install -d "%{buildroot}%{_datadir}/icons/hicolor/$size/apps"
done

# Install the application binarys
for exe in '%{app_name}' '%{app_name}c' '%{app_name}l'; do
  install -Dm 0755 "./build/release/$exe" -t %{buildroot}%{_bindir}
done

# Copy required libraires for Detect It Easy
cp -a ./XStyles/qss %{buildroot}/lib/%{app_name}/
cp -a ./XYara/yara_rules %{buildroot}/lib/%{app_name}/
cp -a ./XInfoDB/info %{buildroot}/lib/%{app_name}/
cp -a ./images %{buildroot}/lib/%{app_name}/
cp -a ./Detect-It-Easy/{db_custom,db} %{buildroot}/lib/%{app_name}/
cp -a ./signatures/crypto.db %{buildroot}/lib/%{app_name}/signatures/

# Remove executable permissions for all files in /lib/die
find %{buildroot}/lib/%{app_name} -type f -exec chmod 0644 {} +

# Change the directory to ./LINUX
pushd ./LINUX

# Install the desktop file
install -Dm 0644 ./%{app_name}.desktop \
  -t %{buildroot}%{_datadir}/applications

# Install application icons
for size in '16x16' '20x20' '24x24' '32x32' '48x48' '256x256'; do
  install -Dm 0644 "./hicolor/$size/apps/%{name}.png" \
    -t "%{buildroot}%{_datadir}/icons/hicolor/$size/apps"
done

# Change the directory back to the root
popd


%files
%{_bindir}/%{app_name}
%{_bindir}/%{app_name}c
%{_bindir}/%{app_name}l
/lib/%{app_name}
%{_datadir}/applications/%{app_name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%license ./LICENSE


%changelog
%autochangelog
