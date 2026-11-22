%global         __brp_check_rpaths %nil
%global         __provides_exclude_from ^/opt/%{name}/.*$
%global         __requires_exclude_from ^/opt/%{name}/.*$
%global         url_part https://cdn.%{name}.com/download/%{name}
%global         app_name JOPDF
%global         debug_package %nil

%ifarch x86_64
%global         default_src %SOURCE0
%else
%global         default_src %SOURCE1
%endif

Name:           %(v='%{app_name}'; echo "${v,,}")
Version:        2.4.3
Release:        1%{?dist}
Summary:        Edit, read, convert, compress, perform OCR, fill out PDF forms, and manage PDFs seamlessly

License:        Freeware
URL:            https://www.%{name}.com/

Source0:        %{url_part}/%{name}-linux-amd64_setup.deb#/%{name}-%{version}_amd64.deb
Source1:        %{url_part}/%{name}-linux-arm64_setup.deb#/%{name}-%{version}_arm64.deb

BuildRequires:  dpkg

%description
JOPDF helps you tackle all your PDF tasks with ease.
Edit, convert, compress, merge, split, create, annotate,
organize, fill forms, OCR, and protect your PDF files
without hassle. All for free, no sign-up required.


%install
dpkg -x %default_src ./%{name}

# Copy all the application files to the buildroot
cp -a ./%{name}/* %{buildroot}

# Create a symlink to the application executable
install -d %{buildroot}%{_bindir}
ln -sv /opt/%{name}/%{app_name} %{buildroot}%{_bindir}


%files
%{_bindir}/%{app_name}
/opt/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*


%changelog
%autochangelog
