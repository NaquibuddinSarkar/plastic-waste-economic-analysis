import sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from plastic_waste_economics.model import mass_balance, project_cash_flows, npv, irr, simple_payback_years


def test_mass_balance_conserves_mass():
    result = mass_balance(100, .8)
    assert result["saleable_product_tonnes"] == pytest.approx(80)
    assert result["residue_tonnes"] == pytest.approx(20)


def test_mass_balance_rejects_bad_yield():
    with pytest.raises(ValueError):
        mass_balance(100, 1.2)


def test_npv_known_case():
    assert npv([-100, 60, 60], 0.0) == pytest.approx(20)


def test_irr_and_payback():
    flows = [-100, 60, 60]
    assert irr(flows) == pytest.approx(0.13066, rel=1e-3)
    assert simple_payback_years(flows) == pytest.approx(1.6666667)


def test_cash_flow_vector():
    result = project_cash_flows(
        feedstock_tonnes_per_year=1000, recovery_yield=.7,
        product_price_per_tonne=400, gate_fee_per_tonne=10,
        variable_opex_per_tonne=100, fixed_opex_per_year=25000,
        capex=200000, project_years=10, discount_rate=.1
    )
    assert len(result["cash_flows"]) == 11
    assert result["mass_balance"]["residue_tonnes"] >= 0
