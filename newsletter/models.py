from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class Newsletter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    created_date: datetime = Field(default_factory=datetime.utcnow) 