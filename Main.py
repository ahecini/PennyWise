import sqlite3
conn = sqlite3.connect('example.db')  # Creates a new database file if it doesn’t exist
cursor = conn.cursor()