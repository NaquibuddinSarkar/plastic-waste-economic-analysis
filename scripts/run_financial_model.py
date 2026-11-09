"""Run the illustrative plastic-waste financial base case."""
from pathlib import Path
import json
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from plastic_waste_economics.model import (
    project_cash_flows,
    npv,
    irr,
    simple_payback_years,
    break_even_gate_fee_per_tonne,
)


def main():
    cfg = json.loads((ROOT / "config" / "base_case.json").read_text())
    result = project_cash_flows(**cfg)
    flows = result["cash_flows"]
    metrics = {
        "NPV": npv(flows, cfg["discount_rate"]),
        "IRR": irr(flows),
        "simple_payback_years": simple_payback_years(flows),
        "break_even_gate_fee_per_tonne": break_even_gate_fee_per_tonne(cfg),
    }

    output = ROOT / "outputs"
    output.mkdir(exist_ok=True)
    pd.DataFrame(result["annual_cash_flow_table"]).to_csv(
        output / "annual_cash_flows_demo.csv", index=False
    )
    (output / "financial_summary_demo.json").write_text(
        json.dumps({"model": result, "metrics": metrics}, indent=2)
    )

    print("MATERIAL BALANCE — ILLUSTRATIVE CASE")
    print(pd.Series(result["mass_balance"]).to_string())
    print("\nSTEADY-STATE FINANCIAL SUMMARY")
    for key in [
        "annual_revenue_at_steady_state",
        "annual_variable_opex_at_steady_state",
        "annual_fixed_opex",
        "annual_ebitda_at_steady_state",
    ]:
        print(f"{key}: {result[key]:,.2f}")
    print("\nPROJECT METRICS")
    for key, value in metrics.items():
        print(f"{key}: {value:,.4f}" if value is not None else f"{key}: not available")
    print("\nWARNING: Assumptions are illustrative, not verified Bangladesh market inputs "
          "or an investment recommendation.")


if __name__ == "__main__":
    main()
