from session import database

from app import app
from flask import render_template, request, redirect, session
from sqlalchemy.sql.functions import now

from scripts.user_util import get_user
from scripts.assignment_util import get_current_timestamp, create_assignment

@app.route("/assignments/add/")
def add():
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

@app.route("/assignments/edit/<assignment_id>")
def edit(assignment_id = 1):
	print(assignment_id)

	return render_template(
		"assignments.html",

		mode = "edit"
	)
