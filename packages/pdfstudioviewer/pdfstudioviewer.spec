%define         code echo %{version} | cut -d. -f1

%global         __provides_exclude_from ^/opt/%{fullname}/.*$
%global         __requires_exclude_from ^/opt/%{fullname}/.*$
%global         __spec_install_post %{nil}
%global         __os_install_post %{_dbpath}/brp-compress
%global         year %%(%{code})
%global         underscore_version %%(echo %{version} | tr '.' '_')
%global         fullname %{name}%%(%{code})
%global         debug_package %{nil}

Name:           pdfstudioviewer
Version:        2024.0.1
Release:        1%{?dist}
Summary:        Create, Review and Edit PDF Documents

License:        Freeware (https://www.qoppa.com/pdfstudio/buy/eula/)
URL:            https://www.qoppa.com/pdfstudioviewer/

Source0:        https://download.qoppa.com/pdfstudioviewer/v%{year}/PDFStudioViewer_v%{underscore_version}_linux64.deb
Source1:        %{name}.desktop
Source2:        %{name}

BuildRequires:  dpkg

ExclusiveArch:  x86_64

# Taken from the website
%description
PDF Studio Viewer™ is a cross-platform PDF reader that is reliable and easy to use.
PDF Studio Viewer can annotate PDF documents and fill interactive forms.
For more editing features, Qoppa Software publishes PDF Studio Standard and Pro editions.

%prep
dpkg -x %{SOURCE0} .

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Create the new build root
%__install -d %{buildroot}{%{_bindir},/opt,%{_datadir}/applications}
%__install -d %{buildroot}%{_iconsdir}/hicolor/128x128/apps

# Copy the application files to the application directory
%__cp -a ./opt/%{fullname} %{buildroot}/opt

# Install the shell script wrapper for the application binary
%__install -Dm 0755 %{SOURCE2} -t %{buildroot}%{_bindir}
%__sed -i -e 's/%{name}/%{fullname}/g' %{buildroot}%{_bindir}/%{name}

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application icon
%__install -Dm 0644 ./opt/%{fullname}/.install4j/%{fullname}.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

%files
%{_bindir}/%{name}
/opt/%{fullname}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/128x128/apps/%{name}.png

%changelog
%autochangelog
