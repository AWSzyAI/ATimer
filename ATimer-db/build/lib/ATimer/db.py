import sqlite3

with open('schema.sql') as f:
    conn.executescript(f.read())