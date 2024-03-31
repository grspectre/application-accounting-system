from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# @app.get("/")
# async def root():
#     return {"success": True, "message": "Hello World"}


@app.get("/api/ping")
async def ping():
    return {"success": True}


app.mount("/", StaticFiles(directory="../public"), name="")
