from pydantic import BaseModel


class EquipmentCreate(BaseModel):
    name: str
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str | None = None
    location: str | None = None


class EquipmentResponse(EquipmentCreate):
    id: int

    class Config:
        from_attributes = True