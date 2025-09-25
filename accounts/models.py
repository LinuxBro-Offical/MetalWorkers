from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    leads: List["Lead"] = Relationship(back_populates="service")


class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True)
    mobile: Optional[str] = None
    message: Optional[str] = None

    service_id: Optional[int] = Field(default=None, foreign_key="service.id")
    service: Optional[Service] = Relationship(back_populates="leads") 