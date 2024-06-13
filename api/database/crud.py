import uuid
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, select

from . import models, schemas


def get_user(db: Session, user_token: Optional[str] = None, email: Optional[str] = None, user_id: Optional[int] = None):
    if user_token is None and email is None and user_id is None:
        return None
    query = db.query(models.User)
    if email is not None:
        query = query.filter(models.User.email == email)
    if user_token is not None:
        query = query.filter(models.User.hashed_password == user_token)
    if user_id is not None:
        query = query.filter(models.User.id == user_id)
    return query.first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        hashed_password=user.password,
        name=user.name,
        context=user.context
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def change_role(db: Session, user: models.User, role: schemas.UserRole):
    available = schemas.StaticDictionary.get_types('user_roles')
    if role.role not in available:
        return user
    roles = user.roles[:]
    if role.action == schemas.ActionEnum.add and role.role not in roles:
        roles.append(role.role)
    if role.action == schemas.ActionEnum.remove and role.role in roles:
        roles.remove(role.role)
    user.roles = roles
    db.commit()
    db.refresh(user)
    return user


def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(
        customer_id=order.customer_id,
        order_type=order.order_type,
        order_text=order.order_text,
        order_status=order.order_status,
        context={"uuid": str(uuid.uuid4())}
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_list(db: Session, user_id: int):
    query = db.query(models.Order)
    query = query.filter(or_(models.Order.customer_id == user_id, models.Order.employee_id == user_id))
    response = query.all()
    users_cache = {}
    orders = schemas.OrderList()
    for order in response:
        cid = order.customer_id
        eid = order.employee_id
        if cid not in users_cache:
            users_cache[cid] = get_user(db, user_id=cid)
        if eid is not None and eid not in users_cache:
            users_cache[eid] = get_user(db, user_id=eid)
        customer_info = users_cache[cid].get_schemas().get_info()
        employee_info = users_cache[eid].get_schemas().get_info() if eid is not None else None
        orderItem = schemas.OrderGet(
            order_type=order.order_type,
            order_status=order.order_status,
            order_text=order.order_text,
            customer=customer_info,
            employee=employee_info
        )
        orders.append(orderItem)
    return orders
