from scripts.user_util import get_user

def clear_session(user_session):
	user_session.clear()

	return False

def validate_session(user_session):
	user = get_user(user_session.get("email_address"))

	if not user:
		return clear_session(user_session)

	return True
