def run_query(query, parameters = None):
	return sql.execute(text(query), parameters)

def run_file(path, parameters = None):
	path = (EXECUTING_DIRECTORY / path).resolve()

	file = open(path)

	return run_query(file.read(), parameters)

def user_exists(email_address):
	user = run_query(f"select * from `users` where `email_address` = {email_address}")

	if not user: return False
	if not user.first(): return False
	if not user.first()._mapping: return False

	user = user.first()._mapping

	if not user.id or not user.id.isnumeric():
		return False

	return user.id

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
