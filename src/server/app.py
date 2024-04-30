from flask import Flask
from pathlib import Path
from secrets import token_hex
import os

EXECUTING_DIRECTORY = Path(__file__).parent.resolve()

app = Flask(
	__name__,

	static_folder = (EXECUTING_DIRECTORY / "../client/static").resolve(),
	template_folder = (EXECUTING_DIRECTORY / "../client/templates").resolve()
)

app.secret_key = token_hex()

# Load routes
for route_name in os.listdir(EXECUTING_DIRECTORY / "routes"):
	if not route_name.endswith(".py"):
		continue

	if route_name == "__init__.py":
		continue

	__import__(f"routes.{route_name[:-3]}", locals(), globals())
