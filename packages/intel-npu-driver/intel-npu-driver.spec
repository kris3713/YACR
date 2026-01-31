# Imported from https://src.fedoraproject.org/rpms/intel-npu-driver/blob/rawhide/f/intel-npu-driver.spec
%global         repo_name linux-npu-driver
%global         debug_package %nil
%global         desc %{expand: \
Intel NPU device is an AI inference accelerator integrated with Intel client
CPUs, starting from Intel Core Ultra generation of CPUs (formerly known as
Meteor Lake). It enables energy-efficient execution of artificial neural
network tasks.}

Name:           intel-npu-driver
Version:        1.28.0
Release:        1%{?dist}
Summary:        Intel Neural Processing Unit Driver

License:        MIT AND Apache-2.0
URL:            https://github.com/intel/%{repo_name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0:         https://src.fedoraproject.org/rpms/%{name}/raw/rawhide/f/npu-driver-fedora.patch

ExclusiveArch:  x86_64

BuildRequires:  git cmake gcc gcc-c++ glibc-devel gmock-devel
BuildRequires:  gtest-devel libudev-devel oneapi-level-zero-devel
BuildRequires:  openssl-devel yaml-cpp-devel
# openvino-npu_plugin_elf
Provides: bundled(openvino-npu_plugin_elf)
# level-zero-npu-extensions
Provides: bundled(level-zero-npu-extensions)
Requires: oneapi-level-zero


%description
%{desc}


%package test
Summary:  Test files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description test
The %{name}-test package contains kernel-mode (kmd) and user-mode (umd)
parts of the %{name}.


%prep
%autosetup -N -n ./%{repo_name}-%{version}
# thirdparty deps (requires git)
git init -q
git remote add origin %{url}.git
git fetch --tags --recurse-submodules -q
git checkout -fb 'v%{version}' 'v%{version}'
git submodule update --init --recursive
%autopatch -p1


%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DUSE_SYSTEM_LIBRARIES=ON \
  -DENABLE_NPU_COMPILER_BUILD=OFF
%cmake_build


%install
%cmake_install
# remove the unversioned so file
rm -vf %{buildroot}%{_libdir}/libze_intel_npu.so


%files
%license LICENSE.md
%doc README.md
%{_libdir}/libze_intel_npu.so.1
%{_libdir}/libze_intel_npu.so.%{version}


%files test
%{_bindir}/npu-kmd-test
%{_bindir}/npu-umd-test


%changelog
%autochangelog
