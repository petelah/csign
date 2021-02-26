import unittest
from src import create_app, db
from src.models import User, SignIn
import os


class TestSite(unittest.TestCase):
	TEST_PASSWORD = '123456'

	@classmethod
	def setUpClass(cls):
		cls.app = create_app()
		cls.app_context = cls.app.app_context()
		cls.app_context.push()
		cls.client = cls.app.test_client()

		if os.environ.get("FLASK_ENV") != "testing":
			raise EnvironmentError("FLASK_ENV not equal to 'testing'")
		runner = cls.app.test_cli_runner()
		runner.invoke(args=["db-custom", "create"])
		runner.invoke(args=["db-custom", "seed"])

	@classmethod
	def tearDownClass(cls):
		cls.app_context.pop()
		try:
			os.remove('../testdb.db')
		except Exception as e:
			print(e)
			print("Test db unable to be deleted, please delete manually.")
		# Remove qr codes
		for root, dirs, images in os.walk('../static/qr_codes'):
			for image in images:
				os.remove(os.path.join('../static/qr_codes/', image))

	# Helpers
	def login(self, data):
		return self.client.post(
			'/login',
			content_type='application/x-www-form-urlencoded',
			data=data,
			follow_redirects=True
		)

	def register(self, data):
		return self.client.post(
			'/register',
			content_type='application/x-www-form-urlencoded',
			data=data,
			follow_redirects=True
		)

	def logout(self):
		return self.client.get(
			'/logout',
			follow_redirects=True
		)

	def test_is_up(self):
		response = self.client.get("/")

		self.assertEqual(response.status_code, 200)

	def test_change_account(self):
		# Login
		login_data = {
			'email': 'test1@test.com',
			'password': self.TEST_PASSWORD
		}
		response = self.login(login_data)
		self.assertEqual(response.status_code, 200)

		# Change user data
		user = User.query.filter_by(email="test1@test.com").first()
		change_data = {
			'email': 'test99@test.com',
			'business_name': user.business_name,
			'business_url': user.business_name,
			'menu_url': user.menu_url

		}
		response = self.client.post(
			'/account',
			content_type='application/x-www-form-urlencoded',
			data=change_data,
		)
		# Check data has changed
		user = User.query.filter_by(business_name="test1").first()
		self.assertEqual(response.status_code, 302)
		self.assertEqual(user.email, "test99@test.com")

		# Logout to destroy the session
		response = self.logout()
		self.assertEqual(response.status_code, 200)

	def test_change_password(self):
		login_data = {
			'email': 'test1@test.com',
			'password': self.TEST_PASSWORD
		}
		response = self.login(login_data)
		self.assertEqual(response.status_code, 200)

		change_pw = {
			'password': 'test1',
			'confirm_password': 'test1'
		}
		response = self.client.post(
			'/account/change_password',
			content_type='application/x-www-form-urlencoded',
			data=change_pw,
		)
		self.assertEqual(response.status_code, 302)

		# Logout
		response = self.logout()
		self.assertEqual(response.status_code, 200)

		# Login with new password
		login_data = {
			'email': 'test1@test.com',
			'password': 'test1'
		}
		response = self.login(login_data)
		self.assertEqual(response.status_code, 200)

		# Logout
		self.logout()
		self.assertEqual(response.status_code, 200)

	def test_login(self):
		login_data = {
			'email': 'test0@test.com',
			'password': self.TEST_PASSWORD
		}
		response = self.login(login_data)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Account', response.data)

	def test_logout(self):
		# logout
		response = self.logout()
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'C-Sign', response.data)

	def test_register_user(self):
		new_user = {
			'email': 'test8@test.com',
			'business_name': 'test22',
			'first_name': 'test',
			'last_name': 'test',
			'phone_number': '0423456789',
			'address': '40 Test St, Sydney',
			'post_code': '2000',
			'state': 'nsw',
			'menu_url': 'www.google.com',
			'password': self.TEST_PASSWORD,
			'confirm_password': self.TEST_PASSWORD,
		}
		response = self.register(new_user)
		user = User.query.filter_by(email='test8@test.com').first()
		files = os.path.isfile(f'../static/qr_codes/{user.qr_image}')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(user.email, 'test8@test.com')
		self.assertTrue(files, True)

	def test_sign_in(self):
		user_data = {
			'first_name': 'test111',
			'last_name': 'test222',
			'email': 't@t.com',
			'phone_number': '435345345345',
			'symptoms': True
		}
		response = self.client.post(
			'/signin/test1',
			content_type='application/x-www-form-urlencoded',
			data=user_data,
		)
		new_signin = SignIn.query.filter_by(first_name="test111").first()
		self.assertEqual(response.status_code, 302)
		self.assertEqual(new_signin.first_name, 'test111')
		self.assertIn('microsoft', response.location)
