import torch
from dotenv import load_dotenv
import os
import ast  # ← importante para fazer parsing de listas e tuplas

load_dotenv()

class Config:
    # Carrega valores do .env
    _model_path = os.getenv("MODEL_PATH")
    _class_labels = os.getenv("CLASS_LABELS")
    _image_size = os.getenv("IMAGE_SIZE")
    _threshold = os.getenv("CONFIDENCE_THRESHOLD")
    _debug = os.getenv("DEBUG")
    _api_token = os.getenv("API_TOKEN")
    _token_telegram = os.getenv("TOKEN_TELEGRAM")
    _chat_id = os.getenv("CHAT_ID")
    _message = os.getenv("MESSAGE")

    # Atribuições parseadas corretamente
    MODEL_PATH = _model_path
    CLASS_LABELS = ast.literal_eval(_class_labels)
    IMAGE_SIZE = ast.literal_eval(_image_size)
    CONFIDENCE_THRESHOLD = float(_threshold)
    DEBUG = _debug.lower() in ("true", "1", "yes")
    API_TOKEN = _api_token
    TOKEN_TELEGRAM = _token_telegram
    CHAT_ID = _chat_id
    MESSAGE = _message

    # Dispositivo controlado por torch, ignora o .env pra evitar burrice humana
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
