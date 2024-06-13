import datetime

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
from enum import Enum


class StaticDictionary:
    __dictionaries: Dict = {
        "order_types": (
            {"type": "call", "value": "Звонок"}, 
            {"type": "chat", "value": "Чат"}, 
            {"type": "visit", "value": "Визит"},
        ),
        "order_statuses": (
            {"type": "new", "value": "Новая",}, 
            {"type": "processed", "value": "Обработанная",}, 
            {"type": "in_progress", "value": "В процессе",}, 
            {"type": "declined", "value": "Отклонённая",},
        ),
        "user_roles": (
            {"type": "manager", "value": "Менеджер",}, 
            {"type": "admin", "value": "Администратор",}, 
        )
    }

    @classmethod
    def get_types(cls, key: str) -> List:
        if key not in cls.__dictionaries:
            return []
        return [item["type"] for item in cls.__dictionaries[key]]

    @classmethod
    def get(cls, key: str) -> List:
        if key not in cls.__dictionaries:
            return []
        return cls.__dictionaries[key]

    @classmethod
    def all(cls):
        return cls.__dictionaries


class BaseOrder(BaseModel):
    order_type: str = Field(default=None, description="Order type")
    order_status: str = Field(default="new", description="Order status")

    @field_validator("order_status")
    @classmethod
    def order_status_validator(cls, v: str) -> str:
        # FIXME не самое лучшее место, но пока так
        statuses = ["new", "processed", "in_progress", "declined"] 
        if v not in statuses:
            raise ValueError("Status '{}' unavailable. Available statuses: {}".format(v, ", ".join(statuses)))
        return v

    @field_validator("order_type")
    @classmethod
    def order_type_validator(cls, v: str) -> str:
        # FIXME не самое лучшее место, но пока так
        # Тут я понял, что не понимаю это поле.
        types = ["call", "chat", "visit"]
        if v not in types:
            raise ValueError("Status '{}' unavailable. Available types: {}".format(v, ", ".join(types)))
        return v


class OrderPost(BaseOrder):
    order_text: str = Field(default=None, description="Order text", max_length=1024)


class OrderCreate(OrderPost):
    customer_id: int


class Order(BaseOrder):
    id: int
    customer_id: int
    employee_id: Optional[int]
    order_text: str
    context: Dict
    order_history: Dict
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True


class ActionEnum(str, Enum):
    add = 'add'
    remove = 'remove'


class UserRole(BaseModel):
    role: str
    action: ActionEnum = ActionEnum.remove


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str
    password: str
    context: Dict


class UserInfo(UserBase):
    email: str
    name: str
    surname: str
    display_name: str
    avatar_url: str
    roles: set
    created_at: datetime.datetime
    updated_at: datetime.datetime
    is_deleted: bool
    is_active: bool
    is_company: bool

    def __hash__(self) -> int:
        return self.email.__hash__()


class User(UserBase):
    id: int
    name: str
    roles: List
    context: Dict
    is_active: bool
    is_company: bool
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]
    customer_orders: list[Order] = []
    employee_orders: list[Order] = []

    class Config:
        from_attributes = True

    def get_info(self):
        return UserInfo(
            email=self.email,
            name=self.context['first_name'],
            surname=self.context['last_name'],
            display_name=self.name,
            avatar_url='https://avatars.mds.yandex.net/get-yapic/{}/islands-retina-middle'.format(self.context['default_avatar_id']),
            roles=set(self.roles),
            created_at=self.created_at,
            updated_at=self.updated_at if self.updated_at is not None else self.created_at,
            is_deleted=self.deleted_at is not None,
            is_active=self.is_active,
            is_company=self.is_company
        )

class OrderGet(OrderPost):
    customer: UserInfo
    employee: Optional[UserInfo]


class OrderList(BaseModel):
    success: bool = True
    orders: List[OrderGet] = []

    def append(self, item: OrderGet):
        self.orders.append(item)
