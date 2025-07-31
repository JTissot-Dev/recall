from sqlmodel import Session, select
from app.models import User
from app.schemas import UserInDB


def get_user(session: Session, email: str) -> User | None:
    query = select(User).where(User.email == email)
    return session.exec(query).first()


def create_user(session: Session, user_in_db: UserInDB) -> User:
    user = User.model_validate(user_in_db)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
