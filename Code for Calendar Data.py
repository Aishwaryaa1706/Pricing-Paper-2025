import os
import pandas as pd

# ====== CONFIG ======
FOLDER = r"C:\Users\aishw\AppData\Local\Programs\Python\Python312\data\seattle\calendar"
OUT_CSV = os.path.join(FOLDER, "calendar_from_filenames.csv")
OUT_XLSX = os.path.join(FOLDER, "calendar_from_filenames.xlsx")

# ====== MAIN ======
rows = []

for fname in os.listdir(FOLDER):
    if not fname or fname.lower().startswith("listing_id"):
        # skip header-like files
        continue

    # remove extension if any
    base, ext = os.path.splitext(fname)
    parts = base.split(",")

    if len(parts) < 7:
        print(f"Skipping (unexpected format): {fname}")
        continue

    row = {
        "listing_id": parts[0],
        "date": parts[1],
        "available": parts[2],
        "price": parts[3] if parts[3] != "" else None,
        "adjusted_price": parts[4] if parts[4] != "" else None,
        "minimum_nights": parts[5],
        "maximum_nights": parts[6],
    }
    rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Convert numeric fields
for col in ["price", "adjusted_price", "minimum_nights", "maximum_nights"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Convert availability to boolean
df["available"] = df["available"].map({"t": True, "f": False}).astype("boolean")

print("Parsed rows:", len(df))
print(df.head())

# Save outputs
df.to_csv(OUT_CSV, index=False)
df.to_excel(OUT_XLSX, index=False, engine="openpyxl")

print("\nSaved:")
print(" CSV :", OUT_CSV)
print(" XLSX:", OUT_XLSX)
