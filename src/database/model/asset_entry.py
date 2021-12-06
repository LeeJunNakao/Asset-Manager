from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from .asset import Asset
from .currency import Curency

Base = declarative_base()


class AssetEntry(Base):
    __tablename__ = 'asset_entry'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    date = Column(String)
    quantity = Column(Integer)
    asset_id = Column(Integer, ForeignKey(Asset.id, ondelete="CASCADE"),
                      nullable=False)
    currency_id = Column(Integer, ForeignKey(Curency.id, ondelete="CASCADE"),
                         nullable=False)
    value = Column(Integer)


asset_entry_metadata = Base.metadata
