from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BLOB, TEXT, TIMESTAMP, BOOLEAN, ENUM
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

	type:Mapped[str] = mapped_column(
		ENUM("STUDENT", "TEACHER")
	)

	def __repr__(self) -> str:
		return f"<User {self.email_address}>"

class Assignment(Base):
	__tablename__ = "assignments"

	id:Mapped[int] = mapped_column(
		INTEGER(unsigned = True),

		primary_key = True
	)

	creator_id:Mapped[int] = mapped_column(
		ForeignKey("users.id")
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

	type:Mapped[str] = mapped_column(
		ENUM("MULTIPLE_CHOICE", "OPEN_ENDED")
	)

	options = relationship(
		"Option",
		backref = "Question"
	)

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

	submitter_id:Mapped[int] = mapped_column(
		ForeignKey("users.id")
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

	responses = relationship(
		"AttemptResponse",
		backref = "Attempt"
	)

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
