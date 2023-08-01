import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine, MetaData, Table, select

# Connect to the database
engine = create_engine('sqlite:///library.db')
metadata = MetaData()
metadata.reflect(bind=engine)
connection = engine.connect()

# Create the main window
window = tk.Tk()
window.title("Library Reports System")
window.geometry('360x480')
window.iconbitmap('report.ico')
window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
window.resizable(False, False)
window.configure(bg="#F9F9F9")

# Function to fetch and display table data
def display_table(table_name):
    table = metadata.tables[table_name]
    select_query = table.select()
    result = connection.execute(select_query)
    data = result.fetchall()

    # Create a new window to display table data
    table_window = tk.Toplevel(window)
    table_window.title(table_name)
    table_window.configure(bg="#F9F9F9")

    # Create a Frame to hold the Treeview and scrollbar
    frame = ttk.Frame(table_window)
    frame.pack(expand=True, fill="both")

    # Create a Treeview widget to display the table data
    treeview = ttk.Treeview(frame, show="headings")
    treeview["columns"] = tuple(table.columns.keys())

    # Add column names to the Treeview
    for column in table.columns:
        treeview.heading(column.name, text=column.name)

    # Add data rows to the Treeview
    for row in data:
        treeview.insert("", "end", values=row)

    # Add vertical scrollbar to the Treeview
    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")

    # Add horizontal scrollbar to the Treeview
    scrollbar_x = ttk.Scrollbar(table_window, orient="horizontal", command=treeview.xview)
    treeview.configure(xscrollcommand=scrollbar_x.set)
    scrollbar_x.pack(side="bottom", fill="x")

    # Pack the Treeview
    treeview.pack(expand=True, fill="both")

# Fetch and display the Books table
button_books = tk.Button(window, text="Books Within Library", command=lambda: display_table("books"), bg="#FF4081", fg="#FFFFFF")
button_books.pack(pady=10)

# Fetch and display the Authors table
button_authors = tk.Button(window, text="Authors of Books in Library", command=lambda: display_table("authors"), bg="#536DFE", fg="#FFFFFF")
button_authors.pack(pady=10)

# Fetch and display the Patrons table
button_patrons = tk.Button(window, text="Registered Patrons", command=lambda: display_table("patrons"), bg="#FFC107", fg="#FFFFFF")
button_patrons.pack(pady=10)

# Fetch and display the Users table
button_users = tk.Button(window, text="Registered Users", command=lambda: display_table("users"), bg="#9C27B0", fg="#FFFFFF")
button_users.pack(pady=10)

# Fetch and display the Loans table
button_loans = tk.Button(window, text="Loaned books", command=lambda: display_table("loans"), bg="#4CAF50", fg="#FFFFFF")
button_loans.pack(pady=10)

# Run the main Tkinter event loop
window.mainloop()
