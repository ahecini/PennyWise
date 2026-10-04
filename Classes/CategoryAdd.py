import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from random import randrange

from .Database import Database

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