def run_query(query, parameters = None):
	return sql.execute(text(query), parameters)

def run_file(path, parameters = None):
	path = (EXECUTING_DIRECTORY / path).resolve()

	file = open(path)

	return run_query(file.read(), parameters)

def user_exists(email_address):
	data = run_query(f"select * from `users` where `email_address` = {email_address}")

	if not data or not data.first():
		return False

	if not data["id"] or not data["id"].isnumeric():
		return False

	return True

def validate_login(email_address, password):
	if not user_exists(email_address):
		return False

	password.encode("utf-8")
	stored_password = run_query(f"select `password` from `users` where `email_address` = {email_address}").first()[0]

	return hashlib.sha256(password.digest()) == stored_password

def destroy_session(session):
	if not session or not session.get("email_address"):
		return

	del session["email_address"]
