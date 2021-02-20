import unittest
from src import create_app, db, Bcrypt
from src.models import User, SignIn
from src.services import generate_qr, strip_chars


class TestUser(unittest.TestCase):
	# @classmethod
	# def setUp(cls):
	# 	cls.app = create_app()
	# 	cls.app_context = cls.app.app_context()
	# 	cls.app_context.push()
	# 	cls.client = cls.app.test_client()
	#
	# 	if os.environ.get("FLASK_ENV") != "testing":
	# 		raise EnvironmentError("FLASK_ENV not equal to 'testing'")
	#
	# 	db.create_all()
	# 	runner = cls.app.test_cli_runner()
	# 	runner.invoke(args=["db-custom", "seed"])
	#
	# @classmethod
	# def tearDown(cls):
	# 	db.session.remove()
	# 	db.drop_all()
	# 	cls.app_context.pop()
	# 	try:
	# 		os.remove('../testdb.db')
	# 	except Exception as e:
	# 		print(e)
	# 		print("Test db unable to be deleted, please delete manually.")

	@classmethod
	def setUp(cls):
		cls.app = create_app()
		cls.app_context = cls.app.app_context()
		cls.app_context.push()
		cls.client = cls.app.test_client()
		cls.app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///csign.db'
		cls.app.config["SECRET_KEY"] = '983475987498573485394ht'
		cls.bcrypt = Bcrypt()
		db.create_all()
		print("Setup complete")

	@classmethod
	def tearDown(cls):
		db.session.remove()
		db.drop_all()
		cls.app_context.pop()
		print("Tear down complete")

	def test_register_page(self):
		response = self.client.get("/register")

		self.assertEqual(response.status_code, 200)

	def test_register_user(self):
		hashed_password = self.bcrypt.generate_password_hash('Testing1').decode('utf-8')
		test_user = User(email='test@test.com',
		                 business_name="test's'66",
		                 business_url='test',
		                 first_name='test',
		                 last_name='test',
		                 phone_number='0423456789',
		                 address='40 Test St, Sydney',
		                 post_code='2000',
		                 state='nsw',
		                 menu_url='www.google.com',
		                 qr_image='test.png',
		                 password=hashed_password,
		                 verified=True,
		                 admin=True)
		test_user.business_url = strip_chars(test_user.business_name)
		db.session.add(test_user)
		db.session.commit()
		user = User.query.filter_by(email='test@test.com').first()

		self.assertEqual(user.email, 'test@test.com')
		self.assertEqual(user.business_name, "test's'66")
		self.assertEqual(user.business_url, 'tests66')
		self.assertEqual(user.first_name, 'test')
		self.assertEqual(user.last_name, 'test')
		self.assertEqual(user.address, '40 Test St, Sydney')
		self.assertEqual(user.post_code, 2000)
		self.assertEqual(user.state, 'nsw')
		self.assertEqual(user.menu_url, 'www.google.com')
		self.assertEqual(user.qr_image, 'test.png')
		self.assertEqual(user.password, hashed_password)
		self.assertEqual(user.verified, 1)
		self.assertEqual(user.admin, 1)
		User.query.filter_by(email='test@test.com').delete()
		db.session.commit()



	# def test_login(self):
	# 	hashed_password = self.bcrypt.generate_password_hash('Testing1').decode('utf-8')
	# 	test_user = User(email='test@test.com',
	# 	                 business_name="test's'66",
	# 	                 business_url='test',
	# 	                 first_name='test',
	# 	                 last_name='test',
	# 	                 phone_number='0423456789',
	# 	                 address='40 Test St, Sydney',
	# 	                 post_code='2000',
	# 	                 state='nsw',
	# 	                 menu_url='www.google.com',
	# 	                 qr_image='test.png',
	# 	                 password=hashed_password,
	# 	                 verified=True,
	# 	                 admin=True)
	# 	test_user.business_url = strip_chars(test_user.business_name)
	# 	db.session.add(test_user)
	# 	db.session.commit()
	# 	user = User.query.filter_by(email='test@test.com').first()
	# 	pw = self.bcrypt.check_password_hash(user.password, 'Testing1')
	# 	self.assertEqual(pw, True)
	# 	User.query.filter_by(email='test@test.com').delete()
	# 	db.session.commit()

	def test_signin(self):
		hashed_password = self.bcrypt.generate_password_hash('Testing1').decode('utf-8')
		test_user = User(email='test@test.com',
		                 business_name="test's'66",
		                 business_url='test',
		                 first_name='test',
		                 last_name='test',
		                 phone_number='0423456789',
		                 address='40 Test St, Sydney',
		                 post_code='2000',
		                 state='nsw',
		                 menu_url='www.google.com',
		                 qr_image='test.png',
		                 password=hashed_password,
		                 verified=True,
		                 admin=True)
		test_user.business_url = strip_chars(test_user.business_name)
		test_signin = SignIn(first_name='Peter',
		                     last_name='Seabrook',
		                     email='test@test.com',
		                     phone='04123456789',
		                     signup=1,
		                     symptoms=0,
		                     user_id=test_user)
		db.session.add(test_user)
		db.session.add(test_signin)
		db.session.commit()

		test_signin = SignIn.query.filter_by(email='test@test.com').first()
		self.assertEqual(test_signin.email, 'test@test.com')

		User.query.filter_by(email='test@test.com').delete()
		SignIn.query.filter_by(email='test@test.com').delete()
		db.session.commit()
