from flask import Blueprint, request, jsonify, send_from_directory, render_template
import os
import zipfile
from .pdf_processor import extract_text_from_pdf
from .utils import delete_files_in_folder


main_bp = Blueprint('main', __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main_bp.route("/", methods=["GET"])
def index():
    """
    Route to render the upload file.
    """
    return render_template("upload_file.html")

@main_bp.route("/upload", methods=["POST"])
def upload_file():
    try:
        file = request.files["file"]
        pattern = request.form.get("pattern", r'Trans\s+(\d+)')

        if "file" not in request.files:
            return jsonify({"error": "File not found"}), 400

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        
        if not file.filename.endswith(".pdf"):
            return jsonify({"error": "Invalid file format, Only PDFs are allowed."}), 400
        
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        result = extract_text_from_pdf(file_path, pattern)

        if "error" in result:
            return jsonify(result), 400
        
        saved_file = result["files"]

        if len(saved_file) == 1:
            folder_path, filename = os.path.split(saved_file[0])
            absolute_folder_path = os.path.abspath(folder_path)
            response = send_from_directory(absolute_folder_path, filename, as_attachment=True)
        else:
            zip_filename = "processed_pdf.zip"
            zip_filepath = os.path.join(UPLOAD_FOLDER, zip_filename)

            with zipfile.ZipFile(zip_filepath, "w") as zipf:
                for file in saved_file:
                    zipf.write(file, os.path.basename(file))

            response = send_from_directory(os.path.abspath(UPLOAD_FOLDER), zip_filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        delete_files_in_folder(UPLOAD_FOLDER)

    return response
