import tkinter as tk
import ttkbootstrap as ttk

from .Main import Main

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