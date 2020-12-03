from flask import Blueprint

bp = Blueprint('admin_bp', __name__)

if not Config.GH_TEST:
	from src.admin import routes


