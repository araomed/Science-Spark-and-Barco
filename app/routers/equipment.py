from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.equipment import (
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentResponse,
)

from app.crud.crud_equipment import (
    create_equipment,
    get_all_equipment,
    get_equipment,
    update_equipment,
    delete_equipment,
)

router = APIRouter(
    prefix="/equipment",
    tags=["Equipment"],
)


@router.get("/", response_model=list[EquipmentResponse])
def read_equipment(db: Session = Depends(get_db)):
    return get_all_equipment(db)


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def read_equipment_by_id(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    equipment = get_equipment(db, equipment_id)

    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return equipment


@router.post("/", response_model=EquipmentResponse)
def add_equipment(
    equipment: EquipmentCreate,
    db: Session = Depends(get_db),
):
    return create_equipment(db, equipment)


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def edit_equipment(
    equipment_id: int,
    equipment: EquipmentUpdate,
    db: Session = Depends(get_db),
):
    updated = update_equipment(db, equipment_id, equipment)

    if not updated:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return updated


@router.delete("/{equipment_id}")
def remove_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_equipment(db, equipment_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return {"message": "Equipment deleted successfully"}