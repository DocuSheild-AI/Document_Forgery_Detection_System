import torch
import timm
from PIL import Image
import torchvision.transforms as transforms

# Load model globally (runs once)
model = timm.create_model("efficientnet_b4", pretrained=True)
model.eval()

# Image transform
transform = transforms.Compose([
    transforms.Resize((380, 380)),
    transforms.ToTensor(),
])

def run_efficientnet(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(image)

        # Get confidence (softmax-like)
        confidence = torch.nn.functional.softmax(output, dim=1)
        max_conf = torch.max(confidence).item()

        # Dummy classification logic (temporary)
        if max_conf > 0.6:
            label = "Possibly Real"
        else:
            label = "Possibly Forged"

        return {
            "label": label,
            "confidence": round(max_conf * 100, 2)
        }

    except Exception as e:
        return {"error": str(e)}