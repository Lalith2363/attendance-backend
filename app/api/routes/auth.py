from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.deps import get_db
from app.models.user import User
from app.models.token import RefreshToken
from app.schemas.auth import TokenResponse
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    REFRESH_TOKEN_EXPIRE_DAYS
)

router = APIRouter(prefix="/auth")


# 🔐 LOGIN (OAuth2 Compatible)
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({
        "sub": user.email,
        "role": user.role,
        "employee_id": user.id
    })

    refresh_token = create_refresh_token()

    db_token = RefreshToken(
        user_email=user.email,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    db.add(db_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# 🔄 REFRESH TOKEN
@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):

    token_entry = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if not token_entry:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    new_access_token = create_access_token({
        "sub": token_entry.user_email
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


# 🚪 LOGOUT (REVOKE TOKEN)
@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):

    token_entry = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if token_entry:
        db.delete(token_entry)
        db.commit()

    return {"message": "Logged out successfully"}