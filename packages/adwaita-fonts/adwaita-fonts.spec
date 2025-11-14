%global         debug_package %{nil}
%global         fedora_pkgs_raw_src_url https://src.fedoraproject.org/rpms/adwaita-fonts/raw/rawhide/f
%global         major %%(echo %{version} | cut -d. -f1)

# General package information
%global         foundry adwaita-fonts
%global         fontdocs ./README.md
%global         common_description %{expand:
Adwaita Fonts contains Adwaita Sans, a variation of Inter,
and Adwaita Mono, Iosevka customized to match Inter.
}

# adwaita-sans-fonts
%global         fontfamily1 adwaita-sans-fonts
%global         fontsummary1 Adwaita Sans font family
%global         fonts1 ./sans/*.ttf
%global         fontlicenses1 ./LICENSE
%global         fontconfs1 %{SOURCE1}
%global         fontdescription1 %{expand:
%{common_description}
Adwaita Sans is a variation of the Inter font family.
}

# adwaita-mono-fonts
%global         fontfamily2 adwaita-mono-fonts
%global         fontsummary2 Adwaita Mono font family
%global         fonts2 ./mono/*.ttf
%global         fontlicenses2 ./LICENSE
%global         fontconfs2 %{SOURCE2}
%global         fontdescription2 %{expand:
%{common_description}
Adwaita Mono is a customized version of the Iosevka font, designed to match Inter.
}

Name:           adwaita-fonts
Summary:        Adwaita fonts
Version:        49.0
Release:        1%{?dist}

License:        OFL-1.1
URL:            https://gitlab.gnome.org/GNOME/adwaita-fonts

Source0:        https://download.gnome.org/sources/adwaita-fonts/%{major}/adwaita-fonts-%{version}.tar.xz
Source1:        %{fedora_pkgs_raw_src_url}/59-adwaita-sans-fonts.conf
Source2:        %{fedora_pkgs_raw_src_url}/59-adwaita-mono-fonts.conf

BuildRequires:  meson fonts-rpm-macros fonts-rpm-templates

BuildArch:      noarch

%description
%wordwrap -v common_description

%fontpkg -a
%fontmetapkg

%prep
%setup -q -n ./%{name}-%{version}

%build
%fontbuild -a

%install
%fontinstall -a

%fontfiles -a
