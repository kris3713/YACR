%global         __provides_exclude_from ^/opt/%{app_name}/.*$
%global         __requires_exclude_from ^/opt/%{app_name}/.*$
%global         app_name massCode
%global         debug_package %{nil}

Name:           masscode
Version:        3.12.1
Release:        1%{?dist}
Summary:        A free and open source code snippets manager for developers

License:        AGPL-3.0
URL:            https://masscode.io/

Source0:        https://github.com/massCodeIO/massCode/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}.desktop
Source2:        pnpm-workspace.yaml

BuildRequires:  nodejs-npm pnpm

ExclusiveArch:  x86_64

%description
A free and open source code snippets manager for developers.
It helps you create and organize your own personal
snippet collection and have quick access to it.

%prep
%setup -q -n ./%{app_name}-%{version}

%build
%__cp -a %{SOURCE2} .
pnpm install
pnpm run build

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},/opt/%{app_name},%{_datadir}/{applications,pixmaps}}
%__install -d %{buildroot}%{_iconsdir}/hicolor/256x256/apps

# Copy the application files to the application directory
%__cp -a ./dist/linux-unpacked/* %{buildroot}/opt/%{app_name}

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Create a symlink to the application binary
%__ln_s /opt/%{app_name}/%{name} %{buildroot}%{_bindir}

# Install the application icon
%__install -Dm 0644 ./config/icons/256x256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

# Install the pixmap
%__install -Dm 0644 ./config/icons/256x256.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

%files
/opt/%{app_name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%license ./LICENSE
