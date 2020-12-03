from flask import Blueprint
from src.config import Config

bp = Blueprint('admin_bp', __name__)

if not Config.GH_TEST:
	from src.admin import routes


