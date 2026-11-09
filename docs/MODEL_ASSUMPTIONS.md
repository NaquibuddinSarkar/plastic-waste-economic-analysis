# Model assumptions and boundaries

This model is a screening-level financial calculation built around one aggregate saleable product stream. It is not a technology-specific process simulator.

## Material balance

Incoming feedstock is split into:
- recovered stream = feedstock × recovery_yield;
- saleable product = recovered stream × saleable_fraction;
- recovery rejects = feedstock − recovered stream;
- product specification rejects = recovered stream − saleable product;
- grouped residue = both reject streams combined.

The arithmetic mass balance closes by construction. A real process model must separately track material, water, emissions, wastewater and named residue streams as appropriate to the selected technology.

## Revenue

- product revenue = saleable product tonnes × selling price per tonne;
- gate fee revenue = incoming feedstock tonnes × gate fee per tonne.

The model allows a non-negative gate fee. It does not establish whether a fee is contractually or legally collectible.

## Operating costs and cash flow

Variable OPEX is applied per incoming tonne. Fixed OPEX is charged each operating year, including ramp-up years. The ramp-up factor increases linearly over the configured number of years.

The model uses straight-line depreciation of initial CAPEX over the project life for a simplified tax proxy. Tax is calculated on positive EBIT only; tax-loss carry-forward, debt and financing costs are excluded. Annual maintenance CAPEX, year-specific replacement costs and terminal salvage value are entered separately.

## Currency and discount rate

All currency inputs must use one currency and one price-year convention. If the model is in nominal terms, include escalation/inflation assumptions and use a nominal discount rate. If the model is in real terms, use real values and a real discount rate.

## Metrics

- NPV discounts the full cash-flow vector, with year zero at index zero.
- IRR is reported only when a unique bracketed root is found across the search range; non-conventional cash flows can have multiple IRRs.
- Simple payback is undiscounted and interpolated within the year when cumulative cash flow turns positive.
- Break-even gate fee solves for the lowest non-negative gate fee that makes modelled NPV reach zero under the same tax, ramp-up and replacement assumptions.

## Not modelled by default

Debt/equity, working capital, VAT and detailed tax rules, price escalation, foreign exchange, ramp-up of fixed OPEX, separate multi-product revenues, process energy balance, carbon credits, emissions externalities, detailed environmental compliance and decommissioning obligations. Add only with documented inputs and a transparent methodology.
