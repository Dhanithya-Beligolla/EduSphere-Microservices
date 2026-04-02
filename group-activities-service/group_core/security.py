"""
group_core/security.py
JWT token validation dependency.
The API Gateway forwards a verified Bearer token; this service validates it
and extracts the user context (userId, role, schoolId).
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
from group_core.config import get_settings

bearer_scheme = HTTPBearer()
settings = get_settings()


class UserContext(BaseModel):
    userId: str
    role: str          # PRINCIPAL | DEPUTY | SECTIONAL_HEAD | CLASS_TEACHER | SUBJECT_TEACHER | STUDENT | PARENT
    schoolId: str
    name: str | None = None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> UserContext:
    """
    Decode and validate the JWT token.
    Returns the user context extracted from the token claims.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role", "STUDENT")
        school_id: str = payload.get("schoolId", "")
        name: str = payload.get("name", "")
        if user_id is None:
            raise credentials_exception
        return UserContext(userId=user_id, role=role, schoolId=school_id, name=name)
    except JWTError:
        raise credentials_exception


def require_role(*allowed_roles: str):
    """
    Factory for role-based access control dependency.
    Usage: Depends(require_role("SUBJECT_TEACHER", "PRINCIPAL"))
    """
    def role_checker(current_user: UserContext = Depends(get_current_user)) -> UserContext:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' is not permitted for this action.",
            )
        return current_user
    return role_checker
