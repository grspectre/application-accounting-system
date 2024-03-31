from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import relationship
import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    roles = Column(JSONB, default=[])
    hashed_password = Column(String)
    context = Column(JSONB, default=[])
    is_active = Column(Boolean, default=True)
    is_company = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.now)
    deleted_at = Column(TIMESTAMP, nullable=True)