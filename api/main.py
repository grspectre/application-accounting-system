import urllib.parse

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import models, schemas
from database.database import SessionLocal, engine
from packages.common.yandex_id import get_access_token


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


@app.get("/api/verify/yandex")
async def verify_yandex(code: str):
    response = get_access_token(code)
    print(response)
    if response is None:
        params = {'error': 'Yandex ID error'}
    else:
        params = {'refresh_token': response['refresh_token'], 'access_token': response['access_token']}
    return RedirectResponse("/?{}".format(urllib.parse.urlencode(params)))


app.mount("/", StaticFiles(directory="../public"), name="")
