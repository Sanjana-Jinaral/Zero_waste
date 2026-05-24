import sqlite3

# connect to database
conn = sqlite3.connect("users.db")

# create cursor
cursor = conn.cursor()

# fetch all users
cursor.execute("SELECT * FROM users")

# store result
users = cursor.fetchall()

# print result
print(users)

# close connection
conn.close()
