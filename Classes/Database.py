import sqlite3

class Database:

    """
    Constructor used to create the database object.
    """
    def __init__(self):
        self.conn = sqlite3.connect('example.db')  # Creates a new database file if it doesn’t exist
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()

    """
    Private method : creates the database's tables for the application
    """
    def __createDatabase(self):

        # Execute the script that creates all the tables necessary for the database
        self.cursor.executescript("""
                    create table `user`( 
                        username varchar(50) PRIMARY KEY,
                        pin varchar(50),
                        balance float
                    );
                    create table `category`(
                        name varchar(50) PRIMARY KEY,
                        colour varcher(7),
                        username varchar(50),
                        FOREIGN KEY (`username`) REFERENCES `user`(`username`)
                    );
                    create table `transaction`(
                        trans_id integer PRIMARY KEY,
                        description varchar(50),
                        amount float,
                        ttype text,
                        tdate text,
                        category varchar(50),
                        username varchar(50),
                        FOREIGN KEY (category) REFERENCES `category`(`name`),
                        FOREIGN KEY (`username`) REFERENCES `user`(`username`)
                    );
                    create table `budget`(
                        budget_id integer primary key,
                        category varchar(50),         
                        amount float,
                        FOREIGN KEY (`category`) REFERENCES `category`(`name`)
                    );
                    """)
        
        # Commit the changes made to the database
        self.insertUser(("user", "xxx", 100.0))
        self.insertUser(("wild6", "xxx", 100.0))
        self.insertCategory(("car","#1536f3","user"))
        self.insertCategory(("shopping","#27f315","wild6"))
        self.insertCategory(("blood","#f31515","wild6"))
        self.insertBudget(("car", 100.0))
        self.insertBudget(("shopping", 150.0))
        #self.insertBudget(("blood", 150.0))
        self.conn.commit()

    """
    Private method : drops all the tables in the database
    """
    def __dropDatabase(self):

        # Execute the script that drops all the tables necessary for the database
        self.cursor.executescript("""
                     drop table budget;
                     drop table `transaction`;
                     drop table category;
                     drop table user;
                    """)
        
        # Commit the changes made to the database
        self.conn.commit()

    """
    Method : deletes and recreates all the tables in the database
    """
    def startOver(self):

        self.__dropDatabase()
        self.__createDatabase()

    """
    Method : inserts a user in the `user` table.
    Parameters :
    - data(tuple): data corresponding to the informations of the user.
    Returns : void.
    """
    def insertUser(self, data):

        # Execute the script that inserts a user with the needed data
        self.cursor.execute("insert into user values (?,?,?)", data)

        # Commit the changes made to the database
        self.conn.commit()

    """
    Method : checks if a user in the `user` table.
    Parameters :
    - data(tuple): data corresponding to the informations of the user.
    Returns : boolean.
    """  
    def isUserExist(self, data):

        # Execute the script that searches for specific user
        self.cursor.execute("select count(*) from user where username = ? and pin = ?", data)

        # Returns True if the user is found, otherwise it returns False
        return self.cursor.fetchall()[0][0]!=0
    
    """
    Method : gets the balance of a user in the `balance` table.
    Parameters :
    - data(tuple): data corresponding to the informations of the user.
    Returns : float.
    """  
    def getUserBalance(self, data):

        # Execute the script that searches for a specific user's balance
        self.cursor.execute("select balance from user where username = ?", data)

        # Returns the corresponding budget
        return self.cursor.fetchall()
    
    """
    Method : updates the balance of a user in the `balance` table.
    Parameters :
    - data(tuple): data corresponding to the informations of the user and the amount to add/substract of the current balance.
    Returns : float.
    """  
    def setUserBalance(self, data):

        # Execute the script that searches for a specific user's balance
        self.cursor.execute("update user set balance = ? where username = ?", data)

        # Commit the changes made to the database
        self.conn.commit()
    
    """
    Method : inserts a category in the `category` table.
    Parameters :
    - data(tuple): data corresponding to the informations of the category to insert.
    Returns : void.
    """
    def insertCategory(self, data):

        # Execute the script that inserts a category
        self.cursor.execute("insert into category values (?,?,?)", data)

        # Commit the changes made to the database
        self.conn.commit()

    """
    Method : gets all usernames from the `user` table.
    Returns : string[].
    """  
    def getUsernames(self):

        # Execute the script to select all category names
        self.cursor.execute("select username from user")

        # Returns a list of strings
        return self.cursor.fetchall()  
    
    """
    Method : gets all category names from the `category` table.
    Returns : string[].
    """  
    def getCategories(self):

        # Execute the script to select all category names
        self.cursor.execute("select name from category")

        # Returns a list of strings
        return self.cursor.fetchall()   

    """
    Method : gets all category names from the `category` table associated with a user.
    Returns : string[].
    """  
    def getCategoriesId(self, id):

        # Execute the script to select all category names
        self.cursor.execute("select name from category where `username`=? ", (id,))

        # Returns a list of strings
        return self.cursor.fetchall()   

    """
    Method : inserts a transaction in the `transaction` table.
    Parameters :
    - data(tuple): data corresponding to the informations of the transaction to insert.
    Returns : void.
    """
    def insertTransaction(self, data):     

        # Execute the script that inserts a category
        self.cursor.execute("insert into `transaction`(description,amount,ttype,tdate,category,username) values (?,?,?,?,?,?)", data)

        # Commit the changes made to the database
        self.conn.commit()

    """
    Method : gets all transactions from the `transaction` table.
    Returns : string[].
    """  
    def getTransactions(self, username):

        # Execute the script to select all category names
        self.cursor.execute("select tdate,ttype,amount,category,description from `transaction` where `username`=?", username)

        # Returns a list of strings
        return self.cursor.fetchall()  
     
    """
    Method : inserts a budget in the `budget` table.
    Parameters :
    - data(tuple): data corresponding to the informations of the budget to insert.
    Returns : void.
    """
    def insertBudget(self, data):     

        # Execute the script that inserts a budget
        self.cursor.execute("insert into `budget`(category,amount) values (?,?)", data)

        # Commit the changes made to the database
        self.conn.commit()

    """
    Method : gets all budget amounts corresponding to a user from the `budget` table.
    Returns : string[].
    """  
    def getBudget(self, username):

        # Execute the script to select all category names
        self.cursor.execute("select category,amount from `budget` inner join `category` on `budget`.`category`=`category`.`name` where `username`=?", (username,))

        # Returns a list of strings
        return self.cursor.fetchall()

    """
    Method : gets all budget amounts corresponding to a user from the `budget` table.
    Returns : string[].
    """  
    def getBudget(self, username):

        # Execute the script to select all category names
        self.cursor.execute("select category,amount from `budget` inner join `category` on `budget`.`category`=`category`.`name` where `username`=?", (username,))

        # Returns a list of strings
        return self.cursor.fetchall()

    """
    Method : gets the total amount of expenses of a given category.
    Returns : float[].
    """  
    def getCategoryExpenses(self, category):

        # Execute the script to select all category names
        self.cursor.execute("select sum(amount) from `transaction` where `category`=? and `ttype`='Expense'", (category,))

        # Returns a list of strings
        return self.cursor.fetchall()
    
    """
    Method : updates a budget amount in the `budget` table.
    Parameters :
    - data(tuple): data corresponding to the amount of the budget to update to.
    Returns : void.
    """
    def updateBudgetAmount(self, data):     

        # Execute the script that inserts a budget
        self.cursor.execute("update `budget` set amount=? where `category`=?", data)

        # Commit the changes made to the database
        self.conn.commit()

    """
    Method : gets the budget amount corresponding to a category from the `budget` table.
    Returns : string[].
    """  
    def getBudgetAmount(self, category):

        # Execute the script to select all category names
        self.cursor.execute("select amount from `budget` where `category`=?", (category,))

        # Returns a list of strings
        return self.cursor.fetchall()