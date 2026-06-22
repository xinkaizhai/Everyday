import os
from datetime import datetime
import pandas as pd


def parse_dmm_to_mmyyyy(label):
    """Convert d-mmm (e.g. 26-Jun) to mm/yyyy using year inference."""
    dt = datetime.strptime(str(label).strip(), "%d-%b")
    now = datetime.now()
    # If month is ahead of current month, it belongs to the previous year
    year = now.year if dt.month <= now.month else now.year - 1
    return datetime(year, dt.month, 1).strftime("%m/%Y")


def extract_1mo_cpr(folder):
    results = []

    for filename in os.listdir(folder):
        if "_CStat" not in filename or not filename.endswith(".csv"):
            continue

        cusip = filename[:9]
        filepath = os.path.join(folder, filename)

        df = pd.read_csv(filepath, header=None)

        months = df.iloc[1]
        cpr_row = df.iloc[16]

        row = {"CUSIP": cusip}
        for col_idx in range(3, len(months)):
            raw_month = months[col_idx]
            cpr = cpr_row[col_idx]
            if pd.isna(raw_month) or pd.isna(cpr):
                continue
            label = parse_dmm_to_mmyyyy(raw_month)
            row[label] = cpr

        results.append(row)

    # Sort date columns oldest to newest
    all_dates = sorted(
        set(k for r in results for k in r if k != "CUSIP"),
        key=lambda x: datetime.strptime(x, "%m/%Y")
    )

    output_df = pd.DataFrame(results)[["CUSIP"] + all_dates]
    return output_df


if __name__ == "__main__":
    folder = r"K:\path\to\your\folder"  # update this path
    output_df = extract_1mo_cpr(folder)
    print(output_df)
    output_df.to_excel("CPR_summary.xlsx", index=False)
