from functools import wraps
from flask import abort, request
from flask_login import current_user
from src.models import User


def verify_business(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		url_args = request.view_args
		user = User.query.filter_by(business_name=url_args["business_name"]).first()
		if user is None or not user.verified:
			return abort(404)
		return f(*args, **kwargs)
	return decorated_function


def admin_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if current_user.is_authenticated:
			user = User.query.get(current_user.id)
			if not user.admin:
				return abort(401)
		else:
			return abort(401)
		return f(*args, **kwargs)
	return decorated_function
