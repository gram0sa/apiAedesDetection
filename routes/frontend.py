from flask import Blueprint, render_template
from config.Config import Config

bp = Blueprint("front", __name__)

@bp.route("/")
def index():
    return render_template("index.html", token=Config.API_TOKEN)
