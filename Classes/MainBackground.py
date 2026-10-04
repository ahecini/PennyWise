import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk

from .Database import Database
from .ReportView import ReportView
from .BudgetView import BudgetView
from .CategoryAdd import CategoryAdd
from .TransactionView import TransactionView
from .TransactionAdd import TransactionAdd

class MainBackground(tk.Frame):
    def __init__(self, root, id):
        self.db = Database()
        self.id = id
        self.balanceAmount = self.db.getUserBalance((self.id,))[0][0]
        self.moneyPng = ImageTk.PhotoImage(Image.open('Ressources/money.png'))
        # Setting up the main frame
        self.root = root
        super().__init__(self.root, width=1066, height=768)
        self.config(bg="#2b3e50")
        self.place(x=300,y=0)

        # Placing the report option frame
        self.reportView = ReportView(self, self.id)

        # Placing the budget option frame
        self.budgetView = BudgetView(self, self.id)

        # Placing the add category frame
        self.categoryAdd = CategoryAdd(self, self.id)

        # Placing the background
        self.background = tk.Frame(self, width=1066, height=768)
        self.background.config(bg="#2b3e50")
        self.background.place(x=0,y=0)

        #Placing the label with the balance amount
        self.balance = tk.Frame(self.background, width=200, height=50)
        self.balance.config(bg="#46919e")
        self.balance.place(x=650,y=20)
        self.labelMoney = tk.Label(self.balance, image=self.moneyPng, height=50 ,width=50 ,borderwidth=0)
        self.labelMoney.config(bg="#46919e")
        self.labelMoney.place(x=5, y=0)
        self.balanceAmountLabel = ttk.Label(self.balance, text=self.balanceAmount, font=('Segoe UI', 20), background="#46919e")
        self.balanceAmountLabel.place(x=50, y=0)

        # Placing the add category frame
        self.categoryAdd = CategoryAdd(self, self.id)
        self.categoryAdd.tkraise()

        # Placing the transaction option frame
        self.transactionView = TransactionView(self, id)
        self.background.tkraise()

        # Allowing switch between transaction frames
        self.transactionAdd = TransactionAdd(self, id)
        self.transactionAdd.setViewTransactionButton(self.background, self.transactionView)
        self.transactionView.setAddTransactionButton(self.background, self.transactionAdd)
        self.transactionAdd.setAddCategoryButton(self.background, self.categoryAdd)
        self.categoryAdd.setCancelButton(self.background, self.transactionAdd)

        # Starting screen
        self.background.tkraise()

    # Method for bringing the transaction interface upfront
    def showTransaction(self):
        self.background.tkraise()
        self.transactionView.tkraise()
        self.background.tkraise()
        self.transactionAdd.tkraise()

    # Method for bringing the budget interface upfront
    def showBudget(self):
        self.background.tkraise()
        self.budgetView.tkraise()

    def showReport(self):
        self.background.tkraise()
        self.reportView.tkraise()

    def showCategoryAdd(self):
        self.background.tkraise()
        self.categoryAdd.tkraise()
    
    def refreshBudget(self):
        # Placing the budget frame
        self.budgetView = BudgetView(self, self.id)
        self.background.tkraise()    
        self.budgetView.tkraise()    

    def refresh(self):

        # Placing the report frame
        self.reportView = ReportView(self, self.id)
        self.background.tkraise()

        # Placing the budget frame
        self.budgetView = BudgetView(self, self.id)
        self.background.tkraise()
        
        # Placing the transaction option frame
        self.transactionView = TransactionView(self, self.id)
        self.background.tkraise()

        # Allowing switch between transaction frames
        self.transactionAdd = TransactionAdd(self, self.id)
        self.transactionAdd.setViewTransactionButton(self.background, self.transactionView)
        self.transactionView.setAddTransactionButton(self.background, self.transactionAdd)
        self.transactionAdd.setAddCategoryButton(self.background, self.categoryAdd)
        self.categoryAdd.setCancelButton(self.background, self.transactionAdd)

    def updateBalance(self, amount):
        #Updating the balance
        currentBalance = float(self.db.getUserBalance((self.id,))[0][0])
        currentBalance = currentBalance + amount
        self.db.setUserBalance((currentBalance, self.id))
        self.balanceAmountLabel['text'] = str(currentBalance)