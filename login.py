import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('example.db')  # Creates a new database file if it doesn’t exist
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()
    def __createDatabase(self):
        self.cursor.executescript("""
                    create table `user`( 
                        username varchar(50) PRIMARY KEY,
                        pin varchar(50),
                        balance float
                    );
                    create table `category`(
                        name varchar(50) PRIMARY KEY,
                        colour varcher(7)
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
        self.conn.commit()
    def __dropDatabase(self):
        self.cursor.executescript("""
                     drop table budget;
                     drop table `transaction`;
                     drop table category;
                     drop table user;
                    """)
        self.conn.commit()
    def startOver(self):
        self.__dropDatabase()
        self.__createDatabase()
    def insertUser(self, data):
        self.cursor.execute("insert into user values (?,?,?)", data)
        self.conn.commit()
    def isUserExist(self, data):
        self.cursor.execute("select count(*) from user where username = ? and pin = ?", data)
        return self.cursor.fetchall()[0][0]!=0
    def getUserBalance(self, data):
        self.cursor.execute("select balance from user where username = ? and pin = ?", data)
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
    def setLoginButtonCommand(self, background):
        self.login_button['command'] = lambda:self.login(self.hello, background)
    def setSignupButtonCommand(self, frame, background):
        self.signup_button['command'] = lambda:self.signup(frame, background)
    def login(self, frame, background):
        if self.db.isUserExist((self.text1.get(),self.text2.get())) :
            self.hello.setDashboard(self.text1.get())
            self.hello.setBackButtonCommand(self, background)
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
    def __init__(self, root):
        
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
        self.daySpinbox = ttk.Spinbox(self, from_=1, to=30, width=5, textvariable=self.day_ValueInside)
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
        self.category_Options = ["Groceries", "Car", "Groceries", "Phone"]
        self.category_ValueInside = tk.StringVar(self)
        self.category_ValueInside.set("Expense")
        self.category_QuestionMenu = ttk.OptionMenu(self, self.category_ValueInside, *self.category_Options, bootstyle="dark")
        self.category_QuestionMenu.place(x=16,y=215.5)
        self.AddCategoryButton = ttk.Button(self, text="+", bootstyle="success", width=1)
        
        self.addCategoryButton = tk.Button(self, image=self.add, height=15 ,width=15 ,borderwidth=0)
        self.addCategoryButton.config(bg="#4B41D7")
        self.addCategoryButton.place(x=85,y=188.5)
        #self.AddCategoryButton.place(x=85,y=183.5) #115.5

        # Income/Expense area
        self.incomeExpenselabel = ttk.Label(self, text="Income/Expense", font=('Segoe UI', 12), background="#4B41D7")
        self.incomeExpenselabel.place(x=150,y=183.5)
        self.incomeExpense_Options = ["Income", "Expense", "Income"]
        self.incomeExpense_ValueInside = tk.StringVar(self)
        self.incomeExpense_ValueInside.set("Expense")
        self.incomeExpense_QuestionMenu = ttk.OptionMenu(self, self.incomeExpense_ValueInside, *self.incomeExpense_Options, bootstyle="dark")
        self.incomeExpense_QuestionMenu.place(x=160,y=215.5)

        # AddTransaction button
        self.AddTransactionButton = ttk.Button(self, text="Add transaction", bootstyle="success", width=15)
        self.AddTransactionButton.place(x=16,y=260.5) #115.5

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

class TransactionView(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=504, height=225)
        self.config(bg="#2b3e50")
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
        self.data = [
            ('07/07/2025', 'Income', 300.01, 'Shopping', 'groceries'),
            ('17/07/2025', 'Expanse', 10.01, 'Shopping', 'interest'),
            ('17/07/2025', 'Expanse', 10.01, 'Shopping', 'interest')
        ]

        # Configure alternating row colors
        '''
        self.table.tag_configure('oddrow', background="#5F07EC")
        self.table.tag_configure('evenrow', background="#082470")
        '''

        # Configure alternating row colors
        self.table.tag_configure('Income', background="#29BB15")
        self.table.tag_configure('Expanse', background="#FA0808")

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
    def __init__(self, root):
        super().__init__(root, width=504, height=225)
        self.config(bg="#2b3e50")
        self.place(x=200,y=180) #115
        self.table = ttk.Treeview(self)

        # Define the columns
        self.table['columns'] = ('Category', 'Budget')

        # Format the columns
        self.table.column('#0', width=0, stretch=tk.NO)
        self.table.column('Category', anchor=tk.W, width=100)
        self.table.column('Budget', anchor=tk.W, width=100)

        # Create the headings
        self.table.heading('#0', text='', anchor=tk.W)
        self.table.heading('Category', text='Category', anchor=tk.W)
        self.table.heading('Budget', text='Budget', anchor=tk.W)

        # Sample data
        self.data = [
            ('Shopping', 300.01),
            ('Car', 10.01),
            ('Groceries', 10.01)
        ]

        # Configure alternating row colors
        '''
        self.table.tag_configure('oddrow', background="#5F07EC")
        self.table.tag_configure('evenrow', background="#082470")
        '''

        # Configure alternating row colors
        self.table.tag_configure('Income', background="#29BB15")
        self.table.tag_configure('Expanse', background="#FA0808")

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
            self.table.insert(parent='', index=i, values=self.data[i], tags=("Expanse",))
            
        # Pack the table
        #self.table.pack(expand=True, fill=tk.BOTH)
        self.table.place(x=0,y=0)

        # Go to add transaction interface
        self.AddTransactionButton = ttk.Button(self, text="Modify/Fix budget", bootstyle="success", width=20)
        self.AddTransactionButton.place(x=0,y=187.5) #115.5

        # Frame carrying the form to modify the budget
        # The main Frame
        self.modifyInterface = tk.Frame(self, width=200, height=185)
        self.modifyInterface.config(bg="#4B41D7")
        self.modifyInterface.place(x=250,y=0) #115

        # Category area
        self.categoryLabel = ttk.Label(self.modifyInterface, text="Category", font=('Segoe UI', 12), background="#4B41D7")
        self.categoryLabel.place(x=16,y=0.5) 
        self.categoryText = ttk.Entry(self.modifyInterface, font=('Helvetica',8), width=25, bootstyle="info")
        self.categoryText.place(x=16,y=30.5)
        self.categoryText.config(state=tk.DISABLED)

        # Budget area
        self.budgetLabel = ttk.Label(self.modifyInterface, text="Budget", font=('Segoe UI', 12), background="#4B41D7")
        self.budgetLabel.place(x=16,y=60.5) 
        self.budgetText = ttk.Entry(self.modifyInterface, font=('Helvetica',8), width=25, bootstyle="info")
        self.budgetText.place(x=16,y=90.5)

        # Approve button 
        self.approveButton = ttk.Button(self.modifyInterface, text="Approve", bootstyle="success", width=20)
        self.approveButton.place(x=25,y=140.5) #115.5
        self.approveButton.config(state=tk.DISABLED)

    def changeFrame(self, background, frame):
        background.tkraise()
        frame.tkraise()
    def setAddTransactionButton(self, background, frame):
        self.AddTransactionButton['command'] = lambda:self.changeFrame(background, frame)

class MainBackground(tk.Frame):
    def __init__(self, root):

        # Setting up the main frame
        self.root = root
        super().__init__(self.root, width=1066, height=768)
        self.config(bg="#2b3e50")
        self.place(x=300,y=0)

        # Placing the budget option frame
        self.budgetView = BudgetView(self)

        # Placing the background
        self.background = tk.Frame(self, width=1066, height=768)
        self.background.config(bg="#2b3e50")
        self.background.place(x=0,y=0)
        
        # Placing the transaction option frame
        self.transactionView = TransactionView(self)
        self.background.tkraise()

        # Allowing switch between transaction frames
        self.transactionAdd = TransactionAdd(self)
        self.transactionAdd.setViewTransactionButton(self.background, self.transactionView)
        self.transactionView.setAddTransactionButton(self.background, self.transactionAdd)

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

class Hello(tk.Frame):
    def __init__(self, root):
        super().__init__(root,width=300, height=150)
        self.root = root
    def setBackButtonCommand(self, frame, background):
        self.button['command'] = lambda:self.raise_frame(frame, background)
    def raise_frame(self, frame, background):
        background.tkraise()
        frame.tkraise()
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
        self.mainBackground = MainBackground(self.root) 

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
        self.buttonReport.place(x=50,y=220)

        """
        self.buttonViewReport = ttk.Button(self.left_window, text="view report", bootstyle="info", width=30)
        self.buttonViewReport.place(x=50,y=270)
        """       

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style(theme='superhero')
        self.title('Login App')
        self.width= self.winfo_screenwidth() 
        self.height= self.winfo_screenheight()
        self.geometry("%dx%d" % (self.width-200, self.height-200))
        #400x300
        #1366x768
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
        self.frame1.setLoginButtonCommand(self.frame_background)
        #self.frame2.setBackButtonCommand(self.frame1,self.frame_background)
        self.frame3.setSignupButtonCommand(self.frame1,self.frame_background)
        self.frame3.setLoginButtonCommand(self.frame1,self.frame_background)
        self.frame1.setSignupButtonCommand(self.frame3,self.frame_background)

if __name__ == "__main__":
    
    root = Main()
    root.mainloop() 
    #x = datetime.datetime.now()
    #print(root.width, root.height)  
    '''
    db = Database()
    db.startOver()
    '''
    #print(db.isUserExist(('wildcat6','xxx')))

