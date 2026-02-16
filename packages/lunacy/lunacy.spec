%global         app_name %%(v='%{name}'; echo "${v^}")
%global         debug_package %nil

%define         raw_github_url https://raw.githubusercontent.com/icons8/%{name}-docs

Name:           lunacy
Version:        12.2
Release:        2%{?dist}
Summary:        UI/UX and Web Designer Tool

License:        Freeware (See EULA.md)
URL:            https://icons8.com/%{name}

Source0:        https://lcdn.icons8.com/setup/%{app_name}_%{version}.deb
Source1:        %{raw_github_url}/refs/heads/master/docs/%{name}%20license.md#/EULA.md

BuildRequires:  dpkg

ExclusiveArch:  x86_64

%description
Cross-platform vector editor for UI, UX, and web projects with
native .sketch file editing, real-time multi-user collaboration,
an AI-backed asset library, code and asset export, Figma integration,
offline use, seamless cloud management, and auto layout tools.


%install
dpkg -x %SOURCE0 ./%{name}
cp -a %SOURCE1 .

# Copy all the applications files to the buildroot
cp -a ./%{name}/* %{buildroot}/

sed -i 's|/opt/icons8/%{name}/Assets/%{app_name}Logo.png|%{name}|' \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

sed -i 's|x-scheme-handler/i8-lunacy;|x-scheme-handler/i8-lunacy;zip/sketch;zip/free|' \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

install -Dm 0644 ./%{name}/opt/icons8/%{name}/Assets/%{app_name}Logo.png \
  %{buildroot}%{_iconsdir}/hicolor/200x200/apps/%{name}.png

install -d %{buildroot}%{_bindir}
ln -sv /opt/icons8/%{name}/%{app_name} %{buildroot}%{_bindir}


%post
if ! [ -f %{_datadir}/mime/packages/zip-sketch.xml ]; then
  cat << 'XML' > %{_datadir}/mime/packages/zip-sketch.xml
<?xml version="1.0"?>
<mime-info xmlns='http://www.freedesktop.org/standards/shared-mime-info'>
  <mime-type type="zip/sketch">
    <comment>Sketch file</comment>
    <glob pattern="*.sketch"/>
  </mime-type>
</mime-info>
XML
fi

if ! [ -f %{_datadir}/mime/packages/zip-free.xml ]; then
  cat << 'XML' > %{_datadir}/mime/packages/zip-free.xml
<?xml version="1.0"?>
<mime-info xmlns='http://www.freedesktop.org/standards/shared-mime-info'>
  <mime-type type="zip/free">
    <comment>Lunacy Free file</comment>
    <glob pattern="*.free"/>
  </mime-type>
</mime-info>
XML
fi

MIMEAPPS_LIST='%{_datadir}/applications/mimeapps.list'
# Associate .sketch
xdg-mime install --mode system %{_datadir}/mime/packages/zip-sketch.xml
SKETCH_MIME_TYPE='zip/sketch=lunacy.desktop'
if grep -Fxq "$SKETCH_MIME_TYPE" "$MIMEAPPS_LIST"; then
  echo ': .sketch already registered'
else
  echo "$SKETCH_MIME_TYPE" >> "$MIMEAPPS_LIST"
fi
# Associate .free
xdg-mime install --mode system %{_datadir}/mime/packages/zip-sketch.xml
FREE_MIME_TYPE='zip/free=lunacy.desktop'
if grep -Fxq "$FREE_MIME_TYPE" "$MIMEAPPS_LIST"; then
  echo ': .free already registered'
else
  echo "$FREE_MIME_TYPE" >> "$MIMEAPPS_LIST"
fi

update-mime-database %{_datadir}/mime
update-desktop-database
# Associate icons
gtk-update-icon-cache %{_iconsdir}/hicolor -f


%files
%{_bindir}/%{app_name}
/opt/icons8/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/200x200/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/mimetypes/zip-sketch.svg
%dir %{_datadir}/mime/
%license ./EULA.md


%changelog
%autochangelog
