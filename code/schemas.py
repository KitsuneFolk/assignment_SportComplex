from datetime import date
from typing import Optional

from pydantic import BaseModel


class VisitorBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    membership_type: str
    registration_date: date
    is_active: bool = True
    email: str


class VisitorCreate(VisitorBase):
    pass


class VisitorUpdate(VisitorBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    membership_type: Optional[str] = None
    registration_date: Optional[date] = None
    is_active: Optional[bool] = None
    email: Optional[str] = None


class Visitor(VisitorBase):
    id: int

    class Config:
        from_attributes = True


class VisitorSearchResults(BaseModel):
    results: list[Visitor]
