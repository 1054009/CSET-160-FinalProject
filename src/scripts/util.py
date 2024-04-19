def run_query(query, parameters = None):
	return sql.execute(text(query), parameters)
