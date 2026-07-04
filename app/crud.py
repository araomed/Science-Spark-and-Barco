from sqlalchemy.orm import Session
from app import models, schemas


def create_equipment(db: Session, equipment: schemas.EquipmentCreate):
    db_equipment = models.Equipment(**equipment.model_dump())

    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)

    return db_equipment


def get_all_equipment(db: Session):
    return db.query(models.Equipment).all()