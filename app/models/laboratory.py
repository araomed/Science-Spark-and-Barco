from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Laboratory(Base):
    __tablename__ = "laboratories"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"))

    name = Column(String, nullable=False)

    building = Column(String)

    floor = Column(String)

    room_number = Column(String)

    customer = relationship("Customer", back_populates="laboratories")