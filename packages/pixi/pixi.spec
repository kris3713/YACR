%global         __requires_exclude_from ^%{bash_completions_dir}/.*$
%global         __requires_exclude_from ^%{fish_completions_dir}/.*$
%global         __requires_exclude_from ^%{zsh_completions_dir}/.*$
%global         debug_package %{nil}

Name:           pixi
Version:        0.61.0
Release:        1%{?dist}
Summary:        Package management made easy.

License:        BSD-3-Clause
URL:            https://pixi.sh/

Source0:        https://github.com/prefix-dev/%{name}/releases/download/v%{version}/source.tar.gz

# BuildRequires:  pkgconfig(openssl)
BuildRequires:  cargo-rpm-macros rust cargo

%description
%{name} is a cross-platform, multi-language package manager and
workflow tool built on the foundation of the conda ecosystem.
It provides developers with an exceptional experience similar to
popular package managers like cargo or npm, but for any language.


%prep
%autosetup -n ./%{name}-%{version}


%build
# export OPENSSL_NO_VENDOR=1
export CARGO_HOME="$(realpath ./.cargo)"
export PIXI_SELF_UPDATE_DISABLED_MESSAGE="$(cat << 'EOF'
`self-update` has been disabled for this build.
Run `sudo dnf upgrade pixi` instead
EOF
)"

# cargo build --locked --profile dist --verbose "-j$(nproc)" --no-default-features --features native-tls
cargo build --locked --profile dist --verbose "-j$(nproc)"


%install
install -d %{buildroot}{%{_bindir},%{bash_completions_dir},%{fish_completions_dir},%{zsh_completions_dir}}

# Install pixi
install -Dm 0755 ./.cargo/bin/%{name} -t %{buildroot}%{_bindir}

# Install shell completions for pixi
# (No need to use chmod since the generated files
# are guaranteed to have a file mode of 0644)
./.cargo/bin/%{name} completions --shell bash > %{buildroot}%{bash_completions_dir}/%{name}
./.cargo/bin/%{name} completions --shell fish > %{buildroot}%{fish_completions_dir}/%{name}.fish
./.cargo/bin/%{name} completions --shell zsh > %{buildroot}%{zsh_completions_dir}/_%{name}


%files
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}
%license ./LICENSE
%doc ./README.md


%changelog
%autochangelog
