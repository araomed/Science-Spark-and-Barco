from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    company: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None


class CustomerResponse(CustomerCreate):
    id: int

    class Config:
        from_attributes = True