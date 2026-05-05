import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import datetime
from random import randrange, randint
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from matplotlib import style
import calendar

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
    
class Login(tk.Frame):
    def __init__(self, root):
        self.hello = Hello(root) 
        super().__init__(root, width=300, height=150) 
        self.db = Database()
        self.config(bg="#4B41D7")
        self.place(x=438,y=234) #50
        self.label1 = ttk.Label(self, text="user", font=('Segoe UI', 12), background="#4B41D7")
        self.label1.place(x=16,y=0.5)
        self.label2 = ttk.Label(self, text="password", font=('Segoe UI', 12), background="#4B41D7")
        self.label2.place(x=16,y=50.5) 
        self.text1 = ttk.Entry(self, font=('Helvetica',8), width=40, bootstyle="info")
        self.text1.place(x=16,y=20.5)
        self.text2 = ttk.Entry(self, font=('Helvetica',8), width=40, bootstyle="info")
        self.text2.place(x=16,y=70.5)
        self.login_button = ttk.Button(self, text="Login", bootstyle="success", width=20)
        self.login_button.place(x=16,y=115.5) 
        self.signup_button = ttk.Button(self, text="Sign up", bootstyle="info", width=13)
        self.signup_button.place(x=170,y=115.5)
    def setLoginButtonCommand(self, mainframe):
        self.login_button['command'] = lambda:self.login(mainframe)
    def setSignupButtonCommand(self, frame, background):
        self.signup_button['command'] = lambda:self.signup(frame, background)
    def login(self, frame):
        if self.db.isUserExist((self.text1.get(),self.text2.get())) :
            self.hello.setDashboard(self.text1.get())
            self.hello.setBackButtonCommand(frame)
            #background.tkraise()
            #frame.tkraise()
        else:
            messagebox.showinfo("Failure", "Username not found!")
    def signup(self, frame, background):
        background.tkraise()
        frame.tkraise()
    '''
    def popup(self):
        messagebox.showinfo("Success", "Login successful!")
    '''

class Signup(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=300, height=200) #150
        self.db = Database()
        self.config(bg="#4B41D7")
        self.place(x=438,y=234) #115
        self.label1 = ttk.Label(self, text="user", font=('Segoe UI', 12), background="#4B41D7")
        self.label1.place(x=16,y=0.5)
        self.label2 = ttk.Label(self, text="password", font=('Segoe UI', 12), background="#4B41D7")
        self.label2.place(x=16,y=50.5) 
        self.label3 = ttk.Label(self, text="balance", font=('Segoe UI', 12), background="#4B41D7")
        self.label3.place(x=16,y=100.5)
        self.text1 = ttk.Entry(self, font=('Helvetica',8), width=40, bootstyle="info")
        self.text1.place(x=16,y=20.5)
        self.text2 = ttk.Entry(self, font=('Helvetica',8), width=40, bootstyle="info")
        self.text2.place(x=16,y=70.5)
        self.text3 = ttk.Entry(self, font=('Helvetica',8), width=40, bootstyle="info")
        self.text3.place(x=16,y=120.5)
        self.login_button = ttk.Button(self, text="Login", bootstyle="success", width=20)
        self.login_button.place(x=16,y=155.5) #115.5
        self.signup_button = ttk.Button(self, text="Sign up", bootstyle="info", width=13)
        self.signup_button.place(x=170,y=155.5) #115.5
    def setSignupButtonCommand(self, frame, background):
        self.signup_button['command'] = lambda:self.signup(frame, background)
    def setLoginButtonCommand(self, frame, background):
        self.login_button['command'] = lambda:self.login(frame, background)
    def signup(self, frame, background):
        try:
            data = (self.text1.get(), self.text2.get(), float(self.text3.get()))
            self.db.insertUser(data)
            background.tkraise()
            frame.tkraise()
        except:
            messagebox.showinfo("Failure", "Could not sign up!")
    def login(self, frame, background):
        background.tkraise()
        frame.tkraise()
    '''
    def popup(self):
        messagebox.showinfo("Success", "Login successful!")
    '''

