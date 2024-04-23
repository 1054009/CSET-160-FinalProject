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

	n = get_query_rows(f"""


					""")


	"""

	"""
