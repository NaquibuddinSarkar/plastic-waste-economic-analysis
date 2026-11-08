# Beginner Guide: Plastic Waste Project Economics

## 1. What is this model for?

This project is a screening model for a hypothetical plastic-waste processing project. It estimates how incoming waste is split into saleable product and residue, then calculates revenues, costs and project cash flow.

It is not a plant design, process recipe, environmental assessment, legal opinion or investment recommendation. The base configuration is illustrative.

## 2. Understand the material balance first

A facility cannot sell more product mass than the material it processes. Start with incoming feedstock:

1. Some material may be rejected during sorting because of contamination or unsuitable polymer types.
2. The remaining processed feed enters the assumed recovery process.
3. Some mass becomes saleable product.
4. The remainder must still be accounted for as residue, emissions, water loss or another explicitly defined stream.

The current simplified model groups all non-saleable mass as residue. A real process model must break this into measured and regulated streams.

## 3. Revenue and cost concepts

- **Product revenue:** saleable tonnes × selling price per tonne.
- **Gate-fee revenue:** incoming tonnes × fee charged for accepting waste.
- **Variable operating cost:** throughput × variable processing cost per tonne.
- **Fixed OPEX:** costs that continue even when throughput falls, such as management, security and some service contracts.
- **CAPEX:** initial investment in land, civil works, equipment, utilities, installation and commissioning.
- **NPV:** value today of future cash flows after discounting.
- **IRR:** discount rate that makes NPV equal to zero, where a meaningful solution exists.
- **Simple payback:** time until cumulative undiscounted cash flow recovers initial investment.

## 4. Run the model

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest -q
python scripts/run_financial_model.py
python scripts/run_sensitivity.py
```

The model reads `config/base_case.json`. Edit a copy of the configuration and preserve the original illustrative case before using real quotes.

## 5. Read the result carefully

A positive NPV means the cash flows are positive under the assumptions entered. It does not mean a plant is feasible. A real project needs:
- reliable feedstock volumes and quality;
- proven process yields and uptime;
- buyers who accept the product at the assumed specification and price;
- realistic CAPEX/OPEX quotations;
- working capital and financing assumptions;
- a compliant environmental, health and safety plan;
- permits and regulatory confirmation.

A negative break-even gate fee can indicate that the modelled cash flows already cover the cost at a zero gate fee. It does not prove that a plant can actually collect that gate fee or sell the output.

## 6. Sensitivity analysis

Change one assumption at a time to understand its effect. Typical variables include throughput, uptime, product yield, selling price, gate fee, electricity and transport cost, CAPEX and discount rate.

One-at-a-time sensitivity is useful for understanding direction and scale, but it does not capture interactions. Add combined downside cases and Monte Carlo analysis only when input ranges are evidence-based.

## 7. Common mistakes

- Treating a closed mass balance as proof that the process is technically viable.
- Counting gas or residue as a saleable product without an offtake/use case.
- Using a single vendor quote or informal market price as a robust cost basis.
- Forgetting fixed costs during downtime.
- Ignoring feedstock contamination, moisture, collection radius and competing uses.
- Using IRR alone when cash flows change sign more than once.
- Treating policy background statistics as current facility-level feedstock data.

## 8. Responsible use

The project is technology-neutral at the financial layer. Mechanical recycling, sorting and conversion routes have different technical, environmental and market characteristics. Each route needs an independent mass balance, process design, life-cycle assessment and safety review. Do not infer environmental benefit from the NPV model alone.
