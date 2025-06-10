import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
import sqlite3
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
        super().__init__(root, width=300, height=150) 
        self.db = Database()
        self.config(bg="#4B41D7")
        self.place(x=50,y=115) 
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
    def setLoginButtonCommand(self, frame, background):
        self.login_button['command'] = lambda:self.login(frame, background)
    def setSignupButtonCommand(self, frame, background):
        self.signup_button['command'] = lambda:self.signup(frame, background)
    def login(self, frame, background):
        if self.db.isUserExist((self.text1.get(),self.text2.get())) :
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
        self.place(x=50,y=85) #115
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
        self.place(x=50,y=115)
        self.label = ttk.Label(self, text="Hello user!", font=('Segoe UI', 40))
        self.label.place(x=16,y=0.5)
        self.button = ttk.Button(self, text="back", bootstyle="success", width=20)
        self.button.place(x=70,y=115.5)
    def setBackButtonCommand(self, frame, background):
        self.button['command'] = lambda:self.raise_frame(frame, background)
    def raise_frame(self, frame, background):
        background.tkraise()
        frame.tkraise()
class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style(theme='superhero')
        self.title('Login App')
        self.geometry('400x300')
        self.title = ttk.Label(self, font=('Segoe UI',25), text="PennyWise")
        self.title.place(x=115,y=2)
        self.subtitle = ttk.Label(self, font=('Segoe UI',15), text="Know where your money at")
        self.subtitle.place(x=75,y=50)
        self.frame_background = tk.Frame(self, width=300, height=200)
        self.frame_background.config(bg="#2b3e50")
        self.frame3 = Signup(self)
        self.frame2 = Hello(self)
        self.frame_background.place(x=50,y=85) #115
        self.frame_background.tkraise()
        self.frame1 = Login(self)
        self.frame1.setLoginButtonCommand(self.frame2,self.frame_background)
        self.frame2.setBackButtonCommand(self.frame1,self.frame_background)
        self.frame3.setSignupButtonCommand(self.frame1,self.frame_background)
        self.frame3.setLoginButtonCommand(self.frame1,self.frame_background)
        self.frame1.setSignupButtonCommand(self.frame3,self.frame_background)
if __name__ == "__main__":
    root = Main()
    root.mainloop()   
    """
    db = Database()
    db.startOver()
    """
    #print(db.isUserExist(('wildcat6','xxx')))

