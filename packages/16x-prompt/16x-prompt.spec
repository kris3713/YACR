%global         __provides_exclude_from ^/opt/%{name}/.*$
%global         __requires_exclude_from ^/opt/%{name}/.*$
%global         company %%(echo %name | cut '-d-' -f1)
%global         product %%(echo %name | cut '-d-' -f2)
%global         Product %%(v="%%{product}"; echo "${v^}")
%global         debug_package %nil

Name:           16x-prompt
Version:        0.0.143
Release:        1%{?dist}
Summary:        AI Coding with Context Management

License:        Freeware
URL:            https://%{product}.%{company}.engineer/

Source0:        https://download.%{company}.engineer/%{name}_0.0.143_amd64.deb

BuildRequires:  dpkg

ExclusiveArch:  x86_64

%description
%company %Product is a desktop application that helps developers manage source code
context and craft prompts for complex coding tasks on existing codebases.
It provides structured prompt creation, code editing, custom instructions,
BYOK API integrations, token limit tracking, and a no‑black‑box workflow.


%install
dpkg -x %SOURCE0 ./%{name}

mv -v './%{name}/opt/%{company} %{Product}' %{buildroot}/opt/%{name}
sed -i 's;"/opt/%{company} %{Product};16x-prompt";/opt/%{name}/%{name};'

# Copy all the applications files to the buildroot
cp -a ./%{name}/* %{buildroot}/


%files
/opt/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/doc/%{name}
%{_iconsdir}/hicolor/1024x1024/apps/%{name}.png


%changelog
%autochangelog
