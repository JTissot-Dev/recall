from datetime import timedelta
from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    status, 
    Response
)
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.core.config import settings
from app.core.database import SessionDep
from app.core.utils.jwt import create_access_token
from app.services.user_service import (
    signup_user,
    authenticate_user
)
from app.schemas import (
    Token,
    UserCreate,
    UserPayload
)


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserPayload, status_code=status.HTTP_201_CREATED)
async def signup(
    session: SessionDep,
    user_create: UserCreate,
    response: Response
):
    user = signup_user(session, user_create)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User could not be created",
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data=UserPayload.model_validate(user).model_dump(mode="json"), 
        expires_delta=access_token_expires
    )
    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        max_age=access_token_expires.total_seconds(),
        secure=settings.SECURE_COOKIE,
        samesite="strict"
    )
    return user


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")