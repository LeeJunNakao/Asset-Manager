import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from src.config import DB_URI


engine = create_engine(
    DB_URI, echo=True, future=True
)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
