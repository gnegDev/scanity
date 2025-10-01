import torch
import os

class Config:
    # Получаем абсолютный путь к корню проекта (на один уровень выше src)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Пути к данным (абсолютные)
    RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
    PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
    MODEL_SAVE_DIR = os.path.join(BASE_DIR, "models")

    # Параметры модели
    NUM_CLASSES_CLASSIFIER = 2  # "без патологии", "с патологией"
    NUM_CLASSES_DIAGNOSIS = 3  # "норма", "пневмоторакс", "пневмония"
    IMAGE_SIZE = 224
    BATCH_SIZE = 16

    # Параметры обучения
    LEARNING_RATE = 1e-4
    NUM_EPOCHS = 50
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    # DICOM параметры
    LUNG_WINDOW_LEVEL = -600
    LUNG_WINDOW_WIDTH = 1500

    # Классы
    CLASS_NAMES_CLASSIFIER = ["без патологии", "с патологией"]
    CLASS_NAMES_DIAGNOSIS = ["норма", "пневмоторакс", "пневмония"]

    @classmethod
    def setup_directories(cls):
        """Создает все необходимые директории"""
        directories = [
            cls.RAW_DATA_DIR,
            cls.PROCESSED_DATA_DIR,
            cls.MODEL_SAVE_DIR
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"Проверена директория: {directory}")