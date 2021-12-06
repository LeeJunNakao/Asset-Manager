from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Curency(Base):
    __tablename__ = 'currency'
    __table_args__ = (UniqueConstraint(
        'code', 'user_id', name='currency_unique__code__user_id'),)

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    decimal = Column(Integer)
    user_id = Column(Integer)


currency_metadata = Base.metadata
