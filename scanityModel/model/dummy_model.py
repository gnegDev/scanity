from random import choice

results = [
    {
        "has_illness": True,
        "diagnosis": "COVID-19",
        "description": "COVID-19"
    },
    {
        "has_illness": True,
        "diagnosis": "Pneumonia",
        "description": "Pneumonia"
    },
    {
        "has_illness": False,
        "diagnosis": "Healthy",
        "description": "No illnesses"
    },
]

def analyze(data):
    result = choice(results)
    result["file"] = data["file"]

    return result