import base64

import cv2
import numpy as np
import torch

from config import Config
from data_preprocessing import DICOMProcessor
from model import CTClassifier  # , GradCAM


class CTScanAnalyzer:

    def __init__(self, model_path=None):
        self.device = Config.DEVICE
        self.model = CTClassifier().to(self.device)

        if model_path and torch.cuda.is_available():
            checkpoint = torch.load(model_path, map_location=self.device)
        elif model_path:
            checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
        else:
            checkpoint = None

        if checkpoint:
            self.model.load_state_dict(checkpoint['model_state_dict'])
            print("Модель загружена успешно")
        else:
            print("Модель не загружена, используются случайные веса")

        self.model.eval()

        # self.grad_cam = GradCAM(self.model, self.model.backbone.features[-1])

    def predict(self, data):
        result = {
            "has_illness": False,
            "diagnosis": "Здоров",
            "description": "Патологии не обнаружено."
        }

        try:
            dicom_bytes = data["file"].read()
            processed_image = DICOMProcessor.preprocess_dicom(dicom_bytes)

            # Преобразование в тензор
            input_tensor = torch.from_numpy(processed_image).permute(2, 0, 1).float()
            input_tensor = input_tensor.unsqueeze(0).to(self.device)

            with torch.no_grad():
                output_classifier, output_diagnosis = self.model(input_tensor)

                has_illness = output_classifier.argmax(dim=1).item() == 1
            result["has_illness"] = bool(has_illness)

            if has_illness:
                diagnosis_idx = output_diagnosis.argmax(dim=1).item()
                diagnosis_label = Config.CLASS_NAMES_DIAGNOSIS[diagnosis_idx]

                result["diagnosis"] = diagnosis_label
                result["description"] = f"Обнаружена патология: {diagnosis_label}"

                # try:
                #     cam_map = self.grad_cam.generate_cam(input_tensor, target_class=1)
                # except Exception as e:
                #     print(f"Ошибка генерации CAM: {e}")

            return result

        except Exception as e:
            result["error"] = f"Ошибка во время анализа: {str(e)}"
            return result

    def _cam_to_base64(self, cam_map):
        cam_map = (cam_map * 255).astype(np.uint8)
        cam_colored = cv2.applyColorMap(cam_map, cv2.COLORMAP_JET)
        _, buffer = cv2.imencode('.png', cam_colored)
        return base64.b64encode(buffer).decode('utf-8')

_analyzer = None


def get_analyzer(model_path="models/best_model.pth"):
    global _analyzer
    if _analyzer is None:
        Config.setup_directories()
        _analyzer = CTScanAnalyzer(model_path)
    return _analyzer


def analyze_ct_scan(data):
    analyzer = get_analyzer()
    return analyzer.predict(data)