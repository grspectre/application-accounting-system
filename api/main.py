import urllib.parse

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import models, schemas, crud
from database.database import SessionLocal, engine
from packages.common.yandex_id import get_access_token, get_user_info

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.middleware("http")
async def check_token(request: Request, call_next):
    if '/api' not in str(request.url):
        return await call_next(request)
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return JSONResponse({"error": "Authorization token not found"}, status_code=401)
    db = next(get_db())
    user = crud.get_user(db, auth_header)
    if user is None:
        _, token = auth_header.split(' ')
        print(token)
        yandex_user_info = get_user_info(token)
        print(yandex_user_info)
    return await call_next(request)


@app.get("/api/user")
async def api_user():
    return {"success": True, "message": "Hello World"}


@app.get("/api/ping")
async def ping():
    return {"success": True}


@app.get("/api/verify/yandex")
async def verify_yandex(code: str):
    response = get_access_token(code)
    if response is None:
        params = {'error': 'Yandex ID error'}
    else:
        params = {'refresh_token': response['refresh_token'], 'access_token': response['access_token']}
    return RedirectResponse("/?{}".format(urllib.parse.urlencode(params)))


app.mount("/", StaticFiles(directory="../public"), name="")
