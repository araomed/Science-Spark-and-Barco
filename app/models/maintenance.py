from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Maintenance(Base):
    __tablename__ = "maintenance"
    __table_args__ = (
        CheckConstraint(
            "status IN ('scheduled', 'completed', 'cancelled', 'overdue')",
            name="maintenance_status_check",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=False,
        index=True,
    )

    maintenance_type = Column(String, nullable=False)

    performed_date = Column(Date, nullable=False)

    next_due_date = Column(Date)

    performed_by = Column(String)

    notes = Column(Text)

    status = Column(String, nullable=False)

    cost = Column(Numeric(10, 2))

    equipment = relationship(
        "Equipment",
        back_populates="maintenance_records",
    )
