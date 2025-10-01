import torch
import torch.nn as nn
import torchvision.models as models


class CTClassifier(nn.Module):

    def __init__(self, num_classes_classifier=2, num_classes_diagnosis=3):
        super(CTClassifier, self).__init__()

        self.backbone = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)

        in_features = self.backbone.classifier[1].in_features

        self.classifier = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(in_features, num_classes_classifier)
        )

        self.diagnosis_classifier = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(in_features, num_classes_diagnosis)
        )

        self.feature_maps = None

        def hook_fn(module, input, output):
            self.feature_maps = output

        self.backbone.features.register_forward_hook(hook_fn)

    def forward(self, x, return_features=False):
        features = self.backbone.features(x)
        features = nn.functional.adaptive_avg_pool2d(features, (1, 1))
        features = torch.flatten(features, 1)

        output_classifier = self.classifier(features)

        output_diagnosis = self.diagnosis_classifier(features)

        if return_features:
            return output_classifier, output_diagnosis, self.feature_maps
        else:
            return output_classifier, output_diagnosis