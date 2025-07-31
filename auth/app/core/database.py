from typing import Annotated
from sqlmodel import create_engine, Session
from fastapi import Depends
from app.core.config import settings


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,  # Vérifier la connexion avant utilisation
    pool_size=20,  # Taille du pool de connexions
    max_overflow=30,  # Nombre de connexions supplémentaires autorisées
)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
