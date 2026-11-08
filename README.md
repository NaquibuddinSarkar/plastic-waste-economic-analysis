# Plastic Waste Economic Analysis

A simplified material-flow and project-finance model for evaluating a hypothetical plastic-waste recycling or processing facility.

## Project contents

- `src/plastic_waste_economics/model.py`: mass balance, annual cash flows, NPV, IRR and simple payback.
- `scripts/run_financial_model.py`: runs the illustrative base case.
- `scripts/run_sensitivity.py`: checks one-factor sensitivity to recovery yield.
- `config/base_case.json`: editable operational and financial assumptions.
- `notebooks/01_plastic_waste_financial_model.ipynb`: interactive model walkthrough.
- `docs/`: model assumptions, data sources and feasibility-gate checklist.
- `tests/`: manual tests for mass balance and financial calculations.

## Quick start

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

## Model boundaries

The model is a simplified unlevered cash-flow case. It does not fully model working capital, debt financing, inflation/escalation, polymer-specific contamination, detailed utilities, downtime, product quality premiums, permitting, environmental liability or terminal value. Extend these items before using the model for a feasibility decision.

## Data and investment assumptions

The included assumptions are illustrative, not verified Bangladesh market quotations, measured plant performance or an investment recommendation. Replace feedstock prices, process yields, capex, opex, product prices, utility rates, logistics and regulatory costs with sourced and dated values. Secure feedstock and offtake evidence and complete the feasibility checklist before making investment claims.

No GitHub Actions or CI workflow is configured. Tests are available for manual local execution.

## Licence

MIT. See [LICENSE](LICENSE).
