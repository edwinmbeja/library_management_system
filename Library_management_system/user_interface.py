import tkinter as tk
import subprocess

# Global variable to keep track of the currently opened process
current_process = None

def open_file(filename):
    global current_process
    if current_process:
        # Close the existing process if any
        current_process.kill()
    # Open the new file
    current_process = subprocess.Popen(["python", filename])

def open_book_management():
    open_file("book_management.py")

def open_borrowing_system():
    open_file("borrowing_system.py")

def open_patron_management():
    open_file("patron_management.py")

def open_registration_system():
    open_file("registration_system.py")

def open_report():
    open_file("report_system.py")

# Create the main Tkinter window
root = tk.Tk()
root.title("Edwin's Library Management System")
root.geometry("600x600+490+60")
root.configure(bg="#F9F9F9")
root.iconbitmap('library.ico')
root.resizable(False, False)

# Title for the UI window
title = tk.Label(root, bg="#FF4081", fg="#FFFFFF", text="EDWIN LIBRARY", font=("Helvetica", 30, "bold"))
title.pack(pady=(10, 0), ipady=30, fill='x')

# Creating button frames for the left, right, and center
left_frame = tk.Frame(root)
left_frame.pack(side="left", padx=10, pady=5, fill="both")

right_frame = tk.Frame(root)
right_frame.pack(side="right", padx=10, pady=5, fill="both")

center_frame = tk.Frame(root)
center_frame.pack(side="bottom", padx=10, pady=5, fill="both")

# Create buttons for each Python file
button_background_color = "#4CAF50"
button_foreground_color = "#FFFFFF"

book_management_button = tk.Button(left_frame, text="Book Management", command=open_book_management, width=30, bg=button_background_color, fg=button_foreground_color)
borrowing_system_button = tk.Button(right_frame, text="Borrowing System", command=open_borrowing_system, width=30, bg=button_background_color, fg=button_foreground_color)
patron_management_button = tk.Button(left_frame, text="Patron Management", command=open_patron_management, width=30, bg=button_background_color, fg=button_foreground_color)
registration_system_button = tk.Button(right_frame, text="Registration System", command=open_registration_system, width=30, bg=button_background_color, fg=button_foreground_color)
report_system_button = tk.Button(center_frame, text="Reports", command=open_report, width=30, bg=button_background_color, fg=button_foreground_color)

# Placing the buttons in the window
book_management_button.pack(pady=5)
borrowing_system_button.pack(pady=5)
patron_management_button.pack(pady=5)
registration_system_button.pack(pady=5)
report_system_button.pack(pady=5)

# Run the main UI
root.mainloop()
