%global         __brp_check_rpaths %nil
# The reason for this is to avoid the "broken rpath" error
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         app_name XnConvert
%global         debug_package %nil

Name:           %(v="%{app_name}"; echo "${v,,}")
Version:        1.111.0
Release:        1%{?dist}
Summary:        %{app_name} is a fast, powerful and free cross-platform batch image converter.

License:        Freeware (Non-Commercial) | Proprietary (Commercial)
URL:            https://www.xnview.com/en/%{name}/

Source0:        https://download.xnview.com/old_versions/%{app_name}/%{app_name}-%{version}-linux-x64.tgz
Source1:        %{name}.png
Source2:        %{name}.desktop

ExclusiveArch:  x86_64

%description
%summary
It allows to automate editing of your photo collections: you can rotate,
convert and compress your images, photos and pictures easily, and apply
over 80 actions (like resize, crop, color adjustments, filter, ...)
All common picture and graphics formats are supported (JPEG, TIFF, PNG, GIF,
WebP, PSD, JPEG2000, JPEG-XL, OpenEXR, camera RAW, AVIF, HEIC, HEIF, PDF, DNG, CR2).
You can save and re-use your presets for another batch image conversion.

%prep
%autosetup -n ./%{app_name}

%install
export QA_RPATHS=$[ 0x0002 | 0x0010 ]

# Create directories in the buildroot
install -d %{buildroot}{%{_bindir},/opt/%{app_name},%{_datadir}/applications}
install -d %{buildroot}%{_iconsdir}/hicolor/{64x64,512x512}/apps

# Remove some unnecessary files
rm -v ./{%{app_name}.desktop,%{name}.sh}

# Copy the application files to the application directory
cp -a . %{buildroot}/opt/%{app_name}

# Install the desktop file
install -Dm 0644 %{SOURCE2} -t %{buildroot}%{_datadir}/applications

# Install the shell script wrapper for the application binary
ln -sv /opt/%{app_name}/%{name}.sh %{buildroot}%{_bindir}/%{name}

# Install the application icons
install -Dm 0644 ./%{name}.png -t %{buildroot}%{_iconsdir}/hicolor/64x64/apps
install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_iconsdir}/hicolor/512x512/apps

%files
/opt/%{app_name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%license ./license.txt

%changelog
%autochangelog
