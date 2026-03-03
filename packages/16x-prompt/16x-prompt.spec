%global         __provides_exclude_from ^/opt/%{name}/.*$
%global         __requires_exclude_from ^/opt/%{name}/.*$
%global         company %%(echo %name | cut '-d-' -f1)
%global         product %%(echo %name | cut '-d-' -f2)
%global         whitespaced_name %%company %%product
%global         Whitespaced_name %%company %%(v=%%{product}; echo "${v^}")
%global         debug_package %nil

Name:           16x-prompt
Version:        0.0.143
Release:        1%{?dist}
Summary:        Helps developer create the perfect prompt for complex coding tasks with AI.

License:        Freeware
URL:            https://%{product}.%{company}.engineer/

Source0:        https://download.%{company}.engineer/%{name}_0.0.143_amd64.deb

BuildRequires:  dpkg

ExclusiveArch:  x86_64

%description
%Whitespaced_name is a desktop application that helps developers manage source code
context and craft prompts for complex coding tasks on existing codebases.
It provides structured prompt creation, code editing, custom instructions,
BYOK API integrations, token limit tracking, and a no‑black‑box workflow.


%install
dpkg -x %SOURCE0 ./%{name}

OLD_DIR='opt/%{Whitespaced_name}'
NEW_DIR='opt/%{name}'

# Change directory name
mv -v "./%{name}/$OLD_DIR" "./%{name}/$NEW_DIR"

# Edit desktop file
sed -i "s;\"/$OLD_DIR/%{name}\";%{name};" \
  ./%{name}%{_datadir}/applications/%{name}.desktop
sed -i 's;Icon=%{name};Icon=%{_iconsdir}/hicolor/1024x1024/apps/%{name}.png;' \
  ./%{name}%{_datadir}/applications/%{name}.desktop

# Copy all the applications files to the buildroot
cp -a ./%{name}/* %{buildroot}/

# Create a symlink to the application executable
install -d %{buildroot}%{_bindir}
ln -sv "/$NEW_DIR/%{name}" %{buildroot}%{_bindir}


%files
%{_bindir}/%{name}
/opt/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/doc/%{name}
%{_iconsdir}/hicolor/1024x1024/apps/%{name}.png


%changelog
%autochangelog
