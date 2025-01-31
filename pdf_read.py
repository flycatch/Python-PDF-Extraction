import os
import re
import fitz
from flask import Flask, request, jsonify


app = Flask(__name__)
UPLOAD_FOLDER = "uploaded_files"
OUTPUT_FOLDER = "output_pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Function to read uploaded pdf file and validations.
    """
    try:
        file = request.files["file"]

        if "file" not in request.files:
            return jsonify({"error": "File not found"}), 400

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        
        if not file.filename.endswith(".pdf"):
            return jsonify({"error": "Invalid file format, Only PDFs are allowed."}), 400
        
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        output_folder = request.form.get("output_folder", "output_pdfs")
        output_folder_path = os.path.join(output_folder)
        # Check if output folder exists
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path, exist_ok=True)
        else:
            return jsonify({"error": f"Output folder '{output_folder}' already exists."}), 400

        result = extract_text_from_pdf(file_path, output_folder)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def extract_text_from_pdf(file_path, output_folder):
    """
    Function used to extract text which contins 'Trans' from pdf and
    create new pdf based on extracted trans_numbers as pdf name and
    respective page.
    """
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

                output_path = os.path.join(output_folder, f"{trans_num}.pdf")
                new_doc.save(output_path)
                new_doc.close()
                saved_files.append(output_path)

            return {"message": "Files saved successfully", "files": saved_files}
        else:
            return {"error": "No 'Trans' number found in the document"}

    except Exception as e:
        return {"error": f"An error occurred during PDF processing: {str(e)}"}


if __name__ == "__main__":
    app.run(debug=True)
