from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import relationship
import datetime
from .database import Base
from .schemas import User as UserSchema

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

    customer_orders = relationship("Order", back_populates="customer")
    employee_orders = relationship("Order", back_populates="employee")

    def get_schemas(self):
        data = self.__dict__
        return UserSchema(**data)

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    order_type = Column(String(50), index=True)
    order_text = Column(Text)
    order_status = Column(String(50), index=True)
    context = Column(JSONB, default=[])
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.now)
    deleted_at = Column(TIMESTAMP, nullable=True)

    customer = relationship("User", foreign_keys=[customer_id], back_populates="customer_orders")
    employee = relationship("User", foreign_keys=[employee_id], back_populates="employee_orders")

    def get_schemas(self):
        data = self.__dict__
        return UserSchema(**data)
