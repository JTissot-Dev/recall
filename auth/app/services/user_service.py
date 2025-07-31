from sqlmodel import Session
from app.repositories.user_repository import (
    create_user,
    get_user,
)
from app.core.utils.hash import verify_password, get_password_hash
from app.models import User
from app.schemas import UserCreate, UserInDB


def signup_user(session: Session, user_create: UserCreate) -> User:
    hashed_password = get_password_hash(user_create.password)
    user_in_db = UserInDB(
        **user_create.model_dump(), hashed_password=hashed_password
    )
    user = create_user(session, user_in_db)
    return user


def authenticate_user(session: Session, email: str, password: str):
    user = get_user(session, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
