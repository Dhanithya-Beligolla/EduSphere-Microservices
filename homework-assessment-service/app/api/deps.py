from typing import Generator
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import extract_bearer_token
from app.services.identity_client import verify_user_token



def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(authorization: str | None = Header(default=None)):
    token = extract_bearer_token(authorization)
    return await verify_user_token(f"Bearer {token}")



def require_roles(*roles: str):
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )
        return current_user

    return role_checker