import tkinter as tk
from tkinter import filedialog
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.primitives import hashes
from os import urandom

class FileEncryptor:
    def __init__(self):
        # Generate a random AES key using SHA256
        self.key = hashes.Hash(hashes.SHA256(), backend=default_backend()).finalize()

    def generate_random_iv(self, size):
        return urandom(size)

    def encrypt_file(self, input_file, output_file):
        # Generate a random IV with a size compatible with AES block size (e.g., 16 bytes)
        iv = self.generate_random_iv(16)

        with open(input_file, 'rb') as file:
            plaintext = file.read()

        # Create a Cipher object with AES algorithm and CFB mode
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        # Create an encryptor using the Cipher
        encryptor = cipher.encryptor()
        # Encrypt the plaintext
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        # Write the IV and encrypted data to the output file
        with open(output_file, 'wb') as file:
            file.write(iv + urlsafe_b64encode(ciphertext))

        print("File encrypted successfully.")

    def decrypt_file(self, input_file, output_file):
        # Read the IV and ciphertext from the input file
        with open(input_file, 'rb') as file:
            data = file.read()

        # Extract the IV and ciphertext
        iv = data[:16]
        ciphertext = urlsafe_b64decode(data[16:])

        # Create a Cipher object with AES algorithm and CFB mode
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        # Create a decryptor using the Cipher
        decryptor = cipher.decryptor()
        # Decrypt the ciphertext
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Write the decrypted plaintext to the output file
        with open(output_file, 'wb') as file:
            file.write(plaintext)

        print("File decrypted successfully.")

class FileEncryptorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("File Encryptor")

        # Create labels
        self.label_file = tk.Label(self.master, text="Select File:")

        # Create buttons
        self.button_browse = tk.Button(self.master, text="Browse", command=self.browse_file)
        self.button_encrypt = tk.Button(self.master, text="Encrypt", command=self.encrypt_file)
        self.button_decrypt = tk.Button(self.master, text="Decrypt", command=self.decrypt_file)

        # Set layout using grid
        self.label_file.grid(row=0, column=0, padx=10, pady=10)
        self.button_browse.grid(row=0, column=1, padx=10, pady=10)
        self.button_encrypt.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.button_decrypt.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Initialize FileEncryptor
        self.encryptor = FileEncryptor()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.file_path = file_path

    def encrypt_file(self):
        if not hasattr(self, 'file_path'):
            print("Please select a file.")
            return

        output_file = self.file_path.replace('.txt', '_encrypted.txt')
        self.encryptor.encrypt_file(self.file_path, output_file)

    def decrypt_file(self):
        if not hasattr(self, 'file_path'):
            print("Please select a file.")
            return

        output_file = self.file_path.replace('_encrypted.txt', '_decrypted.txt')
        self.encryptor.decrypt_file(self.file_path, output_file)

def main():
    root = tk.Tk()
    gui = FileEncryptorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
