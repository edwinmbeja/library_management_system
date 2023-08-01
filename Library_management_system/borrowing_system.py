from tkinter import Tk, Label, Entry, Button, messagebox
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

engine = create_engine('sqlite:///library.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship('Book', back_populates='author')


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    publication_date = Column(Date)
    author = relationship('Author', back_populates='books')

    def is_checked_out(self):
        loan = session.query(Loan).filter_by(book_id=self.id, returned=False).first()
        return loan is not None


class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact = Column(String)
    membership_status = Column(Boolean)
    loans = relationship('Loan', back_populates='patron')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)


class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    patron_id = Column(Integer, ForeignKey('patrons.id'))
    borrowed_date = Column(Date, default=date.today())  # New column
    due_date = Column(Date)
    returned = Column(Boolean, default=False)
    book = relationship('Book')
    patron = relationship('Patron')


Base.metadata.create_all(engine)


def check_out_book(book_title, patron_id):
    patron = session.query(Patron).get(patron_id)
    if patron is None:
        messagebox.showwarning('Invalid Patron ID', 'The entered patron ID does not exist. Register as a Patron to borrow books.')
        return

    if len(patron.loans) >= 3:
        messagebox.showwarning('Maximum Limit Reached', 'You have reached the maximum limit of books allowed.')
        return

    book = session.query(Book).filter_by(title=book_title).first()  # Query book by title
    if not book:
        messagebox.showwarning('Book Not Found', 'The requested book was not found.')
        return
    if book.is_checked_out():
        messagebox.showwarning('Book Unavailable', 'The requested book is currently checked out.')
        return

    borrowed_date = date.today()
    due_date = borrowed_date + timedelta(weeks=2)

    loan = Loan(book_id=book.id, patron_id=patron.id, borrowed_date=borrowed_date, due_date=due_date)
    session.add(loan)
    session.commit()

    messagebox.showinfo('Book Checked Out', f'You have successfully checked out the book "{book.title}". '
                                            f'Please return it by {due_date}.')


def check_in_book(book_id):
    loan = session.query(Loan).filter_by(book_id=book_id, returned=False).first()
    if not loan:
        messagebox.showwarning('Book Not Checked Out', 'The requested book is not currently checked out.')
        return

    due_date = loan.due_date
    if date.today() > due_date:
        days_overdue = (date.today() - due_date).days
        fine_amount = 10 * days_overdue
        messagebox.showwarning('Book Overdue', f'This book is {days_overdue} days overdue. '
                                                f'A fine of {fine_amount} KES has been imposed.')

        patron = loan.patron
        patron.fines_paid += fine_amount

    loan.returned = True
    session.commit()

    messagebox.showinfo('Book Checked In', f'Thank you for returning the book "{loan.book.title}".')


def handle_check_out():
    book_title = book_id_entry.get()
    patron_id = patron_id_entry.get()
    check_out_book(book_title, patron_id)


def handle_check_in():
    book_id = book_id_entry.get()
    check_in_book(book_id)


root = Tk()
root.title('Library System')
root.iconbitmap('borrow.ico')

book_id_label = Label(root, text='Book Name:')
book_id_label.grid(row=0, column=0)
book_id_entry = Entry(root)
book_id_entry.grid(row=0, column=1)

patron_id_label = Label(root, text='Patron ID:')
patron_id_label.grid(row=1, column=0)
patron_id_entry = Entry(root)
patron_id_entry.grid(row=1, column=1)

check_out_button = Button(root, text='Check Out', command=handle_check_out)
check_out_button.grid(row=2, column=0)

check_in_button = Button(root, text='Check In', command=handle_check_in)
check_in_button.grid(row=2, column=1)

root.mainloop()
