from app import app
from flask import send_file

@app.route("/static/js/<path:path>")
def fix_mime(path):
	return send_file(f"{app.static_folder}/js/{path}", mimetype = "text/javascript")
