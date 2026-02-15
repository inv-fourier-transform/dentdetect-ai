from PIL import Image
import torch
from torchvision import transforms
import model_definition, model_helper

trained_model = None

class_labels = ["Front Breakage", "Front Crushed", "Front Normal", "Rear Breakage", "Rear Crushed", "Rear Normal"]

def predict_damage(image_path):
    image = Image.open(image_path).convert("RGB") # Open binary file and convert to RGB
    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225])
    ])
    transform_image = transform(image) # (3, 224, 224) but our model works on batches like (32, 3, 224, 224)
    image_tensor = transform_image.unsqueeze(0) # (1, 3, 224, 224)

    global trained_model

    if not trained_model:

            trained_model = model_definition.CarClassifierResNetFinal(num_classes=6, dropout_rate=0.33754833234743464)

            # Load the model weights
            trained_model.load_state_dict(torch.load("models\saved_model.pth"))

            # Evaluation mode
            trained_model.eval()

    # Make predictions
    with torch.no_grad():
        output = trained_model(image_tensor) # Eg. [[12, 22, 3, 4, 5, 14]]
        _, predicted_idx_labels = torch.max(output.data, 1) # Eg. 22,1
        return class_labels[predicted_idx_labels.item()]
