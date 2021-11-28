from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Asset(Base):
    __tablename__ = 'asset'
    __table_args__ = (UniqueConstraint(
        'code', 'user_id', name='unique__code__user_id'),)

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    user_id = Column(Integer)


asset_metadata = Base.metadata
