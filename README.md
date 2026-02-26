# MUIOGO

<img src="assets/UN_Crest.png" width="75" align="left">

**M**odelling **U**ser **I**nterface for **OG**-Core and **O**SeMOSYS

MUIOGO is the integration project for OG-Core and OSeMOSYS/CLEWS.
This repository currently starts from a MUIO baseline and is being evolved into
a maintainable, cross-platform integration workflow.

For project context, see:
- [Project Background and Vision](https://github.com/EAPD-DRB/MUIOGO/wiki/Project-Background-and-Vision)
- [Timeline](https://github.com/EAPD-DRB/MUIOGO/wiki/Timeline)

## Quick Start (macOS / Linux)

### 1) Leave any active conda environment

```bash
conda deactivate
```

If your prompt still shows `(base)` or another conda env, run `conda deactivate` again.

### 2) Ensure Python 3.11 is installed

```bash
python3.11 --version
```

If missing on macOS:

```bash
brew install python@3.11
```

### 3) Run setup (venv + dependencies + solvers + demo data)

```bash
./scripts/setup.sh
```

Optional: skip demo data

```bash
./scripts/setup.sh --no-demo-data
```

### 4) Start the app (browser opens automatically)

```bash
./scripts/start.sh
```

### 5) Optional verification check

```bash
./scripts/setup.sh --check
```

## Quick Start (Windows)

```bat
scripts\setup.bat
scripts\start.bat
```

Optional: skip demo data

```bat
scripts\setup.bat --no-demo-data
```

## Demo Data

Demo data archive in this repo:

- `assets/demo-data/CLEWs.Demo.zip`
- `SHA-256: facf4bda703f67b3c8b8697fea19d7d49be72bc2029fc05a68c61fd12ba7edde`

Setup defaults:
- Creates virtual environment at `~/.venvs/muiogo` (unless overridden).
- Installs demo data by default.
- Supports demo-data opt-out with `--no-demo-data`.
- Supports forced demo-data reinstall with `--force-demo-data --yes`.

## Repository Layout

- `API/`: Flask backend and run/data endpoints
- `WebAPP/`: frontend assets served by Flask
- `WebAPP/DataStorage/`: model inputs, case data, and run outputs
- `docs/`: project and contributor documentation

## Contributing

Start with:
- `CONTRIBUTING.md`
- `docs/GSoC-2026.md`
- `docs/ARCHITECTURE.md`
- `docs/DOCS_POLICY.md`

Contribution rule:
- Create (or use) an issue first.
- Work in a feature branch (for example `feature/<issue-number>-short-description`).

Templates:
- `.github/ISSUE_TEMPLATE/`
- `.github/pull_request_template.md`

## Project Boundaries

This repository is downstream and separately managed from upstream:

- Upstream: `https://github.com/OSeMOSYS/MUIO`
- This repo: `https://github.com/EAPD-DRB/MUIOGO`

Delivery in MUIOGO cannot depend on upstream timelines or release cycles.

## License

Apache License 2.0 (`LICENSE`).
