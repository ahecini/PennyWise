import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox

from .Database import Database

class BudgetView(tk.Frame):
    def __init__(self, root, id):
        super().__init__(root, width=504, height=225)
        self.root = root
        self.config(bg="#2b3e50")
        self.place(x=200,y=180) #115
        self.table = ttk.Treeview(self, selectmode="browse")
        self.table.bind('<ButtonRelease-1>', self.selectItem)
        self.table.bind('<ButtonRelease-3>', self.deselectItem)

        self.db = Database()
        self.id = id

        # Define the columns
        self.table['columns'] = ('Category', 'Budget', 'expenses')

        # Format the columns
        self.table.column('#0', width=0, stretch=tk.NO)
        self.table.column('Category', anchor=tk.W, width=75)
        self.table.column('Budget', anchor=tk.W, width=75)
        self.table.column('expenses', anchor=tk.W, width=75)

        # Create the headings
        self.table.heading('#0', text='', anchor=tk.W)
        self.table.heading('Category', text='Category', anchor=tk.W)
        self.table.heading('Budget', text='Budget', anchor=tk.W)
        self.table.heading('expenses', text='expenses', anchor=tk.W)

        # Sample data
        self.data = self.db.getBudget(self.id)
        self.cleanData = []
        for data in self.data :
            dataList = list(data)
            if dataList[1]==-1:
                dataList[1]="no budget"
            else:
                dataList[1]=data[1]
            dataList.append(self.db.getCategoryExpenses(dataList[0])[0][0])
            self.cleanData.append(tuple(dataList))

        # Configure alternating row colors
        '''
        self.table.tag_configure('oddrow', background="#5F07EC")
        self.table.tag_configure('evenrow', background="#082470")
        '''

        # Configure alternating row colors
        self.table.tag_configure('Respected', background="#29BB15")
        self.table.tag_configure('Not-respected', background="#FA0808")

        # Add data with alternating row colors
        '''
        for i in range(len(self.data)):
            if i % 2 == 0:
                self.table.insert(parent='', index=i, values=self.data[i], tags=('evenrow',))
            else:
                self.table.insert(parent='', index=i, values=self.data[i], tags=('oddrow',))
        '''
        print("clean data",self.cleanData)
        # Add data with alternating row colors
        for i in range(len(self.cleanData)):
            print("hey",self.cleanData[i][1],self.cleanData[i][2])
            self.table.insert(parent='', index=i, values=self.cleanData[i], 
                              tags=("Respected" 
                                    if isinstance(self.cleanData[i][1], str) or self.cleanData[i][1]>float(self.cleanData[i][2] if self.cleanData[i][2] is not None else 0.0) 
                                    else "Not-respected",))
            
        # Pack the table
        #self.table.pack(expand=True, fill=tk.BOTH)
        self.table.place(x=0,y=0)

        # Go to add transaction interface
        self.ModifiyBudget = ttk.Button(self, text="Modify/Fix budget", bootstyle="success", width=20)
        self.ModifiyBudget.place(x=0,y=187.5) #115.5
        self.ModifiyBudget.config(state=tk.DISABLED)
        self.ModifiyBudget['command'] = self.modifyBudget

        # Frame carrying the form to modify the budget
        # The main Frame
        self.modifyInterface = tk.Frame(self, width=200, height=185)
        self.modifyInterface.config(bg="#4B41D7")
        self.modifyInterface.place(x=275,y=0) #115

        # Category area
        self.categoryTextValue = ttk.StringVar()
        self.categoryLabel = ttk.Label(self.modifyInterface, text="Category", font=('Segoe UI', 12), background="#4B41D7")
        self.categoryLabel.place(x=16,y=0.5) 
        self.categoryText = ttk.Entry(self.modifyInterface, font=('Helvetica',8), width=25, bootstyle="info", textvariable=self.categoryTextValue)
        self.categoryText.place(x=16,y=30.5)
        self.categoryText.config(state=tk.DISABLED)

        # Budget area
        self.budgetLabel = ttk.Label(self.modifyInterface, text="New budget", font=('Segoe UI', 12), background="#4B41D7")
        self.budgetLabel.place(x=16,y=60.5) 
        self.budgetText = ttk.Entry(self.modifyInterface, font=('Helvetica',8), width=25, bootstyle="info")
        self.budgetText.place(x=16,y=90.5)

        # Approve button 
        self.approveButton = ttk.Button(self.modifyInterface, text="Approve", bootstyle="success", width=9)
        self.approveButton.place(x=15,y=140.5) #115.5
        self.approveButton.config(state=tk.DISABLED)
        self.approveButton['command'] = self.approveModification

        # Approve button 
        self.cancelButton = ttk.Button(self.modifyInterface, text="Cancel", bootstyle="info", width=7)
        self.cancelButton.place(x=110,y=140.5) #115.5
        self.cancelButton.config(state=tk.DISABLED)
        self.cancelButton['command'] = self.cancelModification

    def selectItem(self, a):
        curItem = self.table.focus()
        self.ModifiyBudget.config(state=tk.NORMAL)

    def deselectItem(self, a):
        curItem = self.table.focus()
        self.table.selection_remove(curItem)
        self.ModifiyBudget.config(state=tk.DISABLED)
    
    def changeFrame(self, background, frame):
        background.tkraise()
        frame.tkraise()

    def modifyBudget(self):
        curItem = self.table.focus()
        self.categoryTextValue.set(self.table.item(curItem)["values"][0])
        self.approveButton.config(state=tk.NORMAL)
        self.cancelButton.config(state=tk.NORMAL)
        self.ModifiyBudget.config(state=tk.DISABLED)
        self.table["selectmode"]="none"
        self.table.bind('<ButtonRelease-1>', lambda *args:None)
        self.table.bind('<ButtonRelease-3>', lambda *args:None)

    def cancelModification(self):
        self.categoryTextValue.set("")
        self.approveButton.config(state=tk.DISABLED)
        self.cancelButton.config(state=tk.DISABLED)
        curItem = self.table.focus()
        self.table.selection_remove(curItem)
        self.ModifiyBudget.config(state=tk.DISABLED)
        self.table["selectmode"]="browse"  
        self.table.bind('<ButtonRelease-1>', self.selectItem)
        self.table.bind('<ButtonRelease-3>', self.deselectItem)    
        curItem = self.table.focus()
        self.table.selection_remove(curItem)

    def approveModification(self):
        try:
            amount = float(self.budgetText.get())
            category = self.categoryText.get()
            self.db.updateBudgetAmount((amount, category))
            self.root.refreshBudget()
        except:
            messagebox.showinfo("Failure", "Please insert a valid amount!")