"""Run the illustrative plastic-waste financial base case."""
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from plastic_waste_economics.model import project_cash_flows, npv, irr, simple_payback_years


def main():
    cfg = json.loads((ROOT / "config" / "base_case.json").read_text())
    model = project_cash_flows(**cfg)
    flows = model["cash_flows"]
    print("Mass balance:", model["mass_balance"])
    print("Annual revenue:", round(model["annual_revenue"], 2))
    print("NPV:", round(npv(flows, cfg["discount_rate"]), 2))
    print("IRR:", irr(flows))
    print("Simple payback (years):", simple_payback_years(flows))
    print("\nWARNING: Inputs are illustrative only; not an investment recommendation.")


if __name__ == "__main__":
    main()
