import urllib.parse

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import models, schemas, crud
from database.database import SessionLocal, engine
from packages.common.yandex_id import get_access_token, get_user_info

models.Base.metadata.create_all(bind=engine)

print(get_user_info('y0_AgAEA7qkc6tpAAuODgAAAAEA0JD9AACtRvYJwe1MEo9Hg_s5i7GdCRmt6w'))