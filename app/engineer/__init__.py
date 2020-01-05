from flask import Blueprint

bp = Blueprint('engineer', __name__)

from app.engineer import routes