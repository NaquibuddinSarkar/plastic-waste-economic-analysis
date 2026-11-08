"""Run one- and two-way sensitivity cases for the illustrative base case."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from plastic_waste_economics.sensitivity import one_way_sensitivity, two_way_npv_sensitivity
from plastic_waste_economics.model import break_even_gate_fee_per_tonne


def main():
    cfg = json.loads((ROOT / "config" / "base_case.json").read_text())
    output = ROOT / "outputs"
    output.mkdir(exist_ok=True)

    one_way = one_way_sensitivity(
        cfg,
        "recovery_yield",
        [0.50, 0.60, 0.70, 0.80, 0.90],
    )
    one_way.to_csv(output / "sensitivity_recovery_yield_demo.csv", index=False)

    two_way = two_way_npv_sensitivity(
        cfg,
        "recovery_yield",
        [0.50, 0.60, 0.70, 0.80],
        "product_price_per_tonne",
        [300, 400, 500, 600, 700],
    )
    two_way.to_csv(output / "sensitivity_yield_price_demo.csv", index=False)

    gate_fee = break_even_gate_fee_per_tonne(cfg)
    print("ONE-WAY SENSITIVITY — RECOVERY YIELD")
    print(one_way.to_string(index=False))
    print("\nTWO-WAY SENSITIVITY — YIELD AND PRODUCT PRICE")
    print(two_way.to_string(index=False))
    print(f"\nBreak-even gate fee per incoming tonne under this model: {gate_fee:,.2f}")
    print("\nWARNING: All default assumptions are illustrative, not verified market inputs.")


if __name__ == "__main__":
    main()
