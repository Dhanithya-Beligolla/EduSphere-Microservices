from datetime import datetime, timezone
from uuid import uuid4


def meta_payload() -> dict:
    return {
        "requestId": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "v1",
    }


def success_payload(data) -> dict:
    return {
        "data": data,
        "meta": meta_payload(),
        "errors": [],
    }


def error_payload(message: str, code: str, status_code: int) -> dict:
    return {
        "data": None,
        "meta": {**meta_payload(), "statusCode": status_code},
        "errors": [{"message": message, "code": code}],
    }
