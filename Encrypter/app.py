from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.primitives import hashes
from os import urandom
import sys

class FileEncryptor:
    def __init__(self):
        self.key = hashes.Hash(hashes.SHA256(), backend=default_backend()).finalize()

    def generate_random_iv(self, size):
        return urandom(size)

    def encrypt_file(self, input_file, output_file):
        iv = self.generate_random_iv(16)

        with open(input_file, 'rb') as file:
            plaintext = file.read()

        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        with open(output_file, 'wb') as file:
            file.write(iv + urlsafe_b64encode(ciphertext))

        print("File encrypted successfully.")

    def decrypt_file(self, input_file, output_file):
        with open(input_file, 'rb') as file:
            data = file.read()

        iv = data[:16]
        ciphertext = urlsafe_b64decode(data[16:])

        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        with open(output_file, 'wb') as file:
            file.write(plaintext)

        print("File decrypted successfully.")

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <encrypt/decrypt> <input_file> <output_file>")
        sys.exit(1)

    operation = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    encryptor = FileEncryptor()

    if operation == "encrypt":
        encryptor.encrypt_file(input_file, output_file)
    elif operation == "decrypt":
        encryptor.decrypt_file(input_file, output_file)
    else:
        print("Invalid operation. Use 'encrypt' or 'decrypt'.")

if __name__ == "__main__":
    main()


'''
command line inputs : 
python app.py encrypt input.txt encrypted_output.txt
python app.py decrypt encrypted_output.txt decrypted_output.txt

'''
