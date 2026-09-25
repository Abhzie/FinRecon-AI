import pandas as pd

def reconcile(bank, ledger):
    b = bank.copy()
    l = ledger.copy()
    b["date"] = pd.to_datetime(b["date"])
    l["date"] = pd.to_datetime(l["date"])

    duplicate_ids = set(l[l.duplicated("transaction_id", keep=False)]["transaction_id"])

    merged = b.merge(
        l[["transaction_id","date","vendor","amount"]],
        on="transaction_id", how="left", suffixes=("_bank","_ledger")
    )

    def classify(row):
        if pd.isna(row["amount_ledger"]):
            return "MISSING_IN_LEDGER"
        if row["transaction_id"] in duplicate_ids:
            return "DUPLICATE"
        if abs(row["amount_bank"] - row["amount_ledger"]) > 0.01:
            return "AMOUNT_MISMATCH"
        if row["date_bank"] != row["date_ledger"]:
            return "DATE_MISMATCH"
        return "MATCHED"

    merged["status"] = merged.apply(classify, axis=1)
    merged["variance"] = merged["amount_bank"] - merged["amount_ledger"].fillna(0)
    return merged
