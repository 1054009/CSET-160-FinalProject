def run_query(query, parameters = None):
	return sql.execute(text(query), parameters)

def run_file(path, parameters = None):
	path = (EXECUTING_DIRECTORY / path).resolve()

	file = open(path)

	return run_query(file.read(), parameters)

def raw_get_query_rows(query_result):
	better_rows = []

	if not query_result: return better_rows
	if not query_result.all(): return better_rows

	for row in query_result.all():
		better_rows.append(row._mapping)

	return better_rows

def get_query_rows(query, parameters = None):
	return raw_get_query_rows(run_query(query, parameters))

def user_exists(email_address):
	user = get_query_rows(f"select * from `users` where `email_address` = {email_address}")

	if len(user) < 1:
		return False

	user = user[0]

	if not user.id or not user.id.isnumeric():
		return False

	return user.id

def validate_login(email_address, password):
	if not user_exists(email_address):
		return False

	stored_password = get_query_rows(f"select `password` from `users` where `email_address` = {email_address}")
	if len(stored_password) < 1:
		return Flase

	password.encode("utf-8")

	return hashlib.sha256(password.digest()) == stored_password[0].password

def destroy_session(session):
	if not session or not session.get("email_address"):
		return

	del session["email_address"]
