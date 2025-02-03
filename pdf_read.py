import os
import re
import fitz
import zipfile
from flask import Flask, request, jsonify, send_from_directory


app = Flask(__name__)
UPLOAD_FOLDER = "temp_folder"
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

        # # output_folder = request.form.get("output_folder", "output_pdfs")
        # output_folder_path = os.path.join(output_folder)
        # # Check if output folder exists
        # if not os.path.exists(output_folder_path):
        #     os.makedirs(output_folder_path, exist_ok=True)
        # else:
        #     return jsonify({"error": f"Output folder '{output_folder}' already exists."}), 400

        result = extract_text_from_pdf(file_path)

        if "error" in result:
            return jsonify(result), 400
        
        saved_file = result["files"]

        if len(saved_file) == 1:
            folder_path, filename = os.path.split(saved_file[0])
            absolute_folder_path = os.path.abspath(folder_path)
            response =  send_from_directory(absolute_folder_path, filename, as_attachment=True)
        else:
            zip_filename = "processed_pdf.zip"
            zip_filepath = os.path.join(UPLOAD_FOLDER, zip_filename)

            with zipfile.ZipFile(zip_filepath, "w") as zipf:
                for file in saved_file:
                    zipf.write(file, os.path.basename(file))  # Store files with their names

            response = send_from_directory(os.path.abspath(UPLOAD_FOLDER), zip_filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        # Ensure all files and directories are deleted after processing
        delete_files_in_folder(UPLOAD_FOLDER)

    return response


def extract_text_from_pdf(file_path):
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

                output_path = os.path.join(UPLOAD_FOLDER, f"{trans_num}.pdf")
                new_doc.save(output_path)
                new_doc.close()
                saved_files.append(output_path)

            return {"message": "Files saved successfully", "files": saved_files}
        else:
            return {"error": "No 'Trans' number found in the document"}

    except Exception as e:
        return {"error": f"An error occurred during PDF processing: {str(e)}"}


def delete_files_in_folder(folder_path):
    """
    Deletes all files inside the specified folder, without deleting the folder itself.
    """
    try:
        # Loop through and remove all files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        app.logger.info(f"Successfully deleted files in folder: {folder_path}")
    except Exception as e:
        app.logger.error(f"Failed to delete files in folder {folder_path}: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
