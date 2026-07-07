from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


MaintenanceStatus = Literal["scheduled", "completed", "cancelled", "overdue"]


class MaintenanceBase(BaseModel):
    equipment_id: int
    maintenance_type: str = Field(min_length=1, max_length=100)
    performed_date: date
    next_due_date: date | None = None
    performed_by: str | None = None
    notes: str | None = None
    status: MaintenanceStatus = "scheduled"
    cost: Decimal | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.next_due_date and self.next_due_date < self.performed_date:
            raise ValueError("next_due_date cannot be before performed_date")

        return self


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(BaseModel):
    equipment_id: int | None = None
    maintenance_type: str | None = Field(default=None, min_length=1, max_length=100)
    performed_date: date | None = None
    next_due_date: date | None = None
    performed_by: str | None = None
    notes: str | None = None
    status: MaintenanceStatus | None = None
    cost: Decimal | None = Field(default=None, ge=0)


class MaintenanceResponse(MaintenanceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
