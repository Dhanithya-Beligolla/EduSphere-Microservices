"""
Material Version domain model.
"""

from datetime import datetime
from typing import Any


def new_material_version(
    *,
    material_id: str,
    version_number: int,
    file_id: str | None = None,
    external_url: str | None = None,
    change_log: str = "",
    created_by: str,
) -> dict[str, Any]:
    """
    Factory function that builds a new material version document.
    """
    return {
        "materialId": material_id,
        "versionNumber": version_number,
        "fileId": file_id,
        "externalUrl": external_url,
        "changeLog": change_log,
        "createdAt": datetime.utcnow(),
        "createdBy": created_by,
    }
