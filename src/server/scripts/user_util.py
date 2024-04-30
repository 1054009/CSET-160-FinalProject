from models import User, Student, Teacher
from session import database

def create_user(first_name, last_name, email_address, hashed_password):
	try:
		new_user = User(
			first_name = first_name,
			last_name = last_name,
			email_address = email_address,
			password = hashed_password.encode("utf-8")
		)

		database.add(new_user)
		database.flush()

		return new_user
	except:
		return None

def get_user(email_address):
	try:
		users = database.query(User)

		return users.filter(User.email_address == email_address).first()
	except:
		return None

def register_student(user):
	try:
		new_student = Student(
			user_id = user.id
		)

		database.add(new_student)
		database.flush()

		return new_student
	except:
		return None

def register_teacher(user):
	try:
		new_teacher = Teacher(
			user_id = user.id
		)

		database.add(new_teacher)
		database.flush()

		return new_teacher
	except:
		return None
