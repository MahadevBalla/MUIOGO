# MUIOGO

MUIOGO is the integration project for combining MUIO with OG workflows.

At the moment, this repository starts from a direct copy baseline of MUIO. The
goal of MUIOGO is to evolve that baseline into an integrated, maintainable, and
platform-independent project.

If you are new to this repo, start with the current installation notes below.

## Current installation status

### Windows (MUIO `.exe`, current stable path)

MUIO is currently distributed primarily as a Windows desktop installer.

1. Download the latest `.exe` installer from:
   `https://forms.office.com/Pages/ResponsePage.aspx?id=wE8mz7iun0SQVILORFQISwwn5YyR7ONHs-3JdG3f5AFUODlJOEQwWTBXMlRRNFUwNEpUTUZYQ1RXOS4u`
2. Move the `.exe` file to a folder where you have administrator permissions.
3. Right-click `MUIO.exe` and select **Run as administrator**.
4. Wait for installation to complete.
5. Open the app from the Start Menu if it does not open automatically.

### macOS (current available path)

Use `MUIO-Mac` as the current macOS-capable path:

- `https://github.com/SeaCelo/MUIO-Mac`

### Platform-independence goal

One of the core goals of MUIOGO is to become platform independent so separate
platform-specific ports are no longer required.

## What is in this repository

- `API/`: Flask backend and run/data endpoints
- `WebAPP/`: frontend assets served by Flask
- `WebAPP/DataStorage/`: model inputs, case data, and run outputs
- `docs/`: user and model documentation sources

## For new contributors

Start here:

- `CONTRIBUTING.md`
- `docs/GSoC-2026.md`
- `docs/ARCHITECTURE.md`
- `docs/DOCS_POLICY.md`

Issue and PR templates:

- `.github/ISSUE_TEMPLATE/`
- `.github/pull_request_template.md`

Contribution rule:

- Create (or use) an issue first.
- Implement in a feature branch (for example:
  `feature/<issue-number>-short-description`).

## Important project boundaries

This repository is downstream and separately managed from upstream `OSeMOSYS/MUIO`.

- Upstream: `https://github.com/OSeMOSYS/MUIO`
- This repo: `https://github.com/EAPD-DRB/MUIOGO`

Contributions upstream are welcome, but delivery in MUIOGO cannot depend on
upstream timelines or releases.

`MUIO-Mac` is a separate macOS port effort and can continue in parallel, but
MUIOGO should not depend on it for delivery decisions.

## Wiki usage

The wiki is used only for high-level background context:

- [Project Background and Vision](https://github.com/EAPD-DRB/MUIOGO/wiki/Project-Background-and-Vision)

Setup, architecture, contribution process, and governance docs are maintained in
this repository.

## License

Apache License 2.0 (`LICENSE`).
