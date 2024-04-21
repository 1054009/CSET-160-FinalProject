@app.route("/")
@app.route("/home/")
def home():
	if not session.get("email_address") or not session.get("user_id"):
		destroy_session(session)

		return redirect("/login")

	return render_template("home.html", account_type = session.get("account_type"))

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

@app.route("/tasks/manage/<mode>")
def edit_task(mode):
	mode = get_task_mode(mode)

	# task_id = request.form.get("task_id")


@app.route("/signup/", methods = [ "GET", "POST" ])
def signup():
	destroy_session(session) # Log them out

	if request.method == "POST":
		email_address = request.form.get("email_address")
		password = request.form.get("password") # Not encrypted during transit oh well
		password_verify = request.form.get("password_verify")

		if password != password_verify:
			return render_template(
				"signup.html",
				no_navbar = True,
				error = "Passwords don't match"
			)

		if user_exists(email_address):
			return render_template(
				"signup.html",
				no_navbar = True,
				error = "A user with this email already exists!"
			)

		try:
			run_query(
				"insert into `users` values ( NULL, :first_name, :last_name, :email_address, :password )",

				{
					"first_name": request.form.get("first_name"),
					"last_name": request.form.get("last_name"),
					"email_address": email_address,
					"password": sha_string(password),
				}
			)

			# Insert into students or teachers table
			account_type = request.form.get("account_type")
			user_id = user_exists(email_address)

			run_query(
				f"insert into `{account_type}` values ( NULL, :user_id )",
				{
					"user_id": user_id
				}
			)

			sql.commit()

			return redirect("/login")
		except:
			return render_template(
				"signup.html",
				no_navbar = True,
				error = "Failed to create account. Contact an administrator."
			)
	else:
		return render_template("signup.html", no_navbar = True)

@app.route("/login/", methods = [ "GET", "POST" ])
def login():
	destroy_session(session)

	if request.method == "POST":
		email_address = request.form.get("email_address")
		password = request.form.get("password")
		user_id = user_exists(email_address)

		if not user_id:
			return render_template("login.html", no_navbar = True, error = "A user with this email does not exist")

		if validate_login(email_address, password):
			session["user_id"] = user_id
			session["email_address"] = email_address

			account_type = get_account_type(user_id)
			session["account_type"] = account_type

			return redirect("/home")
		else:
			return render_template("login.html", no_navbar = True, error = "Invalid password")
	else:
		return render_template("login.html", no_navbar = True)

@app.route("/accounts/", methods = [ "GET", "POST"])
def view_accounts():
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
