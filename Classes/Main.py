import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from PIL import Image, ImageTk

from .Signup import Signup
from .Database import Database
from .MainBackground import MainBackground


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
        self.profile = ImageTk.PhotoImage(Image.open('Ressources/profile.png'))
        self.off = ImageTk.PhotoImage(Image.open('Ressources/off.png'))

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
