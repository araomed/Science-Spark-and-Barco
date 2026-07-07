from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.equipment import (
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentResponse,
)

from app.crud.crud_equipment import (
    create_equipment,
    get_equipment_by_asset_tag,
    get_equipment_by_serial_number,
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
def read_equipment(
    laboratory_id: int | None = None,
    db: Session = Depends(get_db),
):
    return get_all_equipment(db, laboratory_id=laboratory_id)


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def read_equipment_by_id(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    equipment = get_equipment(db, equipment_id)

    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return equipment


@router.post(
    "/",
    response_model=EquipmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_equipment(
    equipment: EquipmentCreate,
    db: Session = Depends(get_db),
):
    errors = []

    if get_equipment_by_serial_number(db, equipment.serial_number):
        errors.append("serial_number already exists")

    if get_equipment_by_asset_tag(db, equipment.asset_tag):
        errors.append("asset_tag already exists")

    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=", ".join(errors),
        )

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
