from sqlalchemy.orm import Session

from app.models.maintenance import Maintenance
from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceUpdate,
)


def create_maintenance(
    db: Session,
    maintenance: MaintenanceCreate
):
    db_maintenance = Maintenance(
        **maintenance.model_dump()
    )

    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)

    return db_maintenance


def get_all_maintenance(
    db: Session
):
    return db.query(Maintenance).all()


def get_maintenance(
    db: Session,
    maintenance_id: int
):
    return (
        db.query(Maintenance)
        .filter(Maintenance.id == maintenance_id)
        .first()
    )


def get_equipment_maintenance(
    db: Session,
    equipment_id: int
):
    return (
        db.query(Maintenance)
        .filter(Maintenance.equipment_id == equipment_id)
        .all()
    )


def update_maintenance(
    db: Session,
    maintenance_id: int,
    maintenance: MaintenanceUpdate
):
    db_maintenance = get_maintenance(
        db,
        maintenance_id
    )

    if db_maintenance is None:
        return None

    for key, value in maintenance.model_dump(
        exclude_unset=True
    ).items():
        setattr(
            db_maintenance,
            key,
            value
        )

    db.commit()
    db.refresh(db_maintenance)

    return db_maintenance


def delete_maintenance(
    db: Session,
    maintenance_id: int
):
    db_maintenance = get_maintenance(
        db,
        maintenance_id
    )

    if db_maintenance is None:
        return None

    db.delete(db_maintenance)
    db.commit()

    return db_maintenance