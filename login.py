import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
class Login(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=300, height=150)
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
    def setButtonCommand(self, frame):
        self.login_button['command'] = lambda:frame.tkraise()
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
    def setButtonCommand(self, frame):
        self.button['command'] = lambda:frame.tkraise()
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
        self.frame2 = Hello(self)
        self.frame1 = Login(self)
        self.frame1.setButtonCommand(self.frame2)
        self.frame2.setButtonCommand(self.frame1)
if __name__ == "__main__":
    root = Main()
    root.mainloop()