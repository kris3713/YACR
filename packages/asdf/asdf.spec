%global         __requires_exclude_from ^%{bash_completions_dir}/.*$
%global         __requires_exclude_from ^%{fish_completions_dir}/.*$
%global         __requires_exclude_from ^%{zsh_completions_dir}/.*$
%global         debug_package %{nil}

Name:           asdf
Version:        0.18.0
Release:        1%{?dist}
Summary:        Extendable version manager with support for Ruby, Node.js, Elixir, Erlang & more

License:        MIT
URL:            https://asdf-vm.com/

Source0:        https://github.com/asdf-vm/asdf/archive/refs/tags/v0.18.0.tar.gz

BuildRequires:  golang
Requires:       bash git

%description
asdf is a CLI tool that can manage multiple language runtime versions on a per-project basis.
It is like gvm, nvm, rbenv & pyenv (and more) all in one! Simply install your language's plugin!

%package bash-completion
Summary:        Bash completion for asdf
Requires:       asdf
%description bash-completion
Bash completion for asdf

%package fish-completion
Summary:        Fish completion for asdf (NOTE: FISH is not included in this package)
Requires:       asdf
%description fish-completion
Fish completion for asdf

%package zsh-completion
Summary:        Zsh completion for asdf (NOTE: ZSH is not included in this package)
Requires:       asdf
%description zsh-completion
Zsh completion for asdf

%prep
%setup -q -n ./%{name}-%{version}

%build
%__make

%install
# Remove the old build root
%__rm -rf %{buildroot}

# Install the new build root
%__install -d %{buildroot}{%{_bindir},%{bash_completions_dir},%{fish_completions_dir},%{zsh_completions_dir}}

# Install the application binary
%__install -Dm 0755 ./asdf -t %{buildroot}%{_bindir}

# Install the completions for bash, fish and zsh
%__install -Dm 0644 ./internal/completions/asdf.bash -t %{buildroot}%{bash_completions_dir}
%__install -Dm 0644 ./internal/completions/asdf.fish -t %{buildroot}%{fish_completions_dir}
%__install -Dm 0644 ./internal/completions/asdf.zsh %{buildroot}%{zsh_completions_dir}/_asdf

%files
%{_bindir}/asdf
%license ./LICENSE

%files bash-completion
%{bash_completions_dir}/asdf.bash

%files fish-completion
%{fish_completions_dir}/asdf.fish

%files zsh-completion
%{zsh_completions_dir}/_asdf
