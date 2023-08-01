import tkinter as tk
from tkinter import messagebox
import re
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import subprocess

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(50))
    email = Column(String(50), unique=True)

engine = create_engine('sqlite:///library.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def register():
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    if not validate_email(email):
        messagebox.showerror("Error", "Invalid Email Format")
        return

    new_user = User(username=username, password=password, email=email)
    session.add(new_user)
    session.commit()
    messagebox.showinfo("Registration", "Registration Successful")

def login():
    username = username_entry.get()
    password = password_entry.get()
    user = session.query(User).filter_by(username=username).first()
    if user is None:
        messagebox.showerror("Error", "Invalid Username")
        return False
    elif user.password != password:
        messagebox.showerror("Error", "Invalid Password")
        return False
    else:
        messagebox.showinfo("Login", "Login Successful")
        return True

def open_user_interface():
    subprocess.Popen(["python", "user_interface.py"])

def authenticate():
    if login():
        answer = answer_entry.get()
        if answer == "24":
            print("Login successful.")
        else:
            pass

window = tk.Tk()
window.title("Registration Window")
window.geometry("300x200")
window.iconbitmap('registration.ico')
window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
window.resizable(False, False)

username_label = tk.Label(window, text="Username")
username_label.pack()

username_entry = tk.Entry(window)
username_entry.pack()

password_label = tk.Label(window, text="Password")
password_label.pack()

password_entry = tk.Entry(window, show="*")
password_entry.pack()

email_label = tk.Label(window, text="Email")
email_label.pack()

email_entry = tk.Entry(window)
email_entry.pack()

register_button = tk.Button(window, text="Register", command=register)
register_button.pack()

login_button = tk.Button(window, text="Login", command=authenticate)
login_button.pack()

authenticator_number = tk.Label(window, text="Answer with '24' to prove if human.")
answer_entry = tk.Entry(window)
answer_entry.pack()

window.mainloop()
