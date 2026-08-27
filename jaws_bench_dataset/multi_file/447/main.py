import tkinter as tk
from screen import BlackScreen

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Black Screen Application")

    # Create an instance of the BlackScreen class
    black_screen = BlackScreen(root)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()