# MUIOGO

<img src="assets/UN_Crest.png" width="75" align="left">

**M**odelling **U**ser **I**nterface for **OG**-Core and **O**SeMOSYS

MUIOGO is the integration project for OG-Core and OSeMOSYS/CLEWS.
This repository currently starts from a MUIO baseline and is being evolved into
a maintainable, cross-platform integration workflow.

For project context, see:
- [Project Background and Vision](https://github.com/EAPD-DRB/MUIOGO/wiki/Project-Background-and-Vision)
- [Timeline](https://github.com/EAPD-DRB/MUIOGO/wiki/Timeline)

## Quick Start (All Platforms)

### 1) Setup environment, dependencies, and solvers

```bash
# macOS / Linux
./scripts/setup.sh --with-demo-data

# Windows
scripts\setup.bat --with-demo-data
```

Alternative (direct Python entrypoint):

```bash
# macOS / Linux
python3.11 scripts/setup_dev.py --with-demo-data

# Windows (PowerShell / CMD)
py -3.11 scripts/setup_dev.py --with-demo-data
```

### 2) Verify setup

```bash
# macOS / Linux
python3.11 scripts/setup_dev.py --check --with-demo-data

# Windows
py -3.11 scripts/setup_dev.py --check --with-demo-data
```

### 3) Start the app

```bash
# macOS / Linux
"$HOME/.venvs/muiogo/bin/python" API/app.py

# Windows (PowerShell)
# "$env:USERPROFILE\.venvs\muiogo\Scripts\python.exe" API\app.py
```

Open: `http://127.0.0.1:5002`

## Demo Data

Demo data archive in this repo:

- `assets/demo-data/CLEWs.Demo.zip`
- `SHA-256: facf4bda703f67b3c8b8697fea19d7d49be72bc2029fc05a68c61fd12ba7edde`

Setup defaults:
- Creates virtual environment at `~/.venvs/muiogo` (unless overridden).
- Can install demo data with `--with-demo-data`.
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
