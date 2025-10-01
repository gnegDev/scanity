from base64 import b64encode
from io import BytesIO

from flask import Blueprint, make_response, redirect, render_template, send_file
import requests

from config import API_HOST

download_controller = Blueprint("download_controller", __name__, template_folder="../static")

@download_controller.route("/dashboard/<scan_id>/download", methods=["GET"])
def download_scan(scan_id):
    scan = requests.get(API_HOST + f"/scanity/api/scans/{scan_id}").json()
    scan_filename = scan["dicom_filename"]

    response = requests.get(API_HOST + f"/scanity/api/scans/file/{scan_filename}")

    if response.status_code == 200:
        # redirect_response = make_response(redirect(f"/dashboard/{scan_id}"))
        # return redirect_response
        file = BytesIO(response.content)
        return send_file(file, download_name=scan_filename, mimetype="application/dicom", as_attachment=True)

    return render_template("error_template.html", status_code=response.status_code, error=response.text, link=f"/dashboard/{scan_id}")
