import datetime

from pydantic import BaseModel
from typing import List, Dict, Optional


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
