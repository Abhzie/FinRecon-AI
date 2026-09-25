import sqlite3

def load_to_sqlite(bank, ledger, path="finance.db"):
    conn = sqlite3.connect(path)
    bank.to_sql("bank_transactions", conn, if_exists="replace", index=False)
    ledger.to_sql("general_ledger", conn, if_exists="replace", index=False)
    return conn
