# Plastic Waste Economic Analysis

A financial and material-flow model for evaluating a hypothetical plastic-waste processing or recycling project. The complete project source package is provided in [source-code.zip](./source-code.zip).

## What is included

The source archive contains a Python cash-flow model, sensitivity analysis, configurable assumptions, a Jupyter walkthrough, CLI scripts, feasibility-gate checklist, data-source register and unit tests.

The model calculates feedstock and product mass balance, revenue, operating costs, capital costs, NPV, IRR, payback and break-even conditions.

## Quick start

Download and extract [source-code.zip](./source-code.zip), then run from the extracted project directory:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest -q
python scripts/run_financial_model.py
python scripts/run_sensitivity.py
```

## Data and investment assumptions

The bundled base case uses illustrative assumptions, not verified Bangladesh market quotations, actual plant performance or an investment recommendation. Replace feedstock prices, process yields, capex, opex, product prices, utilities, logistics, financing and regulatory requirements with sourced, dated inputs. Test downside scenarios before making feasibility claims.

**No GitHub Actions or CI workflow is included, as requested.** Local tests are retained for manual verification.

[Download complete source package](./source-code.zip)
