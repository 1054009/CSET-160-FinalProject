#
#	This is retarded....
#	:/
#

@app.route("/static/js/<path:path>")
def fix_mime(path):
	return send_file(f"{SERVER_DIRECTORY}/static/js/{path}", mimetype = "text/javascript")
