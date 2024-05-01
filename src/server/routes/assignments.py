from session import database

import json
from app import app
from flask import render_template, request, redirect, session

from models import Assignment, Question, Option
from scripts.user_util import get_user
from scripts.session_util import validate_session_type
from scripts.assignment_util import get_current_timestamp, create_assignment, get_assignment, create_question, create_option

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
	data = {
		"creator_id": 0,
		"title": "Invalid Assignment",
		"due_date": get_current_timestamp(),

		"questions": []
	}

	assignment = get_assignment(assignment_id)
	if assignment is None:
		return data

	data["creator_id"] = assignment.creator_id
	data["title"] = assignment.title
	data["due_date"] = assignment.due_date

	for question in assignment.questions:
		options = []

		for option in question.options:
			options.append({
				"text": option.text,
				"is_correct": option.is_correct
			})

		data["questions"].append({
			"text": question.text,
			"points": question.points,
			"type": question.type,

			"options": options
		})

	return data

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

	assignment_data = json.loads(assignment_data)

	# Get base assignment
	assignment = get_assignment(assignment_data.get("id"))
	if assignment is None:
		assignment = create_assignment(
			current_user.id,
			assignment_data.get("title"),
			assignment_data.get("due_date")
		)

	# Delete the old questions and options
	for question in assignment.questions:
		for option in question.options:
			database.query(Option).filter(Option.id == option.id).delete()

		database.query(Question).filter(Question.id == question.id).delete()

	# Add the new stuff
	for question in assignment_data.get("questions", []):
		new_question = create_question(
			assignment.id,
			question.get("text", "invalid"),
			question.get("points", 0),
			question.get("type", "OPEN_ENDED")
		)

		for option in question.get("options", []):
			create_option(
				new_question.id,
				option.get("text", "invalid"),
				option.get("is_correct", False)
			)

	return redirect("/home/")
