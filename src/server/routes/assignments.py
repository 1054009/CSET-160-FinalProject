from session import database

from app import app
from flask import render_template, request, redirect, session

from models import Assignment, Question, Option
from scripts.user_util import get_user
from scripts.session_util import validate_session_type
from scripts.assignment_util import get_current_timestamp, create_assignment, get_assignment, create_question, create_option, to_json, from_json

@app.route("/assignments/add/")
def add():
	if not validate_session_type(session, "TEACHER"):
		return redirect("/login/")

	current_user = get_user(session.get("email_address"))

	new_assignment = create_assignment(
		current_user.id,
		"New Assignment",
		get_current_timestamp()
	)

	new_question = create_question(
		new_assignment.id,
		"Example",
		3,
		"MULTIPLE_CHOICE"
	)

	create_option(
		new_question.id,
		"Option 1",
		True
	)

	create_option(
		new_question.id,
		"Option 2",
		False
	)

	new_question = create_question(
		new_assignment.id,
		"Example 2",
		2,
		"OPEN_ENDED"
	)

	database.commit()

	return redirect(f"/assignments/edit/{new_assignment.id}")

@app.route("/assignments/get_data/<assignment_id>")
def get_questions(assignment_id = 0):
	assignment = get_assignment(assignment_id)
	if assignment is None:
		return {
			"creator_id": 0,
			"title": "Invalid Assignment",
			"due_date": get_current_timestamp(),

			"questions": []
		}

	return to_json(assignment.id)

@app.route("/assignments/edit/<assignment_id>")
def edit_get(assignment_id = 0):
	if not validate_session_type(session, "TEACHER"):
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
	if not validate_session_type(session, "TEACHER"):
		return redirect("/login/")

	current_user = get_user(session.get("email_address"))

	assignment_data = request.form.get("assignment_data")
	if assignment_data is None:
		return redirect("/home/") # TODO: Error

	from_json(assignment_data)

	return redirect("/home/")
