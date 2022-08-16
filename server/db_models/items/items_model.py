from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from server.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    brand = Column(String, index=True)
    size = Column(String, index=True)
    condition = Column(String, index=True)
    color = Column(String, index=True)
    views = Column(Integer, index=True)
    upload_date = Column(DateTime)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")