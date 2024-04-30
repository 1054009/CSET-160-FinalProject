from engine import engine
from sqlalchemy.orm import Session

database = Session(bind = engine)