class TransactionAdd(tk.Frame):
    """
    TransactionAdd constructor method
    """
    def __init__(self, root, id):

        self.root = root
        self.id = id
        self.db = Database()
        self.add = ImageTk.PhotoImage(Image.open('add.png'))

        # Parent attributes initialization
        self.root = root
        super().__init__(self.root, width=300, height=300)

        # Configuring and placing the frame
        self.config(bg="#4B41D7")
        self.place(x=300,y=134) #115

        # Amount area
        self.amountLabel = ttk.Label(self, text="Amount", font=('Segoe UI', 12), background="#4B41D7")
        self.amountLabel.place(x=16,y=0.5)
        self.amountText = ttk.Entry(self, font=('Helvetica',8), width=40, bootstyle="info")
        self.amountText.place(x=16,y=30.5)

        # Description area
        self.descriptionLabel = ttk.Label(self, text="Description", font=('Segoe UI', 12), background="#4B41D7")
        self.descriptionLabel.place(x=16,y=60.5) 
        self.descriptionText = ttk.Entry(self, font=('Helvetica',8), width=40, bootstyle="info")
        self.descriptionText.place(x=16,y=90.5)

        # Date area
        self.today = datetime.datetime.now() # Today's date

        self.dateLabel = ttk.Label(self, text="Date", font=('Segoe UI', 12), background="#4B41D7")
        self.dateLabel.place(x=16,y=120.5)

        # Day spinbox
        self.day_ValueInside = tk.StringVar(self)
        self.day_ValueInside.set(self.today.day)
        self.daySpinbox = ttk.Spinbox(self, from_=1, to=31, width=5, textvariable=self.day_ValueInside)
        self.daySpinbox.place(x=16,y=150.5)

        # first anti-slash
        self.antislachLabel1 = ttk.Label(self, text="/", font=('Segoe UI', 12), background="#4B41D7")
        self.antislachLabel1.place(x=92,y=150.5)

        # Month spinbox
        self.month_ValueInside = tk.StringVar(self)
        self.month_ValueInside.set(self.today.month)
        self.monthSpinbox = ttk.Spinbox(self, from_=1, to=12, width=5, textvariable=self.month_ValueInside)
        self.monthSpinbox.place(x=110,y=150.5)

        # second anti-slash
        self.antislachLabel2 = ttk.Label(self, text="/", font=('Segoe UI', 12), background="#4B41D7")
        self.antislachLabel2.place(x=186,y=150.5)

        # Year spinbox
        self.year_ValueInside = tk.StringVar(self)
        self.year_ValueInside.set(self.today.year)
        self.yearSpinbox = ttk.Spinbox(self, from_=2025, to=2026, width=5, textvariable=self.year_ValueInside)
        self.yearSpinbox.place(x=200,y=150.5)

        # Category area
        self.categoryLabel = ttk.Label(self, text="Category", font=('Segoe UI', 12), background="#4B41D7")
        self.categoryLabel.place(x=16,y=183.5)
        #self.category_Options = ["Groceries", "Car", "Groceries", "Phone"]
        self.category_Options = [self.db.getCategoriesId(self.id)[i][0] for i in range(len(self.db.getCategoriesId(self.id)))]
        self.category_Options.insert(0,"")
        self.category_ValueInside = tk.StringVar(self)
        self.category_ValueInside.set("")
        self.category_QuestionMenu = ttk.OptionMenu(self, self.category_ValueInside, *self.category_Options, bootstyle="dark")
        self.category_QuestionMenu.place(x=16,y=215.5)
        self.AddCategoryButton = ttk.Button(self, text="+", bootstyle="success", width=1)
        
        self.addCategoryButton = tk.Button(self, image=self.add, height=15 ,width=15 ,borderwidth=0)
        self.addCategoryButton.config(bg="#4B41D7")
        self.addCategoryButton.place(x=85,y=188.5)
        #self.addCategoryButton['command'] = lambda:self.printFormInfos()
        #self.AddCategoryButton.place(x=85,y=183.5) #115.5

        # Income/Expense area
        self.incomeExpenselabel = ttk.Label(self, text="Income/Expense", font=('Segoe UI', 12), background="#4B41D7")
        self.incomeExpenselabel.place(x=150,y=183.5)
        self.incomeExpense_Options = ["", "Expense", "Income"]
        self.incomeExpense_ValueInside = tk.StringVar(self)
        self.incomeExpense_ValueInside.set("Expense")
        self.incomeExpense_QuestionMenu = ttk.OptionMenu(self, self.incomeExpense_ValueInside, *self.incomeExpense_Options, bootstyle="dark")
        self.incomeExpense_QuestionMenu.place(x=160,y=215.5)

        # AddTransaction button
        self.AddTransactionButton = ttk.Button(self, text="Add transaction", bootstyle="success", width=15)
        self.AddTransactionButton.place(x=16,y=260.5) #115.5
        self.AddTransactionButton['command'] = lambda:self.printFormInfos()
        # ViewTransaction button
        self.ViewTransactionButton = ttk.Button(self, text="View transactions", bootstyle="info", width=18)
        self.ViewTransactionButton.place(x=140,y=260.5) #115.5

    """
    changeFrame: Method to switch to another frame
    """
    def changeFrame(self, background, frame):
        background.tkraise()
        frame.tkraise()

    """
    setViewTransactionButton: Method to set which frame to switch to in changeFrame
    """
    def setViewTransactionButton(self, background, frame):
        self.ViewTransactionButton['command'] = lambda:self.changeFrame(background, frame)

    """
    setAddCategoryButton: Method to set which frame to switch to in changeFrame
    """
    def setAddCategoryButton(self, background, frame):
        self.addCategoryButton['command'] = lambda:self.changeFrame(background, frame)

    def printFormInfos(self):
        try:
            amount = float(self.amountText.get())
            amountIsValid = True
        except:
            amountIsValid = False
        description = self.descriptionText.get()
        day = self.day_ValueInside.get()
        month = self.month_ValueInside.get()
        year = self.year_ValueInside.get()
        date = day+"-"+month+"-"+year
        ttype = self.incomeExpense_ValueInside.get()
        category = self.category_ValueInside.get()

        descriptionIsValid = description.replace(" ", "")!=""
        date1 = day=="31" and (month in ["2", "4", "6", "9", "11"])
        date2 = day=="30" and month=="2"
        date3 = day=="29" and month=="2" and int(year)%4!=0
        dateIsValid = not date1 and not date2 and not date3
        categoryIsValid = category.replace(" ", "")!=""

        if(not amountIsValid):
            messagebox.showinfo("Failure", "Please insert a valid amount!")
        elif(not descriptionIsValid):
            messagebox.showinfo("Failure", "Please insert a valid description!")
        elif(not dateIsValid):
            messagebox.showinfo("Failure", "Please insert a valid date!")
        elif(not categoryIsValid):
            messagebox.showinfo("Failure", "Please choose or create a category!")
        else:
            messagebox.showinfo("Success", "Transaction added successfully!")
            self.db.insertTransaction((description,amount,ttype,date,category,self.id))
            self.root.refresh()
            operationType = (-1)**int(bin(ttype=="Expense")[2:])
            self.root.updateBalance(operationType*amount)
            expenses = self.db.getCategoryExpenses((category))[0][0]
            budget = self.db.getBudgetAmount((category))[0][0]
            if(expenses>=budget and budget>=0):
                messagebox.showinfo("Warning!", "A budget was not respected. Please check the budget table")

