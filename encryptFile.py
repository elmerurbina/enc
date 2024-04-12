import tkinter as tk
from tkinter import filedialog, simpledialog
from cryptography.fernet import Fernet
import os

KEY_FILE = "encryption_key.key"  # Path to the file where the key will be stored

# Generate a key from the provided password
def generate_key_from_password(password):
    return Fernet.generate_key()

# Encrypt the data
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    return encrypted_data

# Write encrypted data to a new file
def save_encrypted_data(encrypted_data, output_file):
    with open(output_file, 'wb') as file:
        file.write(encrypted_data)

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

# Generate or load the encryption key
def get_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as file:
            key = file.read()
    else:
        password = prompt_for_password()
        if not password:
            print("No password provided. Exiting.")
            return None
        key = generate_key_from_password(password.encode())
        with open(KEY_FILE, 'wb') as file:
            file.write(key)
    return key

def main():
    # Prompt for file path
    file_to_encrypt = prompt_for_file_path()
    if not file_to_encrypt:
        print("No file selected. Exiting.")
        return

    # Generate or load the encryption key
    key = get_key()
    if not key:
        return

    # Read data from the file
    with open(file_to_encrypt, 'rb') as file:
        data = file.read()

    # Encrypt the data
    encrypted_data = encrypt_data(data, key)

    # Add ".enc" extension to the original file name
    output_file = file_to_encrypt + ".enc"

    # Save encrypted data to a new file
    save_encrypted_data(encrypted_data, output_file)

    print("File encrypted successfully.")

if __name__ == "__main__":
    main()
