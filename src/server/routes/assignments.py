from session import database

from app import app
from flask import render_template, request, redirect, session

from scripts.user_util import get_user
from scripts.session_util import validate_session
from scripts.assignment_util import get_current_timestamp, create_assignment, get_assignment

@app.route("/assignments/add/")
def add():
	if not validate_session(session):
		return redirect("/login/")

	current_user = get_user(session.get("email_address"))
	if current_user is None or current_user.type != "TEACHER":
		return redirect("/home/")

	new_assignment = create_assignment(
		current_user.id,
		"New Assignment",
		get_current_timestamp()
	)

	database.commit()

	return redirect(f"/assignments/edit/{new_assignment.id}")

@app.route("/assignments/get_questions/<assignment_id>")
def get_questions(assignment_id = 0):
	if not validate_session(session):
		return redirect("/login/")

	assignment = get_assignment(assignment_id)
	if assignment is None:
		return {}

	return assignment.questions

@app.route("/assignments/edit/<assignment_id>")
def edit_get(assignment_id = 0):
	if not validate_session(session):
		return redirect("/login/")

	assignment = get_assignment(assignment_id)
	if assignment is None:
		return redirect("/home/") # TODO: Error

	return render_template(
		"assignments.html",

		mode = "edit",
		assignment_id = assignment_id
	)

@app.route("/assignments/edit/", methods = [ "POST" ])
def edit_post():
	print(request.form)

	return render_template("home.html")
