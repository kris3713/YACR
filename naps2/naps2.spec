%define         n2 dotnet run --project NAPS2.Tools --

%global         full_name naps2
%global         app_name NAPS2
%global         debug_package %{nil}

Name:           naps2
Version:        8.1.4
Release:        1%{?dist}
Summary:        Scan documents to PDF and more, as simply as possible.

License:        GPL-2.0-or-later
URL:            https://www.naps2.com/

Source0:        https://github.com/cyanfish/naps2/archive/refs/tags/v8.1.4.tar.gz

BuildRequires:  dotnet-sdk-9.0 liberation-fonts-all google-noto-fonts-common google-noto-sans-cjk-vf-fonts
Requires:       dotnet-host dotnet-runtime-9.0

%description
NAPS2 allows you to scan from USB (using SANE) and network scanners. Use your chosen settings, or
set up multiple profiles for different devices and configurations. Once you've finished scanning, you can
save, email, or print with only a couple clicks. Save to PDF, TIFF, JPEG, PNG, or other file types.

Easily rotate, crop, and rearrange scanned pages. Adjust brightness, contrast, and apply automatic document
corrections to make your scanned pages look great. Use OCR to add searchable text to your PDFs in any of
over 100 languages. Use batch scanning, advanced profile settings, and an optional CLI to automate tedious
tasks.

%prep
%setup -q -n ./%{full_name}-%{version}

%build
dotnet restore ./NAPS2.Tools/NAPS2.Tools.csproj
%{n2} build debug && %{n2} build release
%{n2} clean
# The echo commands are here for better looking log output
echo '----------------------------------'
%ifarch x86_64
dotnet publish NAPS2.App.Gtk -c Release -r linux-x64 --self-contained '-p:DebugType=None' '-p:DebugSymbols=false'
echo '----------------------------------'
%else
dotnet publish NAPS2.App.Gtk -c Release -r linux-arm64 --self-contained '-p:DebugType=None' '-p:DebugSymbols=false'
echo '----------------------------------'
%endif


%install
%make_install


%files
/opt/%{app_name}
%{_bindir}/naps2
%{_datadir}/applications/naps2.desktop
%{_datadir}/icons/hicolor/128x128/apps/com.naps2.Naps2.png
%{_datadir}/metainfo/com.naps2.Naps2.metainfo.xml
