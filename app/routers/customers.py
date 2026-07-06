from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.crud.crud_customer import (
    create_customer,
    get_all_customers,
    get_customer,
    update_customer,
    delete_customer,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post("/", response_model=CustomerResponse)
def create(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, customer)


@router.get("/", response_model=list[CustomerResponse])
def get_all(db: Session = Depends(get_db)):
    return get_all_customers(db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_one(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


@router.put("/{customer_id}", response_model=CustomerResponse)
def update(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    updated = update_customer(db, customer_id, customer)

    if updated is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return updated


@router.delete("/{customer_id}")
def delete(customer_id: int, db: Session = Depends(get_db)):
    deleted = delete_customer(db, customer_id)

    if deleted is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {"message": "Customer deleted successfully"}