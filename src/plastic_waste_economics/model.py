"""Plastic waste processing mass balance and discounted cash-flow model."""
from __future__ import annotations
import numpy as np
from scipy.optimize import brentq


def mass_balance(feedstock_tonnes, recovery_yield, saleable_fraction=1.0):
    """Return saleable product and residue tonnes from annual feedstock."""
    if feedstock_tonnes < 0 or not 0 <= recovery_yield <= 1 or not 0 <= saleable_fraction <= 1:
        raise ValueError("feedstock must be >=0 and yield/fraction must be in [0,1]")
    recovered = feedstock_tonnes * recovery_yield
    product = recovered * saleable_fraction
    residue = feedstock_tonnes - product
    return {
        "feedstock_tonnes": float(feedstock_tonnes),
        "saleable_product_tonnes": float(product),
        "residue_tonnes": float(residue),
        "overall_product_yield": float(product / feedstock_tonnes) if feedstock_tonnes else 0.0
    }


def project_cash_flows(*, feedstock_tonnes_per_year, recovery_yield, product_price_per_tonne,
                       gate_fee_per_tonne, variable_opex_per_tonne, fixed_opex_per_year,
                       capex, project_years, discount_rate, annual_capacity_utilisation=1.0,
                       tax_rate=0.0, annual_maintenance_capex=0.0):
    """Build annual unlevered cash flows using simplified tax and depreciation assumptions.

    Taxes are applied to positive EBIT after straight-line depreciation; interest and
    financing are excluded. Assumptions must be replaced with sourced project inputs.
    """
    if min(feedstock_tonnes_per_year, product_price_per_tonne, gate_fee_per_tonne,
           variable_opex_per_tonne, fixed_opex_per_year, capex, annual_maintenance_capex) < 0:
        raise ValueError("financial inputs cannot be negative")
    if not 0 <= recovery_yield <= 1 or not 0 <= annual_capacity_utilisation <= 1 or not 0 <= tax_rate < 1:
        raise ValueError("yield, utilisation and tax rate are outside valid ranges")
    if project_years < 1 or discount_rate < 0:
        raise ValueError("project years must be >=1 and discount rate non-negative")

    annual_feed = feedstock_tonnes_per_year * annual_capacity_utilisation
    balance = mass_balance(annual_feed, recovery_yield)
    revenue = balance["saleable_product_tonnes"] * product_price_per_tonne + annual_feed * gate_fee_per_tonne
    variable_cost = annual_feed * variable_opex_per_tonne
    depreciation = capex / project_years
    ebit = revenue - variable_cost - fixed_opex_per_year - depreciation
    tax = max(ebit, 0.0) * tax_rate
    operating_cash = revenue - variable_cost - fixed_opex_per_year - tax
    flows = [-float(capex)] + [float(operating_cash - annual_maintenance_capex)] * int(project_years)
    return {
        "mass_balance": balance,
        "annual_revenue": float(revenue),
        "annual_variable_opex": float(variable_cost),
        "annual_fixed_opex": float(fixed_opex_per_year),
        "annual_depreciation": float(depreciation),
        "annual_tax": float(tax),
        "cash_flows": flows
    }


def npv(cash_flows, discount_rate):
    if discount_rate <= -1:
        raise ValueError("discount rate must be greater than -100%")
    return float(sum(cf / ((1 + discount_rate) ** year) for year, cf in enumerate(cash_flows)))


def irr(cash_flows):
    """Return IRR if a unique bracketed root exists, otherwise NaN."""
    flows = np.asarray(cash_flows, dtype=float)
    if not (np.any(flows < 0) and np.any(flows > 0)):
        return float("nan")
    def f(rate):
        return sum(cf / ((1 + rate) ** year) for year, cf in enumerate(flows))
    grid = np.linspace(-0.9, 5.0, 500)
    vals = [f(x) for x in grid]
    for a, b, fa, fb in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if fa == 0:
            return float(a)
        if fa * fb < 0:
            return float(brentq(f, a, b))
    return float("nan")


def simple_payback_years(cash_flows):
    """Return the first year cumulative undiscounted cash flow becomes non-negative."""
    if len(cash_flows) < 2:
        return float("nan")
    cumulative = float(cash_flows[0])
    for year, cash in enumerate(cash_flows[1:], start=1):
        previous = cumulative
        cumulative += float(cash)
        if cumulative >= 0 and cash > 0:
            return float(year - 1 + (-previous / cash))
    return float("nan")
