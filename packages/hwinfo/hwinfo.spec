# Imported from: https://src.fedoraproject.org/rpms/hwinfo/blob/rawhide/f/hwinfo.spec
%global         debug_package %nil

# el6 compatibility
%{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro}

%global         make_flags \\\
        LDFLAGS="%{__global_ldflags} -Lsrc" \\\
        LIBDIR=%{_libdir} \\\
        HWINFO_VERSION=%{version}

Name:           hwinfo
Version:        25.2
Release:        1%{?dist}
Summary:        Hardware information tool

License:        GPL-1.0-or-later
URL:            https://github.com/openSUSE/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  libx86emu-devel libuuid-devel gcc
BuildRequires:  flex perl-interpreter make
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes:      %{name} < 22.2-1

%description
%name is to probe for the hardware present in the system. It can be used to
generate a system overview log which can be later used for support.


%package libs
Summary:        Libraries for %{name}
Obsoletes:      %{name} < 22.2-1
%description libs
Libraries for using %{name}, a hardware information tool, in other applica%{name}


%package devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
Header files and libraries for developing with libhd library from %{name}, a
hardware information tool.


%prep
%autosetup


%build
# Parallel make disabled due to missing libhd.a dependency
make %{make_flags}


%install
%make_install %{make_flags}

%ldconfig_scriptlets libs

%if "%{_sbindir}" == "%{_bindir}"
# Makefile hardcodes sbin paths. Fix the install locations here.
mv %{buildroot}/usr/sbin  %{buildroot}%{_sbindir}
%endif


%files
%{_sbindir}/check_hd
%{_sbindir}/convert_hd
%{_sbindir}/getsysinfo
%{_sbindir}/%{name}
%{_sbindir}/mk_isdnhwdb
%{_datadir}/%{name}
%doc ./*.md ./MAINTAINER
%license ./COPYING


%files libs
%{_libdir}/libhd.so.*


%files devel
%{_includedir}/hd.h
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/libhd.so


%changelog
%autochangelog
