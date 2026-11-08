"""Plastic-waste material balance and project cash-flow screening model.

This model is a financial calculation scaffold, not a process-design model.
All yields, prices and costs must be supported by evidence before a feasibility
assessment. A closed arithmetic mass balance does not prove physical viability.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


def _finite_nonnegative(name, value):
    if not np.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return float(value)


def mass_balance(feedstock_tonnes, recovery_yield, saleable_fraction=1.0):
    """Split incoming feed into saleable product and residual tonnes.

    recovery_yield is the fraction of feed mass entering the recoverable stream.
    saleable_fraction is the share of that recovered stream meeting the stated
    product specification. All other mass is grouped as residual in this
    simplified function; a real process model should break out rejects,
    moisture, emissions, wastewater and named residue streams.
    """
    feed = _finite_nonnegative("feedstock_tonnes", feedstock_tonnes)
    if not np.isfinite([recovery_yield, saleable_fraction]).all():
        raise ValueError("yield inputs must be finite")
    if not 0 <= recovery_yield <= 1 or not 0 <= saleable_fraction <= 1:
        raise ValueError("recovery_yield and saleable_fraction must be in [0,1]")

    recovered = feed * float(recovery_yield)
    product = recovered * float(saleable_fraction)
    recovery_reject = feed - recovered
    product_reject = recovered - product
    residue = recovery_reject + product_reject
    return {
        "feedstock_tonnes": feed,
        "recovered_stream_tonnes": float(recovered),
        "saleable_product_tonnes": float(product),
        "recovery_reject_tonnes": float(recovery_reject),
        "product_specification_reject_tonnes": float(product_reject),
        "residue_tonnes": float(residue),
        "overall_product_yield": float(product / feed) if feed else 0.0,
        "mass_balance_residual_tonnes": float(feed - product - residue),
    }


def project_cash_flows(
    *,
    feedstock_tonnes_per_year,
    recovery_yield,
    product_price_per_tonne,
    gate_fee_per_tonne,
    variable_opex_per_tonne,
    fixed_opex_per_year,
    capex,
    project_years,
    discount_rate,
    annual_capacity_utilisation=1.0,
    tax_rate=0.0,
    annual_maintenance_capex=0.0,
    saleable_fraction=1.0,
    ramp_up_years=0,
    replacement_costs=None,
    salvage_value=0.0,
):
    """Build annual unlevered project cash flows for a simplified screening case.

    The model:
    - scales feedstock throughput by capacity utilisation;
    - applies the mass-balance yields to saleable product and residue;
    - calculates product and gate-fee revenue;
    - applies variable OPEX to incoming feedstock and fixed OPEX annually;
    - uses straight-line depreciation for a simplified tax proxy;
    - excludes interest/financing and does not carry tax losses forward;
    - optionally applies a linear ramp-up across the first ramp_up_years;
    - includes year-specific replacement costs and terminal salvage value.

    Use nominal or real currency consistently. If price/cost escalation is
    material, add it explicitly and match the discount-rate basis.
    """
    numeric_inputs = {
        "feedstock_tonnes_per_year": feedstock_tonnes_per_year,
        "product_price_per_tonne": product_price_per_tonne,
        "gate_fee_per_tonne": gate_fee_per_tonne,
        "variable_opex_per_tonne": variable_opex_per_tonne,
        "fixed_opex_per_year": fixed_opex_per_year,
        "capex": capex,
        "annual_maintenance_capex": annual_maintenance_capex,
        "salvage_value": salvage_value,
    }
    for name, value in numeric_inputs.items():
        _finite_nonnegative(name, value)

    if not np.isfinite([recovery_yield, saleable_fraction, annual_capacity_utilisation, tax_rate, discount_rate]).all():
        raise ValueError("fractions and discount rate must be finite")
    if not 0 <= recovery_yield <= 1 or not 0 <= saleable_fraction <= 1:
        raise ValueError("recovery and saleable fractions must be in [0,1]")
    if not 0 <= annual_capacity_utilisation <= 1:
        raise ValueError("annual_capacity_utilisation must be in [0,1]")
    if not 0 <= tax_rate < 1:
        raise ValueError("tax_rate must be in [0,1)")
    if discount_rate <= -1:
        raise ValueError("discount_rate must be greater than -1")
    if not isinstance(project_years, (int, np.integer)) or project_years < 1:
        raise ValueError("project_years must be a positive integer")
    if not isinstance(ramp_up_years, (int, np.integer)) or ramp_up_years < 0:
        raise ValueError("ramp_up_years must be a non-negative integer")

    replacement_costs = replacement_costs or {}
    if not isinstance(replacement_costs, dict):
        raise TypeError("replacement_costs must be a {year: cost} mapping")
    for year, value in replacement_costs.items():
        if not isinstance(year, (int, np.integer)) or year < 1 or year > project_years:
            raise ValueError("replacement-cost years must fall within project life")
        _finite_nonnegative(f"replacement_costs[{year}]", value)

    nominal_feed = float(feedstock_tonnes_per_year)
    actual_feed = nominal_feed * float(annual_capacity_utilisation)
    balance = mass_balance(actual_feed, recovery_yield, saleable_fraction)
    revenue_product = balance["saleable_product_tonnes"] * float(product_price_per_tonne)
    revenue_gate = actual_feed * float(gate_fee_per_tonne)
    annual_revenue = revenue_product + revenue_gate
    variable_cost = actual_feed * float(variable_opex_per_tonne)
    fixed_cost = float(fixed_opex_per_year)
    depreciation = float(capex) / int(project_years)
    ebitda = annual_revenue - variable_cost - fixed_cost
    ebit = ebitda - depreciation
    tax = max(ebit, 0.0) * float(tax_rate)
    annual_operating_cash = ebitda - tax

    cash_flows = [-float(capex)]
    annual_rows = []
    for year in range(1, int(project_years) + 1):
        ramp_factor = min(1.0, year / ramp_up_years) if ramp_up_years else 1.0
        # Fixed OPEX is assumed payable throughout the year, including ramp-up.
        revenue_y = annual_revenue * ramp_factor
        variable_y = variable_cost * ramp_factor
        ebitda_y = revenue_y - variable_y - fixed_cost
        ebit_y = ebitda_y - depreciation
        tax_y = max(ebit_y, 0.0) * float(tax_rate)
        replacement_y = float(replacement_costs.get(year, 0.0))
        maintenance_y = float(annual_maintenance_capex)
        operating_cash_y = ebitda_y - tax_y
        terminal_salvage = float(salvage_value) if year == project_years else 0.0
        net_cash_y = operating_cash_y - replacement_y - maintenance_y + terminal_salvage
        cash_flows.append(float(net_cash_y))
        annual_rows.append({
            "year": int(year),
            "ramp_factor": float(ramp_factor),
            "revenue": float(revenue_y),
            "variable_opex": float(variable_y),
            "fixed_opex": fixed_cost,
            "depreciation": depreciation,
            "tax": float(tax_y),
            "maintenance_capex": maintenance_y,
            "replacement_cost": replacement_y,
            "salvage_value": terminal_salvage,
            "net_cash_flow": float(net_cash_y),
        })

    return {
        "mass_balance": balance,
        "nominal_feedstock_tonnes_per_year": nominal_feed,
        "actual_feedstock_tonnes_per_year": actual_feed,
        "product_revenue": float(revenue_product),
        "gate_fee_revenue": float(revenue_gate),
        "annual_revenue_at_steady_state": float(annual_revenue),
        "annual_variable_opex_at_steady_state": float(variable_cost),
        "annual_fixed_opex": fixed_cost,
        "annual_ebitda_at_steady_state": float(ebitda),
        "annual_depreciation": depreciation,
        "tax_at_steady_state": float(tax),
        "cash_flows": cash_flows,
        "annual_cash_flow_table": annual_rows,
        "project_years": int(project_years),
        "discount_rate": float(discount_rate),
    }


def npv(cash_flows, discount_rate):
    """Net present value with year-zero cash flow at index zero."""
    flows = np.asarray(cash_flows, dtype=float)
    if flows.ndim != 1 or len(flows) < 1 or not np.isfinite(flows).all():
        raise ValueError("cash_flows must be a finite one-dimensional vector")
    if not np.isfinite(discount_rate) or discount_rate <= -1:
        raise ValueError("discount_rate must be finite and greater than -1")
    return float(sum(cf / ((1.0 + discount_rate) ** year) for year, cf in enumerate(flows)))


def irr(cash_flows):
    """Return the unique IRR found on a broad search grid, otherwise NaN.

    Non-conventional cash flows can have multiple IRRs. When more than one
    bracketed root is found, this function returns NaN rather than silently
    selecting one. Inspect the NPV profile in such cases.
    """
    flows = np.asarray(cash_flows, dtype=float)
    if flows.ndim != 1 or len(flows) < 2 or not np.isfinite(flows).all():
        raise ValueError("cash_flows must be a finite one-dimensional vector")
    if not (np.any(flows < 0) and np.any(flows > 0)):
        return float("nan")

    def value(rate):
        return npv(flows, rate)

    grid = np.concatenate([
        np.linspace(-0.95, 0.0, 300, endpoint=False),
        np.geomspace(1e-5, 6.0, 700),
    ])
    values = [value(float(rate)) for rate in grid]
    roots = []
    for left, right, f_left, f_right in zip(grid[:-1], grid[1:], values[:-1], values[1:]):
        if f_left == 0:
            roots.append(float(left))
        elif f_left * f_right < 0:
            roots.append(float(brentq(value, float(left), float(right))))
    unique_roots = []
    for root in roots:
        if not any(abs(root - existing) < 1e-5 for existing in unique_roots):
            unique_roots.append(root)
    return float(unique_roots[0]) if len(unique_roots) == 1 else float("nan")


def simple_payback_years(cash_flows):
    """Undiscounted payback with linear interpolation inside the recovery year."""
    flows = np.asarray(cash_flows, dtype=float)
    if flows.ndim != 1 or len(flows) < 2 or not np.isfinite(flows).all():
        raise ValueError("cash_flows must be a finite vector with year-zero investment")
    cumulative = float(flows[0])
    if cumulative >= 0:
        return 0.0
    for year, cash in enumerate(flows[1:], start=1):
        previous = cumulative
        cumulative += float(cash)
        if cumulative >= 0 and cash > 0:
            return float((year - 1) + (-previous / cash))
    return float("nan")


def break_even_gate_fee_per_tonne(cfg, max_search_fee=1_000_000.0):
    """Find the minimum non-negative gate fee per incoming tonne for NPV >= 0.

    Uses the full project cash-flow function, so tax and ramp-up effects are
    included in the calculation. A gate fee is assumed to apply to actual
    incoming tonnes in every operating year. The result is a mathematical
    break-even value under the input assumptions, not evidence that a
    customer, municipality or supplier will pay that fee.

    If NPV is already non-negative with a zero gate fee, returns 0. If NPV
    remains negative at max_search_fee, raises ValueError rather than
    returning an unbracketed or misleading estimate.
    """
    if not np.isfinite(max_search_fee) or max_search_fee <= 0:
        raise ValueError("max_search_fee must be a positive finite number")
    base = dict(cfg)
    base["gate_fee_per_tonne"] = 0.0
    base_npv = npv(
        project_cash_flows(**base)["cash_flows"],
        base["discount_rate"],
    )
    if base_npv >= 0:
        return 0.0

    def npv_at_gate_fee(fee):
        case = dict(cfg)
        case["gate_fee_per_tonne"] = float(fee)
        result = project_cash_flows(**case)
        return npv(result["cash_flows"], case["discount_rate"])

    upper = 1.0
    while upper < max_search_fee and npv_at_gate_fee(upper) < 0:
        upper = min(upper * 2.0, max_search_fee)
    upper_npv = npv_at_gate_fee(upper)
    if upper_npv < 0:
        raise ValueError(
            "NPV remains negative at max_search_fee; inspect the base case or increase the search cap."
        )
    return float(brentq(npv_at_gate_fee, 0.0, upper))
