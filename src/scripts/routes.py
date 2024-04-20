@app.route("/")
@app.route("/home/")
def home():
	if not session.get("email_address") or not session.get("user_id"):
		destroy_session(session)

		return redirect("/login")

	return render_template("home.html")

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

			return redirect("/home")
		else:
			return render_template("login.html", no_navbar = True, error = "Invalid password")
	else:
		return render_template("login.html", no_navbar = True)
