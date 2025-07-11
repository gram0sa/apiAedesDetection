import numpy as np
from utils.labels import get_class_labels
import torch
from services.image_drawer import draw_label_on_image_bytes


def infer(session, image_tensor, image_bytes):  # ← recebe os bytes crus da imagem
    input_tensor = image_tensor.unsqueeze(0).numpy()
    inputs = {session.get_inputs()[0].name: input_tensor}
    outputs = session.run(None, inputs)

    output_array = torch.nn.functional.softmax(torch.tensor(outputs[0][0]), dim=0).numpy()
    predicted_idx = int(np.argmax(output_array))
    predicted_label = get_class_labels()[predicted_idx]
    confidence = float(np.max(output_array))

    # Gera a imagem anotada corretamente
    image_b64 = draw_label_on_image_bytes(image_bytes, predicted_label, confidence)

    return {
        "class_index": predicted_idx,
        "class_name": predicted_label,
        "confidence": confidence,
        "image_base64": image_b64
    }