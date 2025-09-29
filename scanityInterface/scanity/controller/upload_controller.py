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
        filename = file.filename
        file_bytes = file.read()

        if file.content_type == "application/dicom":
            print("converting dicom...")
            file_bytes = converter.dcm_to_png(file_bytes)
            filename = Path(filename).stem + ".png"

        elif file.content_type == "image/jpeg":
            print("converting jpeg...")
            file_bytes = converter.jpg_to_png(file_bytes)
            filename = Path(filename).stem + ".png"

        elif file.content_type == "image/png":
            print("png file...")

        else:
            return render_template("error_template.html", status_code=415, error="Unsupported Media Type", link="/upload")

        files = {'file': (filename, file_bytes, "image/png")}

        response = requests.post(API_HOST + "/scanity/api/scans/upload", data=body, files=files)

        if response.status_code == 201:

            redirect_response = make_response(redirect("/dashboard"))
            return redirect_response

        return render_template("error_template.html", status_code=response.status_code, error=response.text)


    return render_template("upload_template.html")
