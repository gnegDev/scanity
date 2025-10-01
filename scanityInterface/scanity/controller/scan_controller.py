from base64 import b64encode

import requests
from flask import Blueprint, render_template

from config import API_HOST

scan_controller = Blueprint("scan_controller", __name__, template_folder="../static")
@scan_controller.route("/dashboard/<scan_id>", methods=["GET"])
def render_scan_page(scan_id):
    scan = requests.get(API_HOST + f"/scanity/api/scans/{scan_id}").json()

    scan_url = scan["url"]
    date = scan["date"].replace("T", " ")
    name = scan["name"]
    scan_description = scan["description"]

    scan_filename = scan["filename"]
    scan_image = b64encode(requests.get(API_HOST + f"/scanity/api/scans/file/{scan_filename}").content).decode('utf-8')

    scan_analysis = scan["scan_analysis"]
    scan_analysis["date"] = scan_analysis["date"].replace("T", " ")

    scan_data = {
        "scan_id": scan_id,
        "scan_url": scan_url,
        "scan_filename": scan_filename,
        "scan_image": scan_image,
        "date": date,
        "name": name,
        "scan_description": scan_description,
        "scan_analysis": scan_analysis
    }

    download_link = f"/dashboard/{scan_id}/download"

    return render_template("scan_template.html", scan=scan_data, download_link=download_link)