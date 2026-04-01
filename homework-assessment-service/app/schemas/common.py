from pydantic import BaseModel
from typing import Any


class StandardResponse(BaseModel):
    success: bool = True
    message: str
    data: Any = None