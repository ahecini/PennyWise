import tkinter as tk
import ttkbootstrap as ttk

from .Database import Database

class TransactionView(tk.Frame):
    def __init__(self, root, id):
        self.id = id
        super().__init__(root, width=504, height=225)
        self.config(bg="#2b3e50")
        self.db = Database()
        self.place(x=200,y=180) #115
        self.table = ttk.Treeview(self)

        # Define the columns
        self.table['columns'] = ('Date', 'Type', 'Amount', 'Category', 'Description')

        # Format the columns
        self.table.column('#0', width=0, stretch=tk.NO)
        self.table.column('Date', anchor=tk.W, width=100)
        self.table.column('Type', anchor=tk.W, width=100)
        self.table.column('Amount', anchor=tk.W, width=100)
        self.table.column('Category', anchor=tk.W, width=100)
        self.table.column('Description', anchor=tk.W, width=100)

        # Create the headings
        self.table.heading('#0', text='', anchor=tk.W)
        self.table.heading('Date', text='Date', anchor=tk.W)
        self.table.heading('Type', text='Type', anchor=tk.W)
        self.table.heading('Amount', text='Amount', anchor=tk.W)
        self.table.heading('Category', text='Category', anchor=tk.W)
        self.table.heading('Description', text='Description', anchor=tk.W)

        # Sample data
        '''
        self.data = [
            ('07/07/2025', 'Income', 300.01, 'Shopping', 'groceries'),
            ('17/07/2025', 'expense', 10.01, 'Shopping', 'interest'),
            ('17/07/2025', 'expense', 10.01, 'Shopping', 'interest')
        ]
        '''
        self.data = self.db.getTransactions((self.id,))

        # Configure alternating row colors
        '''
        self.table.tag_configure('oddrow', background="#5F07EC")
        self.table.tag_configure('evenrow', background="#082470")
        '''

        # Configure alternating row colors
        self.table.tag_configure('Income', background="#29BB15")
        self.table.tag_configure('Expense', background="#FA0808")

        # Add data with alternating row colors
        '''
        for i in range(len(self.data)):
            if i % 2 == 0:
                self.table.insert(parent='', index=i, values=self.data[i], tags=('evenrow',))
            else:
                self.table.insert(parent='', index=i, values=self.data[i], tags=('oddrow',))
        '''

        # Add data with alternating row colors
        for i in range(len(self.data)):
            self.table.insert(parent='', index=i, values=self.data[i], tags=(self.data[i][1],))
            
        # Pack the table
        #self.table.pack(expand=True, fill=tk.BOTH)
        self.table.place(x=0,y=0)

        # Go to add transaction interface
        self.AddTransactionButton = ttk.Button(self, text="Add transaction", bootstyle="success", width=15)
        self.AddTransactionButton.place(x=16,y=187.5) #115.5

    def changeFrame(self, background, frame):
        background.tkraise()
        frame.tkraise()
    def setAddTransactionButton(self, background, frame):
        self.AddTransactionButton['command'] = lambda:self.changeFrame(background, frame)