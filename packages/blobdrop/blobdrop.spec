%global         __requires_exclude_from ^%{bash_completions_dir}/.*$
%global         __requires_exclude_from ^%{fish_completions_dir}/.*$
%global         __requires_exclude_from ^%{zsh_completions_dir}/.*$
%global         debug_package %nil

Name:           blobdrop
Version:        2.1
Release:        1%{?dist}
Summary:        Drag and drop files directly out of the terminal

License:        GPL-3.0
URL:            https://github.com/vimpostor/%{name}

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}.desktop

BuildRequires:  cmake-rpm-macros cmake clang
BuildRequires:  qt6-qttools-devel qt-devel qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel xcb-util-wm-devel

%description
Drag and drop files directly out of the terminal.

* Start drag automatically without a GUI
* Hide the parent terminal emulator while dragging
* Automatically quit once all paths have been dragged
* Auto-hide the GUI while dragging
* Show mime icons and thumbnails for media
* Drag all files at once
* Preview files with a single click
* Shell completions
* Act as a sink and print dropped files to the terminal
* Pipe filenames asynchronously into stdin


%package bash-completion
Summary:        Bash completion for %{name}
Requires:       %{name}
%description bash-completion
Bash completion for %{name}


%package fish-completion
Summary:        Fish completion for %{name} (NOTE: FISH is not included in this package)
Requires:       %{name}
%description fish-completion
Fish completion for %{name}


%package zsh-completion
Summary:        Zsh completion for %{name} (NOTE: ZSH is not included in this package)
Requires:       %{name}
%description zsh-completion
Zsh completion for %{name}


%prep
%setup -q -n ./%{name}-%{version}


%build
# Remove unneeded build flags from C flags (clang doesn't need them)
export CFLAGS="$(
  echo '%{build_cflags}' |
  sed -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-hardened-cc1;;' \
    -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1;;'
)"
# Remove unneeded build flags from CXX flags (clang doesn't need them)
export CXXFLAGS="$(
  echo '%{build_cxxflags}' |
  sed -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-hardened-cc1;;' \
    -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1;;'
)"
# Remove unneeded build flags from LD flags (clang doesn't need them)
export LDFLAGS="$(
  echo '%{build_ldflags}' |
  sed -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-hardened-ld;;' \
    -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-hardened-ld-errors;;' \
    -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1;;' \
    -e 's;-specs=\/usr\/lib\/rpm\/redhat\/redhat-package-notes;;'
)"

# Force cmake to use clang
export CC='clang' CXX='clang++'

# Force cmake to install to /usr instead of /usr/local
cmake -DCMAKE_INSTALL_PREFIX=/usr -B ./redhat-linux-build
%cmake_build


%install
# Create important directories in the buildroot
install -d %{buildroot}{%{_bindir},%{_datadir}/applications,%{_mandir}/man1}
install -d %{buildroot}%{_iconsdir}/hicolor/scalable/apps
install -d %{buildroot}{%{bash_completions_dir},%{fish_completions_dir},%{zsh_completions_dir}}

# Use cmake to install everything else
%cmake_install

# Install the desktop file
install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application icon
install -Dm 0644 ./assets/%{name}.svg \
  -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_mandir}/*
%license ./LICENSE.txt


%files bash-completion
%{bash_completions_dir}/%{name}


%files fish-completion
%{fish_completions_dir}/%{name}.fish


%files zsh-completion
%{zsh_completions_dir}/_%{name}


%changelog
%autochangelog
