from torchvision import transforms
from PIL import Image
from config.Config import Config

# Transforma em tensor com normalização padrão do ImageNet
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

def preprocess_image(image_bytes):
    try:
        image = Image.open(image_bytes).convert("RGB")
        tensor = transform(image)
        return tensor
    except Exception as e:
        raise ValueError(f"Erro ao preprocessar imagem: {e}")