class TransactionView(tk.Frame):
    def __init__(self, root, id):
        self.id = id
        super().__init__(root, width=504, height=225)
        self.config(bg="#2b3e50")
        self.db = Database()
        self.place(x=200,y=180) #115
        self.table = ttk.Treeview(self)

        # Define the columns
        self.table['columns'] = ('Date', 'Type', 'Amount', 'Category', 'Description')

        # Format the columns
        self.table.column('#0', width=0, stretch=tk.NO)
        self.table.column('Date', anchor=tk.W, width=100)
        self.table.column('Type', anchor=tk.W, width=100)
        self.table.column('Amount', anchor=tk.W, width=100)
        self.table.column('Category', anchor=tk.W, width=100)
        self.table.column('Description', anchor=tk.W, width=100)

        # Create the headings
        self.table.heading('#0', text='', anchor=tk.W)
        self.table.heading('Date', text='Date', anchor=tk.W)
        self.table.heading('Type', text='Type', anchor=tk.W)
        self.table.heading('Amount', text='Amount', anchor=tk.W)
        self.table.heading('Category', text='Category', anchor=tk.W)
        self.table.heading('Description', text='Description', anchor=tk.W)

        # Sample data
        '''
        self.data = [
            ('07/07/2025', 'Income', 300.01, 'Shopping', 'groceries'),
            ('17/07/2025', 'expense', 10.01, 'Shopping', 'interest'),
            ('17/07/2025', 'expense', 10.01, 'Shopping', 'interest')
        ]
        '''
        self.data = self.db.getTransactions((self.id,))

        # Configure alternating row colors
        '''
        self.table.tag_configure('oddrow', background="#5F07EC")
        self.table.tag_configure('evenrow', background="#082470")
        '''

        # Configure alternating row colors
        self.table.tag_configure('Income', background="#29BB15")
        self.table.tag_configure('Expense', background="#FA0808")

        # Add data with alternating row colors
        '''
        for i in range(len(self.data)):
            if i % 2 == 0:
                self.table.insert(parent='', index=i, values=self.data[i], tags=('evenrow',))
            else:
                self.table.insert(parent='', index=i, values=self.data[i], tags=('oddrow',))
        '''

        # Add data with alternating row colors
        for i in range(len(self.data)):
            self.table.insert(parent='', index=i, values=self.data[i], tags=(self.data[i][1],))
            
        # Pack the table
        #self.table.pack(expand=True, fill=tk.BOTH)
        self.table.place(x=0,y=0)

        # Go to add transaction interface
        self.AddTransactionButton = ttk.Button(self, text="Add transaction", bootstyle="success", width=15)
        self.AddTransactionButton.place(x=16,y=187.5) #115.5

    def changeFrame(self, background, frame):
        background.tkraise()
        frame.tkraise()
    def setAddTransactionButton(self, background, frame):
        self.AddTransactionButton['command'] = lambda:self.changeFrame(background, frame)

