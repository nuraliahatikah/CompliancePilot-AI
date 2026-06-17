from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user, get_password_hash, verify_password
from app.config import get_settings
from app.database import get_db
from app.models import AuditLog, User, UserRole
from app.schemas import LoginRequest, MessageResponse, Token, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
settings = get_settings()


def _log_action(db: Session, user_id: int | None, action: str, details: dict | None = None) -> None:
    log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type="auth",
        details=details or {},
    )
    db.add(log)
    db.commit()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Annotated[Session, Depends(get_db)]):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_count = db.query(User).count()
    role = user_data.role if user_count > 0 else UserRole.ADMIN

    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    _log_action(db, user.id, "user_registered", {"email": user.email})
    return user


@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")

    token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role.value},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    _log_action(db, user.id, "user_login", {"email": user.email})
    return Token(access_token=token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/logout", response_model=MessageResponse)
def logout(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    _log_action(db, current_user.id, "user_logout")
    return MessageResponse(message="Successfully logged out")
