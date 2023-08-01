import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, String, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
engine = create_engine('sqlite:///library.db', echo=True)
Base = declarative_base()

# Define the Patron model
class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(String, primary_key=True)
    name = Column(String)
    contact = Column(Integer)
    membership_status = Column(Boolean)
    fine_amount = Column(Integer, default=0)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Tkinter setup
window = tk.Tk()
window.title("Patron Management System")
window.iconbitmap('patron.ico')
window.eval('tk::PlaceWindow %s center' %window.winfo_toplevel())
window.resizable(False,False)
window.configure(bg="#F9F9F9")

# Functions
def clear_entries():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    membership_status_var.set(False)

def add_patron():
    patron_id = id_entry.get()
    name = name_entry.get()
    contact = contact_entry.get()
    membership_status = membership_status_var.get()
    
    if patron_id and name and contact:
        patron = Patron(id=patron_id, name=name, contact=contact, membership_status=membership_status)
        session.add(patron)
        session.commit()
        messagebox.showinfo("Success", "Patron added successfully.")
        clear_entries()
    else:
        messagebox.showerror("Error", "Please fill in all the fields.")

def search_patrons():
    query = search_entry.get()
    patrons = session.query(Patron).filter(Patron.name.like(f"%{query}%") |
                                           Patron.contact.like(f"%{query}%")).all()
    
    if patrons:
        search_result.delete(0, tk.END)
        for patron in patrons:
            membership_status = "Active" if patron.membership_status else "Inactive"
            search_result.insert(tk.END, f"{patron.name} ({patron.contact}) - {membership_status}")
    else:
        messagebox.showinfo("Not Found", "No patrons found.")

def delete_patron():
    selected_patron = search_result.get(tk.ACTIVE)
    
    if selected_patron:
        patron_name = selected_patron.split("(")[0].strip()
        patron = session.query(Patron).filter(Patron.name == patron_name).first()
        
        if patron:
            confirmation = messagebox.askyesno("Confirm", f"Do you want to delete {patron.name}?")
            
            if confirmation:
                session.delete(patron)
                session.commit()
                search_patrons()
        else:
            messagebox.showinfo("Not Found", "Patron not found.")
    else:
        messagebox.showinfo("No Selection", "Please select a patron to delete.")

# UI
window_frame = tk.Frame(window, bg="#F9F9F9")
window_frame.pack(padx=20, pady=20)

id_label = tk.Label(window_frame, text="ID:", bg="#F9F9F9")
id_label.grid(row=0, column=0, sticky=tk.E)

id_entry = tk.Entry(window_frame)
id_entry.grid(row=0, column=1)

name_label = tk.Label(window_frame, text="Name:", bg="#F9F9F9")
name_label.grid(row=1, column=0, sticky=tk.E)

name_entry = tk.Entry(window_frame)
name_entry.grid(row=1, column=1)

contact_label = tk.Label(window_frame, text="Contact:", bg="#F9F9F9")
contact_label.grid(row=2, column=0, sticky=tk.E)

contact_entry = tk.Entry(window_frame)
contact_entry.grid(row=2, column=1)

membership_status_label = tk.Label(window_frame, text="Membership Status:", bg="#F9F9F9")
membership_status_label.grid(row=3, column=0, sticky=tk.E)

membership_status_var = tk.BooleanVar()
membership_status_checkbox = tk.Checkbutton(window_frame, variable=membership_status_var, bg="#F9F9F9")
membership_status_checkbox.grid(row=3, column=1, sticky=tk.W)

add_button = tk.Button(window_frame, text="Add Patron", command=add_patron, bg="#FF4081", fg="#FFFFFF")
add_button.grid(row=4, column=0, columnspan=2, pady=10)

search_label = tk.Label(window_frame, text="Search:", bg="#F9F9F9")
search_label.grid(row=5, column=0, sticky=tk.E)

search_entry = tk.Entry(window_frame)
search_entry.grid(row=5, column=1)

search_button = tk.Button(window_frame, text="Search", command=search_patrons, bg="#FF4081", fg="#FFFFFF")
search_button.grid(row=6, column=0, columnspan=2, pady=10)

search_result = tk.Listbox(window_frame, bg="#F9F9F9")
search_result.grid(row=7, column=0, columnspan=2)

delete_button = tk.Button(window_frame, text="Delete", command=delete_patron, bg="#FF4081", fg="#FFFFFF")
delete_button.grid(row=8, column=0, columnspan=2, pady=10)

window.mainloop()
