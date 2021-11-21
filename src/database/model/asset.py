from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Asset(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)
    user_id = Column(Integer)


asset_metadata = Base.metadata
