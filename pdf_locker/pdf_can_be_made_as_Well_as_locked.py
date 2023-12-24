# Import necessary modules from the tkinter library and other libraries
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

# Define a class for the PDF Generator and Locker application
class PDFGeneratorLockerApp:
    # Constructor method to initialize the application
    def __init__(self, root):
        # Set the root window and its title
        self.root = root
        self.root.title("PDF Generator & Locker")

        # Text input widget
        self.text_entry = tk.Entry(root, width=50)
        self.text_entry.pack(pady=10)

        # "Create PDF" button
        self.create_pdf_button = tk.Button(root, text="Create PDF", command=self.create_pdf)
        self.create_pdf_button.pack(pady=5)

        # "Lock PDF" button
        self.lock_pdf_button = tk.Button(root, text="Lock PDF", command=self.lock_pdf)
        self.lock_pdf_button.pack(pady=5)

    # Method to create a PDF with entered text
    def create_pdf(self):
        # Get text from the entry widget and ask for the output file path
        text_to_add = self.text_entry.get()
        output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        # Check if text and output path are provided
        if text_to_add and output_pdf_path:
            # Call the create_pdf function to generate the PDF
            create_pdf(output_pdf_path, text_to_add)
            # Show a message box indicating successful PDF creation
            messagebox.showinfo("PDF Created", f"PDF '{output_pdf_path}' created successfully.")
        else:
            # Show a warning message if input is missing
            messagebox.showwarning("Error", "Please enter text and select a valid output path.")

    # Method to lock an existing PDF with a password
    def lock_pdf(self):
        # Ask for input and output PDF file paths and a password
        input_pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        password = simpledialog.askstring("Password", "Enter password for PDF encryption:")

        # Check if all required information is provided
        if input_pdf_path and output_pdf_path and password:
            # Call the pdf_locker function to lock the PDF
            pdf_locker(input_pdf_path, output_pdf_path, password)
            # Show a message box indicating successful PDF locking
            messagebox.showinfo("PDF Locked", f"PDF '{output_pdf_path}' locked successfully.")
        else:
            # Show a warning message if input is missing
            messagebox.showwarning("Error", "Please select valid input and output paths, and enter a password.")

# Function to create a PDF with specified text
def create_pdf(output_pdf, text):
    try:
        # Create a new PDF file using the reportlab library
        pdf = canvas.Canvas(output_pdf)

        # Set the font and font size
        pdf.setFont("Helvetica", 12)

        # Add the text to the PDF at specified coordinates
        pdf.drawString(100, 700, text)

        # Save the PDF file
        pdf.save()

    except Exception as e:
        # Show an error message if an exception occurs
        messagebox.showerror("Error", f"Error: {e}")

# Function to lock an existing PDF with a password
def pdf_locker(input_pdf, output_pdf, password):
    try:
        # Open the original PDF using PyPDF2
        with open(input_pdf, 'rb') as file:
            pdf_reader = PdfReader(file)

            # Create a new PDF writer
            pdf_writer = PdfWriter()

            # Add all pages to the writer
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            # Encrypt the PDF with a password
            pdf_writer.encrypt(password)

            # Write the encrypted PDF to a new file
            with open(output_pdf, 'wb') as output_file:
                pdf_writer.write(output_file)

    except Exception as e:
        # Show an error message if an exception occurs
        messagebox.showerror("Error", f"Error: {e}")

# Main part of the script
if __name__ == "__main__":
    # Create the Tkinter root window
    root = tk.Tk()

    # Create an instance of the PDFGeneratorLockerApp class
    app = PDFGeneratorLockerApp(root)

    # Start the Tkinter event loop
    root.mainloop()
