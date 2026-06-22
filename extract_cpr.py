import os
import pandas as pd


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
            month = months[col_idx]
            cpr = cpr_row[col_idx]
            if pd.isna(month) or pd.isna(cpr):
                continue
            row[month] = cpr

        results.append(row)

    output_df = pd.DataFrame(results)

    # Sort month columns oldest to newest and rename to mm/yyyy
    month_cols = [c for c in output_df.columns if c != "CUSIP"]
    parsed = {m: pd.to_datetime(m, dayfirst=True) for m in month_cols}
    month_cols = sorted(month_cols, key=lambda x: parsed[x])
    output_df = output_df[["CUSIP"] + month_cols]
    rename_map = {m: parsed[m].strftime("%m/%Y") for m in month_cols}
    output_df = output_df.rename(columns=rename_map)

    return output_df


if __name__ == "__main__":
    folder = r"K:\path\to\your\folder"  # update this path
    output_df = extract_1mo_cpr(folder)
    print(output_df)
    output_df.to_excel("CPR_summary.xlsx", index=False)
