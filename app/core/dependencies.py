"""
FastAPI dependency callables for authentication and authorization.
These are injected into route handlers via Depends().
"""

from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import TokenClaims, decode_token
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.constants import Role, ADMIN_ROLES, WRITE_ROLES

# Scheme extractor — returns the bearer token or raises 401
_bearer_scheme = HTTPBearer(auto_error=False)


async def require_authenticated_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> TokenClaims:
    """
    Validate the Bearer token and return parsed claims.
    Raises 401 if missing or invalid.
    """
    if credentials is None:
        raise AuthenticationError("Bearer token is required")

    claims = decode_token(credentials.credentials)

    # Attach to request state for downstream access
    request.state.claims = claims
    return claims


async def require_material_read_access(
    claims: TokenClaims = Depends(require_authenticated_user),
) -> TokenClaims:
    """
    Ensures the user has at least read-level access to materials.
    All authenticated users can read, but students/parents only see published materials
    (filtering is enforced at the service layer).
    """
    # All authenticated roles can attempt to read — the service layer
    # applies visibility filtering based on role + scope.
    return claims


async def require_material_write_access(
    claims: TokenClaims = Depends(require_authenticated_user),
) -> TokenClaims:
    """
    Ensures the user has a role that permits creating/updating materials.
    Students and parents cannot write.
    """
    if not claims.has_any_role(WRITE_ROLES):
        raise AuthorizationError(
            "Your role does not permit creating or modifying materials"
        )
    return claims


async def require_admin_or_principal(
    claims: TokenClaims = Depends(require_authenticated_user),
) -> TokenClaims:
    """
    Ensures the user is ADMIN or PRINCIPAL — full management access.
    """
    if not claims.has_any_role(ADMIN_ROLES):
        raise AuthorizationError("Admin or Principal role required")
    return claims
