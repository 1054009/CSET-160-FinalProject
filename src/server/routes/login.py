from session import database

from app import app
from flask import render_template, request, redirect, session

from scripts.session_util import clear_session
from scripts.password_util import sha_string
from scripts.user_util import create_user, get_user

@app.route("/login/")
def login_get():
	clear_session(session)

	# TODO: Remove test accounts
	if get_user("s@s.s") is None:
		create_user(
			"Student",
			"Account",
			"s@s.s",
			sha_string("s"),
			"STUDENT"
		)

	if get_user("t@t.t") is None:
		create_user(
			"Teacher",
			"Account",
			"t@t.t",
			sha_string("t"),
			"TEACHER"
		)

	return render_template("login.html")

@app.route("/login/", methods = [ "POST" ])
def login_post():
	existing = get_user(request.form.get("email", "idiot@gmail.com"))
	if existing is None:
		return render_template(
			"login.html",

			error_msg = "User does not exist"
		)

	session["email_address"] = existing.email_address
	session["account_type"] = existing.type

	return redirect("/home/")
