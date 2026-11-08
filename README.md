# Bangladesh Plastic Waste Economic Analysis

A configurable screening-level model for evaluating the material flows and financial performance of a hypothetical plastic-waste recovery or processing project. The model calculates feedstock handling, sorting rejects, saleable outputs, residual mass, annual revenues and costs, cash flows, NPV, IRR, simple payback and sensitivity.

> **Important:** all default numbers are illustrative assumptions, not verified Bangladesh market prices, measured process yields, a bankable feasibility study or an investment recommendation. Actual facilities require independent process engineering, environmental and occupational-health assessment, emissions and residue controls, permits, feedstock due diligence and buyer/offtake validation.

## Start here

Read [the beginner guide](docs/BEGINNER_GUIDE.md) before changing the financial assumptions.

### Quick start

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
pytest -q
python scripts/run_financial_model.py
python scripts/run_sensitivity.py
```

## What the model does

### 1. Material balance

Incoming feedstock is split into sorting rejects and processed feed. The processed share is allocated across configured product streams. Any remaining fraction is recorded as an unallocated process residue so the material balance closes.

A closed arithmetic balance is necessary but not sufficient. The assumed product yields still need to be validated by representative feedstock sampling, a documented process design and pilot/operational evidence.

### 2. Revenue model

The base configuration includes example product streams such as oil, char and gas-equivalent output. These are user-editable scenario variables, not typical or guaranteed process yields. Revenue is calculated from saleable mass multiplied by a user-entered selling price, plus an optional gate fee.

### 3. Operating costs

The model includes configurable feedstock purchase cost, transport, utilities, variable processing cost and fixed annual operating cost. Replace every placeholder with a dated, location-specific quote or transparent assumption.

### 4. Project cash flow

The model calculates year-zero capex and annual operating cash flows across the project life. It reports:
- **NPV:** present value of future cash flows less initial investment.
- **IRR:** discount rate at which the modelled NPV equals zero, where a meaningful solution exists.
- **Simple payback:** time until cumulative undiscounted cash flow turns positive.
- **Break-even gate fee:** fee per incoming tonne required to achieve a target financial condition under the model's assumptions.

These are screening metrics. A positive NPV alone does not demonstrate technical, environmental, social, legal or commercial feasibility.

## Bangladesh context and data sources

- **Department of Environment (DoE), Multi-sectoral Action Plan for Sustainable Plastic Management:** https://doe.gov.bd/pages/publications/multi-sectoral-action-plan-for-sustainable-plastic-management-in-bangladesh-c9f642-6922da8a81fc96cef9eb684e
- **World Bank, Meeting Bangladesh's Plastic Challenge through a Multisectoral Approach:** https://www.worldbank.org/en/news/feature/2021/12/23/meeting-bangladesh-s-plastic-challenge-through-a-multisectoral-approach
- **World Bank, Extended Producer Responsibility for Advancing Circular Economies for Plastics in Bangladesh:** https://documents.worldbank.org/curated/en/099121624201515863/pdf/P175908-d4a8d387-3aa2-45e8-899a-c0b8bfb342ad.pdf
- **MoEFCC policy and rules portal:** https://moef.gov.bd/pages/static-pages/6940329b35ce18e1c055f3d8

These are policy and sector-context sources, not plant-specific supply contracts, offtake prices, process yields or CAPEX quotations. Historical national figures should be used with their publication year and original definitions, not presented as current market data.

## How to build a credible feasibility case

1. **Feedstock audit:** identify polymer types, contamination, moisture, seasonal availability, collection radius and competing uses.
2. **Supply evidence:** validate supplier volumes and quality through site visits, sampling and written agreements.
3. **Process validation:** obtain independent engineering review and a pilot/operational mass balance.
4. **Product market:** confirm specifications and buyer acceptance with written offtake evidence.
5. **Cost evidence:** obtain dated supplier quotations for equipment, civil works, utilities, labour, transport, maintenance, insurance and residue management.
6. **Environmental and safety review:** assess emissions, wastewater, residues, fire/explosion hazards, worker exposure and permitting requirements.
7. **Financial stress test:** test downside cases for uptime, yield, price, feedstock quality, transport, energy cost, FX, inflation and capex overruns.

See [the feasibility gate checklist](docs/FEASIBILITY_GATE_CHECKLIST.md).

## Repository structure

```text
config/       editable base-case assumptions
docs/         beginner guide, data sources, assumptions and feasibility checks
notebooks/    interactive model walkthrough
scripts/      base-case and sensitivity runs
src/          reusable mass-balance and financial calculations
tests/        unit tests
outputs/      generated model results
```

## Model boundaries

The default model is simplified and does not fully model debt financing, income tax, working capital, depreciation, ramp-up, inflation/escalation, foreign exchange, detailed process energy balance, emissions, wastewater, product quality discounts, shutdowns, insurance, salvage or environmental externalities. Add the relevant components before using the model for an investment decision.

## Reproducibility

Run `pytest -q` to execute the manual tests. No GitHub Actions or CI workflow is configured.

## Licence

MIT for the code. Third-party data and source documents retain their own licences and reuse conditions.
