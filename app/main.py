from fastapi import FastAPI

from app.database import Base, engine
from app.routers import equipment, customers
from app.routers import laboratories
from app.routers import maintenance

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab Management API")

app.include_router(equipment.router)
app.include_router(customers.router)
app.include_router(laboratories.router)
app.include_router(maintenance.router)

@app.get("/")
def root():
    return {"message": "Lab Management API is running!"}