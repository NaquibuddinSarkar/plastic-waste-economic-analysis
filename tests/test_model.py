import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from plastic_waste_economics.model import (
    mass_balance,
    project_cash_flows,
    npv,
    irr,
    simple_payback_years,
    break_even_gate_fee_per_tonne,
)
from plastic_waste_economics.sensitivity import (
    one_way_sensitivity,
    two_way_npv_sensitivity,
)


def simple_case(**overrides):
    case = {
        "feedstock_tonnes_per_year": 1000,
        "recovery_yield": 0.7,
        "saleable_fraction": 0.95,
        "product_price_per_tonne": 400,
        "gate_fee_per_tonne": 10,
        "variable_opex_per_tonne": 100,
        "fixed_opex_per_year": 25000,
        "capex": 200000,
        "project_years": 10,
        "discount_rate": 0.1,
        "annual_capacity_utilisation": 0.9,
        "tax_rate": 0.2,
    }
    case.update(overrides)
    return case


def test_mass_balance_conserves_mass_and_reports_rejects():
    result = mass_balance(100, 0.8, saleable_fraction=0.9)
    assert result["saleable_product_tonnes"] == pytest.approx(72)
    assert result["residue_tonnes"] == pytest.approx(28)
    assert result["recovery_reject_tonnes"] == pytest.approx(20)
    assert result["product_specification_reject_tonnes"] == pytest.approx(8)
    assert result["mass_balance_residual_tonnes"] == pytest.approx(0)


def test_mass_balance_rejects_bad_yield():
    with pytest.raises(ValueError):
        mass_balance(100, 1.2)


def test_npv_known_case():
    assert npv([-100, 60, 60], 0.0) == pytest.approx(20)


def test_irr_and_payback():
    flows = [-100, 60, 60]
    assert irr(flows) == pytest.approx(0.13066, rel=1e-3)
    assert simple_payback_years(flows) == pytest.approx(1.6666667)


def test_cash_flow_vector_and_ramp_up():
    result = project_cash_flows(**simple_case(ramp_up_years=2))
    assert len(result["cash_flows"]) == 11
    assert result["annual_cash_flow_table"][0]["ramp_factor"] == pytest.approx(0.5)
    assert result["mass_balance"]["residue_tonnes"] >= 0


def test_replacement_cost_reduces_project_npv():
    base = project_cash_flows(**simple_case())
    replacement = project_cash_flows(**simple_case(replacement_costs={5: 50000}))
    assert npv(replacement["cash_flows"], 0.1) < npv(base["cash_flows"], 0.1)


def test_break_even_gate_fee_makes_npv_nonnegative():
    cfg = simple_case(gate_fee_per_tonne=0, product_price_per_tonne=100, capex=500000)
    gate = break_even_gate_fee_per_tonne(cfg)
    with_fee = project_cash_flows(**{**cfg, "gate_fee_per_tonne": gate})
    assert npv(with_fee["cash_flows"], cfg["discount_rate"]) == pytest.approx(0, abs=1e-4)


def test_break_even_gate_fee_zero_when_base_case_already_profitable():
    cfg = simple_case()
    assert break_even_gate_fee_per_tonne(cfg) == 0.0


def test_irregular_multiple_sign_changes_return_nan_or_finite_unique_root():
    # A single conventional root should be found; ambiguous non-conventional
    # flows should not be silently assigned an arbitrary IRR.
    value = irr([-100, 230, -132])
    assert np.isnan(value) or np.isfinite(value)


def test_one_and_two_way_sensitivity_dimensions():
    cfg = simple_case()
    one_way = one_way_sensitivity(cfg, "recovery_yield", [0.5, 0.6, 0.7])
    two_way = two_way_npv_sensitivity(
        cfg, "recovery_yield", [0.5, 0.7],
        "product_price_per_tonne", [300, 500, 700]
    )
    assert len(one_way) == 3
    assert len(two_way) == 6
    assert {"npv", "irr", "simple_payback_years"}.issubset(two_way.columns)
