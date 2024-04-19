# Clear everything out
run_query("set FOREIGN_KEY_CHECKS = 0")

run_query("drop table if exists `users`")
run_query("drop table if exists `teachers`")
run_query("drop table if exists `students`")

run_query("drop table if exists `assignments`")
run_query("drop table if exists `assignment_questions`")

run_query("set FOREIGN_KEY_CHECKS = 1")

# Initialize tables
run_query("""
	create table `users`
	(
		`id` int unsigned auto_increment,
		`first_name` varchar(64) not null,
		`last_name` varchar(64) not null,
		`email_address` varchar(64) unique not null,
		`password` blob not null,

		primary key (`id`)
	)
""")

# Apply
sql.commit()
