%global srcname altgraph

Name:      python-%{srcname}
Version:   0.17.5
Release:   1%{?dist}
Summary:   Python graph (network) package
License:   MIT
BuildArch: noarch
URL:       https://github.com/ronaldoussoren/%{srcname}

Source0:   https://github.com/ronaldoussoren/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
altgraph is a fork of graphlib: a graph (network) package for constructing
graphs, BFS, and DFS traversals, topological sort, shortest paths, etc. with
graphviz output.

%package -n python3-%{srcname}
Summary:    %{summary}
Requires:   graphviz

%description -n python3-%{srcname}
altgraph is a fork of graphlib: a graph (network) package for constructing
graphs, BFS, and DFS traversals, topological sort, shortest paths, etc. with
graphviz output.

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%license LICENSE

%changelog
%autochangelog
