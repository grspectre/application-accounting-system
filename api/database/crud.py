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
