def get_int(value, min, default):
	try:
		value = int(value)
		assert(value >= min)
	except:
		value = default

	return value

def clamp(x, min, max):
	if x < min: return min
	if x > max: return max

	return x

def get_data(table, page = 1, per_page = 10):
	page = get_int(page, 1, 1)
	per_page = get_int(per_page, 10, 10)

	count = run_query(f"select count(*) from `{table}`").first()[0]

	min_page = 1
	max_page = math.ceil(count / per_page)

	page = clamp(page, min_page, max_page)

	data = get_query_rows(f"select * from `{table}` limit {per_page} offset {(page - 1) * per_page}")

	return data, page, per_page, min_page, max_page

def get_points(response_id):
	return get_query_rows(f"""
		select `points`
		from `assignment_questions` as `aq`
		where `aq`.`id` =
		(
			select `question_id`
			from `assignment_attempt_responses` as `aar`
			where `aar`.`id` = {response_id}
		);
	""")[0].points

def get_is_correct(response_id):
	return get_query_rows(f"""
		select `is_correct`
		from `assignment_question_options` as `aqo`
		where `aqo`.`id =
		(
			select `option_id`
			from `assignment_attempt_responses` as `aar`
			where `aar`.`id` = {response_id}
		);
	""")[0].is_correct

def get_grade(attempt_id):
	grade = 0

	# All the responses_ids for the attempt_id
	responses_ids = get_query_rows(f"""
		select `id` from `assignment_attempt_responses`
		where attempt_id = {attempt_id}
	""")


	for j in range(len(responses_ids)):
		response_id = responses_ids[j]

		points = get_points(response_id)

		is_correct = get_is_correct(response_id)

		if is_correct:
			grade += points

	return grade
