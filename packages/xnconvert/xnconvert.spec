%global         __brp_check_rpaths %{nil}
# The reason for this is to avoid the "broken rpath" error
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         app_name XnConvert
%global         debug_package %{nil}

Name:           xnconvert
Version:        1.106.0
Release:        1%{?dist}
Summary:        XnConvert is a fast, powerful and free cross-platform batch image converter.

License:        Freeware (Non-Commercial) | Proprietary (Commercial)
URL:            https://www.xnview.com/en/xnconvert/

Source0:        https://download.xnview.com/old_versions/XnConvert/XnConvert-%{version}-linux-x64.tgz
Source1:        %{name}.png
Source2:        %{name}.desktop
Source3:        %{name}.sh
Source4:        %{name}

ExclusiveArch:  x86_64

%description
XnConvert is a fast, powerful and free cross-platform batch image converter.
It allows to automate editing of your photo collections: you can rotate,
convert and compress your images, photos and pictures easily, and apply
over 80 actions (like resize, crop, color adjustments, filter, ...)
All common picture and graphics formats are supported (JPEG, TIFF, PNG, GIF,
WebP, PSD, JPEG2000, JPEG-XL, OpenEXR, camera RAW, AVIF, HEIC, HEIF, PDF, DNG, CR2).
You can save and re-use your presets for another batch image conversion.

%prep
%setup -q -n ./%{app_name}

%install
export QA_RPATHS=$[ 0x0002 | 0x0010 ]
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},/opt/%{app_name},%{_datadir}/applications}
%__install -d %{buildroot}%{_iconsdir}/hicolor/{64x64,512x512}/apps

# Remove some unnecessary files
%__rm ./{%{app_name}.desktop,%{name}.sh}

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}
%__install -Dm 0755 %{SOURCE3} -t %{buildroot}/opt/%{app_name}

# Install the desktop file
%__install -Dm 0644 %{SOURCE2} -t %{buildroot}%{_datadir}/applications

# Install the shell script wrapper for the application binary
%__install -Dm 0755 %{SOURCE4} -t %{buildroot}%{_bindir}

# Install the application icons
%__install -Dm 0644 ./%{name}.png -t %{buildroot}%{_iconsdir}/hicolor/64x64/apps
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_iconsdir}/hicolor/512x512/apps

%files
/opt/%{app_name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%{_iconsdir}/hicolor/512x512/apps/%{name}.png
%license ./license.txt
