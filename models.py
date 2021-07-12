from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(UserMixin):
	"""docstring for User"""
	"""userType=1 is applicant. userType=2 is company"""

	def __init__(self, id, userType, active=True, name=''):
		self.name = name
		self.id = id
		self.active = active
		self.userType = userType

	def get_id(self):
		return self.id

	@staticmethod
	def is_active():
		return True

	@staticmethod
	def is_anonymous():
		return False

	@staticmethod
	def is_authenticated():
		return True

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
		return s.dumps({"id": self.id}).decode("utf-8")

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config["SECRET_KEY"])
		try:
			id = s.loads(token)["id"]
			return id
		except:
			return None