"""
ObjectId helpers — convert between MongoDB ObjectId and string for API exposure.
"""

from bson import ObjectId
from bson.errors import InvalidId

from app.core.exceptions import ValidationError


def to_object_id(id_str: str) -> ObjectId:
    """Convert a string to a BSON ObjectId, raising ValidationError if invalid."""
    try:
        return ObjectId(id_str)
    except (InvalidId, TypeError):
        raise ValidationError(f"Invalid ID format: {id_str}", field="id")


def serialize_doc(doc: dict) -> dict:
    """
    Convert a MongoDB document for API output:
    - Converts _id ObjectId to 'id' string
    - Removes _id field
    """
    if doc is None:
        return doc
    doc = dict(doc)
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


def serialize_docs(docs: list[dict]) -> list[dict]:
    """Serialize a list of MongoDB documents."""
    return [serialize_doc(d) for d in docs]
