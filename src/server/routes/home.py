from app import app
from flask import render_template, session, redirect

from scripts.session_util import validate_session

@app.route("/")
@app.route("/home/")
def home():
	if not validate_session(session):
		return redirect("/login/")

	return render_template("base.html")
