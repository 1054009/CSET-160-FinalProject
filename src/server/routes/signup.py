from app import app
from flask import render_template, request, redirect

from scripts.password_util import sha_string
from scripts.user_util import create_user, get_user

@app.route("/signup/")
def signup_get():
	return render_template("signup.html")

@app.route("/signup/", methods = [ "POST" ])
def signup_post():
	existing = get_user(request.form.get("email", "idiot@gmail.com"))
	if existing is not None:
		return render_template(
			"signup.html",

			error_msg = "User with email already exists"
		)

	password = request.form.get("password", "nice one")
	password_verify = request.form.get("password_verify", "nice one")

	if password != password_verify:
		return render_template(
			"signup.html",

			error_msg = "Passwords don't match"
		)

	new_user = create_user(
		request.form.get("first_name", "nice name"),
		request.form.get("last_name", "nice name"),
		request.form.get("email", "idiot@gmail.com"),
		sha_string(password)
	)

	return redirect("/home/")
