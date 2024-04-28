import uuid
from typing import Optional
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_token: Optional[str] = None, email: Optional[str] = None):
    if user_token is None and email is None:
        return None
    query = db.query(models.User)
    if email is not None:
        query.filter(models.User.email == email)
    if user_token is not None:
        query.filter(models.User.hashed_password == user_token)
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
