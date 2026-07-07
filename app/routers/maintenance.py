from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceUpdate,
    MaintenanceResponse,
)

from app.crud.crud_maintenance import (
    create_maintenance,
    get_all_maintenance,
    get_maintenance,
    get_equipment_maintenance,
    update_maintenance,
    delete_maintenance,
)

from app.crud.crud_equipment import get_equipment


router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"]
)


@router.post("/", response_model=MaintenanceResponse, status_code=201)
def create_new_maintenance(
    maintenance: MaintenanceCreate,
    db: Session = Depends(get_db)
):
    equipment = get_equipment(db, maintenance.equipment_id)

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    return create_maintenance(db, maintenance)


@router.get("/", response_model=list[MaintenanceResponse])
def read_all_maintenance(
    db: Session = Depends(get_db)
):
    return get_all_maintenance(db)


@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
def read_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db)
):
    maintenance = get_maintenance(
        db,
        maintenance_id
    )

    if maintenance is None:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found"
        )

    return maintenance


@router.get("/equipment/{equipment_id}", response_model=list[MaintenanceResponse])
def read_equipment_maintenance(
    equipment_id: int,
    db: Session = Depends(get_db)
):
    equipment = get_equipment(db, equipment_id)

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    return get_equipment_maintenance(
        db,
        equipment_id
    )


@router.put("/{maintenance_id}", response_model=MaintenanceResponse)
def edit_maintenance(
    maintenance_id: int,
    maintenance: MaintenanceUpdate,
    db: Session = Depends(get_db)
):
    if maintenance.equipment_id is not None:
        equipment = get_equipment(
            db,
            maintenance.equipment_id
        )

        if equipment is None:
            raise HTTPException(
                status_code=404,
                detail="Equipment not found"
            )

    updated = update_maintenance(
        db,
        maintenance_id,
        maintenance
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found"
        )

    return updated


@router.delete("/{maintenance_id}")
def remove_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_maintenance(
        db,
        maintenance_id
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found"
        )

    return {
        "message": "Maintenance record deleted successfully"
    }