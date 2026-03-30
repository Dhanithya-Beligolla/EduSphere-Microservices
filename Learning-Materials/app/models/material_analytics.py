"""
Material Analytics placeholder model — for future expansion.
"""

from typing import Any


def new_material_analytics(material_id: str) -> dict[str, Any]:
    """
    Stub analytics document for future read-model implementation.
    """
    return {
        "materialId": material_id,
        "viewCount": 0,
        "downloadCount": 0,
        "uniqueViewers": 0,
        "lastAccessedAt": None,
    }
