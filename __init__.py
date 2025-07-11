from flask import Flask
from routes.predict import bp as predict_bp
from routes.frontend import bp as front_bp
from config.Config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registro das rotas
    app.register_blueprint(predict_bp, url_prefix="/api")
    app.register_blueprint(front_bp)

    return app
