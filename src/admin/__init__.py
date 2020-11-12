from flask import Blueprint

bp = Blueprint('admin_bp', __name__)

from src.admin import routes


