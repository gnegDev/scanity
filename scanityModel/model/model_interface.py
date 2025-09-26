import dummy_model
from datetime import datetime

def analyze(data):
    result = dummy_model.analyze(data)
    result["date"] = datetime.now()

    return result