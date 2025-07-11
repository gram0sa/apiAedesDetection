# main.py
from __init__ import create_app
import os
from config.Config import Config

if __name__ == "__main__":
    app = create_app()

    # Lê da .env com fallback básico
    debug = Config.DEBUG
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")

    app.run(debug=debug, host=host, port=port)
