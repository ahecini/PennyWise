import sqlite3
conn = sqlite3.connect('example.db')  # Creates a new database file if it doesn’t exist
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()

#cursor.execute("insert into budget(amount,category,user_id) values(1.0,'var',2);")
#cursor.execute("insert into budget(amount,category,user_id) values(1.5,'varx',3);")
#cursor.execute("delete from budget;")'''

# Delete all tables
'''
cursor.executescript("""
                     drop table budget;
                     drop table `transaction`;
                     drop table category;
                     drop table user;
                    """)
'''
# Main script
'''
cursor.executescript("""
                    create table `user`( 
                        username varchar(50) PRIMARY KEY,
                        pin varchar(50),
                        balance float
                    );
                    create table `category`(
                        name varchar(50) PRIMARY KEY
                    );
                    create table `transaction`(
                        trans_id integer PRIMARY KEY,
                        description varchar(50),
                        amount float,
                        income boolean,
                        tdate date,
                        category varchar(50),
                        username varchar(50),
                        FOREIGN KEY (category) REFERENCES `category`(`name`),
                        FOREIGN KEY (`username`) REFERENCES `user`(`username`)
                    );
                    create table `budget`(
                        budget_id integer primary key,
                        amount float,
                        category varchar(50),
                        username varchar(50),
                        FOREIGN KEY (`category`) REFERENCES `category`(`name`),
                        FOREIGN KEY (`username`) REFERENCES `user`(`username`)
                    );
                    """)
'''
cursor.execute("insert into user values ('wildcat6','xxx',10.0);")
conn.commit()

cursor2 = conn.cursor()
cursor2.execute("select * from user;")
print(cursor2.fetchall())