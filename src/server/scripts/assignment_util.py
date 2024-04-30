from models import Assignment
from session import database

from datetime import datetime

def get_current_timestamp():
	return datetime.now().strftime("%Y%m%d%H%M%S")

def create_assignment(creator_id, title, due_date):
	try:
		new_assignment = Assignment(
			creator_id = creator_id,
			title = title,
			due_date = due_date
		)

		database.add(new_assignment)
		database.flush()

		return new_assignment
	except:
		return None
