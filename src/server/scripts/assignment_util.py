from models import Assignment, Question, Option
from session import database

from datetime import datetime
import json

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

def to_json(id):
	assignment = get_assignment(id)

	if assignment is None:
		return "{}"

	data = {
		"id": assignment.id,
		"creator_id": assignment.creator_id,
		"title": assignment.title,
		"due_date": assignment.due_date,

		"questions": []
	}

	for question in assignment.questions:
		options = []

		for option in question.options:
			options.append({
				"text": option.text,
				"is_correct": option.is_correct
			})

		data["questions"].append({
			"text": question.text,
			"points": question.points,
			"type": question.type,

			"options": options
		})

	return json.dumps(data, default = str)

def from_json(data):
	data = json.loads(data)

	assignment = get_assignment(data.get("id"))
	if assignment is None:
		return "{}"

	# Delete the old questions and options
	for question in assignment.questions:
		for option in question.options:
			database.query(Option).filter(Option.id == option.id).delete()

		database.query(Question).filter(Question.id == question.id).delete()

	# Add the new stuff
	for question in data.get("questions", []):
		new_question = create_question(
			assignment.id,
			question.get("text", "invalid"),
			question.get("points", 0),
			question.get("type", "OPEN_ENDED")
		)

		for option in question.get("options", []):
			create_option(
				new_question.id,
				option.get("text", "invalid"),
				option.get("is_correct", False)
			)

	return assignment
