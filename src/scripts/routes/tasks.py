

# Manage page
@app.route("/tasks/manage/", methods = [ "GET" ])
def navigate_to_manage():
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
					due_date = None
				message = f"Task {request.form.get("title")} has been created"

				run_query(f"insert into `assignments` values(NULL, {teacher_id}, {title}, {due_date})")

		# this is not working
		sql.commit()

	return render_template(
		"task_manage.html",
		mode = mode,
		message = message
	)
