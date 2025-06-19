import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
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
            background.tkraise()
            frame.tkraise()
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
        self.profile = ImageTk.PhotoImage(Image.open('profile.png'))
        self.off = ImageTk.PhotoImage(Image.open('off.png'))
        #self.off.resize((60,60), Image.ANTIALIAS)
        #self.profile = tk.PhotoImage("profile.png")
        self.place(x=438,y=234)
        self.left_window = tk.Frame(self.root, width=300, height=768)
        self.left_window.config(bg="#46919e")
        self.left_window.place(x=0,y=0)
        self.label = ttk.Label(self.left_window, text= id, font=('Segoe UI', 40), background="#46919e")
        self.label.place(x=80,y=0.5)
        self.button = tk.Button(self.left_window, image=self.off, height=50 ,width=50 ,borderwidth=0)
        self.button.config(bg="#46919e")
        self.button.place(x=220,y=15)
        self.labelProfile = tk.Label(self.left_window, image=self.profile, height=50 ,width=50 ,borderwidth=0)
        self.labelProfile.config(bg="#46919e")
        self.labelProfile.place(x=20,y=15)
        self.buttonViewTransaction = ttk.Button(self.left_window, text="view transaction", bootstyle="info", width=30)
        self.buttonViewTransaction.place(x=50,y=120)
        self.buttonAddTransaction = ttk.Button(self.left_window, text="add transaction", bootstyle="info", width=30)
        self.buttonAddTransaction.place(x=50,y=170)
        self.buttonViewBudget = ttk.Button(self.left_window, text="view budget", bootstyle="info", width=30)
        self.buttonViewBudget.place(x=50,y=220)
        self.buttonViewReport = ttk.Button(self.left_window, text="view report", bootstyle="info", width=30)
        self.buttonViewReport.place(x=50,y=270)
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
    print(root.width, root.height)  
    """
    db = Database()
    db.startOver()
    """
    #print(db.isUserExist(('wildcat6','xxx')))

