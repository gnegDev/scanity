import os
from datetime import datetime

from flask import Flask, request

from config import Config
from inference import analyze_ct_scan

# from model import model_interface

API_HOST = os.getenv("API_HOST", "http://localhost:8080")
app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return "pong"

@app.route("/analyze", methods=["POST"])
def analyze_controller():
    data = request.form.to_dict()

    scan = request.files["file"]
    data["file"] = scan

    print(data)

    # response = model_interface.analyze(data)
    response = analyze(data)

    print(response)

    return response

def analyze(data):

    # sample_data = {
    #     "userId": "test_user",
    #     "date": "2024-01-01",
    #     "name": "test_scan",
    #     "description": "test CT scan",
    #     "file": open("data/test.dcm", "rb")  # Замените на реальный путь
    # }

    # try:
    result = analyze_ct_scan(data)
    print("Результат анализа:")
    print(f"Has illness: {result['has_illness']}")
    print(f"Diagnosis: {result['diagnosis']}")
    print(f"Description: {result['description']}")

    if 'error' in result:
        print(f"Error: {result['error']}")

    result["date"] = datetime.now().isoformat()
    return result
    # except:
    #     print("error")
    # finally:
    #     data["file"].close()


# if __name__ == "__main__":
#     main()
if __name__ == '__main__':
    Config.setup_directories()
    app.run("0.0.0.0", debug=True, port=5050)
