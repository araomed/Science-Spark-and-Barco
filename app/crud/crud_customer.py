from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(**customer.model_dump())

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


def get_all_customers(db: Session):
    return db.query(Customer).all()


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def update_customer(db: Session, customer_id: int, customer: CustomerCreate):
    db_customer = get_customer(db, customer_id)

    if not db_customer:
        return None

    for key, value in customer.model_dump().items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)

    return db_customer


def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)

    if not db_customer:
        return None

    db.delete(db_customer)
    db.commit()

    return db_customer