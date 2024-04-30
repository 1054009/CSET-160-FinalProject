from app import app
from flask import send_file, url_for

from pathlib import Path

@app.route("/favicon.ico")
def favicon():
	favicon_path = Path(
		app.static_folder + "/.." +

		url_for(
			"static",
			filename = "img/favicon.ico"
		)
	).resolve()

	return send_file(favicon_path)
