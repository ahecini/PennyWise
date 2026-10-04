import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox

from .Database import Database

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
