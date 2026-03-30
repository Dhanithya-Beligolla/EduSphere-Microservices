"""
Custom domain exceptions for the Learning Materials service.
Each exception maps to a specific HTTP status code and error code.
"""


class DomainError(Exception):
    """Base class for all domain-specific errors."""

    def __init__(self, message: str, code: str = "DOMAIN_ERROR", status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(DomainError):
    """Resource not found."""

    def __init__(self, resource: str = "Resource", identifier: str = ""):
        detail = f"{resource} not found"
        if identifier:
            detail = f"{resource} '{identifier}' not found"
        super().__init__(message=detail, code="NOT_FOUND", status_code=404)


class ConflictError(DomainError):
    """Conflicting state or duplicate resource."""

    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message=message, code="CONFLICT", status_code=409)


class AuthorizationError(DomainError):
    """User does not have permission to perform the action."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message=message, code="FORBIDDEN", status_code=403)


class AuthenticationError(DomainError):
    """Authentication failed or token is invalid."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(message=message, code="UNAUTHORIZED", status_code=401)


class LifecycleError(DomainError):
    """Invalid lifecycle state transition."""

    def __init__(self, current_state: str, target_state: str):
        message = f"Cannot transition from {current_state} to {target_state}"
        super().__init__(message=message, code="LIFECYCLE_ERROR", status_code=422)


class ValidationError(DomainError):
    """Domain validation failure (separate from Pydantic schema validation)."""

    def __init__(self, message: str, field: str | None = None):
        self.field = field
        super().__init__(message=message, code="VALIDATION_ERROR", status_code=422)


class PublishValidationError(DomainError):
    """Material does not meet minimum requirements for publishing."""

    def __init__(self, missing_fields: list[str]):
        fields_str = ", ".join(missing_fields)
        message = f"Cannot publish: missing required fields — {fields_str}"
        self.missing_fields = missing_fields
        super().__init__(message=message, code="PUBLISH_VALIDATION_ERROR", status_code=422)
