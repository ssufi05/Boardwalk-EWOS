import mysql.connector
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import askyesno
import sv_ttk


# load history sql table
def load_history():
    db = mysql.connector.connect(user='root', password='password', host='localhost', database='workorders')
    try:
        #establishing the connection to DB
        db.connect()
        # query to show all completed task
        sql_select_query = """select * from HISTORY"""
        cursor = db.cursor()
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        # Load the records into the table
        list_values = list(records)
        print(list_values)

        for value_tuple in list_values[1:]:
            treeview.insert('', tk.END, values=value_tuple)

    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))

    finally:
        if db.is_connected():
            cursor.close()
            db.connect
# Create the main window
root = Tk()
style = ttk.Style(root)
sv_ttk.set_theme("light")
frame = ttk.Frame(root)
frame.pack()
treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, pady=10, sticky="ns")
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ("Ticket #", "Requestor", "Dept", "Dept #", "Status", " ", "Date Requested", "Notes")
treeview = ttk.Treeview(treeFrame, show="headings",
                        yscrollcommand=treeScroll.set, columns=cols) 
treeview.column("Ticket #", width=50)
treeview.column("Requestor", width=100)
treeview.column("Dept", width=80)
treeview.column("Dept #", width=50)
treeview.column("Status", width=50)
treeview.column(" ", width=70)
treeview.column("Date Requested", width=125)
treeview.column("Notes", width=150)

for col in cols:                    # Gives column headings sort functionality
    treeview.heading(col, text=col, command=lambda c=col: sort_treeview(treeview, c, False))
load_history()
# Load data and set the anchor for each column dynamically
def sort_treeview(tree, col, descending):
    data = [(tree.set(item, col), item) for item in tree.get_children('')]
    data.sort(reverse=descending)
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))

# Set the anchor for each column explicitly
for col in cols:
    treeview.heading(col, text=col, anchor="w")

treeview.pack(fill='y', expand=True)
treeScroll.config(command=treeview.yview)

# This part sorts newest tickets to the top by default when the client opens
treeview.heading('Date Requested', text='Date Requested', command=lambda: sort_treeview(treeview, 'Date Requested', True))
sort_treeview(treeview, 'Date Requested', True)
root.title("History")
root.mainloop()
