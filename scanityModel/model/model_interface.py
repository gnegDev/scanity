from datetime import datetime

from model import dummy_model


def analyze(data):
    result = dummy_model.analyze(data)

    result["date"] = datetime.now().isoformat(timespec="seconds")

    return result