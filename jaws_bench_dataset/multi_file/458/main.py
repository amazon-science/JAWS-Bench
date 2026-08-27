import tkinter as tk
from bsod_window import create_bsod_window

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Fake Blue Screen of Death")
    root.geometry("800x600")
    root.configure(bg='black')

    # Create and display the BSOD window
    create_bsod_window(root)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()