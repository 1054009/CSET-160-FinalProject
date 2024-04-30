from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BLOB, TEXT, TIMESTAMP, BOOLEAN
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
	pass

class User(Base):
	__tablename__ = "users"

	id:Mapped[int] = mapped_column(
		INTEGER(unsigned = True),

		primary_key = True
	)

	username:Mapped[str] = mapped_column(
		VARCHAR(32),

		unique = True
	)

	first_name:Mapped[str] = mapped_column(
		VARCHAR(32)
	)

	last_name:Mapped[str] = mapped_column(
		VARCHAR(32)
	)

	email_address:Mapped[str] = mapped_column(
		VARCHAR(64),

		unique = True
	)

	password:Mapped[str] = mapped_column(
		BLOB
	)

	def __repr__(self) -> str:
		return f"<User {self.email_address}>"

class Student(Base):
	__tablename__ = "students"

	id:Mapped[int] = mapped_column(
		INTEGER(unsigned = True),

		primary_key = True
	)

	user_id:Mapped[int] = mapped_column(
		ForeignKey("users.id"),

		unique = True
	)

	user = relationship(
		"User",
		backref = "Student",
		viewonly = True
	)

	def as_user(self):
		return self.user

	def __repr__(self) -> str:
		return f"<Student {self.as_user().email_address}>"

class Teacher(Base):
	__tablename__ = "teachers"

	id:Mapped[int] = mapped_column(
		INTEGER(unsigned = True),

		primary_key = True
	)

	user_id:Mapped[int] = mapped_column(
		ForeignKey("users.id"),

		unique = True
	)

	user = relationship(
		"User",
		backref = "Teacher",
		viewonly = True
	)

	def as_user(self):
		return self.user

	def __repr__(self) -> str:
		return f"<Teacher {self.as_user().email_address}>"

class Assignment(Base):
	__tablename__ = "assignments"

	id:Mapped[int] = mapped_column(
		INTEGER(unsigned = True),

		primary_key = True
	)

	teacher_id:Mapped[int] = mapped_column(
		ForeignKey("teachers.id")
	)

	title:Mapped[str] = mapped_column(
		VARCHAR(255)
	)

	due_date:Mapped[str] = mapped_column(
		TIMESTAMP
	)

	# TODO: Questions

	def __repr__(self) -> str:
		return f"<Assignment {self.title}>"

class Question(Base):
	__tablename__ = "assignment_questions"

	id:Mapped[int] = mapped_column(
		INTEGER(unsigned = True),

		primary_key = True
	)

	assignment_id:Mapped[int] = mapped_column(
		ForeignKey("assignments.id")
	)

	text:Mapped[str] = mapped_column(
		TEXT
	)

	points:Mapped[int] = mapped_column(
		INTEGER(unsigned = True)
	)

	# TODO: Options

	def __repr__(self) -> str:
		return f"<Question '{self.text}'>"

class Option(Base):
	__tablename__ = "assignment_question_options"

	id:Mapped[int] = mapped_column(
		INTEGER(unsigned = True),

		primary_key = True
	)

	question_id:Mapped[int] = mapped_column(
		ForeignKey("assignment_questions.id")
	)

	text:Mapped[str] = mapped_column(
		TEXT
	)

	is_correct:Mapped[int] = mapped_column(
		BOOLEAN
	)

	def __repr__(self) -> str:
		return f"<Option '{self.text}'>"

class Attempt(Base):
	__tablename__ = "assignment_attempts"

	id:Mapped[int] = mapped_column(
		INTEGER(unsigned = True),

		primary_key = True
	)

	student_id:Mapped[int] = mapped_column(
		ForeignKey("students.id")
	)

	assignment_id:Mapped[str] = mapped_column(
		ForeignKey("assignments.id")
	)

	submission_time:Mapped[str] = mapped_column(
		TIMESTAMP
	)

	is_graded:Mapped[int] = mapped_column(
		BOOLEAN
	)

	# TODO: Responses

	def __repr__(self) -> str:
		return f"<Attempt '{self.id}'>"

class AttemptResponse(Base):
	__tablename__ = "assignment_attempt_responses"

	id:Mapped[int] = mapped_column(
		INTEGER(unsigned = True),

		primary_key = True
	)

	attempt_id:Mapped[int] = mapped_column(
		ForeignKey("assignment_attempts.id")
	)

	option_id:Mapped[str] = mapped_column(
		ForeignKey("assignment_question_options.id")
	)

	is_graded:Mapped[int] = mapped_column(
		BOOLEAN
	)

	def __repr__(self) -> str:
		return f"<AttemptResponse '{self.id}'>"
