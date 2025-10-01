import zipfile
import pydicom
import numpy as np
import cv2
import torch
from torch.utils.data import Dataset, DataLoader
import os
from PIL import Image
import io
from config import Config


class DICOMProcessor:

    @staticmethod
    def dicom_to_array(dicom_bytes):
        try:
            dicom_dataset = pydicom.dcmread(io.BytesIO(dicom_bytes))
            image = dicom_dataset.pixel_array.astype(np.float32)

            # Применение rescale slope и intercept если есть
            if hasattr(dicom_dataset, 'RescaleSlope'):
                image = image * dicom_dataset.RescaleSlope
            if hasattr(dicom_dataset, 'RescaleIntercept'):
                image = image + dicom_dataset.RescaleIntercept

            return image, dicom_dataset
        except Exception as e:
            raise ValueError(f"Ошибка чтения DICOM: {e}")

    @staticmethod
    def apply_lung_window(image, window_level=Config.LUNG_WINDOW_LEVEL,
                          window_width=Config.LUNG_WINDOW_WIDTH):
        window_min = window_level - window_width // 2
        window_max = window_level + window_width // 2

        windowed_image = np.clip(image, window_min, window_max)
        windowed_image = (windowed_image - window_min) / (window_max - window_min)

        return windowed_image

    @staticmethod
    def preprocess_dicom(dicom_bytes, target_size=Config.IMAGE_SIZE):
        image, ds = DICOMProcessor.dicom_to_array(dicom_bytes)

        image = DICOMProcessor.apply_lung_window(image)

        image = (image - np.min(image)) / (np.max(image) - np.min(image) + 1e-8)

        image = cv2.resize(image, (target_size, target_size))

        image = np.stack([image] * 3, axis=-1)

        return image


class CTDataset(Dataset):

    def __init__(self, file_paths, labels, is_train=True):
        self.file_paths = file_paths
        self.labels = labels
        self.is_train = is_train

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        try:
            with open(self.file_paths[idx], 'rb') as f:
                dicom_bytes = f.read()

            image = DICOMProcessor.preprocess_dicom(dicom_bytes)

            image = torch.from_numpy(image).permute(2, 0, 1).float()

            label = torch.tensor(self.labels[idx], dtype=torch.long)

            return image, label

        except Exception as e:
            print(f"Ошибка загрузки файла {self.file_paths[idx]}: {e}")
            return torch.zeros(3, Config.IMAGE_SIZE, Config.IMAGE_SIZE), torch.tensor(0)


def extract_zip_files():
    print(f"Поиск ZIP файлов в: {Config.RAW_DATA_DIR}")

    if not os.path.exists(Config.RAW_DATA_DIR):
        print(f"ОШИБКА: Директория {Config.RAW_DATA_DIR} не существует!")
        return

    all_files = os.listdir(Config.RAW_DATA_DIR)
    print(f"Все файлы в raw директории: {all_files}")

    zip_files = [f for f in all_files if f.lower().endswith('.zip')]

    if not zip_files:
        print("ZIP файлы не найдены!")
        return

    print(f"Найдено ZIP файлов: {len(zip_files)}")

    for zip_file in zip_files:
        zip_path = os.path.join(Config.RAW_DATA_DIR, zip_file)

        extract_dir_name = os.path.splitext(zip_file)[0]
        extract_dir = os.path.join(Config.PROCESSED_DATA_DIR, extract_dir_name)

        print(f"Обработка: {zip_file}")
        print(f"  Будет extracted в: {extract_dir}")

        if os.path.exists(extract_dir):
            import shutil
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir, exist_ok=True)

        print(f"  Извлечение...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            print(f"  Успешно извлечен: {zip_file}")

            extracted_files = os.listdir(extract_dir)
            print(f"  Извлечено файлов в корне: {len(extracted_files)}")

            for item in extracted_files:
                item_path = os.path.join(extract_dir, item)
                if os.path.isdir(item_path):
                    sub_files = os.listdir(item_path)
                    print(f"  В поддиректории {item}: {len(sub_files)} файлов")
                    if sub_files:
                        print(f"    Первые 5: {sub_files[:5]}")

        except Exception as e:
            print(f"  Ошибка при извлечении {zip_file}: {e}")


def is_dicom_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            f.read(128)
            prefix = f.read(4)
            return prefix == b'DICM'
    except:
        return False


def find_dicom_files(directory):
    dicom_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            if (file.lower().endswith(('.dcm', '.dicom')) or
                    is_dicom_file(file_path)):
                dicom_files.append(file_path)

    return dicom_files


def prepare_datasets():
    print("Извлечение ZIP файлов...")
    extract_zip_files()

    data = []
    labels_classifier = []
    labels_diagnosis = []

    class_mapping = {
        'norma_anon': {'classifier': 0, 'diagnosis': 0},
        'pneumonia_anon': {'classifier': 1, 'diagnosis': 2},
        'pneumotorax_anon': {'classifier': 1, 'diagnosis': 1},
    }

    print("Поиск DICOM файлов...")

    for class_name, class_ids in class_mapping.items():
        class_dir = os.path.join(Config.PROCESSED_DATA_DIR, class_name)

        if os.path.exists(class_dir):
            print(f"Поиск DICOM файлов в: {class_dir}")

            dicom_files = find_dicom_files(class_dir)

            print(f"Найдено {len(dicom_files)} DICOM файлов в {class_name}")

            if dicom_files:
                print(f"  Примеры файлов: {dicom_files[:3]}")

            for file_path in dicom_files:
                data.append(file_path)
                labels_classifier.append(class_ids['classifier'])
                labels_diagnosis.append(class_ids['diagnosis'])
        else:
            print(f"Директория не найдена: {class_dir}")

    print(f"Всего найдено DICOM файлов: {len(data)}")

    if len(data) == 0:
        print("ВНИМАНИЕ: Не найдено ни одного DICOM файла!")
        print("Проверьте структуру извлеченных данных:")

        if os.path.exists(Config.PROCESSED_DATA_DIR):
            print(f"Содержимое {Config.PROCESSED_DATA_DIR}:")
            for item in os.listdir(Config.PROCESSED_DATA_DIR):
                item_path = os.path.join(Config.PROCESSED_DATA_DIR, item)
                if os.path.isdir(item_path):
                    print(f"  {item}/")
                    for root, dirs, files in os.walk(item_path):
                        level = root.replace(item_path, '').count(os.sep)
                        indent = ' ' * 2 * level
                        print(f'{indent}{os.path.basename(root)}/')
                        subindent = ' ' * 2 * (level + 1)
                        for file in files[:5]:
                            print(f'{subindent}{file}')
                        if len(files) > 5:
                            print(f'{subindent}... и еще {len(files) - 5} файлов')
                        break

    return data, labels_classifier, labels_diagnosis