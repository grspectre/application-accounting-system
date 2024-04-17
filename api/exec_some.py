import urllib.parse

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import models, schemas, crud
from database.database import SessionLocal, engine
from packages.common.yandex_id import get_access_token, get_user_info

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = next(get_db())
token = ''

user = crud.get_user(db, user_token=token)
user.get_schemas().get_info()
