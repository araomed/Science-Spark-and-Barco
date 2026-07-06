from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.laboratory import (
    LaboratoryCreate,
    LaboratoryResponse,
)

from app.crud.crud_laboratory import (
    create_laboratory,
    get_all_laboratories,
    get_laboratory,
    update_laboratory,
    delete_laboratory,
)

from app.crud.crud_customer import get_customer

router = APIRouter(
    prefix="/laboratories",
    tags=["Laboratories"]
)


@router.post("/", response_model=LaboratoryResponse)
def create_new_laboratory(
    laboratory: LaboratoryCreate,
    db: Session = Depends(get_db)
):
    customer = get_customer(db, laboratory.customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return create_laboratory(db, laboratory)


@router.get("/", response_model=list[LaboratoryResponse])
def read_laboratories(
    db: Session = Depends(get_db)
):
    return get_all_laboratories(db)


@router.get("/{laboratory_id}", response_model=LaboratoryResponse)
def read_laboratory(
    laboratory_id: int,
    db: Session = Depends(get_db)
):
    laboratory = get_laboratory(db, laboratory_id)

    if laboratory is None:
        raise HTTPException(
            status_code=404,
            detail="Laboratory not found"
        )

    return laboratory


@router.put("/{laboratory_id}", response_model=LaboratoryResponse)
def edit_laboratory(
    laboratory_id: int,
    laboratory: LaboratoryCreate,
    db: Session = Depends(get_db)
):
    customer = get_customer(db, laboratory.customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    updated = update_laboratory(
        db,
        laboratory_id,
        laboratory
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Laboratory not found"
        )

    return updated


@router.delete("/{laboratory_id}")
def remove_laboratory(
    laboratory_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_laboratory(
        db,
        laboratory_id
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Laboratory not found"
        )

    return {
        "message": "Laboratory deleted successfully"
    }