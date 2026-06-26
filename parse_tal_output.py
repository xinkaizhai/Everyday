import json
import pandas as pd


def parse_tal_output(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)

    # Header fields (everything except CashFlowList)
    header = {k: v for k, v in data.items() if k != "CashFlowList"}
    header_df = pd.DataFrame([header])

    # CashFlow records
    cashflow_df = pd.DataFrame(data["CashFlowList"])

    # Format Date column
    cashflow_df["Date"] = pd.to_datetime(cashflow_df["Date"], format="%Y%m%d")

    # Reorder columns nicely
    cols = ["Date", "Balance", "CashFlow", "Interest", "Principal", "Prepayment",
            "DiscountFactor", "ExRate", "Term"]
    cols = [c for c in cols if c in cashflow_df.columns]
    cashflow_df = cashflow_df[cols]

    return header_df, cashflow_df


if __name__ == "__main__":
    filepath = r"K:\path\to\TAL_JSON_Output.txt"  # update this path
    header_df, cashflow_df = parse_tal_output(filepath)

    print("=== Header ===")
    print(header_df.T)

    print("\n=== Cash Flows ===")
    print(cashflow_df.to_string(index=False))
