from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
#from server.db_models.items.items_model import ItemModel

from server.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, nullable=False)
    # is_active = Column(Boolean, default=True)
    location = Column(String(50))
    bio = Column(String)

    items = relationship("ItemModel", back_populates="owner")
