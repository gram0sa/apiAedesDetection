import time
import logging
from io import BytesIO
from flask import Blueprint, request, jsonify
from model.loader import load_model
from model.infer import infer
from services.preprocessor import preprocess_image
from services.image_drawer import draw_label_on_image_bytes
from event.MessageTelegram import TelegramNotifier
from config.Config import Config

bp = Blueprint("predict", __name__)

# Carrega o modelo só uma vez
session = load_model()

# Logging raiz
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)


@bp.route("/predict", methods=["POST"])
async def predict():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token de autenticação ausente"}), 401

    token = auth_header.split(" ")[1]

    if token != Config.API_TOKEN:
        return jsonify({"error": "Token inválido"}), 403

    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Arquivo vazio"}), 400

    try:
        image_bytes = file.read()
        filename = file.filename or "sem_nome.jpg"
        ip_cliente = request.remote_addr or "desconhecido"
        start_time = time.time()

        input_tensor = preprocess_image(BytesIO(image_bytes))
        result = infer(session, input_tensor, image_bytes)

        confidence = result["confidence"] * 100

        # Marca a imagem original
        image_base64, image_bytes_processed = draw_label_on_image_bytes(image_bytes, result["class_name"], confidence)

        inference_time = round((time.time() - start_time) * 1000, 2)

        logging.info(
            f"[{ip_cliente}] Arquivo: {filename} | Resultado: {result['class_name']} ({result['class_index']}) | Tempo: {inference_time}ms"
        )

        # Envia pro Telegram (assíncrono de verdade agora)
        telegram = TelegramNotifier()
        await telegram.send_photo(image_bytes_processed, filename)

        return jsonify({
            "annotated_image": image_base64,
            "label": result["class_name"],
            "class_id": result["class_index"],
            "confidence": confidence,
            "inference_time_ms": inference_time
        })

    except Exception as e:
        logging.exception("Erro na inferência")
        return jsonify({"error": str(e)}), 500
