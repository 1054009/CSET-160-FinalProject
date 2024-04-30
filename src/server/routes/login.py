from session import database

from app import app
from flask import render_template, request, redirect, session

from scripts.session_util import clear_session
from scripts.password_util import sha_string
from scripts.user_util import create_user, get_user

@app.route("/login/")
def login_get():
	clear_session(session)

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

	return redirect("/home/")
