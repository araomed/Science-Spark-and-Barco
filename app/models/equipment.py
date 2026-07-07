from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)

    laboratory_id = Column(Integer, ForeignKey("laboratories.id"), nullable=False)

    category = Column(String, nullable=False)

    name = Column(String, nullable=False)

    manufacturer = Column(String)

    model = Column(String)

    serial_number = Column(String, unique=True, nullable=False)

    asset_tag = Column(String, unique=True, nullable=False)

    purchase_date = Column(Date)

    warranty_expiry = Column(Date)

    maintenance_interval_months = Column(Integer)

    next_maintenance_due = Column(Date)

    status = Column(String)

    laboratory = relationship(
        "Laboratory",
        back_populates="equipment"
    )
