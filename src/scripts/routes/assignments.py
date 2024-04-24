@app.route("/assignments/add/")
def initialize_assignment():
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	run_query(f"""
		insert into `assignments` values
		(
			NULL,
			{session.get("teacher_id")},
			'New Assignment',
			'9999-12-31 00:00:00'
		);
	""")

	assignment_id = get_query_rows("select last_insert_id() as 'id' from `assignments`")
	if len(assignment_id) < 1:
		return redirect("/home") # TODO: Show an error

	return redirect(f"/assignments/edit/{assignment_id[0].id}")

@app.route("/assignments/edit/<assignment_id>")
def add_assignment(assignment_id = 1):
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	# TODO: Make sure it's a teacher account

	# Get basic information
	assignment_data = get_query_rows(f"select * from `assignments` where `id` = {assignment_id}")
	if len(assignment_data) < 1:
		return redirect("/home") # TODO: Show error

	# Get questions
	assignment_questions = get_query_rows(f"select * from `assignment_questions` where `assignment_id` = {assignment_id}")

	# Get question options
	assignment_question_options = {}

	for question in assignment_questions:
		question_id = question.get("id")

		assignment_question_options[question_id] = get_query_rows(f"select * from `assignment_question_options` where `question_id` = {question_id}")

	return render_template(
		"assignment_edit.html",
		assignment_data = assignment_data[0],
		assignment_questions = assignment_questions,
		assignment_question_options = assignment_question_options
	)

@app.route("/assignments/edit/", methods = [ "POST" ])
def update_assignment():
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	print(request.form)

	# TODO
	return redirect("/home")

@app.route("/assignments/view/<id>", methods = [ "GET" ])
def view_assignment_info():
	assignment_id = request.args.get("id")

	assignment_data = []

	students = get_assignment_students(assignment_id)

	grades = []

	# TODO any teacher can grade, not just the teacher who created assignment?
	# teachers = []

	# Calculate grade for each student
	for i in range(len(students)):
		attempt_id = get_attempt_id(students[i].student_id, assignment_id)

		grade = get_grade(attempt_id)

		grades.append(grade)

	assignment_data.append(students)
	assignment_data.append(grades)

	return render_template(
		"assignment_info.html",
		students_count = len(students),
		assignment_data = assignment_data
	)
