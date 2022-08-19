from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from server.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    brand = Column(String(50), index=True)
    size = Column(String(10), index=True)
    condition = Column(String(25), index=True)
    color = Column(String(25), index=True)
    views = Column(Integer, index=True)
    upload_date = Column(DateTime, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")