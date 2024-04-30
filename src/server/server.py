# Imports
from app import app
from engine import engine
from models import Base
from session import database

# Setup database
Base.metadata.reflect(engine)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

if  __name__ == "__main__":
	app.run()
