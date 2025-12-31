%global         __brp_check_rpaths %nil
# The reason for this is to avoid the "broken rpath" error

%global         fullname page.kramo.%{app_name}
%global         app_name Sly
%global         debug_package %nil

%define         git_url https://codeberg.org/kramo/%{app_name}

%ifarch x86_64
%global         build_target x64
%else
%global         build_target aarch64
%endif

Name:           sly
Version:        1.0.0
Release:        1%{?dist}
Summary:        A friendly image editor that requires no internet connection or preexisting expertise

License:        GPL-3.0
URL:            https://kramo.page/%{name}/

Source0:        %{git_url}/archive/v%{version}.tar.gz

# `flutter` is provided by `mise`
BuildRequires:  mise
BuildRequires:  git cmake clang ninja-build glib2-devel gtk3-devel

%ifarch %arm64
BuildRequires:  jq
%endif

# ExclusiveArch:  x86_64

%description
Sly is a friendly image editor that requires no internet connection or preexisting expertise.
Just open some photos and have at it.

The app allows you to adjust attributes like brightness or contrast as well as add effects like a
vignette or a border. It also allows you to flip, rotate and crop the image to your heart's desire.
If you're a pro, you can even preview your edits on a histogram.

When you're done, just save the photo with the quality settings of your choosing.
You also get a choice in whether or not to keep metadata such as location information.

%prep
%autosetup -n ./%{name}


%build
# Setup mise, and install flutter
export MISE_GLOBAL_CONFIG_FILE=''
export MISE_CACHE_DIR="$(realpath ./.mise_cache)"
export MISE_DATA_DIR="$(realpath ./.mise_data)"
export PUB_CACHE="$(realpath ./.pub-cache)"
mise install flutter@latest

# Modify $PATH
export PATH="$(mise where flutter@latest)/bin:$PATH"

# Build the application
unset CFLAGS CXXFLAGS
flutter --no-version-check pub get
flutter --no-version-check build linux --release -v


%install
# export QA_RPATHS=$[ 0x0002 | 0x0010 ]

# Create the new build root
install -d %{buildroot}{%{_bindir},/opt/%{app_name},%{_datadir}/applications,%{_metainfodir}}
install -d %{buildroot}%{_iconsdir}/hicolor/scalable/apps

# Copy the application files to the application directory
cp -a ./build/linux/%{build_target}/release/bundle/* %{buildroot}/opt/%{app_name}

# Create a symlink to the application binary
ln -s /opt/%{app_name}/%{name} %{buildroot}%{_bindir}

# Install the desktop file
install -Dm 0644 ./packaging/linux/%{fullname}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install the application icons
install -Dm 0644 ./packaging/linux/%{fullname}.svg -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps
install -Dm 0644 ./packaging/linux/%{fullname}-symbolic.svg -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps

# Install the application metainfo file
install -Dm 0644 ./packaging/linux/%{fullname}.metainfo.xml -t %{buildroot}%{_metainfodir}


%files
/opt/%{app_name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/scalable/apps/*
%{_metainfodir}/%{fullname}.metainfo.xml


%changelog
%autochangelog
