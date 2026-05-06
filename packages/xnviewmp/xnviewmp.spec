%global         __brp_check_rpaths %nil
# The reason for this is to avoid the "broken rpath" error
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         app_name XnViewMP
%global         alt_name %(v='%{app_name}'; echo "${v::-2}")
%global         alt_name_l %(v="%{alt_name}"; echo "${v,,}")
%global         debug_package %nil

Name:           %(v="%{app_name}"; echo "${v,,}")
Version:        1.11.2
Release:        1%{?dist}
Summary:        XnView MP is a powerful, versatile and free image viewer, photo management, and image resizer software.

License:        Freeware (Non-Commercial) | Proprietary (Commercial)
URL:            https://www.xnview.com/en/%{name}/

Source0:        https://download.xnview.com/old_versions/%{alt_name}_MP/%{alt_name}_MP-%{version}-linux-x64.tgz
Source1:        %{name}.png
Source2:        %{name}.desktop

ExclusiveArch:  x86_64

%description
%summary
%alt_name is one of the most stable, user-friendly, and comprehensive photo management tools available today,
perfect for both beginners and professionals. All common picture and graphics formats are supported
(JPEG, TIFF, PNG, GIF, WEBP, PSD, JPEG2000, JPEG-XL, OpenEXR, camera RAW, HEIF, HEIC, AVIF, PDF, DNG, CR2).

%prep
%autosetup -n ./%{alt_name}

%install
export QA_RPATHS=$[ 0x0002 | 0x0010 ]
# Remove the old build root
rm -rf %{buildroot}

# Create the new build root
install -d %{buildroot}{%{_bindir},/opt/%{app_name},%{_datadir}/applications}
install -d %{buildroot}%{_iconsdir}/hicolor/{64x64,512x512}/apps

# Remove some unnecessary files
rm -v ./{%{alt_name}.desktop,%{alt_name_l}_2.png}

# Copy the application files to the application directory
cp -a . %{buildroot}/opt/%{app_name}

# Install the desktop file
install -Dm 0644 %{SOURCE2} -t %{buildroot}%{_datadir}/applications

# Install the shell script wrapper for the application binary
ln -sv /opt/%{app_name}/%{alt_name_l}.sh %{buildroot}%{_bindir}/%{name}

# Install the application icons
install -Dm 0644 ./%{alt_name_l}.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
ln -sv %{_iconsdir}/hicolor/64x64/apps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{alt_name_l}.png
install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_iconsdir}/hicolor/512x512/apps
ln -sv %{_iconsdir}/hicolor/512x512/apps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/512x512/apps/%{alt_name_l}.png

%files
/opt/%{app_name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{alt_name_l}.png
%license ./license.txt

%changelog
%autochangelog
