from pydantic import BaseModel


class LaboratoryCreate(BaseModel):
    customer_id: int
    name: str
    building: str | None = None
    floor: str | None = None
    room_number: str | None = None


class LaboratoryResponse(LaboratoryCreate):
    id: int

    class Config:
        from_attributes = True