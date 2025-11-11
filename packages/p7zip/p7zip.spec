%global        debug_package %{nil}

Name:          p7zip
Version:       17.06
Release:       1%{?dist}
Summary:       Very high compression ratio file archiver

License:       LGPLv2 and (LGPLv2+ or CPL)
URL:           https://github.com/p7zip-project/p7zip

Source:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: gcc-c++ yasm cmake ninja-build devscripts

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with a very high
compression ratio. The original version can be found at http://www.7-zip.org/.

%package plugins
Summary: Additional plugins for p7zip
%description plugins
Additional plugins that can be used with 7z to extend its abilities.

%prep
%setup -q -n ./%{name}-%{version}

# enforce c/cxx flags and remove debug
sed -i -e 's|-I.\\|-I. \\|' -e 's|CFLAGS=-c |CFLAGS=%{build_cflags} -c |' \
  -e 's|CXXFLAGS=-c |CXXFLAGS=%{build_cxxflags} -c |' ./makefile.glb
sed -i 's| -g -| -|' ./makefile.glb

# move license files
%__mv ./DOC/License.txt DOC/copying.txt ./DOC/unRarLicense.txt .
# remove Struct.EAP from docs
%__rm ./DOC/Struct.EAP ./DOC/Struct.ldb

%build
%set_build_flags
pushd ./CPP/7zip/CMAKE/
sh ./generate.sh
popd
%__cp -f ./makefile.linux_amd64_asm ./makefile.machine

# enforce extra flags, remove debug
export OPTFLAGS=$(
  echo "%{optflags} -fPIE -fdata-sections -ffunction-sections %{build_ldflags} -Wl,-s,--gc-sections" | sed -e 's| -g | |'
)

%make_build all2 \
  OPTFLAGS="$OPTFLAGS"
  DEST_HOME=%{_prefix} \
  DEST_BIN=%{_bindir} \
  DEST_SHARE=%{_libexecdir}/p7zip \
  DEST_MAN=%{_mandir}

%install
# If this doesn't work, then manually move these files into the required directories.
%__make install \
  DEST_DIR=%{buildroot} \
  DEST_HOME=%{_prefix} \
  DEST_BIN=%{_bindir} \
  DEST_SHARE=%{_libexecdir}/p7zip \
  DEST_MAN=%{_mandir}

%__mv %{buildroot}%{_docdir}/p7zip/DOC/* %{buildroot}%{_docdir}/p7zip
rmdir %{buildroot}%{_docdir}/p7zip/DOC/

# %check
# make test
# hardening-check %{extraopts} %{buildroot}%{_libexecdir}/p7zip/{7za,7z,7zCon.sfx,Codecs/Rar.so}

%files
%{_bindir}/7za
%{_docdir}/p7zip
%exclude %{_docdir}/p7zip/MANUAL
%license ./copying.txt ./License.txt ./unRarLicense.txt
%dir %{_libexecdir}/p7zip/
%{_libexecdir}/p7zip/7za
%{_libexecdir}/p7zip/7zCon.sfx
%{_mandir}/man1/7za.1*
%exclude %{_mandir}/man1/7zr.1*

%files plugins
%{_bindir}/7z
%dir %{_libexecdir}/p7zip/
%{_libexecdir}/p7zip/7z
%{_libexecdir}/p7zip/7z.so
%{_libexecdir}/p7zip/Codecs/Rar.so
%{_mandir}/man1/7z.1*
