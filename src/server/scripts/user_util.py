from models import User
from session import database

def create_user(username, first_name, last_name, email_address, hashed_password):
	try:
		new_user = User(
			username = username,
			first_name = first_name,
			last_name = last_name,
			email_address = email_address,
			password = hashed_password.encode("utf-8")
		)

		database.add(new_user)
		database.flush()

		return new_user
	except:
		return None

def get_user(username):
	try:
		users = database.query(User)

		return users.filter(User.username == username).first()
	except:
		return None
