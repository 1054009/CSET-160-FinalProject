def run_query(query, parameters = None):
	return sql.execute(text(query), parameters)

def run_file(path, parameters = None):
	path = (EXECUTING_DIRECTORY / path).resolve()

	file = open(path)

	return run_query(file.read(), parameters)

def raw_get_query_rows(query_result):
	better_rows = []

	if not query_result: return better_rows
	if not query_result.all(): return better_rows

	for row in query_result.all():
		better_rows.append(row._mapping)

	return better_rows

def get_query_rows(query, parameters = None):
	return raw_get_query_rows(run_query(query, parameters))