class BudgetView(tk.Frame):
    def __init__(self, root, id):
        super().__init__(root, width=504, height=225)
        self.root = root
        self.config(bg="#2b3e50")
        self.place(x=200,y=180) #115
        self.table = ttk.Treeview(self, selectmode="browse")
        self.table.bind('<ButtonRelease-1>', self.selectItem)
        self.table.bind('<ButtonRelease-3>', self.deselectItem)

        self.db = Database()
        self.id = id

        # Define the columns
        self.table['columns'] = ('Category', 'Budget', 'expenses')

        # Format the columns
        self.table.column('#0', width=0, stretch=tk.NO)
        self.table.column('Category', anchor=tk.W, width=75)
        self.table.column('Budget', anchor=tk.W, width=75)
        self.table.column('expenses', anchor=tk.W, width=75)

        # Create the headings
        self.table.heading('#0', text='', anchor=tk.W)
        self.table.heading('Category', text='Category', anchor=tk.W)
        self.table.heading('Budget', text='Budget', anchor=tk.W)
        self.table.heading('expenses', text='expenses', anchor=tk.W)

        # Sample data
        self.data = self.db.getBudget(self.id)
        self.cleanData = []
        for data in self.data :
            dataList = list(data)
            if dataList[1]==-1:
                dataList[1]="no budget"
            else:
                dataList[1]=data[1]
            dataList.append(self.db.getCategoryExpenses(dataList[0])[0][0])
            self.cleanData.append(tuple(dataList))

        # Configure alternating row colors
        '''
        self.table.tag_configure('oddrow', background="#5F07EC")
        self.table.tag_configure('evenrow', background="#082470")
        '''

        # Configure alternating row colors
        self.table.tag_configure('Respected', background="#29BB15")
        self.table.tag_configure('Not-respected', background="#FA0808")

        # Add data with alternating row colors
        '''
        for i in range(len(self.data)):
            if i % 2 == 0:
                self.table.insert(parent='', index=i, values=self.data[i], tags=('evenrow',))
            else:
                self.table.insert(parent='', index=i, values=self.data[i], tags=('oddrow',))
        '''
        print("clean data",self.cleanData)
        # Add data with alternating row colors
        for i in range(len(self.cleanData)):
            print("hey",self.cleanData[i][1],self.cleanData[i][2])
            self.table.insert(parent='', index=i, values=self.cleanData[i], 
                              tags=("Respected" 
                                    if isinstance(self.cleanData[i][1], str) or self.cleanData[i][1]>float(self.cleanData[i][2] if self.cleanData[i][2] is not None else 0.0) 
                                    else "Not-respected",))
            
        # Pack the table
        #self.table.pack(expand=True, fill=tk.BOTH)
        self.table.place(x=0,y=0)

        # Go to add transaction interface
        self.ModifiyBudget = ttk.Button(self, text="Modify/Fix budget", bootstyle="success", width=20)
        self.ModifiyBudget.place(x=0,y=187.5) #115.5
        self.ModifiyBudget.config(state=tk.DISABLED)
        self.ModifiyBudget['command'] = self.modifyBudget

        # Frame carrying the form to modify the budget
        # The main Frame
        self.modifyInterface = tk.Frame(self, width=200, height=185)
        self.modifyInterface.config(bg="#4B41D7")
        self.modifyInterface.place(x=275,y=0) #115

        # Category area
        self.categoryTextValue = ttk.StringVar()
        self.categoryLabel = ttk.Label(self.modifyInterface, text="Category", font=('Segoe UI', 12), background="#4B41D7")
        self.categoryLabel.place(x=16,y=0.5) 
        self.categoryText = ttk.Entry(self.modifyInterface, font=('Helvetica',8), width=25, bootstyle="info", textvariable=self.categoryTextValue)
        self.categoryText.place(x=16,y=30.5)
        self.categoryText.config(state=tk.DISABLED)

        # Budget area
        self.budgetLabel = ttk.Label(self.modifyInterface, text="New budget", font=('Segoe UI', 12), background="#4B41D7")
        self.budgetLabel.place(x=16,y=60.5) 
        self.budgetText = ttk.Entry(self.modifyInterface, font=('Helvetica',8), width=25, bootstyle="info")
        self.budgetText.place(x=16,y=90.5)

        # Approve button 
        self.approveButton = ttk.Button(self.modifyInterface, text="Approve", bootstyle="success", width=9)
        self.approveButton.place(x=15,y=140.5) #115.5
        self.approveButton.config(state=tk.DISABLED)
        self.approveButton['command'] = self.approveModification

        # Approve button 
        self.cancelButton = ttk.Button(self.modifyInterface, text="Cancel", bootstyle="info", width=7)
        self.cancelButton.place(x=110,y=140.5) #115.5
        self.cancelButton.config(state=tk.DISABLED)
        self.cancelButton['command'] = self.cancelModification

    def selectItem(self, a):
        curItem = self.table.focus()
        self.ModifiyBudget.config(state=tk.NORMAL)

    def deselectItem(self, a):
        curItem = self.table.focus()
        self.table.selection_remove(curItem)
        self.ModifiyBudget.config(state=tk.DISABLED)
    
    def changeFrame(self, background, frame):
        background.tkraise()
        frame.tkraise()

    def modifyBudget(self):
        curItem = self.table.focus()
        self.categoryTextValue.set(self.table.item(curItem)["values"][0])
        self.approveButton.config(state=tk.NORMAL)
        self.cancelButton.config(state=tk.NORMAL)
        self.ModifiyBudget.config(state=tk.DISABLED)
        self.table["selectmode"]="none"
        self.table.bind('<ButtonRelease-1>', lambda *args:None)
        self.table.bind('<ButtonRelease-3>', lambda *args:None)

    def cancelModification(self):
        self.categoryTextValue.set("")
        self.approveButton.config(state=tk.DISABLED)
        self.cancelButton.config(state=tk.DISABLED)
        curItem = self.table.focus()
        self.table.selection_remove(curItem)
        self.ModifiyBudget.config(state=tk.DISABLED)
        self.table["selectmode"]="browse"  
        self.table.bind('<ButtonRelease-1>', self.selectItem)
        self.table.bind('<ButtonRelease-3>', self.deselectItem)    
        curItem = self.table.focus()
        self.table.selection_remove(curItem)

    def approveModification(self):
        try:
            amount = float(self.budgetText.get())
            category = self.categoryText.get()
            self.db.updateBudgetAmount((amount, category))
            self.root.refreshBudget()
        except:
            messagebox.showinfo("Failure", "Please insert a valid amount!")

