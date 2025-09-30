import json

from flask import Flask, request, jsonify, Response
import os

from model import model_interface

API_HOST = os.getenv("API_HOST", "http://localhost:8080")
app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return "pong"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.form.to_dict()

    scan = request.files["file"]
    data["file"] = scan

    print(data)

    response = model_interface.analyze(data)

    print(response)

    return response

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=5050)
