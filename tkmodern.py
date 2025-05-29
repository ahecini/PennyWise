import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox

class GUI:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style(theme='darkly')
        self.root.title('GUI App')
        self.root.geometry('200x100')

        self.button1 = ttk.Button(root, text='button1', bootstyle='info', command=self.popup)
        self.button1.pack()

        self.button2 = ttk.Button(root, text='button2', bootstyle='success')
        self.button2.pack()

        self.button3 = ttk.Button(root, text='button3', bootstyle='warning')
        self.button3.pack()
    def popup(self):
        messagebox.showinfo("Success", "Login successful!")
if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()