from scripts.user_util import get_user

def clear_session(user_session):
	user_session.clear()

	return False, None

def validate_session(user_session):
	user = get_user(user_session.get("email_address"))

	if not user:
		return clear_session(user_session)

	return True, user

def validate_session_type(user_session, type):
	valid, user = validate_session(user_session)

	if not valid:
		return False, None

	if user.type != type:
		return False, user

	return True, user
