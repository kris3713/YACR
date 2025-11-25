%global         __brp_check_rpaths %{nil}
# The reason for this is to avoid the "broken rpath" error

%define         git_url https://codeberg.org/kramo/Sly

%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         fullname page.kramo.Sly
%global         app_name Sly
%global         debug_package %{nil}

Name:           sly
Version:        1.0.0
Release:        1%{?dist}
Summary:        A friendly image editor that requires no internet connection or preexisting expertise

License:        GPL-3.0
URL:            https://kramo.page/sly/

Source0:        %{git_url}/releases/download/v%{version}/Sly-%{version}-Linux.tar.gz
Source1:        %{git_url}/raw/tag/v%{version}/packaging/linux/%{fullname}.desktop
Source2:        %{git_url}/raw/tag/v%{version}/packaging/linux/%{fullname}.svg
Source3:        %{git_url}/raw/tag/v%{version}/packaging/linux/%{fullname}-symbolic.svg
Source4:        %{git_url}/raw/tag/v%{version}/packaging/linux/%{fullname}.metainfo.xml

ExclusiveArch:  x86_64

%description
Sly is a friendly image editor that requires no internet connection or preexisting expertise.
Just open some photos and have at it.

The app allows you to adjust attributes like brightness or contrast as well as add effects like a
vignette or a border. It also allows you to flip, rotate and crop the image to your heart's desire.
If you're a pro, you can even preview your edits on a histogram.

When you're done, just save the photo with the quality settings of your choosing.
You also get a choice in whether or not to keep metadata such as location information.

%prep
%setup -q -c -n ./%{name}-%{version}

%install
export QA_RPATHS=$[ 0x0002 | 0x0010 ]
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},/opt/%{app_name},%{_datadir}/applications,%{_metainfodir}}
%__install -d %{buildroot}%{_iconsdir}/hicolor/scalable/apps

# Copy the application files to the application directory
%__cp -a . %{buildroot}/opt/%{app_name}

# Create a symlink to the application binary
%__ln_s /opt/%{app_name}/%{name} %{buildroot}%{_bindir}

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application icons
%__install -Dm 0644 %{SOURCE2} -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps
%__install -Dm 0644 %{SOURCE3} -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps

# Install the application metainfo file
%__install -Dm 0644 %{SOURCE4} -t %{buildroot}%{_metainfodir}

%files
/opt/%{app_name}
%{_bindir}/%{name}
%{_datadir}/applications/%{fullname}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{fullname}.svg
%{_iconsdir}/hicolor/scalable/apps/%{fullname}-symbolic.svg
%{_metainfodir}/%{fullname}.metainfo.xml

%changelog
%autochangelog
