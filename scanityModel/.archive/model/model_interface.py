from datetime import datetime

from archive.model import dummy_model
from model.lung_classification_project.src import config, inference


def analyze(data):
    result = dummy_model.analyze(data)

    result["date"] = datetime.now().isoformat(timespec="seconds")

    return result