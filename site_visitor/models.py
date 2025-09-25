from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class SiteVisitor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ip_address: str = Field(index=True)
    user_agent: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow) 