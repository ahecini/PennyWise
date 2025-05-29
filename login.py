import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
class Login:
    def __init__(self, root, frame):
        self.root = root
        self.style = ttk.Style(theme='superhero')
        self.root.title('Login App')
        self.root.geometry('400x300')
        self.frame = tk.Frame(self.root, width=300, height=150)
        self.frame.config(bg="#4B41D7")
        self.frame.place(x=50,y=115)
        #self.button1 = ttk.Button(self.frame, text='button1', bootstyle='info', command=self.popup, width='300px')
        #self.button1.place(x=16,y=57.5)
        self.label1 = ttk.Label(self.frame, text="user", font=('Segoe UI', 12), background="#4B41D7")
        self.label1.place(x=16,y=0.5)
        self.label2 = ttk.Label(self.frame, text="password", font=('Segoe UI', 12), background="#4B41D7")
        self.label2.place(x=16,y=50.5)
        
        self.text1 = ttk.Entry(self.frame, font=('Helvetica',8), width=40, bootstyle="info")
        self.text1.place(x=16,y=20.5)
        self.text2 = ttk.Entry(self.frame, font=('Helvetica',8), width=40, bootstyle="info")
        self.text2.place(x=16,y=70.5)

        self.title = ttk.Label(self.root, font=('Segoe UI',25), text="PennyWise")
        self.title.place(x=115,y=2)
        self.subtitle = ttk.Label(self.root, font=('Segoe UI',15), text="Know where your money at")
        self.subtitle.place(x=75,y=50)

        self.login_button = ttk.Button(self.frame, text="Login", bootstyle="success", width=20, command = self.login(frame))
        self.login_button.place(x=16,y=115.5)
        self.signup_button = ttk.Button(self.frame, text="Sign up", bootstyle="info", width=13)
        self.signup_button.place(x=170,y=115.5)
        #self.button2.pack()
        #self.button3 = ttk.Button(self.frame, text='button3', bootstyle='warning')
        #self.button3.pack()
    def popup(self):
        messagebox.showinfo("Success", "Login successful!")
    def login(self, frame):
        frame.tkraise()
if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.config(bg="#ffffff")
    gui = Login(root,frame)
    #print(help(ttk.Style))
    root.mainloop()