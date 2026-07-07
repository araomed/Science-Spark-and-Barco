from sqlalchemy.orm import Session

from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate


def create_equipment(db: Session, equipment: EquipmentCreate):
    db_equipment = Equipment(**equipment.model_dump())

    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)

    return db_equipment


def get_all_equipment(db: Session, laboratory_id: int | None = None):
    query = db.query(Equipment)

    if laboratory_id is not None:
        query = query.filter(Equipment.laboratory_id == laboratory_id)

    return query.all()


def get_equipment(db: Session, equipment_id: int):
    return db.query(Equipment).filter(
        Equipment.id == equipment_id
    ).first()


def get_equipment_by_serial_number(db: Session, serial_number: str):
    return db.query(Equipment).filter(
        Equipment.serial_number == serial_number
    ).first()


def get_equipment_by_asset_tag(db: Session, asset_tag: str):
    return db.query(Equipment).filter(
        Equipment.asset_tag == asset_tag
    ).first()


def update_equipment(
    db: Session,
    equipment_id: int,
    equipment: EquipmentUpdate
):
    db_equipment = get_equipment(db, equipment_id)

    if not db_equipment:
        return None

    update_data = equipment.model_dump(exclude_unset=True)

    for key, value in update_data.items():
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
