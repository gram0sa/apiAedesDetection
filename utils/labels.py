# app/utils/labels.py
import json
from config.Config import Config

def get_class_labels():
    try:
        labels = Config.CLASS_LABELS
        if isinstance(labels, str):
            return json.loads(labels)
        return labels
    except Exception as e:
        raise ValueError(f"Erro ao carregar labels: {e}")
