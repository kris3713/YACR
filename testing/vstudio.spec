%global             full_name vstudio
%global             application_name zen
%global             debug_package %{nil}

Name:               vstudio
Version:            15.1.5
Release:            1%{?dist}
Summary:            Valentina Studio

License:            https://valentina-db.com/docs/dokuwiki/v5/doku.php?id=valentina:licensing:valentina_studio_license_agreement
URL:                https://valentina-db.com/en/
Source0:            https://valentina-db.com/en/studio/download/vstudio_x64_lin_rpm?format=raw

ExclusiveArch:      x86_64

%description
Valentina Studio is the ultimate data management tool for database administrators.
Valentina Studio includes a wealth of database administration tools and more

%prep
%autosetup


%build
%configure
%make_build


%install
%make_install


%files
%license add-license-file-here
%doc add-docs-here



%changelog
* Mon Apr 21 2025 FlawlessCasual17 <07e5297d5b@c0x0.com>
- 
