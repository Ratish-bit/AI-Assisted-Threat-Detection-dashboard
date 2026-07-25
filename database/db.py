import sqlite3

DATABASE = "database/threat.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)   # ✅ CORRECT
    conn.row_factory = sqlite3.Row
    return conn