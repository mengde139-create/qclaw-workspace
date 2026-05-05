# -*- coding: utf-8 -*-
import sqlite3, json, os

db_path = r"C:\Users\mengdejun\AppData\Roaming\flomo卡片笔记\DIPS"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# List all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cur.fetchall()]
print("Tables:", tables)
print()

for tname in tables:
    cur.execute(f"SELECT COUNT(*) FROM [{tname}]")
    cnt = cur.fetchone()[0]
    print(f"Table [{tname}]: {cnt} rows")
    cur.execute(f"PRAGMA table_info([{tname}])")
    cols = [c[1] for c in cur.fetchall()]
    print(f"  Columns: {cols}")
    print()

# Try to find memo/content tables
for tname in tables:
    if any(k in tname.lower() for k in ['memo', 'note', 'tag', 'content']):
        print(f"\n=== Content from [{tname}] ===")
        cur.execute(f"SELECT * FROM [{tname}] LIMIT 3")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        print()

conn.close()
