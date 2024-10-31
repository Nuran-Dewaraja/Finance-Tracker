

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

class FinanceTracker:
    def __init__(self, Tracker):
        self.Tracker = Tracker
        self.Tracker.title("Finance Tracker")
        
        #Data Entry Frame
        frame = ttk.Frame(Tracker)
        frame.grid(row=0, column=0, padx=20, pady=20)
        
        #Labels 
        #ID_Number Entry
        ttk.Label(frame, text="Category:").grid(row=0, column=0, padx=10, pady=5)
        self.category = ttk.Entry(frame)
        self.category.grid(row=0, column=1, padx=10, pady=5)
        
        #Amount Entry
        ttk.Label(frame, text="Amount:").grid(row=0, column=2, padx=10, pady=5)
        self.a_amount = ttk.Entry(frame)
        self.a_amount.grid(row=0, column=3, padx=10, pady=5)
        
        #Data Type Entry
        ttk.Label(frame,text="Type:").grid(row=0,column=4,padx=10,pady=5)
        self.combobox = ttk.Combobox(frame, values=["Income", "Expense"])
        self.combobox.grid(row=0, column=5, padx=10, pady=5)
        
        #Date Entry
        ttk.Label(frame, text="Date:").grid(row=0, column=6, padx=10, pady=5)
        self.d_date = DateEntry(frame, date_pattern='dd-mm-yyyy', showweeknumbers=False)  # Use DateEntry for date selection
        self.d_date.grid(row=0, column=7, padx=10, pady=5)
                
        #Data Entry Button
        ttk.Button(frame,text="Enter",command=self.Entry).grid(row=0, column=8, padx=10, pady=5)
        
        self.entry_data = []
        self.total_income = tk.StringVar()
        self.total_expense = tk.StringVar()
        self.net_income = tk.StringVar()
        
        # Transaction frame
        transaction = ttk.Frame(Tracker)
        transaction.grid(row=1, column=0, padx=10, pady=10)
        
        # Treeview to display transactions
        self.tree = ttk.Treeview(transaction, columns=("Category","Amount", "Type", "Date"))
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Date", text="Date")
        self.tree.grid(row=0, column=0, padx=5, pady=5)
        
        self.entries = []
        self.show_entries = tk.BooleanVar(value=True)
        
        # show/hide button 
        ttk.Checkbutton(transaction, text=" View all", variable=self.show_entries, command=self.show_hide).grid(row=0, column=5, padx=5, pady=5)
        
        # calculate frame
        calculate = ttk.Frame(Tracker)
        calculate.grid(row=2, column=0, padx=10, pady=10)
        
        ttk.Label(calculate, text="Total Income:").grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(calculate, textvariable=self.total_income).grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(calculate, text="Total Expense:").grid(row=0, column=2, padx=10, pady=10)
        ttk.Label(calculate, textvariable=self.total_expense).grid(row=0, column=3, padx=10, pady=10)
        
        ttk.Label(calculate,text="Net Income:").grid(row=0,column=4,padx=10,pady=10)
        ttk.Label(calculate,textvariable=self.net_income).grid(row=0,column=5,padx=10,pady=10)
        
        # specific month summary frame
        month_summary = ttk.Frame(Tracker)
        month_summary.grid(row=3, column=0, padx=10, pady=10)
        
        ttk.Label(month_summary, text="specific month summary:").grid(row=0, column=0, padx=10, pady=5)
        self.m_month = DateEntry(month_summary, date_pattern='dd-mm-yyyy', showweeknumbers=False) 
        self.m_month.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Button(month_summary,text="view_summary",command=self.view_summary).grid(row=0, column=2, padx=10, pady=5)
        
        # save and load buttons
        
        save_load = ttk.Frame(self.Tracker)
        save_load.grid(row=5, column=0, padx=10, pady=10 )
        
        ttk.Button(save_load, text="Save Data", command=self.save_data).grid(row=1, column=8, padx=10, pady=5)
        ttk.Button(save_load, text="Load Data", command=self.load_data).grid(row=1, column=9, padx=10, pady=5)

        # View all recorded
    def show_hide(self):
        if self.show_entries.get():
            self.tree.grid(row=0, column=0, padx=5, pady=5)
        else:
            self.tree.grid_forget()
        
        # 
    def Entry (self):
        c_category = str(self.category.get())
        amount = float(self.a_amount.get())
        type = self.combobox.get()
        date = str(self.d_date.get())
        
        self.entry_data.append({"Category":c_category, "Amount": amount,"Type": type,"Date":date})
        
        self.update_transaction_tree()
        self.calculate_totals()

    def update_transaction_tree(self):
        # Clear existing entries
        for entry in self.tree.get_children():
            self.tree.delete(entry)

        # Populate treeview with new entries
        for i, entry in enumerate(self.entry_data, start=1):
            self.tree.insert("", "end", iid=i, values=(entry["Category"],entry["Amount"], entry["Type"], entry["Date"]))

    def calculate_totals(self):
        total_income = sum(entry["Amount"] for entry in self.entry_data if entry["Type"] == "Income")
        total_expense = sum(entry["Amount"] for entry in self.entry_data if entry["Type"] == "Expense")
        
        self.total_income.set(f"Rs.{total_income:.2f}")
        self.total_expense.set(f"Rs.{total_expense:.2f}")
        
        net_income = total_income - total_expense
        self.net_income.set(f"Rs.{net_income:.2f}")

        # View a summary of transactions for a specific month
    def view_summary(self):
        selected_month = self.m_month.get()

        try:
            # Assuming that '17-01-2024' is in the format '%d-%m-%Y'
            month_number = datetime.strptime(selected_month, "%d-%m-%Y").month
        except ValueError:
            # Handle invalid date format
            messagebox.showerror("Error", "Invalid date format. Please use DD-MM-YYYY.")
            return  # This line should be inside the except block

        month_entries = [entry for entry in self.entry_data if datetime.strptime(entry["Date"], "%d-%m-%Y").month == month_number]

        total_income = sum(entry["Amount"] for entry in month_entries if entry["Type"] == "Income")
        total_expense = sum(entry["Amount"] for entry in month_entries if entry["Type"] == "Expense")

        net_income = total_income - total_expense

        # Create a new frame to display the summary
        summary_frame = ttk.Frame(self.Tracker)
        summary_frame.grid(row=4, column=0, padx=10, pady=10)

        ttk.Label(summary_frame, text=f"Summary for {selected_month}").grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(summary_frame, text=f"Total Income: Rs.{total_income:.2f}").grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(summary_frame, text=f"Total Expense: Rs.{total_expense:.2f}").grid(row=2, column=0, padx=10, pady=5)
        ttk.Label(summary_frame, text=f"Net Income: Rs.{net_income:.2f}").grid(row=3, column=0, padx=10, pady=5)
        

        #Save and load financial data
        
    def save_data(self, filename="financial_data.txt"):
        try:
            with open(filename, "w") as file:
                for entry in self.entry_data:
                    file.write(f"{entry['Category']},{entry['Amount']},{entry['Type']},{entry['Date']}\n")
            messagebox.showinfo("Save Data", "Financial data saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving data: {str(e)}")

    def load_data(self, filename="financial_data.txt"):
        try:
            with open(filename, "r") as file:
                self.entry_data = []
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 4:
                        entry = {
                            "Category": str(data[0]),
                            "Amount": float(data[1]),
                            "Type": data[2],
                            "Date": data[3]
                        }
                        self.entry_data.append(entry)
            self.update_transaction_tree()
            self.calculate_totals()
            messagebox.showinfo("Load Data", "Financial data loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading data: {str(e)}")
        
        
if __name__ == "__main__":
    Tracker = tk.Tk()
    app = FinanceTracker(Tracker)
    Tracker.mainloop()
