from base64 import b64encode

import requests
from flask import Blueprint, render_template, request, make_response, redirect

from config import API_HOST

dashboard_controller = Blueprint("dashboard_controller", __name__, template_folder="../static")
@dashboard_controller.route("/dashboard", methods=["GET"])
def render_main_page():
    user_id = request.cookies.get('user_id')

    if not user_id:
        redirect_response = make_response(redirect("/auth"))
        return redirect_response

    user = requests.get(API_HOST + f"/scanity/api/users/{user_id}")
    scans = list()

    for scan in user.json()["scans"]:
        scan_id = scan["id"]

        scan_filename = scan["filename"]
        scan_image = b64encode(requests.get(API_HOST + f"/scanity/api/scans/file/{scan_filename}").content).decode('utf-8')

        scan_url = scan["url"]
        date = scan["date"].replace("T", " ")
        name = scan["name"]

        diagnosis = scan["scan_analysis"]["diagnosis"]

        scans.append({
            "scan_id": scan_id,
            "scan_url": scan_url,
            "scan_image": scan_image,
            "date": date,
            "name": name,
            "diagnosis": diagnosis
        })

    return render_template("dashboard_template.html", scans=scans)