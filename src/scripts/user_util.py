def sha_string(string):
	return hashlib.sha256(string.encode("utf-8")).hexdigest()

def user_exists(email_address):
	"""
	:param str email_address: The email associated with a user
	:return: The user id if the user account exists, False otherwise
	:rtype: bool

	"""
	user = get_query_rows(f"select * from `users` where `email_address` = '{email_address}'")

	if len(user) < 1:
		return False

	return user[0].id

def validate_login(email_address, password):
	if not user_exists(email_address):
		return False

	stored_password = get_query_rows(f"select `password` from `users` where `email_address` = '{email_address}'")

	if len(stored_password) < 1:
		return False

	stored_password = stored_password[0].password
	stored_password = stored_password.decode("utf-8")

	return sha_string(password) == stored_password

def destroy_session(session):
	if not session:
		return

	if session.get("user_id"): del session["user_id"]
	if session.get("email_address"): del session["email_address"]
