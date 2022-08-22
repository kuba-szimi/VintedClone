from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship
from server.db_models.users.users_model import UserModel

from server.database import Base


class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), index=True, nullable=False)
    brand = Column(String(50), index=True, nullable=False)
    size = Column(String(10), index=True, nullable=False)
    condition = Column(String(25), index=True, nullable=False)
    color = Column(String(25), index=True, nullable=False)
    price = Column(Numeric, nullable=False)
    # views = Column(Integer, index=True)
    upload_date = Column(DateTime, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("UserModel", back_populates="items")
