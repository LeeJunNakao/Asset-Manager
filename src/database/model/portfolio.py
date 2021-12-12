from sqlalchemy import Column, Integer, String, UniqueConstraint, ARRAY
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Portfolio(Base):
    __tablename__ = 'portfolio'
    __table_args__ = (UniqueConstraint(
        'name', 'user_id', name='portfolio_unique__name__user_id'),)

    id = Column(Integer, primary_key=True)
    name = Column(String)
    assets_ids = Column(ARRAY(Integer))
    user_id = Column(Integer)


portfolio_metadata = Base.metadata
