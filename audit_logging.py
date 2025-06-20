import sqlite3
from datetime import datetime
import pandas as pd

# ---------- CONFIG ----------
DB_PATH = 'database/stock_audit.db'

# ---------- CREATE TABLE ----------
def init_audit_table(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            dataset_name TEXT,
            description TEXT,
            row_count INTEGER,
            column_count INTEGER
        )
    """)
    conn.commit()
    conn.close()

# ---------- ADD AUDIT ENTRY ----------
def log_audit(dataset_name, description, df, db_path=DB_PATH):
    row_count, column_count = df.shape
    conn = sqlite3.connect(db_path)
    with conn:
        conn.execute("""
            INSERT INTO audit_log (timestamp, dataset_name, description, row_count, column_count)
            VALUES (?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), dataset_name, description, row_count, column_count))
    conn.close()

# ---------- GET AUDIT LOG ----------
def get_audit_log(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM audit_log ORDER BY timestamp DESC", conn)
    conn.close()
    return df

# ---------- OPTIONAL: Reset Audit Table (for development/testing) ----------
def reset_audit_table(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.execute("DROP TABLE IF EXISTS audit_log")
    conn.commit()
    conn.close()
    init_audit_table(db_path)
