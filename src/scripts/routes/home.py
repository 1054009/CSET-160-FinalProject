@app.route("/")
@app.route("/home/")
def home():
	if not session.get("email_address") or not session.get("user_id"):
		destroy_session(session)

		return redirect("/login")

	return render_template("home.html", account_type = session.get("account_type"))
