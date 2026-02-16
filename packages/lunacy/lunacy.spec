%global         app_name %%(v='%{name}'; echo "${v^}")
%global         debug_package %nil

%define         raw_github_url https://raw.githubusercontent.com/icons8/%{name}-docs

Name:           lunacy
Version:        12.2
Release:        1%{?dist}
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

install -d %{buildroot}%{_bindir}
ln -sv /opt/icons8/%{name}/%{app_name} %{buildroot}%{_bindir}


%post
MIMEINFO_CACHE='%{_datadir}/applications/mimeinfo.cache'
# Associate .sketch
SKETCH_MIME_TYPE='zip/sketch=lunacy.desktop'
update-mime-database %{_datadir}/mime
xdg-mime install --mode system %{_datadir}/mime/packages/zip-sketch.xml
if grep -Fxq "$SKETCH_MIME_TYPE" "$MIMEINFO_CACHE"; then
  echo ': .sketch already registered'
else
  echo "$SKETCH_MIME_TYPE" >> "$MIMEINFO_CACHE"
fi
# Associate .free
FREE_MIME_TYPE='zip/free=lunacy.desktop'
if grep -Fxq "$FREE_MIME_TYPE" "$MIMEINFO_CACHE"; then
  echo ': .free already registered'
else
  echo "$FREE_MIME_TYPE" >> "$MIMEINFO_CACHE"
fi
update-desktop-database
# Associate icons
gtk-update-icon-cache %{_iconsdir}/hicolor -f


%files
%{_bindir}/%{app_name}
/opt/icons8/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/scalable/mimetypes/zip-sketch.svg
%dir %{_datadir}/mime/
%license ./EULA.md


%changelog
%autochangelog
