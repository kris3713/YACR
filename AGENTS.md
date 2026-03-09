# AGENTS.md

This file provides guidance to any AI agent when working with code in this repository.

## High‑Level Structure

- `packages/` – each subdirectory contains a RPM spec file and
  an `update-script` that fetches the latest upstream version.
- `scripts/` – helper utilities:
  - `update-package-versions.sh` runs all `update-script`s.
  - `generate-pkg-list-readme` rebuilds `packages/README.md`.
  - `add-changelog-to-specs` appends `%changelog` macros to specs.
  - `parse-html`, `parse-xml`, `parse-json` – small parsers used by update‑scripts.
  - `build-to-copr` – wrapper around `copr-cli buildscm`.
  - `change-packages` – toggles webhook rebuild for COPR packages.
- CI is defined in `.github/workflows/*` and uses
  `fd`, `rg`, `sd`, `fish`, `python`, `ruff`, and `copr-cli`.
  - The CI workflows rely on **Nix** and **Pixi** to provide a reproducible
    environment for running the scripts.
  - The `.envrc` file is intended for local development only and is never
    sourced by the CI.

## Common commands

```bash
# Setup Python environment (pixi + uv)
./scripts/setup-python-env.sh

# Lint all Python scripts
ruff check ./scripts/*.py

# Run a single update script (example: cudatext)
# ./packages/<package_name>/update-script
./packages/cudatext/update-script

# Run all update scripts
./scripts/update-package-versions.sh

# Re‑generate packages README
./scripts/generate-pkg-list-readme

# Add changelog macros to all specs
./scripts/add-changelog-to-specs

# Build a package in COPR
./scripts/build-to-copr <package-name>
# or with subdir
./scripts/build-to-copr <subdir> <package-name>

# Toggle webhook rebuild
./scripts/change-packages on <subdir> <package-name>
```

## Parsing Utilities

- `scripts/parse-html <url> <regex> <xpath>` – prints captured group.
  - Unlike the other parsing scripts, this one
    explicitly requires a regex pattern to match
    the desired content.
- `scripts/parse-xml <url> <regex> <xpath>` – prints captured group or whole element.
- `scripts/parse-json <url> <regex> <jsonpath>` – prints captured value.

These are used by the `update-script`s to extract the latest version string.

## Building Packages Locally

The repo is a COPR repository; packages are built via `copr-cli`.
Ensure `copr-cli` is installed and authenticated. If it's not installed,
then suggest installing it using:
`uv tool install --no-managed-python copr-cli`.

Ensure that the user has the file `~/.config/copr` exists and follows
the example content structure below. See, <https://copr.fedorainfracloud.org/api/>

```conf
[copr-cli]
login = 123456abcdefg
username = user
token = 12345678abcdefghijk
copr_url = https://copr.fedorainfracloud.org
# expiration date: 2027-07-01
```

_This is required for `copr-cli` to work_

```bash
copr-cli buildscm \
  --clone-url 'https://github.com/kris3713/YACR.git' \
  --commit 'master' \
  --subdir "packages/<subdir>" \
  --spec "<name>.spec" \
  --enable-net 'on' \
  'zliced13/YACR'
```

Use the helper script `scripts/build-to-copr` to avoid typing the full command.

## Updating package versions

Each package’s `update-script` is a shell script that fetches the latest release
and updates the spec file. Running `scripts/update-package-versions.sh` executes
all of them. The script expects `fd`, `rg`, `sd`, and `fish` to be available.

## CI

The GitHub Actions workflows:
- `update-packages.yml` – runs `scripts/update-package-versions.sh` and pushes changes.
- `update-packages-readme_md.yml` – regenerates `packages/README.md`.
