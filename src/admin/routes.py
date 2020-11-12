from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from src import db, admin
from src.models import User, SignIn


class AdminView(ModelView):
	def is_accessible(self):
		if current_user.is_authenticated:
			if current_user.admin:
				return True
			else:
				return False
		return False


admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(SignIn, db.session))
