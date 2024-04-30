from platform import system
from sqlalchemy import create_engine

engine = create_engine(f"mysql+mysqlconnector://root:1234@localhost:3306/cset160final")

sql = engine.connect()
