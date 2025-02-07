from flask import Blueprint, request, jsonify, send_from_directory, render_template
import os
import zipfile
from datetime import datetime
from .pdf_processor import extract_text_from_pdf
from .utils import delete_old_files

main_bp = Blueprint('main', __name__)

# Ensure correct path
UPLOAD_FOLDER = os.path.abspath("uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main_bp.route("/", methods=["GET"])
def index():
    """Route to render the upload page."""
    return render_template("upload_file.html")

@main_bp.route("/upload", methods=["POST"])
def upload_file():
    try:
        file = request.files["file"]
        pattern = request.form.get("pattern", r'Trans\s+(\d+)')
        download_format = request.form.get("download_format", "pdf")

        if not file or file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.endswith(".pdf"):
            return jsonify({"error": "Invalid file format. Only PDFs are allowed."}), 400

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{file.filename}")
        file.save(file_path)

        result = extract_text_from_pdf(file_path, pattern)

        if "error" in result:
            return jsonify({"error": result["error"]}), 400

        saved_files = result["files"]

        if not saved_files:
            return jsonify({"error": "No files were processed."}), 400

        if download_format == "pdf":
            file_urls = [f"/download/{os.path.basename(file)}" for file in saved_files]
            return jsonify({"files": file_urls})

        elif download_format == "zip":
            zip_filename = f"processed_{timestamp}.zip"
            zip_filepath = os.path.join(UPLOAD_FOLDER, zip_filename)

            with zipfile.ZipFile(zip_filepath, "w") as zipf:
                for file in saved_files:
                    zipf.write(file, os.path.basename(file))
            print(f"/download/{zip_filename}")
            return jsonify({"zip_file": f"/download/{zip_filename}"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        delete_old_files(UPLOAD_FOLDER)

@main_bp.route("/download/<filename>")
def download_file(filename):
    """Serve individual PDFs for download."""
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
