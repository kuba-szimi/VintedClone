from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from server.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    nickname = Column(String(50), unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    location = Column(String(50))
    bio = Column(String)

    items = relationship("Item", back_populates="owner")