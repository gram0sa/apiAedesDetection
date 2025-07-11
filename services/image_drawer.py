import numpy as np
import cv2
import base64
from event.MessageTelegram import TelegramNotifier


def draw_label_on_image_bytes(image_bytes, label, confidence):
    file_bytes = np.frombuffer(image_bytes, np.uint8)
    image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image_bgr is None:
        raise ValueError("Falha ao decodificar a imagem")

    h, w, _ = image_bgr.shape

    # Bounding box central estimado
    box_w, box_h = int(w * 0.8), int(h * 0.8)
    x1 = (w - box_w) // 2
    y1 = (h - box_h) // 2
    x2 = x1 + box_w
    y2 = y1 + box_h

    # Escolhe cor com base na classe
    color = (0, 0, 255) if label.lower() == "aedes" else (0, 255, 0)

    # Desenha o retângulo fino
    cv2.rectangle(image_bgr, (x1, y1), (x2, y2), color, 1)

    # Label
    # print(confidence)
    text = f"{label} ({confidence:.2f}%)"
    font_scale = 0.45
    thickness = 1
    (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)

    text_x = x1 + 5
    text_y = y1 - 10 if y1 - 10 > 10 else y1 + text_h + 10

    cv2.putText(
        image_bgr,
        text,
        (text_x, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness,
        lineType=cv2.LINE_AA
    )

    # → Codifica para base64
    _, buffer = cv2.imencode(".jpg", image_bgr)
    jpg_bytes = buffer.tobytes()
    image_base64 = base64.b64encode(jpg_bytes).decode("utf-8")

    return image_base64, jpg_bytes
