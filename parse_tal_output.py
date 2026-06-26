import json
import pandas as pd


def read_multi_json(filepath):
    records = []
    with open(filepath, "r") as f:
        content = f.read().strip()
    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(content):
        while idx < len(content) and content[idx] in ' \t\n\r':
            idx += 1
        if idx >= len(content):
            break
        obj, end_idx = decoder.raw_decode(content, idx)
        records.append(obj)
        idx = end_idx
    return records


def parse_tal_output(filepath):
    records = read_multi_json(filepath)

    all_headers = []
    all_cashflows = []

    for data in records:
        # Header fields (everything except CashFlowList)
        header = {k: v for k, v in data.items() if k != "CashFlowList"}
        all_headers.append(header)

        # CashFlow records
        if "CashFlowList" in data:
            cashflow_df = pd.DataFrame(data["CashFlowList"])
            cashflow_df["Date"] = pd.to_datetime(cashflow_df["Date"], format="%Y%m%d")

            # Reorder columns nicely
            cols = ["Date", "Balance", "CashFlow", "Interest", "Principal",
                    "Prepayment", "DiscountFactor", "ExRate", "Term"]
            cols = [c for c in cols if c in cashflow_df.columns]
            cashflow_df = cashflow_df[cols]
            all_cashflows.append(cashflow_df)

    header_df = pd.DataFrame(all_headers)
    cashflow_df = pd.concat(all_cashflows, ignore_index=True) if all_cashflows else pd.DataFrame()

    return header_df, cashflow_df


if __name__ == "__main__":
    filepath = r"K:\path\to\TAL_JSON_Output.txt"  # update this path
    header_df, cashflow_df = parse_tal_output(filepath)

    print("=== Header ===")
    print(header_df.T)

    print("\n=== Cash Flows ===")
    print(cashflow_df.to_string(index=False))
