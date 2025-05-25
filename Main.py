import sqlite3
conn = sqlite3.connect('example.db')  # Creates a new database file if it doesn’t exist
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()
cursor.execute("insert into budget(amount,category,user_id) values(1.0,'var',2);")
cursor.execute("insert into budget(amount,category,user_id) values(1.5,'varx',3);")
#cursor.execute("delete from budget;")
conn.commit()
cursor2 = conn.cursor()
cursor2.execute("select * from budget;")
print(cursor2.fetchall())