class CategoryAdd(tk.Frame):
    def __init__(self, root, id):
        self.root = root
        super().__init__(self.root, width=300, height=160)
        self.config(bg="#4B41D7")
        self.place(x=300,y=180) #115

        self.db = Database()
        self.id = id

        # Category area
        self.categoryLabel = ttk.Label(self, text="New category", font=('Segoe UI', 12), background="#4B41D7")
        self.categoryLabel.place(x=25,y=15.5) 
        self.categoryText = ttk.Entry(self, font=('Helvetica',8), width=40, bootstyle="info")
        self.categoryText.place(x=25,y=45.5)

        # Approve button 
        self.approveButton = ttk.Button(self, text="Approve", bootstyle="success", width=15)
        self.approveButton.place(x=25,y=95.5) #115.5
        self.approveButton['command'] = lambda:self.approveCategory()
        #self.approveButton.config(state=tk.DISABLED)

        # Cancel button 
        self.cancelButton = ttk.Button(self, text="Cancel", bootstyle="info", width=15)
        self.cancelButton.place(x=165,y=95.5) #115.5

    def changeFrame(self, background, frame):
        background.tkraise()
        frame.tkraise()
    def setCancelButton(self, background, frame):
        self.cancelButton['command'] = lambda:self.changeFrame(background, frame)
    def approveCategory(self):
        description = self.categoryText.get()
        colorHex = hex(randrange(0,2**24))
        color = "#"+colorHex[2:]
        if(len(description.replace(" ",""))==0):
            messagebox.showinfo("Failure", "Please insert a valid description!")
        else:
            try:
                self.db.insertCategory((description, color, self.id))
                self.db.insertBudget((description, -1))
                self.root.refresh()
            except:
                messagebox.showinfo("Failure", "Please insert a non-existant description!")

