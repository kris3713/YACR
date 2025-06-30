%global         __brp_check_rpaths %{nil}
# The reason for this is to avoid the "broken rpath" error
%global         __requires_exclude_from ^%{bash_completions_dir}/.*$
%global         __requires_exclude_from ^%{fish_completions_dir}/.*$
%global         __requires_exclude_from ^%{zsh_completions_dir}/.*$
%global         debug_package %{nil}

Name:           blobdrop
Version:        2.1
Release:        1%{?dist}
Summary:        Drag and drop files directly out of the terminal

License:        GPL-3.0
URL:            https://github.com/vimpostor/blobdrop

Source0:        %{url}/archive/refs/tags/v2.1.tar.gz
Source1:        %{name}.desktop

BuildRequires:  qt6-qttools-devel qt-devel qt6-qtdeclarative-devel qt6-qtsvg-devel xcb-util-wm-devel
# Requires:       qt6-qttools qt6-qtsvg

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
%__mkdir build
%__cmake -B ./build
%__cmake --build ./build

%install
export QA_RPATHS=$[ 0x0002 | 0x0010 ]
# Remove the old build root
%__rm -rf %{buildroot}

# Create a new build root
%__install -d %{buildroot}{%{_bindir},%{_datadir}/applications,%{_iconsdir}/hicolor/scalable/apps}
%__install -d %{buildroot}{%{bash_completions_dir},%{fish_completions_dir},%{zsh_completions_dir}}

# Install the application binary
%__install -Dm 0755 ./build/%{name} -t %{buildroot}%{_bindir}

# Install the desktop file
%__install -Dm 0644 %{SOURCE1} -t %{buildroot}%{_datadir}/applications

# Install the application icon
%__install -Dm 0644 ./assets/%{name}.svg -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps

# Install the completions for bash, fish and zsh
%__install -Dm 0644 ./assets/completions/bash-completion/completions/%{name} %{buildroot}%{bash_completions_dir}/%{name}.bash
%__install -Dm 0644 ./assets/completions/fish/vendor_completions.d/%{name}.fish -t %{buildroot}%{fish_completions_dir}
%__install -Dm 0644 ./assets/completions/zsh/site-functions/_%{name} -t %{buildroot}%{zsh_completions_dir}

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%license ./LICENSE.txt

%files bash-completion
%{bash_completions_dir}/%{name}.bash

%files fish-completion
%{fish_completions_dir}/%{name}.fish

%files zsh-completion
%{zsh_completions_dir}/_%{name}
