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

def get_accounts(page = 1, per_page = 10):
	page = get_int(page, 1, 1)
	per_page = get_int(per_page, 10, 10)

	account_count = run_query("select count(*) from `users`").first()[0]

	min_page = 1
	max_page = math.ceil(account_count / per_page)

	page = clamp(page, min_page, max_page)

	accounts = get_query_rows(f"select * from `users` limit {per_page} offset {(page - 1) * per_page}")

	return accounts, page, per_page, min_page, max_page