class ReportView(tk.Frame):
    def __init__(self, root, id):
        super().__init__(root, width=830, height=380)
        self.root = root
        self.config(bg="#4B41D7")
        self.place(x=20,y=120) #115

        self.db = Database()
        self.id = id
        self.monthYearList = self.getMonthYearList()
        self.chartFrame = tk.Frame(self, width=300, height=220)
        self.chartFrame.config(bg="#D74B41")
        self.chartFrame.place(x=10,y=10) #115
        self.chartFrame.tkraise()

        self.pieChartFrame = tk.Frame(self, width=300, height=220)
        self.pieChartFrame.config(bg="#D74B41")
        self.pieChartFrame.place(x=430,y=10) #115

        # AddTransaction button
        self.ChangeMonthBackButton = ttk.Button(self, text="◀️", bootstyle="success", width=15, command=lambda:self.changeMonthBack())
        self.ChangeMonthBackButton.place(x=246,y=330) #115.5

        # Category area
        self.monthLabel = ttk.Label(self, text=self.currentMonthYear(), font=('Segoe UI', 15), background="#4B41D7")
        self.monthLabel.place(x=386,y=325) 

        # AddTransaction button
        self.ChangeMonthForwardButton = ttk.Button(self, text="▶️", bootstyle="success", width=15, command=lambda:self.changeMonthForward())
        self.ChangeMonthForwardButton.place(x=500,y=330) #115.5

        # Chart generation area
        month, year = self.monthYearNumerical(self.currentMonthYear())
        barChartExpenses, barChartIncome = self.transactionStats(year,month)
        pieChartExpenses, pieChartIncome = self.categoryStats(year,month)

        self.setIncomeButton = ttk.Button(self, text="income", bootstyle='info', command=lambda: self.setIncome(barChartIncome, pieChartIncome))
        self.setIncomeButton.place(x=120, y=330)

        self.setExpensesButton = ttk.Button(self, text="expenses", bootstyle='info', command=lambda: self.setExpenses(barChartExpenses, pieChartExpenses))
        self.setExpensesButton.place(x=30, y=330)

        self.create_graph(barChartIncome, pieChartIncome)
        self.setIncomeButton.config(state=tk.DISABLED)

        print(self.currentMonthYear())
        print(self.monthYearNumerical(self.monthLabel.cget("text")))
        print(self.getMonthYearList())

    def calendarGeneration(self, year):
        list_of_months = list(calendar.month_name)[1:]
        monthDict = {}
        for i in range(len(list_of_months)):
            monthDict[list_of_months[i]] = calendar.monthrange(int(year), i+1)[1]
        return monthDict

    def currentMonthYear(self):
        list_of_months = list(calendar.month_name)[1:]
        current_month = datetime.datetime.now().month
        return list_of_months[current_month-1] + "-" + str(datetime.datetime.now().year)  
    
    def monthYearNumerical(self, monthYearString):
        monthYearStringList = monthYearString.split("-")
        list_of_months = list(calendar.month_name)[1:]
        chosenMonth = list_of_months.index(monthYearStringList[0]) + 1
        chosenYear = int(monthYearStringList[1])
        return chosenMonth, chosenYear
    
    def getMonthYearList(self):
        list_of_months = list(calendar.month_name)[1:]
        allTransactions = self.db.getTransactions((self.id,))
        monthYearList = []
        for transaction in allTransactions :
            year = int(transaction[0].split("-")[2])
            month = int(transaction[0].split("-")[1])
            monthYearList.append(list_of_months[month-1] + "-" + str(year))
        return list(dict.fromkeys(monthYearList))

    def transactionStats(self, chosenYear, chosenMonth):
        allTransactions = self.db.getTransactions((self.id,))
        yearlyExpenses = {}
        yearlyIncome = {}
        for transaction in allTransactions :
            year = int(transaction[0].split("-")[2])
            month = int(transaction[0].split("-")[1])
            day = int(transaction[0].split("-")[0])
            if(transaction[1]=='Expense'):
                if(year not in yearlyExpenses):
                    yearlyExpenses[year] = {}
                if(month not in yearlyExpenses[year]):
                    yearlyExpenses[year][month] = {}
                dailyExpense = yearlyExpenses[year][month][day] + transaction[2] if day in yearlyExpenses[year][month] else transaction[2] 
                yearlyExpenses[year][month][day] = dailyExpense
            else:
                if(year not in yearlyIncome):
                    yearlyIncome[year] = {}
                if(month not in yearlyIncome[year]):
                    yearlyIncome[year][month] = {}
                dailyIncome = yearlyIncome[year][month][day] + transaction[2] if day in yearlyIncome[year][month] else transaction[2] 
                yearlyIncome[year][month][day] = dailyIncome
        #return yearlyExpenses[chosenYear][chosenMonth], yearlyIncome[chosenYear][chosenMonth]
        return yearlyExpenses.get(chosenYear,{}).get(chosenMonth,{}), yearlyIncome.get(chosenYear,{}).get(chosenMonth,{})

    def categoryStats(self, chosenYear, chosenMonth):
        allTransactions = self.db.getTransactions((self.id,))
        incomeCategoryPercentage = {}
        expensesCategoryPercentage = {}
        for transaction in allTransactions :
            year = int(transaction[0].split("-")[2])
            month = int(transaction[0].split("-")[1])
            if(transaction[1]=='Income'):
                if(year not in incomeCategoryPercentage):
                    incomeCategoryPercentage[year] = {}
                if(month not in incomeCategoryPercentage[year]):
                    incomeCategoryPercentage[year][month] = {}
                incomeCategoryPercentage[year][month][transaction[3]] = incomeCategoryPercentage[year][month][transaction[3]] + 1 if transaction[3] in incomeCategoryPercentage[year][month] else 1
            else:    
                if(year not in expensesCategoryPercentage):
                    expensesCategoryPercentage[year] = {}
                if(month not in expensesCategoryPercentage[year]):
                    expensesCategoryPercentage[year][month] = {}
                expensesCategoryPercentage[year][month][transaction[3]] = expensesCategoryPercentage[year][month][transaction[3]] + 1 if transaction[3] in expensesCategoryPercentage[year][month] else 1
        return expensesCategoryPercentage.get(chosenYear,{}).get(chosenMonth,{}), incomeCategoryPercentage.get(chosenYear,{}).get(chosenMonth,{})

    def create_graph(self, barChartData, pieChartData):
        style.use("_mpl-gallery")
        self.fig = Figure(figsize=(4, 3), dpi=100)
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.ax1.set_xlabel('Day')
        self.ax1.set_ylabel('Amount', color='g')
        self.fig.tight_layout()

        barChartDataInitialX = list(barChartData.keys())
        barChartDataInitialY = list(barChartData.values())
        barChartDataX = [i for i in range(1,32)]
        barChartDataY = [0*i for i in range(1,32)]
        for x in range(len(barChartDataInitialX)) :
            barChartDataY[barChartDataInitialX[x]] = barChartDataInitialY[x]
        self.ax1.bar(barChartDataX, barChartDataY)

        self.graph = FigureCanvasTkAgg(self.fig, master=self.chartFrame)
        self.canvas = self.graph.get_tk_widget()
        self.canvas.grid(row=0, column=0)

        self.labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        self.sizes = [15, 30, 45, 10]

        style.use("_mpl-gallery")
        self.fig2 = Figure(figsize=(3.8, 3), dpi=100)
        self.ax2 = self.fig2.add_subplot(1, 1, 1)
        self.fig2.tight_layout()

        self.ax2.pie(pieChartData.values(), labels=pieChartData.keys(), autopct='%1.1f%%')

        self.graph2 = FigureCanvasTkAgg(self.fig2, master=self.pieChartFrame)
        self.canvas2 = self.graph2.get_tk_widget()
        self.canvas2.grid(row=0, column=0)

    '''
    def transactionData(self, month, year):
        yearlyExpenses, yearlyIncome = self.transactionStats()
        calendarDays = self.calendarGeneration(year)
        data = []
    '''

    def setIncome(self, barChartData, pieChartData):
        self.setIncomeButton.config(state=tk.DISABLED)
        self.setExpensesButton.config(state=tk.NORMAL)
        self.create_graph(barChartData, pieChartData)

    def setExpenses(self, barChartData, pieChartData):
        self.setExpensesButton.config(state=tk.DISABLED)
        self.setIncomeButton.config(state=tk.NORMAL)
        self.create_graph(barChartData, pieChartData)

    def changeMonthBack(self):
        index = self.monthYearList.index(self.monthLabel.cget("text"))
        index = index - 1 if index>0 else index
        self.monthLabel['text'] = self.monthYearList[index]
        self.refreshCharts(index)

    def changeMonthForward(self):
        index = self.monthYearList.index(self.monthLabel.cget("text"))
        index = index + 1 if index<len(self.monthYearList)-1 else index
        self.monthLabel['text'] = self.monthYearList[index]
        self.refreshCharts(index)

    def refreshCharts(self, index):
        month, year = self.monthYearNumerical(self.monthYearList[index])
        barChartExpenses, barChartIncome = self.transactionStats(year, month)
        pieChartExpenses, pieChartIncome = self.categoryStats(year, month)
        self.setIncomeButton['command'] = lambda: self.setIncome(barChartIncome, pieChartIncome)
        self.setExpensesButton['command'] = lambda: self.setExpenses(barChartExpenses, pieChartExpenses)
        self.create_graph(barChartIncome, pieChartIncome)
        self.setExpensesButton.config(state=tk.NORMAL)
        self.setIncomeButton.config(state=tk.NORMAL)
        self.setIncomeButton.config(state=tk.DISABLED)

