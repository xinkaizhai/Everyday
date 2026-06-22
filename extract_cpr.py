import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


def extract_1mo_cpr(folder, end_date="06/2026"):
    results = []

    for filename in os.listdir(folder):
        if "_CStat" not in filename or not filename.endswith(".csv"):
            continue

        cusip = filename[:9]
        filepath = os.path.join(folder, filename)

        df = pd.read_csv(filepath, header=None)
        cpr_row = df.iloc[16]

        # Collect non-null CPR values starting from column index 3
        cpr_values = []
        for col_idx in range(3, len(cpr_row)):
            cpr = cpr_row[col_idx]
            if pd.isna(cpr):
                break
            cpr_values.append(cpr)

        # Generate date labels going back from end_date
        end_dt = datetime.strptime(end_date, "%m/%Y")
        date_labels = [
            (end_dt - relativedelta(months=i)).strftime("%m/%Y")
            for i in range(len(cpr_values) - 1, -1, -1)
        ]

        row = {"CUSIP": cusip}
        for label, cpr in zip(date_labels, cpr_values):
            row[label] = cpr

        results.append(row)

    # Collect all date columns and sort oldest to newest
    all_dates = sorted(
        set(k for r in results for k in r if k != "CUSIP"),
        key=lambda x: datetime.strptime(x, "%m/%Y")
    )

    output_df = pd.DataFrame(results)[["CUSIP"] + all_dates]
    return output_df


if __name__ == "__main__":
    folder = r"K:\path\to\your\folder"  # update this path
    output_df = extract_1mo_cpr(folder, end_date="06/2026")
    print(output_df)
    output_df.to_excel("CPR_summary.xlsx", index=False)
