from models import User
from session import database

import json

def create_user(first_name, last_name, email_address, hashed_password, type):
	try:
		new_user = User(
			first_name = first_name,
			last_name = last_name,
			email_address = email_address,
			password = hashed_password.encode("utf-8"),
			type = type
		)

		database.add(new_user)
		database.flush()

		return new_user
	except:
		return None

def get_user(email_address):
	try:
		users = database.query(User)

		return users.filter(User.email_address == email_address).first()
	except:
		return None

def get_user_by_id(id):
	try:
		users = database.query(User)

		return users.filter(User.id == id).first()
	except:
		return None

def to_json(id):
	user = get_user_by_id(id)

	if user is None:
		return "{}"

	data = {
		"id": user.id,
		"first_name": user.first_name,
		"last_name": user.last_name,
		"email_address": user.email_address,
		"type": user.type
	}

	return json.dumps(data, default = str)
