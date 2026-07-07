from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


EquipmentStatus = Literal["active", "inactive", "maintenance", "retired", "Available"]


class EquipmentBase(BaseModel):
    laboratory_id: int
    category: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=150)
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str = Field(min_length=1, max_length=100)
    asset_tag: str = Field(min_length=1, max_length=100)
    purchase_date: date | None = None
    warranty_expiry: date | None = None
    maintenance_interval_months: int | None = Field(default=None, gt=0)
    next_maintenance_due: date | None = None
    status: EquipmentStatus | None = "active"

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.purchase_date
            and self.warranty_expiry
            and self.warranty_expiry < self.purchase_date
        ):
            raise ValueError("warranty_expiry cannot be before purchase_date")

        return self


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    laboratory_id: int | None = None
    category: str | None = Field(default=None, min_length=1, max_length=100)
    name: str | None = Field(default=None, min_length=1, max_length=150)
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str = Field(default=None, min_length=1, max_length=100)
    asset_tag: str = Field(default=None, min_length=1, max_length=100)
    purchase_date: date | None = None
    warranty_expiry: date | None = None
    maintenance_interval_months: int | None = Field(default=None, gt=0)
    next_maintenance_due: date | None = None
    status: EquipmentStatus | None = None


class EquipmentResponse(EquipmentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
