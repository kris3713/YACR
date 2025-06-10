%global         __brp_check_rpaths %{nil}
# The reason for this is to avoid the "broken rpath" error
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         app_name XnViewMP
%global         debug_package %{nil}

Name:           xnviewmp
Version:        1.9.1
Release:        1%{?dist}
Summary:        XnView MP is a powerful, versatile and free image viewer, photo management, and image resizer software.

License:        Freeware (Non-Commercial) | Proprietary (Commercial)
URL:            https://www.xnview.com/en/xnviewmp/

Source0:        https://download.xnview.com/old_versions/XnView_MP/XnView_MP-%{version}-linux-x64.tgz
Source1:        %{name}.png
Source2:        %{name}.desktop
Source3:        xnview
Source4:        %{name}

ExclusiveArch:  x86_64

%description
XnView MP is a powerful, versatile and free image viewer, photo management, and image resizer software.
XnView is one of the most stable, user-friendly, and comprehensive photo management tools available today,
perfect for both beginners and professionals. All common picture and graphics formats are supported
(JPEG, TIFF, PNG, GIF, WEBP, PSD, JPEG2000, JPEG-XL, OpenEXR, camera RAW, HEIF, HEIC, AVIF, PDF, DNG, CR2).

%prep
%setup -q -n ./XnView

%install
export QA_RPATHS=$[ 0x0002 | 0x0010 ]
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},/opt/%{app_name},%{_datadir}/applications}
%__install -d %{buildroot}%{_iconsdir}/hicolor/{64x64,512x512}/apps

# Remove some unnecessary files
%__rm ./{XnView.desktop,xnview_2.png,xnview.sh}

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}
%__install -Dm 0755 %{SOURCE3} -t %{buildroot}/opt/%{app_name}

# Install the desktop file
%__install -Dm 0644 %{SOURCE2} -t %{buildroot}%{_datadir}/applications

# Install the application binary
%__install -Dm 0755 %{SOURCE4} -t %{buildroot}%{_bindir}

# Install the application icon
%__install -Dm 0644 ./xnview.png -t %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%__ln_s {_iconsdir}/hicolor/64x64/apps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/512x512/apps/xnview.png
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_iconsdir}/hicolor/512x512/apps
%__ln_s %{_iconsdir}/hicolor/512x512/apps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/xnview.png

%files
/opt/%{app_name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%{_iconsdir}/hicolor/64x64/apps/xnview.png
%{_iconsdir}/hicolor/512x512/apps/%{name}.png
%{_iconsdir}/hicolor/512x512/apps/xnview.png
%license ./license.txt