class MainBackground(tk.Frame):
    def __init__(self, root, id):
        self.db = Database()
        self.id = id
        self.balanceAmount = self.db.getUserBalance((self.id,))[0][0]
        self.moneyPng = ImageTk.PhotoImage(Image.open('money.png'))
        # Setting up the main frame
        self.root = root
        super().__init__(self.root, width=1066, height=768)
        self.config(bg="#2b3e50")
        self.place(x=300,y=0)

        # Placing the report option frame
        self.reportView = ReportView(self, self.id)

        # Placing the budget option frame
        self.budgetView = BudgetView(self, self.id)

        # Placing the add category frame
        self.categoryAdd = CategoryAdd(self, self.id)

        # Placing the background
        self.background = tk.Frame(self, width=1066, height=768)
        self.background.config(bg="#2b3e50")
        self.background.place(x=0,y=0)

        #Placing the label with the balance amount
        self.balance = tk.Frame(self.background, width=200, height=50)
        self.balance.config(bg="#46919e")
        self.balance.place(x=650,y=20)
        self.labelMoney = tk.Label(self.balance, image=self.moneyPng, height=50 ,width=50 ,borderwidth=0)
        self.labelMoney.config(bg="#46919e")
        self.labelMoney.place(x=5, y=0)
        self.balanceAmountLabel = ttk.Label(self.balance, text=self.balanceAmount, font=('Segoe UI', 20), background="#46919e")
        self.balanceAmountLabel.place(x=50, y=0)

        # Placing the add category frame
        self.categoryAdd = CategoryAdd(self, self.id)
        self.categoryAdd.tkraise()

        # Placing the transaction option frame
        self.transactionView = TransactionView(self, id)
        self.background.tkraise()

        # Allowing switch between transaction frames
        self.transactionAdd = TransactionAdd(self, id)
        self.transactionAdd.setViewTransactionButton(self.background, self.transactionView)
        self.transactionView.setAddTransactionButton(self.background, self.transactionAdd)
        self.transactionAdd.setAddCategoryButton(self.background, self.categoryAdd)
        self.categoryAdd.setCancelButton(self.background, self.transactionAdd)

        # Starting screen
        self.background.tkraise()

    # Method for bringing the transaction interface upfront
    def showTransaction(self):
        self.background.tkraise()
        self.transactionView.tkraise()
        self.background.tkraise()
        self.transactionAdd.tkraise()

    # Method for bringing the budget interface upfront
    def showBudget(self):
        self.background.tkraise()
        self.budgetView.tkraise()

    def showReport(self):
        self.background.tkraise()
        self.reportView.tkraise()

    def showCategoryAdd(self):
        self.background.tkraise()
        self.categoryAdd.tkraise()
    
    def refreshBudget(self):
        # Placing the budget frame
        self.budgetView = BudgetView(self, self.id)
        self.background.tkraise()    
        self.budgetView.tkraise()    

    def refresh(self):

        # Placing the report frame
        self.reportView = ReportView(self, self.id)
        self.background.tkraise()

        # Placing the budget frame
        self.budgetView = BudgetView(self, self.id)
        self.background.tkraise()
        
        # Placing the transaction option frame
        self.transactionView = TransactionView(self, self.id)
        self.background.tkraise()

        # Allowing switch between transaction frames
        self.transactionAdd = TransactionAdd(self, self.id)
        self.transactionAdd.setViewTransactionButton(self.background, self.transactionView)
        self.transactionView.setAddTransactionButton(self.background, self.transactionAdd)
        self.transactionAdd.setAddCategoryButton(self.background, self.categoryAdd)
        self.categoryAdd.setCancelButton(self.background, self.transactionAdd)

    def updateBalance(self, amount):
        #Updating the balance
        currentBalance = float(self.db.getUserBalance((self.id,))[0][0])
        currentBalance = currentBalance + amount
        self.db.setUserBalance((currentBalance, self.id))
        self.balanceAmountLabel['text'] = str(currentBalance)

