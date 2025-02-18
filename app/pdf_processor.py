import fitz  # PyMuPDF
import re
import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from rapidfuzz import fuzz, process  # For fuzzy matching

def extract_text_from_pdf(file_path, patterns):
    try:
        pdf_file = fitz.open(file_path)
        trans_numbers = []
        page_numbers = []

        # Convert each PDF page to an image
        images = convert_from_path(file_path, dpi=300)  # High DPI for better OCR

        # for number, image in enumerate(images):
        #     # Convert image to text using Tesseract OCR
        #     text = pytesseract.image_to_string(image)

        #     for pattern in patterns:
        #         regex = rf'{re.escape(pattern)}\s+(\d+)'
        #         matches = re.findall(regex, text)

        #         if matches:
        #             trans_numbers.append(matches[0])
        #             page_numbers.append(number)
        #             break  # Stop checking once a pattern matches on a page

        for number, image in enumerate(images):
            # Convert image to text using Tesseract OCR
            text = pytesseract.image_to_string(image)

            for pattern in patterns:
                # Use fuzzy matching to find a close match
                best_match, score, _ = process.extractOne(pattern, text.split("\n"), scorer=fuzz.partial_ratio)

                if score > 80:  # If similarity score is high
                    print(1)
                    print(2)
                    print(best_match)
                    match = re.findall('\d{3,}', best_match)  # Match 3 or more digits
                    print(match)
                    if match:
                        trans_numbers.append(match[0])
                        page_numbers.append(number)
                        break  # Stop checking once a match is found

            # # Search for pattern in extracted text
            # regex = rf'{re.escape(pattern)}\s+(\d+)'
            # matches = re.findall(regex, text)

            # if matches:
            #     trans_numbers.append(matches[0])
            #     page_numbers.append(number)

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
            return {"error": f"No matches found in the document"}

    except Exception as e:
        return {"error": f"An error occurred during PDF processing: {str(e)}"}
