from fastapi import APIRouter, HTTPException, Query
from communication_models.communication_schemas import NoticeCreate, Notice, APIResponse
from communication_data.communication_mock_data import NOTICES
from datetime import datetime
import uuid

router = APIRouter(prefix="/notices", tags=["Notices"])

@router.post("", response_model=APIResponse)
async def create_notice(notice: NoticeCreate):
    """
    Create a new notice.
    Restricted to: Principal (ALL), Sectional Head (SECTION level), Teacher (CLASS level - if applicable)
    """
    # Role-based check (Simplified simulation)
    if notice.author_role not in ["Principal", "Sectional Head"]:
         raise HTTPException(status_code=403, detail="Only Principal or Sectional Heads can create notices.")
    
    new_notice = {
        "id": f"N_{str(uuid.uuid4())[:8]}",
        "title": notice.title,
        "content": notice.content,
        "audience": notice.audience,
        "status": "DRAFT",
        "created_at": datetime.utcnow(),
        "published_at": None,
        "author_id": notice.author_id,
        "author_role": notice.author_role
    }
    NOTICES.append(new_notice)
    return APIResponse(data=new_notice)

@router.get("", response_model=APIResponse)
async def get_notices(audience: str = Query(None)):
    """
    List notices, optionally filtered by audience.
    """
    if audience:
        filtered = [n for n in NOTICES if n["audience"] == audience or n["audience"] == "ALL"]
    else:
        filtered = NOTICES
    return APIResponse(data=filtered)

@router.post("/{noticeId}/publish", response_model=APIResponse)
async def publish_notice(noticeId: str):
    """
    Publish a draft notice.
    """
    for notice in NOTICES:
        if notice["id"] == noticeId:
            if notice["status"] == "PUBLISHED":
                raise HTTPException(status_code=400, detail="Notice is already published.")
            notice["status"] = "PUBLISHED"
            notice["published_at"] = datetime.utcnow()
            return APIResponse(data=notice)
    
    raise HTTPException(status_code=404, detail="Notice not found.")
