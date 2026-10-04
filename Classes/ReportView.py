import tkinter as tk
import ttkbootstrap as ttk
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
import calendar

from .Database import Database

class ReportView(tk.Frame):
    def __init__(self, root, id):
        super().__init__(root, width=830, height=380)
        self.root = root
        self.config(bg="#4B41D7")
        self.place(x=20,y=120) #115

        self.db = Database()
        self.id = id
        self.monthYearList = self.getMonthYearList()
        self.chartFrame = tk.Frame(self, width=300, height=220)
        self.chartFrame.config(bg="#D74B41")
        self.chartFrame.place(x=10,y=10) #115
        self.chartFrame.tkraise()

        self.pieChartFrame = tk.Frame(self, width=300, height=220)
        self.pieChartFrame.config(bg="#D74B41")
        self.pieChartFrame.place(x=430,y=10) #115

        # AddTransaction button
        self.ChangeMonthBackButton = ttk.Button(self, text="◀️", bootstyle="success", width=15, command=lambda:self.changeMonthBack())
        self.ChangeMonthBackButton.place(x=220,y=330) #115.5

        # Category area
        self.monthLabel = ttk.Label(self, text=self.currentMonthYear(), font=('Segoe UI', 15), background="#4B41D7")
        self.monthLabel.place(x=350,y=325) 

        # AddTransaction button
        self.ChangeMonthForwardButton = ttk.Button(self, text="▶️", bootstyle="success", width=15, command=lambda:self.changeMonthForward())
        self.ChangeMonthForwardButton.place(x=500,y=330) #115.5

        # Chart generation area
        month, year = self.monthYearNumerical(self.currentMonthYear())
        barChartExpenses, barChartIncome = self.transactionStats(year,month)
        pieChartExpenses, pieChartIncome = self.categoryStats(year,month)

        self.setIncomeButton = ttk.Button(self, text="income", bootstyle='info', command=lambda: self.setIncome(barChartIncome, pieChartIncome))
        self.setIncomeButton.place(x=120, y=330)

        self.setExpensesButton = ttk.Button(self, text="expenses", bootstyle='info', command=lambda: self.setExpenses(barChartExpenses, pieChartExpenses))
        self.setExpensesButton.place(x=30, y=330)

        self.create_graph(barChartIncome, pieChartIncome)
        self.setIncomeButton.config(state=tk.DISABLED)

        print(self.currentMonthYear())
        print(self.monthYearNumerical(self.monthLabel.cget("text")))
        print(self.getMonthYearList())

    def calendarGeneration(self, year):
        list_of_months = list(calendar.month_name)[1:]
        monthDict = {}
        for i in range(len(list_of_months)):
            monthDict[list_of_months[i]] = calendar.monthrange(int(year), i+1)[1]
        return monthDict

    def currentMonthYear(self):
        list_of_months = list(calendar.month_name)[1:]
        current_month = datetime.datetime.now().month
        return list_of_months[current_month-1] + "-" + str(datetime.datetime.now().year)  
    
    def monthYearNumerical(self, monthYearString):
        monthYearStringList = monthYearString.split("-")
        list_of_months = list(calendar.month_name)[1:]
        chosenMonth = list_of_months.index(monthYearStringList[0]) + 1
        chosenYear = int(monthYearStringList[1])
        return chosenMonth, chosenYear
    
    def getMonthYearList(self):
        list_of_months = list(calendar.month_name)[1:]
        allTransactions = self.db.getTransactions((self.id,))
        monthYearList = []
        for transaction in allTransactions :
            year = int(transaction[0].split("-")[2])
            month = int(transaction[0].split("-")[1])
            monthYearList.append(list_of_months[month-1] + "-" + str(year))
        return list(dict.fromkeys(monthYearList))

    def transactionStats(self, chosenYear, chosenMonth):
        allTransactions = self.db.getTransactions((self.id,))
        yearlyExpenses = {}
        yearlyIncome = {}
        for transaction in allTransactions :
            year = int(transaction[0].split("-")[2])
            month = int(transaction[0].split("-")[1])
            day = int(transaction[0].split("-")[0])
            if(transaction[1]=='Expense'):
                if(year not in yearlyExpenses):
                    yearlyExpenses[year] = {}
                if(month not in yearlyExpenses[year]):
                    yearlyExpenses[year][month] = {}
                dailyExpense = yearlyExpenses[year][month][day] + transaction[2] if day in yearlyExpenses[year][month] else transaction[2] 
                yearlyExpenses[year][month][day] = dailyExpense
            else:
                if(year not in yearlyIncome):
                    yearlyIncome[year] = {}
                if(month not in yearlyIncome[year]):
                    yearlyIncome[year][month] = {}
                dailyIncome = yearlyIncome[year][month][day] + transaction[2] if day in yearlyIncome[year][month] else transaction[2] 
                yearlyIncome[year][month][day] = dailyIncome
        #return yearlyExpenses[chosenYear][chosenMonth], yearlyIncome[chosenYear][chosenMonth]
        return yearlyExpenses.get(chosenYear,{}).get(chosenMonth,{}), yearlyIncome.get(chosenYear,{}).get(chosenMonth,{})

    def categoryStats(self, chosenYear, chosenMonth):
        allTransactions = self.db.getTransactions((self.id,))
        incomeCategoryPercentage = {}
        expensesCategoryPercentage = {}
        for transaction in allTransactions :
            year = int(transaction[0].split("-")[2])
            month = int(transaction[0].split("-")[1])
            if(transaction[1]=='Income'):
                if(year not in incomeCategoryPercentage):
                    incomeCategoryPercentage[year] = {}
                if(month not in incomeCategoryPercentage[year]):
                    incomeCategoryPercentage[year][month] = {}
                incomeCategoryPercentage[year][month][transaction[3]] = incomeCategoryPercentage[year][month][transaction[3]] + 1 if transaction[3] in incomeCategoryPercentage[year][month] else 1
            else:    
                if(year not in expensesCategoryPercentage):
                    expensesCategoryPercentage[year] = {}
                if(month not in expensesCategoryPercentage[year]):
                    expensesCategoryPercentage[year][month] = {}
                expensesCategoryPercentage[year][month][transaction[3]] = expensesCategoryPercentage[year][month][transaction[3]] + 1 if transaction[3] in expensesCategoryPercentage[year][month] else 1
        return expensesCategoryPercentage.get(chosenYear,{}).get(chosenMonth,{}), incomeCategoryPercentage.get(chosenYear,{}).get(chosenMonth,{})

    def create_graph(self, barChartData, pieChartData):
        style.use("_mpl-gallery")
        self.fig = Figure(figsize=(4, 3), dpi=100)
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.ax1.set_xlabel('Day')
        self.ax1.set_ylabel('Amount', color='g')
        self.fig.tight_layout()

        barChartDataInitialX = list(barChartData.keys())
        barChartDataInitialY = list(barChartData.values())
        barChartDataX = [i for i in range(1,32)]
        barChartDataY = [0*i for i in range(1,32)]
        for x in range(len(barChartDataInitialX)) :
            barChartDataY[barChartDataInitialX[x]] = barChartDataInitialY[x]
        self.ax1.bar(barChartDataX, barChartDataY)

        self.graph = FigureCanvasTkAgg(self.fig, master=self.chartFrame)
        self.canvas = self.graph.get_tk_widget()
        self.canvas.grid(row=0, column=0)

        self.labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        self.sizes = [15, 30, 45, 10]

        style.use("_mpl-gallery")
        self.fig2 = Figure(figsize=(3.8, 3), dpi=100)
        self.ax2 = self.fig2.add_subplot(1, 1, 1)
        self.fig2.tight_layout()

        self.ax2.pie(pieChartData.values(), labels=pieChartData.keys(), autopct='%1.1f%%')

        self.graph2 = FigureCanvasTkAgg(self.fig2, master=self.pieChartFrame)
        self.canvas2 = self.graph2.get_tk_widget()
        self.canvas2.grid(row=0, column=0)

    '''
    def transactionData(self, month, year):
        yearlyExpenses, yearlyIncome = self.transactionStats()
        calendarDays = self.calendarGeneration(year)
        data = []
    '''

    def setIncome(self, barChartData, pieChartData):
        self.setIncomeButton.config(state=tk.DISABLED)
        self.setExpensesButton.config(state=tk.NORMAL)
        self.create_graph(barChartData, pieChartData)

    def setExpenses(self, barChartData, pieChartData):
        self.setExpensesButton.config(state=tk.DISABLED)
        self.setIncomeButton.config(state=tk.NORMAL)
        self.create_graph(barChartData, pieChartData)

    def changeMonthBack(self):
        index = self.monthYearList.index(self.monthLabel.cget("text"))
        index = index - 1 if index>0 else index
        self.monthLabel['text'] = self.monthYearList[index]
        self.refreshCharts(index)

    def changeMonthForward(self):
        index = self.monthYearList.index(self.monthLabel.cget("text"))
        index = index + 1 if index<len(self.monthYearList)-1 else index
        self.monthLabel['text'] = self.monthYearList[index]
        self.refreshCharts(index)

    def refreshCharts(self, index):
        month, year = self.monthYearNumerical(self.monthYearList[index])
        barChartExpenses, barChartIncome = self.transactionStats(year, month)
        pieChartExpenses, pieChartIncome = self.categoryStats(year, month)
        self.setIncomeButton['command'] = lambda: self.setIncome(barChartIncome, pieChartIncome)
        self.setExpensesButton['command'] = lambda: self.setExpenses(barChartExpenses, pieChartExpenses)
        self.create_graph(barChartIncome, pieChartIncome)
        self.setExpensesButton.config(state=tk.NORMAL)
        self.setIncomeButton.config(state=tk.NORMAL)
        self.setIncomeButton.config(state=tk.DISABLED)