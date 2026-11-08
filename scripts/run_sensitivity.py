"""Simple one-factor sensitivity of project NPV."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from plastic_waste_economics.model import project_cash_flows,npv

def main():
    cfg=json.loads((ROOT/"config/base_case.json").read_text())
    results=[]
    for yield_value in [.55,.65,.75,.85]:
        case=dict(cfg); case["recovery_yield"]=yield_value
        model=project_cash_flows(**case)
        results.append({"recovery_yield":yield_value,"NPV":npv(model["cash_flows"],case["discount_rate"])})
    print("Sensitivity to recovery yield")
    for row in results: print(row)

if __name__=="__main__":
    main()
