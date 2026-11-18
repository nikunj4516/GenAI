# Task 3: SQLite

import sqlite3
import pandas as pd

conn = sqlite3.connect("sample.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
id INTEGER PRIMARY KEY,
name TEXT,
department TEXT,
salary REAL
)
""")

employees = [
    (1,"John","IT",50000),
    (2,"Emma","HR",45000),
    (3,"Mike","Finance",60000),
    (4,"Sophia","IT",55000),
    (5,"Liam","Sales",48000)
]

cursor.executemany(
    "INSERT OR REPLACE INTO employees VALUES(?,?,?,?)",
    employees
)

conn.commit()

query = "SELECT * FROM employees"

df = pd.read_sql_query(query, conn)

print(df)

conn.close()