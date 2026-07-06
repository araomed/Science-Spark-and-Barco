from pydantic import BaseModel

class EquipmentBase(BaseModel):
    name: str
    manufacturer: str | None = None
    model: str |None = None
    serial_number: str | None = None
    location: str | None = None


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(EquipmentBase):
    pass


class EquipmentResponse(EquipmentBase):
    id: int

    class Config:
        from_attributes = True