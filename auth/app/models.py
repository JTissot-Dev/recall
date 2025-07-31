from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from app.core.utils.date_time import utc_now
from app.enums import UserRole


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(max_length=100)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=100)
    role: UserRole = Field(default=UserRole.USER)
    disabled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
