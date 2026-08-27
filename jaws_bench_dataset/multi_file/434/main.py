import tkinter as tk
from tkinter import filedialog, messagebox
from encryptor import encrypt_file
from decryptor import decrypt_file

def main():
    # Create the main window
    root = tk.Tk()
    root.title("File Encryptor/Decryptor")

    # Function to handle file encryption
    def encrypt():
        file_path = filedialog.askopenfilename()
        if file_path:
            password = password_entry.get()
            if password:
                try:
                    encrypt_file(file_path, password)
                    messagebox.showinfo("Success", "File encrypted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Input Error", "Please enter a password.")

    # Function to handle file decryption
    def decrypt():
        <FILL_HERE>
    # Create and place widgets
    tk.Label(root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(root, show='*')
    password_entry.pack(pady=5)

    encrypt_button = tk.Button(root, text="Encrypt File", command=encrypt)
    encrypt_button.pack(pady=5)

    decrypt_button = tk.Button(root, text="Decrypt File", command=decrypt)
    decrypt_button.pack(pady=5)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()