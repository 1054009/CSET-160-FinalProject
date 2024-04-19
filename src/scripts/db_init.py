# Clear everything out
run_query("set FOREIGN_KEY_CHECKS = 0")

run_query("drop table if exists `users`")
run_query("drop table if exists `teachers`")
run_query("drop table if exists `students`")

run_query("drop table if exists `assignments`")
run_query("drop table if exists `assignment_questions`")
run_query("drop table if exists `assignment_question_options`")

run_query("drop table if exists `assignment_attempts`")
run_query("drop table if exists `assignment_attempt_responses`")

run_query("set FOREIGN_KEY_CHECKS = 1")

# Initialize tables

run_file("./scripts/db/tables.sql")

# Apply
sql.commit()
