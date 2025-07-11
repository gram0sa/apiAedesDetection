# app/model/loader.py
import onnxruntime as ort
from config.Config import Config

def load_model():
    providers = ["CUDAExecutionProvider"] if Config.DEVICE == "cuda" else ["CPUExecutionProvider"]
    # print(providers)

    session = ort.InferenceSession(
        Config.MODEL_PATH,
        providers=providers
    )

    return session
