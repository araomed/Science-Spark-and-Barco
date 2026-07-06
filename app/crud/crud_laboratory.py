from sqlalchemy.orm import Session
from app.models.laboratory import Laboratory
from app.schemas.laboratory import LaboratoryCreate


def create_laboratory(db: Session, laboratory: LaboratoryCreate):
    db_lab = Laboratory(**laboratory.model_dump())

    db.add(db_lab)
    db.commit()
    db.refresh(db_lab)

    return db_lab


def get_all_laboratories(db: Session):
    return db.query(Laboratory).all()


def get_laboratory(db: Session, laboratory_id: int):
    return db.query(Laboratory).filter(
        Laboratory.id == laboratory_id
    ).first()


def update_laboratory(db: Session, laboratory_id: int, laboratory: LaboratoryCreate):
    db_lab = get_laboratory(db, laboratory_id)

    if not db_lab:
        return None

    for key, value in laboratory.model_dump().items():
        setattr(db_lab, key, value)

    db.commit()
    db.refresh(db_lab)

    return db_lab


def delete_laboratory(db: Session, laboratory_id: int):
    db_lab = get_laboratory(db, laboratory_id)

    if not db_lab:
        return None

    db.delete(db_lab)
    db.commit()

    return db_lab