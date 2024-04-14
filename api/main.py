import urllib.parse

from fastapi import Depends, FastAPI, HTTPException, Request
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


# @app.middleware("http")
# async def check_token(request: Request, call_next):
#     return await call_next(request)
#     print('/api' not in request.url)
#     if '/api' not in request.url:
#         return await call_next(request)
#     auth_header = request.headers.get('Authorization')
#     print(auth_header)
#     if auth_header is None:
#         print("we are here")
#         return JSONResponse({"error": "Authorization token not found"}, status_code=401)
#     return await call_next(request)


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
