from torch import nn
from torchvision import models

class CarClassifierResNetFinal(nn.Module):
    def __init__(self, num_classes=6, dropout_rate=0.5):
        super(CarClassifierResNetFinal, self).__init__()

        self.model = models.resnet50(weights="DEFAULT")

        # Freeze all the layers. Later, we will unfreeze specific layers (if required)
        for param in self.model.parameters():
            param.requires_grad = False

        # Unfreeze Layer 4 parameters
        for param in self.model.layer4.parameters():
            param.requires_grad = True

        # Replace the FCN
        self.model.fc = nn.Sequential(
            nn.Dropout(p=dropout_rate),
            nn.Linear(self.model.fc.in_features, num_classes)
        )


    def forward(self, x):
        x = self.model(x)

        return x