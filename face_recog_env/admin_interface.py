import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
from datetime import datetime

# Load logs for today by default
log_folder = 'logs'
today_log_file = f'{log_folder}/entry_log_{datetime.now().date()}.csv'

class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Entry Logs")
        self.root.geometry("700x500")

        # Title Label
        tk.Label(root, text="Employee Entry Logs", font=("Arial", 18, "bold")).pack(pady=10)

        # Date Filter
        tk.Label(root, text="Filter by Date (YYYY-MM-DD):").pack(pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.pack(pady=5)

        # Filter Button
        tk.Button(root, text="Load Logs", command=self.load_logs).pack(pady=5)

        # Treeview for displaying logs
        self.tree = ttk.Treeview(root, columns=("Name", "Entry Time"), show='headings')
        self.tree.heading("Name", text="Employee Name")
        self.tree.heading("Entry Time", text="Entry Time")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Export Button
        tk.Button(root, text="Export to Excel", command=self.export_logs).pack(pady=10)

        # Load today's logs by default
        self.load_logs()

    def load_logs(self):
        date_filter = self.date_entry.get().strip()
        log_file = f'{log_folder}/entry_log_{date_filter}.csv' if date_filter else today_log_file

        if os.path.exists(log_file):
            df = pd.read_csv(log_file)
            self.display_logs(df)
        else:
            messagebox.showerror("Error", f"No logs found for {date_filter if date_filter else 'today'}.")
            self.clear_tree()

    def display_logs(self, df):
        self.clear_tree()
        for _, row in df.iterrows():
            self.tree.insert('', tk.END, values=(row['Name'], row['Entry Time']))

    def clear_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def export_logs(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            date_filter = self.date_entry.get().strip()
            log_file = f'{log_folder}/entry_log_{date_filter}.csv' if date_filter else today_log_file

            if os.path.exists(log_file):
                df = pd.read_csv(log_file)
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Logs exported to {file_path}")
            else:
                messagebox.showerror("Error", "No logs to export.")

# Run the admin app
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminApp(root)
    root.mainloop()
