from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

def create_pdf(output_pdf, text):
    try:
        # Create a new PDF file
        pdf = canvas.Canvas(output_pdf)

        # Set the font and font size
        pdf.setFont("Helvetica", 12)

        # Add the text to the PDF
        pdf.drawString(100, 700, text)

        # Save the PDF file
        pdf.save()

        print(f"PDF '{output_pdf}' created successfully.")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
output_pdf_path = "D:/dsa/my_pdf.pdf"
text_to_add = "my name is arkaprabha banerjee trying to code pdf locker"

create_pdf(output_pdf_path, text_to_add)


def pdf_locker(input_pdf, output_pdf, password):
    try:
        # Open the original PDF
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

        print("PDF locked successfully.")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
input_pdf_path = "D:/dsa/my_pdf.pdf"
output_pdf_path = "D:/dsa/output_pdf.pdf"
password = "your_password"

pdf_locker(input_pdf_path, output_pdf_path, password)
