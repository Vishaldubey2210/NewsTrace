import os
import sqlite3

def check_db(path="data/newstrace.db"):
    if not os.path.exists(path):
        print("Database not found, creating clean instance...")
        return
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA integrity_check;")
    res = cursor.fetchone()
    print("Database Integrity Status:", res[0])
    conn.close()

if __name__ == '__main__':
    check_db()
