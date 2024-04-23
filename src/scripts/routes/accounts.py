@app.route("/accounts/", methods = [ "GET", "POST"])
def view_accounts():
	if not validate_session(session):
		destroy_session(session)
		return redirect("/login")

	page = request.args.get("page")
	per_page = request.args.get("per_page")

	accounts, page, per_page, min_page, max_page = get_data('users', page, per_page)

	return render_template(
		"accounts.html",
		accounts = accounts,
		page = page,
		per_page = per_page,
		min_page = min_page,
		max_page = max_page
	)

@app.route("/accounts/view/<id>", methods = [ "GET" ])
def view_account_info():
	assignment_data = []

	titles = get_query_rows(f"""
		select `title` from `assignments`
		where id in
			(
				select `assignment_id`
				from `assignment_attempts`
				where `student_id` = {session.get("student_id")}
			);
		""")

	grades = []

	assignment_attempts_ids = get_query_rows(f"""
		select 	`id` from `assignment_attempts`
		where `student_id` = {session.get("student_id")}
	""")

	for i in range(len(assignment_attempts_ids)):
		attempt_id = assignment_attempts_ids[i]

		grade = 0

		responses_ids = get_query_rows(f"""
			select `id` from `assignment_attempt_responses`
			where attempt_id = {attempt_id}
		""")

		for j in range(len(responses_ids)):
			response_id = responses_ids[j]

			points = get_query_rows(f"""
				select `points`
				from `assignment_questions` as `aq`
				where `aq`.`id` =
				(
					select `question_id`
					from `assignment_attempt_responses` as `aar`
					where `aar`.`id` = {response_id}
				);
			""")[0].points

			is_correct = get_query_rows(f"""
				select `is_correct`
				from `assignment_question_options` as `aqo`
				where `aqo`.`id =
				(
					select `option_id`
					from `assignment_attempt_responses` as `aar`
					where `aar`.`id` = {response_id}
				);
			""")[0].is_correct

			if is_correct:
				grade += points

		grades.append(grade)

	assignment_data.append(titles)
	assignment_data.append(grades)

	render_template("account_info.html", assignment_data = assignment_data)
