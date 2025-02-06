from flask import Blueprint, request, jsonify, send_from_directory, render_template
import os
import zipfile
from .pdf_processor import extract_text_from_pdf
from .utils import delete_old_files


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
        download_format = request.form.get("download_format", "pdf")  # Get download format

        if not file:
            return render_template("upload_file.html", error="File not found")

        if file.filename == "":
            return render_template("upload_file.html", error="No file selected")

        if not file.filename.endswith(".pdf"):
            return render_template("upload_file.html", error="Invalid file format. Only PDFs are allowed.")

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        result = extract_text_from_pdf(file_path, pattern)

        if "error" in result:
            return render_template("upload_file.html", error=result["error"])

        saved_file = result["files"]

        if download_format == "pdf":
            # print(saved_file)
            # for file in saved_file:
            #     print(file)
            #     folder_path, filename = os.path.split(file)
            #     absolute_folder_path = os.path.abspath(folder_path)
            #     response = send_from_directory(absolute_folder_path, filename, as_attachment=True)

            # file_urls = [request.host_url + "download/" + os.path.basename(file) for file in saved_file]
            # return jsonify({"files": file_urls})  # Return JSON list of file URLs
            return render_template("download_files.html", file_urls=[f"/download/{os.path.basename(file)}" for file in saved_file])

        elif download_format == "zip":
            # if len(saved_file) == 1:
            #     folder_path, filename = os.path.split(saved_file[0])
            #     absolute_folder_path = os.path.abspath(folder_path)
            #     response = send_from_directory(absolute_folder_path, filename, as_attachment=True)
            # else:
                zip_filename = "processed_pdf.zip"
                zip_filepath = os.path.join(UPLOAD_FOLDER, zip_filename)

                with zipfile.ZipFile(zip_filepath, "w") as zipf:
                    for file in saved_file:
                        zipf.write(file, os.path.basename(file))

                response = send_from_directory(os.path.abspath(UPLOAD_FOLDER), zip_filename, as_attachment=True)

    except Exception as e:
        return render_template("upload_file.html", error=f"An error occurred: {str(e)}")

    finally:
        # delete_files_in_folder(UPLOAD_FOLDER)
        delete_old_files(UPLOAD_FOLDER)

    return response

@main_bp.route("/download/<filename>")
def download_file(filename):
    """ Serve individual PDFs for separate downloads """
    return send_from_directory(os.path.abspath(UPLOAD_FOLDER), filename, as_attachment=True)
