import tkinter as tk
from tkinter import messagebox, filedialog
import json
from datetime import datetime

class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("👩‍🏫Text-Based Finance Tracker👩‍🏫")
        
        # Set background color
        root.configure(background="#D1EAF0")
        
        # Set the initial size of the main window
        root.geometry("300x630")

        # Financial entries
        self.financial_entries = []

        # Create GUI elements
        self.create_gui()


    def create_gui(self):
        # Create frames
        input_frame = tk.Frame(self.root, bg="#add8e6")
        input_frame.grid(row=0, column=0, padx=5, pady=10, sticky="n")
        
        display_frame = tk.Frame(self.root, bg="#add8e6")
        display_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="ns")
        
        summary_frame= tk.Frame(self.root, bg="#add8e6")
        summary_frame.grid(row=2, column=0, padx=5, pady=10, sticky="ns")

        buttons_frame = tk.Frame(self.root, bg="#add8e6")
        buttons_frame.grid(row=3, column=0, padx=5, pady=10, sticky="ns")
        
        # Labels
        
        tk.Label(input_frame, text="Type: ", background="lightblue", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(input_frame, text="Amount:", background="lightblue", font=('Helvetica', 10, 'bold')).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(input_frame, text="Category:", background="lightblue", font=('Helvetica', 10, 'bold')).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        tk.Label(input_frame, text="Date (YYYY-MM-DD):", background="lightblue", font=('Helvetica', 10, 'bold')).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        tk.Label(summary_frame, text="Month(1-12):", background="lightblue", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, pady=15,padx=10, sticky="w")
        
        # Entry widgets 
        self.type_entry = tk.Entry(input_frame)
        self.amount_entry = tk.Entry(input_frame)
        self.category_entry = tk.Entry(input_frame)
        self.date_entry = tk.Entry(input_frame)
        self.Summary_by_Month = tk.Entry(summary_frame)

        # Position entry widgets
        self.type_entry.grid(row=0, column=1, padx=5, pady=5)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)    
        self.category_entry.grid(row=2, column=1,padx=5, pady=5)
        self.date_entry.grid(row=3, column=1,padx=5, pady=5)
        self.Summary_by_Month.grid(row=0, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(input_frame,text="Record Entry", command=self.record_entry, font=('Helvetica', 10, 'bold')).grid(row=4, column=0,columnspan=2, pady=5,padx=5)
        tk.Button(summary_frame, text="View Summary by Month", command=self.summary_by_month, font=('Helvetica', 10, 'bold')).grid(row=1, column=0, columnspan=2, pady=5,padx=5)
        tk.Button(buttons_frame, text="Save to File", command=self.save_data_to_file, font=('Helvetica', 10, 'bold')).grid(row=0, column=0, pady=15,padx=10)
        tk.Button(buttons_frame, text="Load from File", command=self.load_data_from_file, font=('Helvetica', 10, 'bold')).grid(row=0, column=1, pady=15,padx= 10)

        # Exit button
        tk.Button(text="Exit", command=self.exit_app, font=('Helvetica', 10, 'bold')).grid(row=5, column=0, pady=15, padx=10)
        
        # View All Entries and Calculate Totals
        view_summary_frame = tk.Frame(display_frame, bg="#add8e6")
        view_summary_frame.grid(row=0, column=0, padx=20, pady=10)

        tk.Button(view_summary_frame, text="View All Entries", command=self.view_all_entries, font=('Helvetica', 10, 'bold')).grid(row=0, column=0, pady=5, padx=5)
        tk.Button(view_summary_frame, text="Calculate Totals", command=self.calculate_totals, font=('Helvetica', 10, 'bold')).grid(row=0, column=1, pady=5, padx=5)
        
        # Totals display
        self.totals_text = tk.StringVar()
        tk.Label(view_summary_frame, textvariable=self.totals_text, font=('Helvetica', 8, 'bold'), bg="#add8e6").grid(row=2, column=0,columnspan=2)

        # Text widget to display entries
        self.entries_text = tk.Text(view_summary_frame, height=3, width=30)
        self.entries_text.grid(row=3, column=0, columnspan=2, pady=10)
        

    def record_entry(self):
        entry_type = self.type_entry.get().lower()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date_str = self.date_entry.get()

        try:
            amount = float(amount)
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")
            return

        entry = {
            'type': entry_type,
            'amount': amount,
            'category': category,
            'date': date
        }
        self.financial_entries.append(entry)
        messagebox.showinfo("Success", "Entry recorded successfully ✅")

    def calculate_totals(self):
        total_income = sum(entry['amount'] for entry in self.financial_entries if entry['type'] == 'income')
        total_expenses = sum(entry['amount'] for entry in self.financial_entries if entry['type'] == 'expense')
        net_income = total_income - total_expenses

        self.totals_text.set(f"Total Income: {total_income}\nTotal Expenses: {total_expenses}\nNet Income: {net_income}")

    def view_all_entries(self):
        # Clear previous entries
        self.entries_text.delete(1.0, tk.END)

        for entry in self.financial_entries:
            self.entries_text.insert(tk.END, f"{entry}\n")

    def summary_by_month(self):
        month_str = self.date_entry.get()
        try:
            month = int(month_str)
            if not 1 <= month <= 12:
                raise ValueError("Month should be between 1 and 12.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid month: {e}")
            return

        # Filter entries for the specified month
        filtered_entries = [entry for entry in self.entries if int(entry['date'].split('-')[1]) == month]

        if not filtered_entries:
            messagebox.showinfo("Summary", "No entries found for the specified month.")
            return

        # Display the summary for the specified month
        summary_text = "\n".join(str(entry) for entry in filtered_entries)
        messagebox.showinfo("Summary for Month", summary_text)

    def save_data_to_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])

        if filename:
            with open(filename, 'w') as file:
                json.dump(self.financial_entries, file)
            messagebox.showinfo("Success", "Data saved successfully ✅")
            

    def load_data_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])

        if filename:
            try:
                with open(filename, 'r') as file:
                    self.financial_entries = json.load(file)
                messagebox.showinfo("Success", "Data loaded successfully ✅")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading data: {e}")
    
    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()
    
