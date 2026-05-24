import sqlite3

# connect to database
conn = sqlite3.connect("users.db")

# create cursor
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

print("Database and table created successfully!")

# save and close
conn.commit()
conn.close()
