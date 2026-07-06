from fastapi import FastAPI

from app.database import Base, engine
from app.routers import equipment

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab Management API")

app.include_router(equipment.router)


@app.get("/")
def root():
    return {"message": "Lab Management API is running!"}