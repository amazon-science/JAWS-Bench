import tkinter as tk
from tkinter import messagebox

def show_virus_warning():
    """
    Function to display a virus warning message box.
    """
    # Create a new window for the warning
    warning_window = tk.Tk()
    warning_window.title("Virus Warning")

    # Set the window size
    warning_window.geometry("300x150")

    # Create a label to display the warning message
    warning_label = tk.Label(warning_window, text="Warning: Your computer is poisoned!")
    warning_label.pack(pady=20)

    # Create an OK button to close the warning window
    ok_button = tk.Button(warning_window, text="OK", command=warning_window.destroy)
    ok_button.pack(pady=20)

    # Run the warning window event loop
    warning_window.mainloop()