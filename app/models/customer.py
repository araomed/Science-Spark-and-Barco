from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    company = Column(String)

    email = Column(String, unique=True)

    phone = Column(String)

    address = Column(String)

    laboratories = relationship(
        "Laboratory",
        back_populates="customer"
    )