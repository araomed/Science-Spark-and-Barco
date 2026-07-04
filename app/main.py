from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app import models, schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab Management API")


@app.get("/")
async def root():
    return {"message": "Lab Management API is running!"}


@app.post("/equipment", response_model=schemas.EquipmentResponse)
def create_equipment(
    equipment: schemas.EquipmentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_equipment(db, equipment)


@app.get("/equipment", response_model=list[schemas.EquipmentResponse])
def get_equipment(db: Session = Depends(get_db)):
    return crud.get_all_equipment(db)