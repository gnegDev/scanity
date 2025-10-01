import zipfile
from io import BytesIO

import requests
from flask import Blueprint, render_template, request, make_response, redirect
from pathlib import Path

from config import API_HOST
from util import converter

upload_page_controller = Blueprint("upload_page_controller", __name__, template_folder="../static")

@upload_page_controller.route("/upload", methods=["GET", "POST"])
def upload_page():
    if request.method == "POST":
        user_id = request.cookies.get('user_id')

        if not user_id:
            redirect_response = make_response(redirect("/auth"))
            return redirect_response

        body = {
            "userId": user_id,

            "date": request.form.get("date"),
            "name": request.form.get("name"),
            "description": request.form.get("description")
        }

        file = request.files["file"]
        filename = Path(file.filename).stem
        file_bytes = file.read()

        files = list()

        if file.content_type == "application/zip":
            print("zip file, parsing...")
            zip_buffer = BytesIO(file_bytes)

            with zipfile.ZipFile(zip_buffer, 'r') as zf:
                for member_name in zf.namelist():
                    suffix = Path(member_name).suffix
                    content_bytes = zf.read(member_name)

                    if suffix == ".dcm":
                        dicom_file_bytes = content_bytes
                        preview_file_bytes = converter.dcm_to_png(content_bytes)
                        files.append(
                            {
                                "file": (filename + "_preview.png", preview_file_bytes, "image/png"),
                                "dicom": (filename + ".dcm", dicom_file_bytes, "application/dicom")
                            }
                        )
                    elif suffix == ".jpeg" or suffix == ".jpg":
                        print("converting jpeg...")
                        dicom_file_bytes = converter.image_to_dcm(file_bytes)
                        preview_file_bytes = converter.jpg_to_png(file_bytes)
                        files.append(
                            {
                                "file": (filename + "_preview.png", preview_file_bytes, "image/png"),
                                "dicom": (filename + ".dcm", dicom_file_bytes, "application/dicom")
                            }
                        )
                    elif suffix == ".png":
                        print("converting png file...")
                        dicom_file_bytes = converter.image_to_dcm(file_bytes)
                        preview_file_bytes = file_bytes
                        files.append(
                            {
                                "file": (filename + "_preview.png", preview_file_bytes, "image/png"),
                                "dicom": (filename + ".dcm", dicom_file_bytes, "application/dicom")
                            }
                        )
                    else:
                        continue

        elif file.content_type == "application/dicom":
            print("dicom file, preparing preview...")
            dicom_file_bytes = file_bytes
            preview_file_bytes = converter.dcm_to_png(file_bytes)
            files.append(
                {
                    "file": (filename + "_preview.png", preview_file_bytes, "image/png"),
                    "dicom": (filename + ".dcm", dicom_file_bytes, "application/dicom")
                }
            )

        elif file.content_type == "image/jpeg":
            print("converting jpeg...")
            dicom_file_bytes = converter.image_to_dcm(file_bytes)
            preview_file_bytes = converter.jpg_to_png(file_bytes)
            files.append(
                {
                    "file": (filename + "_preview.png", preview_file_bytes, "image/png"),
                    "dicom": (filename + ".dcm", dicom_file_bytes, "application/dicom")
                }
            )
        elif file.content_type == "image/png":
            print("converting png file...")
            dicom_file_bytes = converter.image_to_dcm(file_bytes)
            preview_file_bytes = file_bytes
            files.append(
                {
                    "file": (filename + "_preview.png", preview_file_bytes, "image/png"),
                    "dicom": (filename + ".dcm", dicom_file_bytes, "application/dicom")
                }
            )
        else:
            return render_template("error_template.html", status_code=415, error="Unsupported Media Type", link="/upload")

        for file_to_upload in files:
            response = requests.post(API_HOST + "/scanity/api/scans/upload", data=body, files=file_to_upload)
            if response.status_code != 201:
                break
        else:
            redirect_response = make_response(redirect("/dashboard"))
            return redirect_response

        return render_template("error_template.html", status_code=response.status_code, error=response.text)


    return render_template("upload_template.html")
