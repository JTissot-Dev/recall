from uuid import UUID
from pydantic import BaseModel
from app.enums import UserRole


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str


class UserPayload(BaseModel):
    id: UUID
    username: str
    email: str
    role: UserRole
    disabled: bool

    model_config = {"from_attributes": True}
