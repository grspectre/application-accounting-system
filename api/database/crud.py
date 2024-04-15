from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_token: str):
    return db.query(models.User).filter(models.User.hashed_password == user_token).first()
