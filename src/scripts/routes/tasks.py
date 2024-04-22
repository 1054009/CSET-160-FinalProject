

# Manage page
@app.route("/tasks/manage/", methods = [ "GET" ])
def navigate_to_manage():
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	page = request.args.get("page")
	per_page = request.args.get("per_page")

	tasks, page, per_page, min_page, max_page = get_data('assignments', page, per_page)

	return render_template(
		"task_view.html",
		mode = "view",
		tasks = tasks,
		page = page,
		per_page = per_page,
		min_page = min_page,
		max_page = max_page
	)

@app.route("/tasks/manage/<mode>", methods=[ "GET", "POST" ])
def edit_task(mode):
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	mode = get_task_mode(mode)

	message = ""

	title = request.form.get("title")
	due_date = request.form.get("due_date")
	user_id = user_exists(session.get("email_address"))
	teacher_id = get_teacher_id(user_id)

	if request.method == "POST":
		match mode:
			case "add":
				if due_date:
					due_date = due_date.replace("T", " ") + ":59"
				else:
					due_date = "9999-12-31 00:00:00"

				message = f"Task {title} has been created"

				run_query(
					f"insert into `assignments` values(NULL, {teacher_id}, '{title}', '{due_date}')"
				)

				sql.commit()


				questions = []
				points = []
				num = 1

				while True:

					if not request.form.get(f"question{num}"):
						break

					questions.append(request.form.get(f"question{num}"))
					points.append(request.form.get(f"points{num}"))

					num += 1

				assignment_id = get_query_rows("select max(`id`) from `assignments`")[0]['max(`id`)']

				for i in range(len(questions)):
					question = questions[i]
					points = points[i]

					run_query(f"insert into `assignment_questions` values({assignment_id}, '{question}', 'oe', {points})")

					sql.commit()


	return render_template(
		"task_manage.html",
		mode = mode,
		message = message
	)
