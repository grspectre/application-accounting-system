import urllib.parse

from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import ValidationError

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


def get_user_from_token(request: Request, db: Session = Depends(get_db)) -> Optional[models.User]:
    auth_header = request.headers.get('Authorization')
    _, token = auth_header.split(' ')
    return crud.get_user(db, user_token=token)


@app.middleware("http")
async def check_token(request: Request, call_next):
    if '/api' not in str(request.url):
        return await call_next(request)
    exclude = ['/api/ping', '/api/verify/yandex']
    for exclude_path in exclude:
        if exclude_path in str(request.url):
            return await call_next(request)
    auth_header = request.headers.get('Authorization')
    error_json = {"error": "Authorization token not found"}
    if auth_header is None:
        return JSONResponse(error_json, status_code=401)
    db = next(get_db())
    _, token = auth_header.split(' ')
    user = crud.get_user(db, user_token=token)
    if user is None:
        yandex_user_info = get_user_info(token)
        if 'default_email' not in yandex_user_info:
            return JSONResponse(error_json, status_code=401)
        email = yandex_user_info['default_email']
        name = yandex_user_info['display_name']
        user = crud.get_user(db, email=email)
        if user is None:
            user_schema = schemas.UserCreate(
                name=name, email=email, password=token, context=yandex_user_info
            )
            user = crud.create_user(db, user_schema)
    return await call_next(request)


@app.get("/api/user")
async def api_user(request: Request, db: Session = Depends(get_db)):
    user = get_user_from_token(request, db)
    return {
        "success": True,
        "data": user.get_schemas().get_info(),
        "dictionaries": schemas.StaticDictionary.all(),
    }


@app.get("/api/dictionary/all")
async def api_dictionary_all():
    return {
        "success": True,
        "dictionaries": schemas.StaticDictionary.all(),
    }


@app.post("/api/order")
async def api_order_post(request: Request, order: schemas.OrderPost, db: Session = Depends(get_db)):
    user = get_user_from_token(request, db)

    try:
        order_create = schemas.OrderCreate(
            order_type=order.order_type,
            order_text=order.order_text,
            order_status=order.order_status,
            customer_id=user.id
        )
    except ValidationError as e:
        return JSONResponse({'status': False, 'error': 'Validation error', 'errors': e.errors()}, status_code=401)

    order = crud.create_order(db, order_create)
    return JSONResponse({
        "success": True,
        "data": {
            "uuid": order.context['uuid']
        }
    })


@app.get("/api/order/list")
async def api_order_post(request: Request, db: Session = Depends(get_db)):
    user = get_user_from_token(request, db)

    orders = crud.get_order_list(db, user_id=user.id)
    return orders


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
