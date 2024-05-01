from session import database

import json
from app import app
from flask import render_template, session, redirect

from models import Assignment
from scripts.session_util import validate_session
from scripts.assignment_util import to_json

@app.route("/")
@app.route("/home/")
def home():
	if not validate_session(session):
		return redirect("/login/")

	assignments = database.query(Assignment).all()
	assignment_list = []

	for assignment in assignments:
		assignment_list.append(to_json(assignment.id))

	# TODO: Check for already taken assignments

	return render_template(
		"home.html",

		account_email = session.get("email_address"),
		account_type = session.get("account_type"),
		assignment_list = json.dumps(assignment_list)
	)
