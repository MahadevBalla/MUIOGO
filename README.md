# MUIOGO 

**M**odelling **U**ser **I**nterface for **OG**-Core and **O**SeMOSYS.

<img src="assets/UN_Crest.png" width="110" align="left" style="margin-right:5px;"> The United Nations Department of Economic and Social Affairs (DESA) has applied open-source modelling tools in more than 20 countries —particularly in Small Island Developing States, Land-Locked Countries, and Least Developed Countries— to support policies related to Nationally Determined Contributions (NDCs), climate adaptation, social protection, and fiscal sustainability:
- CLEWS, built on OSeMOSYS, analyzes interactions and trade-offs across land, energy, and water systems under climate scenarios.
- OG-Core is a dynamic overlapping-generations macroeconomic model that evaluates long-term fiscal, demographic, and economic policies.

By linking sectoral resource systems (climate, land, energy, and water) with a dynamic macroeconomic model, the unified framework will allow policymakers to assess both the physical feasibility and economy-wide impacts of climate and development policies in a transparent, reproducible, and low-cost way.

The project will create a standardized interface and shared execution system linking the two models, enabling integrated analyses that are not currently possible. The enhanced OG–CLEWS framework will be deployed in more than 10 countries, supporting evidence-based policymaking and helping countries advance toward their Sustainable Development Goals through 2030.

See the [Project Background & Vision](https://github.com/EAPD-DRB/MUIOGO/wiki/Project-Background-and-Vision)

## What this repo contains

- `API/`: Flask backend and run/data endpoints
- `WebAPP/`: frontend UI (served by Flask)
- `WebAPP/DataStorage/`: model inputs, cases, and run outputs
- `docs/`: Sphinx documentation source

## Quick start (local)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python API/app.py
```

Open: `http://127.0.0.1:5002`

## Notes

- The frontend currently calls the local API at `http://127.0.0.1:5002/` from `WebAPP/Classes/Base.Class.js`.
- Model execution uses GLPK and CBC via backend subprocess calls.
- If your environment cannot read UTF-16 requirement files, convert with `iconv` first.

## Documentation

- Project docs source: `docs/source/`
- ReadTheDocs config: `.readthedocs.yml`

## License

Apache License 2.0 (`LICENSE`).