class Hello(tk.Frame):
    def __init__(self, root):
        super().__init__(root,width=300, height=150)
        self.root = root
    def setBackButtonCommand(self, frame):
        self.button['command'] = lambda:self.raise_frame(frame)
    def raise_frame(self, frame):
        newFrame = Main(frame.root)
        newFrame.place(x=0, y=0)
        newFrame.tkraise()
    def setDashboard(self, id):

        # Importing the profile and exit icons
        self.profile = ImageTk.PhotoImage(Image.open('profile.png'))
        self.off = ImageTk.PhotoImage(Image.open('off.png'))

        # Placing the frame
        self.place(x=438,y=234)

        # Left window area
        self.left_window = tk.Frame(self.root, width=300, height=768)
        self.left_window.config(bg="#46919e")
        self.left_window.place(x=0,y=0)

        # Main interface:
        self.mainBackground = MainBackground(self.root, id) 

        # Username label
        self.label = ttk.Label(self.left_window, text=id, font=('Segoe UI', 40), background="#46919e")
        self.label.place(x=80,y=0.5)

        # Disconnect button
        self.button = tk.Button(self.left_window, image=self.off, height=50 ,width=50 ,borderwidth=0)
        self.button.config(bg="#46919e")
        self.button.place(x=220,y=15)

        # Profile picture
        self.labelProfile = tk.Label(self.left_window, image=self.profile, height=50 ,width=50 ,borderwidth=0)
        self.labelProfile.config(bg="#46919e")
        self.labelProfile.place(x=20,y=15)

        # Button area
        # Transaction button
        self.buttonTransaction = ttk.Button(self.left_window, text="Transactions", bootstyle="info", width=30)
        self.buttonTransaction['command'] = lambda:self.mainBackground.showTransaction()
        self.buttonTransaction.place(x=50,y=120)

        # Budget button
        self.buttonBudget = ttk.Button(self.left_window, text="Budget", bootstyle="info", width=30)
        self.buttonBudget['command'] = lambda:self.mainBackground.showBudget()
        self.buttonBudget.place(x=50,y=170)

        #Report button
        self.buttonReport = ttk.Button(self.left_window, text="Report", bootstyle="info", width=30)
        self.buttonReport['command'] = lambda:self.mainBackground.showReport()
        self.buttonReport.place(x=50,y=220)

        """
        self.buttonViewReport = ttk.Button(self.left_window, text="view report", bootstyle="info", width=30)
        self.buttonViewReport.place(x=50,y=270)
        """       

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root, height = root.winfo_screenheight()-200, width = root.winfo_screenwidth()-200)
        #self.mainframe.place(x=0,y=0)
        #self.mainframe.tkraise()
        #400x300
        #1366x768
        self.root = root
        self.title = ttk.Label(self, font=('Segoe UI',25), text="PennyWise")
        self.title.place(x=500,y=2)
        self.subtitle = ttk.Label(self, font=('Segoe UI',15), text="Know where your money at")
        self.subtitle.place(x=465,y=50)
        self.frame_background = tk.Frame(self, width=300, height=200)
        self.frame_background.config(bg="#2b3e50")
        self.frame3 = Signup(self)
        
        self.frame_background.place(x=438,y=234) #115
        self.frame_background.tkraise()
        self.frame1 = Login(self)
        self.frame1.setLoginButtonCommand(self)
        #self.frame2.setBackButtonCommand(self.frame1,self.frame_background)
        self.frame3.setSignupButtonCommand(self.frame1,self.frame_background)
        self.frame3.setLoginButtonCommand(self.frame1,self.frame_background)
        self.frame1.setSignupButtonCommand(self.frame3,self.frame_background)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style(theme='superhero')
        self.title('Login App')
        self.width = self.winfo_screenwidth() 
        self.height = self.winfo_screenheight()
        self.geometry("%dx%d" % (self.width-200, self.height-200))
        self.mainframe = Main(self)
        self.mainframe.place(x=0, y=0)
        self.mainframe.tkraise()

if __name__ == "__main__":
    root = App()
    root.mainloop() 

    #x = datetime.datetime.now()
    #print(root.width, root.height)  

    #db = Database()
    #db.startOver()
    #db.startOver()
    #(description,amount,income,tdate,category,username)
    #print(db.getCategories())
    #db.insertCategory(("car","#1536f3"))
    #db.insertTransaction(("friendo",50.0,"Income","2026-08-26","car","wild6"))
    #db.insertUser(("wild6","xxx",1000.0))

    #print([db.getCategories()[i][0] for i in range(len(db.getCategories()))])
    #print([i*2 for i in range(2)])
    #print(db.getTransactions(("jimx",)))
    #print(db.getUsernames())
    #print(db.getUserBalance(("jimx",))[0][0])
    #db.setUserBalance((10020.0,"jimx"))
    #print(db.getUserBalance(("jimx",))[0][0])
    

    
    

