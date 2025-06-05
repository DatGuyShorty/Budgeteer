import sqlite3


# Connects to the database file (creates it if it doesn’t exist)
conn = sqlite3.connect("budget.db")

# Create a cursor to run SQL commands
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    type TEXT,
    category TEXT,
    amount REAL,
    note TEXT
)
""")

# Save changes and close connection
conn.commit()
conn.close()