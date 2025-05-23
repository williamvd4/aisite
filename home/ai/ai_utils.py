# File: ai_utils.py

from django.conf import settings
import PyPDF2 # Add this import
import io # Add this import

# Function to extract text from a PDF file stream
def extract_text_from_pdf(pdf_file_stream):
    text = ""
    try:
        # Ensure the stream is at the beginning
        pdf_file_stream.seek(0)
        reader = PyPDF2.PdfReader(pdf_file_stream)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    return text
