import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from cryptography.fernet import Fernet
import os

KEY_FILE = "encryption_key.key"  # Path to the file where the key will be stored

# Decrypt the data
def decrypt_data(encrypted_data, key):
    try:
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data
    except Exception as e:
        return None  # Return None if decryption fails

# Write decrypted data to a new file
def save_decrypted_data(decrypted_data, output_file):
    if decrypted_data is not None:
        with open(output_file, 'wb') as file:
            file.write(decrypted_data)
        return True
    else:
        return False

# Prompt for file path using Tkinter
def prompt_for_file_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename()
    return file_path

# Prompt for password using Tkinter
def prompt_for_password():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    password = simpledialog.askstring("Password", "Enter password:", show='*')
    return password

# Prompt for file path to save the decrypted file using Tkinter
def prompt_to_save_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    return file_path

def main():
    # Prompt for file path
    file_to_decrypt = prompt_for_file_path()
    if not file_to_decrypt:
        print("No file selected. Exiting.")
        return

    # Prompt for password
    password = prompt_for_password()
    if not password:
        print("No password provided. Exiting.")
        return

    # Generate or load the encryption key
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as file:
            key = file.read()
    else:
        print("Encryption key not found. Please encrypt a file first.")
        return

    # Read encrypted data from the file
    with open(file_to_decrypt, 'rb') as file:
        encrypted_data = file.read()

    # Decrypt the data
    decrypted_data = decrypt_data(encrypted_data, key)

    # Prompt user for file path to save the decrypted file
    save_file_path = prompt_to_save_file()
    if not save_file_path:
        print("No file path provided. Exiting.")
        return

    # Save decrypted data to a new file if decryption is successful
    if save_decrypted_data(decrypted_data, save_file_path):
        print("File decrypted successfully and saved as:", save_file_path)
    else:
        messagebox.showerror("Error", "Password doesn't match. Please enter a valid password.")

if __name__ == "__main__":
    main()
