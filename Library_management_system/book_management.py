import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, String, Integer, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# SQLAlchemy setup
engine = create_engine('sqlite:///library.db', echo=True)
Base = declarative_base()

# Define the Book model
class Book(Base):
    __tablename__ = 'books'
    isbn = Column(String, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    publication_date = Column(Date)
    author = relationship('Author', back_populates='books')


# Define the Author model
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship('Book', back_populates='author')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Tkinter setup
window = tk.Tk()
window.title("Book Management System")
window.iconbitmap("books.ico")
window.geometry("500x500+50+50")
window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())

# Color setup
BACKGROUND_COLOR = "#ECECEC"
LABEL_COLOR = "#333333"
ENTRY_BACKGROUND_COLOR = "#FFFFFF"
BUTTON_BACKGROUND_COLOR = "#4CAF50"
BUTTON_FOREGROUND_COLOR = "#FFFFFF"
LISTBOX_BACKGROUND_COLOR = "#FFFFFF"

window.configure(bg=BACKGROUND_COLOR)
window.resizable(False, False)

# Functions
def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)
    pub_date_entry.delete(0, tk.END)

def add_book():
    title = title_entry.get()
    author_name = author_entry.get()
    isbn = isbn_entry.get()
    pub_date = pub_date_entry.get()

    if title and author_name and isbn and pub_date:
        try:
            pub_date_obj = datetime.strptime(pub_date, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format YYYY-MM-DD.")
            return

        book = session.query(Book).get(isbn)
        if book:
            messagebox.showerror("Error", "A book with the same ISBN already exists.")
            return

        author = session.query(Author).filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)

        book = Book(title=title, author=author, isbn=isbn, publication_date=pub_date_obj)
        session.add(book)
        session.commit()
        messagebox.showinfo("Success", "Book added successfully.")
        clear_entries()
    else:
        messagebox.showerror("Error", "Please fill in all the fields.")


def search_books():
    query = search_entry.get()
    books = session.query(Book).filter(Book.title.like(f"%{query}%") |
                                       Author.name.like(f"%{query}%") |
                                       Book.isbn.like(f"%{query}%") |
                                       Book.publication_date.like(f"%{query}%")).all()

    if books:
        search_result.delete(0, tk.END)
        for book in books:
            search_result.insert(tk.END, f"{book.title} by {book.author.name} (ISBN: {book.isbn})")
    else:
        messagebox.showinfo("Not Found", "No books found.")

def delete_book():
    selected_book = search_result.get(tk.ACTIVE)

    if selected_book:
        book_isbn = selected_book.split("(ISBN: ")[-1].rstrip(")")
        book = session.query(Book).get(book_isbn)

        if book:
            confirmation = messagebox.askyesno("Confirm", f"Do you want to delete {book.title}?")

            if confirmation:
                session.delete(book)
                session.commit()
                search_books()
                # Check if the author has no more books and delete them as well
                if not book.author.books:
                    session.delete(book.author)
                    session.commit()
                    search_books()
        else:
            messagebox.showinfo("Not Found", "Book not found.")
    else:
        messagebox.showinfo("No Selection", "Please select a book to delete.")

# Tkinter user interface
title_label = tk.Label(window, text="Title:", bg=BACKGROUND_COLOR, fg=LABEL_COLOR)
title_label.grid(row=0, column=0, sticky=tk.E, padx=10, pady=5)

title_entry = tk.Entry(window, bg=ENTRY_BACKGROUND_COLOR)
title_entry.grid(row=0, column=1, padx=10, pady=5)

author_label = tk.Label(window, text="Author:", bg=BACKGROUND_COLOR, fg=LABEL_COLOR)
author_label.grid(row=1, column=0, sticky=tk.E, padx=10, pady=5)

author_entry = tk.Entry(window, bg=ENTRY_BACKGROUND_COLOR)
author_entry.grid(row=1, column=1, padx=10, pady=5)

isbn_label = tk.Label(window, text="ISBN:", bg=BACKGROUND_COLOR, fg=LABEL_COLOR)
isbn_label.grid(row=2, column=0, sticky=tk.E, padx=10, pady=5)

isbn_entry = tk.Entry(window, bg=ENTRY_BACKGROUND_COLOR)
isbn_entry.grid(row=2, column=1, padx=10, pady=5)

pub_date_label = tk.Label(window, text="Publication Date:", bg=BACKGROUND_COLOR, fg=LABEL_COLOR)
pub_date_label.grid(row=3, column=0, sticky=tk.E, padx=10, pady=5)

pub_date_entry = tk.Entry(window, bg=ENTRY_BACKGROUND_COLOR)
pub_date_entry.grid(row=3, column=1, padx=10, pady=5)

add_button = tk.Button(window, text="Add Book", command=add_book, bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

search_label = tk.Label(window, text="Search:")
search_label.grid(row=5, column=0, sticky=tk.E)

search_entry = tk.Entry(window)
search_entry.grid(row=5, column=1)

search_button = tk.Button(window, text="Search", command=search_books, bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR)
search_button.grid(row=6, column=0, columnspan=2, pady=10)

search_result = tk.Listbox(window, bg=LISTBOX_BACKGROUND_COLOR)
search_result.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

delete_button = tk.Button(window, text="Delete", command=delete_book, bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR)
delete_button.grid(row=8, column=0, columnspan=2, pady=10)

window.mainloop()
