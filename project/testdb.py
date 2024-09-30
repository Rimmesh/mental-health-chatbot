import sqlite3

# Connect to the existing database
conn = sqlite3.connect('/mnt/data/database.db')
cursor = conn.cursor()

# Get the structure of the User table
cursor.execute("PRAGMA table_info(User)")
user_table_info = cursor.fetchall()

# Display the structure
user_table_info


