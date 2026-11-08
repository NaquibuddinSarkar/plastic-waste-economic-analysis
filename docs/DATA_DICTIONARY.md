# Data Dictionary and Financial Assumptions

## Base case configuration

File: `config/base_case.json`

| Parameter | Unit | Meaning | Evidence needed |
|---|---|---|---|
| feedstock_tonnes_per_year | tonnes/year | Annual feedstock entering facility at nominal utilisation | Supplier contracts and representative waste audit |
| recovery_yield | fraction | Share of feed converted to saleable product in the simplified model | Pilot/plant mass balance and product QA |
| product_price_per_tonne | currency/tonne | Selling price of saleable product | Written buyer/offtake quotations and quality grade |
| gate_fee_per_tonne | currency/tonne | Fee received for accepting incoming waste | Contract evidence; may be zero or negative |
| variable_opex_per_tonne | currency/tonne | Throughput-related processing cost | Utility/consumables/transport estimates |
| fixed_opex_per_year | currency/year | Annual fixed operating cost | Staffing, insurance, rent, overhead, service contracts |
| capex | currency | Initial project investment | Vendor quotes, civil works, installation, taxes, contingency |
| project_years | years | Modelled operating life | Asset-life and concession assumptions |
| discount_rate | fraction/year | Discount rate for NPV | Financing/investor risk basis |
| annual_capacity_utilisation | fraction | Average utilisation against nameplate input capacity | Ramp-up/availability evidence |
| tax_rate | fraction | Simplified tax rate applied to positive EBIT | Tax advice for project structure/jurisdiction |
| annual_maintenance_capex | currency/year | Annual maintenance investment | Engineering maintenance plan |

## Output definitions

- `mass_balance`: feedstock, saleable product and residue tonnes.
- `annual_revenue`: product plus gate-fee revenue.
- `annual_variable_opex` and `annual_fixed_opex`: simplified operating cost categories.
- `annual_depreciation`: straight-line depreciation for the simplified tax proxy.
- `annual_tax`: simplified tax on positive EBIT.
- `cash_flows`: year 0 capex followed by annual operating cash flow less maintenance capex.

## Important unit and modelling notes

Use one currency consistently and label whether it is BDT, USD or another currency. Do not mix nominal and real prices without modelling inflation consistently. Keep incoming feedstock tonnes distinct from processed tonnes and saleable product tonnes.

The model's mass-balance residue is an arithmetic remainder. It does not describe the actual physical form, composition, safety or disposal route of the residual stream. Add explicit streams for moisture loss, rejects, wastewater, emissions and process residues where the chosen technology requires them.
