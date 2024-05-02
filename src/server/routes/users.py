from session import database

from app import app
from flask import render_template
import json

from models import User

from scripts.user_util import to_json

@app.route("/users/")
def users():
	users = database.query(User).all()

	user_list = []

	for user in users:
		user_list.append(to_json(user.id))

	return render_template(
		"users.html",

		user_list = json.dumps(user_list)
	)
