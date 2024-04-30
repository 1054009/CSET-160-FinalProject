from models import Assignment, Question, Option
from session import database

from datetime import datetime

def get_current_timestamp():
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

def create_question(assignment_id, text, points, type):
	try:
		assignment = get_assignment(assignment_id)
		if assignment is None:
			return None

		new_question = Question(
			assignment_id = assignment_id,
			text = text,
			points = points,
			type = type
		)

		database.add(new_question)
		database.flush()

		return new_question
	except:
		return None

def create_option(question_id, text, is_correct):
	try:
		question = get_question(question_id)
		if question is None:
			return None

		new_option = Option(
			question_id = question_id,
			text = text,
			is_correct = is_correct
		)

		database.add(new_option)
		database.flush()

		return new_option
	except:
		return None

def get_assignment(id):
	try:
		assignments = database.query(Assignment)

		return assignments.filter(Assignment.id == id).first()
	except:
		return None

def get_question(id):
	try:
		questions = database.query(Question)

		return questions.filter(Question.id == id).first()
	except:
		return None

def get_option(id):
	try:
		options = database.query(Option)

		return options.filter(Option.id == id).first()
	except:
		return None
