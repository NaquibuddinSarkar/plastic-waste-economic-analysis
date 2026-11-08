"""One- and two-factor sensitivity analysis for the plastic-waste finance model."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .model import (
    project_cash_flows,
    npv,
    irr,
    simple_payback_years,
)


def _summary_for_case(case: dict, parameter: str, value: float) -> dict:
    model = project_cash_flows(**case)
    flows = model["cash_flows"]
    return {
        "parameter": parameter,
        "value": float(value),
        "npv": npv(flows, case["discount_rate"]),
        "irr": irr(flows),
        "simple_payback_years": simple_payback_years(flows),
        "annual_revenue_steady_state": model["annual_revenue_at_steady_state"],
        "saleable_product_tonnes_per_year": model["mass_balance"]["saleable_product_tonnes"],
        "residue_tonnes_per_year": model["mass_balance"]["residue_tonnes"],
    }


def one_way_sensitivity(cfg: dict, parameter: str, values) -> pd.DataFrame:
    """Change one configured input while holding every other input constant."""
    if parameter not in cfg:
        raise KeyError(f"parameter {parameter!r} does not exist in the base case")
    values = list(values)
    if not values:
        raise ValueError("values cannot be empty")
    rows = []
    for value in values:
        case = dict(cfg)
        case[parameter] = float(value)
        rows.append(_summary_for_case(case, parameter, float(value)))
    return pd.DataFrame(rows)


def two_way_npv_sensitivity(
    cfg: dict,
    parameter_x: str,
    values_x,
    parameter_y: str,
    values_y,
) -> pd.DataFrame:
    """Return a long-form grid of NPV under two simultaneous input changes."""
    if parameter_x == parameter_y:
        raise ValueError("two-way sensitivity parameters must be different")
    if parameter_x not in cfg or parameter_y not in cfg:
        raise KeyError("both sensitivity parameters must exist in the base case")
    values_x = list(values_x)
    values_y = list(values_y)
    if not values_x or not values_y:
        raise ValueError("both value grids must be non-empty")

    rows = []
    for x in values_x:
        for y in values_y:
            case = dict(cfg)
            case[parameter_x] = float(x)
            case[parameter_y] = float(y)
            result = project_cash_flows(**case)
            flows = result["cash_flows"]
            rows.append({
                parameter_x: float(x),
                parameter_y: float(y),
                "npv": npv(flows, case["discount_rate"]),
                "irr": irr(flows),
                "simple_payback_years": simple_payback_years(flows),
            })
    return pd.DataFrame(rows)
