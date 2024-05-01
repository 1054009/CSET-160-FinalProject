from session import database

from app import app
from flask import render_template, session, redirect

from models import Assignment
from scripts.session_util import validate_session

@app.route("/")
@app.route("/home/")
def home():
	if not validate_session(session):
		return redirect("/login/")

	assignments = database.query(Assignment).all()
	assignments_json = str(assignments)

	# TODO: Check for already taken assignments

	return render_template(
		"home.html",

		account_email = session.get("email_address"),
		account_type = session.get("account_type"),
		blarg = assignments_json
	)
