import fitz
import re
import os

def extract_text_from_pdf(file_path):
    try:
        pdf_file = fitz.open(file_path)
        trans_numbers = []
        page_numbers = []

        for number, page in enumerate(pdf_file):
            data = page.get_text("text")
            matches = re.findall(r'Trans\s+(\d+)', data)
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
            return {"error": "No 'Trans' number found in the document"}

    except Exception as e:
        return {"error": f"An error occurred during PDF processing: {str(e)}"}
