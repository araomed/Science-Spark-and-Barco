from sqlalchemy.orm import Session

from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate


def create_equipment(db: Session, equipment: EquipmentCreate):
    db_equipment = Equipment(**equipment.model_dump())

    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)

    return db_equipment


def get_all_equipment(db: Session):
    return db.query(Equipment).all()


def get_equipment(db: Session, equipment_id: int):
    return db.query(Equipment).filter(
        Equipment.id == equipment_id
    ).first()


def update_equipment(
    db: Session,
    equipment_id: int,
    equipment: EquipmentUpdate
):
    db_equipment = get_equipment(db, equipment_id)

    if not db_equipment:
        return None

    for key, value in equipment.model_dump().items():
        setattr(db_equipment, key, value)

    db.commit()
    db.refresh(db_equipment)

    return db_equipment


def delete_equipment(db: Session, equipment_id: int):
    db_equipment = get_equipment(db, equipment_id)

    if not db_equipment:
        return None

    db.delete(db_equipment)
    db.commit()

    return db_equipment