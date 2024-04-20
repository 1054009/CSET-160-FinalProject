def user_exists(email_address):
	user = get_query_rows(f"select * from `users` where `email_address` = '{email_address}'")

	if len(user) < 1:
		return False

	user = user[0]

	if not user.id or not user.id.isnumeric():
		return False

	return user.id

def validate_login(email_address, password):
	if not user_exists(email_address):
		return False

	stored_password = get_query_rows(f"select `password` from `users` where `email_address` = '{email_address}'")
	if len(stored_password) < 1:
		return Flase

	password.encode("utf-8")

	return hashlib.sha256(password.digest()) == stored_password[0].password

def destroy_session(session):
	if not session:
		return

	if session.get("user_id"): del session["user_id"]
	if session.get("email_address"): del session["email_address"]
