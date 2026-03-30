"""
JWT parsing and token claim extraction.
This service does NOT implement login — it trusts tokens from an external IdP.
"""

from dataclasses import dataclass, field
import jwt
from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.core.constants import Role


@dataclass(frozen=True)
class TokenClaims:
    """Parsed and validated JWT claims."""
    sub: str
    school_id: str
    roles: list[str] = field(default_factory=list)
    section_ids: list[str] = field(default_factory=list)
    stream_ids: list[str] = field(default_factory=list)
    class_ids: list[str] = field(default_factory=list)
    subject_ids: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)

    def has_role(self, role: Role) -> bool:
        """Check if user has a specific role."""
        return role.value in self.roles

    def has_any_role(self, roles: set[Role]) -> bool:
        """Check if user has any of the given roles."""
        return bool(set(self.roles) & {r.value for r in roles})

    def is_admin_or_principal(self) -> bool:
        """Check if user has admin-level access."""
        return self.has_any_role({Role.ADMIN, Role.PRINCIPAL})


def decode_token(token: str) -> TokenClaims:
    """
    Decode and validate a JWT token, returning structured claims.

    Args:
        token: Raw JWT string (without 'Bearer ' prefix).

    Returns:
        TokenClaims with parsed scope data.

    Raises:
        AuthenticationError: If token is invalid, expired, or malformed.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise AuthenticationError(f"Invalid token: {str(e)}")

    sub = payload.get("sub")
    school_id = payload.get("school_id")

    if not sub or not school_id:
        raise AuthenticationError("Token missing required claims: sub, school_id")

    return TokenClaims(
        sub=str(sub),
        school_id=str(school_id),
        roles=payload.get("roles", []),
        section_ids=payload.get("section_ids", []),
        stream_ids=payload.get("stream_ids", []),
        class_ids=payload.get("class_ids", []),
        subject_ids=payload.get("subject_ids", []),
        permissions=payload.get("permissions", []),
    )
