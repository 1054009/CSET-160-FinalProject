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

run_query("""
	create table `teachers`
	(
		`id` int unsigned auto_increment,
		`user_id` int unsigned not null,

		primary key (`id`),
		foreign key (`user_id`) references `users` (`id`) on delete cascade on update restrict
	)
""")

run_query("""
	create table `students`
	(
		`id` int unsigned auto_increment,
		`user_id` int unsigned not null,

		primary key (`id`),
		foreign key (`user_id`) references `users` (`id`) on delete cascade on update restrict
	)
""")

# Apply
sql.commit()
