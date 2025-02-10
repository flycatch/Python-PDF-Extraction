import fitz  # PyMuPDF
import re
import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image


def extract_text_from_pdf(file_path, pattern):
    try:
        pdf_file = fitz.open(file_path)
        trans_numbers = []
        page_numbers = []

        # Convert each PDF page to an image
        images = convert_from_path(file_path, dpi=300)  # High DPI for better OCR

        for number, image in enumerate(images):
            # Convert image to text using Tesseract OCR
            text = pytesseract.image_to_string(image)

            # Search for pattern in extracted text
            regex = rf'{re.escape(pattern)}\s+(\d+)'
            matches = re.findall(regex, text)

            if matches:
                trans_numbers.append(matches[0])
                page_numbers.append(number)

        if page_numbers and trans_numbers:
            saved_files = []
            for trans_num, page_num in zip(trans_numbers, page_numbers):
                new_doc = fitz.open()
                new_doc.insert_pdf(pdf_file, from_page=page_num, to_page=page_num)

                output_path = os.path.join(os.path.dirname(file_path), f"{trans_num}.pdf")
                new_doc.save(output_path)
                new_doc.close()
                saved_files.append(output_path)

            return {"message": "Files saved successfully", "files": saved_files}
        else:
            return {"error": f"No '{pattern}' number found in the document"}

    except Exception as e:
        return {"error": f"An error occurred during PDF processing: {str(e)}"}
