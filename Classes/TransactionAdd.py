import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime

from .Database import Database

class TransactionAdd(tk.Frame):
    """
    TransactionAdd constructor method
    """
    def __init__(self, root, id):

        self.root = root
        self.id = id
        self.db = Database()
        self.add = ImageTk.PhotoImage(Image.open('Ressources/add.png'))

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
        self.daySpinbox = ttk.Spinbox(self, from_=1, to=31, width=5, textvariable=self.day_ValueInside)
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
        #self.category_Options = ["Groceries", "Car", "Groceries", "Phone"]
        self.category_Options = [self.db.getCategoriesId(self.id)[i][0] for i in range(len(self.db.getCategoriesId(self.id)))]
        self.category_Options.insert(0,"")
        self.category_ValueInside = tk.StringVar(self)
        self.category_ValueInside.set("")
        self.category_QuestionMenu = ttk.OptionMenu(self, self.category_ValueInside, *self.category_Options, bootstyle="dark")
        self.category_QuestionMenu.place(x=16,y=215.5)
        self.AddCategoryButton = ttk.Button(self, text="+", bootstyle="success", width=1)
        
        self.addCategoryButton = tk.Button(self, image=self.add, height=15 ,width=15 ,borderwidth=0)
        self.addCategoryButton.config(bg="#4B41D7")
        self.addCategoryButton.place(x=85,y=188.5)
        #self.addCategoryButton['command'] = lambda:self.printFormInfos()
        #self.AddCategoryButton.place(x=85,y=183.5) #115.5

        # Income/Expense area
        self.incomeExpenselabel = ttk.Label(self, text="Income/Expense", font=('Segoe UI', 12), background="#4B41D7")
        self.incomeExpenselabel.place(x=150,y=183.5)
        self.incomeExpense_Options = ["", "Expense", "Income"]
        self.incomeExpense_ValueInside = tk.StringVar(self)
        self.incomeExpense_ValueInside.set("Expense")
        self.incomeExpense_QuestionMenu = ttk.OptionMenu(self, self.incomeExpense_ValueInside, *self.incomeExpense_Options, bootstyle="dark")
        self.incomeExpense_QuestionMenu.place(x=160,y=215.5)

        # AddTransaction button
        self.AddTransactionButton = ttk.Button(self, text="Add transaction", bootstyle="success", width=15)
        self.AddTransactionButton.place(x=16,y=260.5) #115.5
        self.AddTransactionButton['command'] = lambda:self.printFormInfos()
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

    """
    setAddCategoryButton: Method to set which frame to switch to in changeFrame
    """
    def setAddCategoryButton(self, background, frame):
        self.addCategoryButton['command'] = lambda:self.changeFrame(background, frame)

    def printFormInfos(self):
        try:
            amount = float(self.amountText.get())
            amountIsValid = True
        except:
            amountIsValid = False
        description = self.descriptionText.get()
        day = self.day_ValueInside.get()
        month = self.month_ValueInside.get()
        year = self.year_ValueInside.get()
        date = day+"-"+month+"-"+year
        ttype = self.incomeExpense_ValueInside.get()
        category = self.category_ValueInside.get()

        descriptionIsValid = description.replace(" ", "")!=""
        date1 = day=="31" and (month in ["2", "4", "6", "9", "11"])
        date2 = day=="30" and month=="2"
        date3 = day=="29" and month=="2" and int(year)%4!=0
        dateIsValid = not date1 and not date2 and not date3
        categoryIsValid = category.replace(" ", "")!=""

        if(not amountIsValid):
            messagebox.showinfo("Failure", "Please insert a valid amount!")
        elif(not descriptionIsValid):
            messagebox.showinfo("Failure", "Please insert a valid description!")
        elif(not dateIsValid):
            messagebox.showinfo("Failure", "Please insert a valid date!")
        elif(not categoryIsValid):
            messagebox.showinfo("Failure", "Please choose or create a category!")
        else:
            messagebox.showinfo("Success", "Transaction added successfully!")
            self.db.insertTransaction((description,amount,ttype,date,category,self.id))
            self.root.refresh()
            operationType = (-1)**int(bin(ttype=="Expense")[2:])
            self.root.updateBalance(operationType*amount)
            expenses = self.db.getCategoryExpenses((category))[0][0]
            budget = self.db.getBudgetAmount((category))[0][0]
            if(expenses>=budget and budget>=0):
                messagebox.showinfo("Warning!", "A budget was not respected. Please check the budget table")
