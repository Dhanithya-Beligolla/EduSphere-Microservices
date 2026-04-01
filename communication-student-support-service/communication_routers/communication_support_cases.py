from fastapi import APIRouter, HTTPException
from communication_models.communication_schemas import SupportCaseCreate, SupportCasePatch, APIResponse
from communication_data.communication_mock_data import SUPPORT_CASES
from datetime import datetime
import uuid

router = APIRouter(prefix="", tags=["Support Cases"])

@router.post("/support-cases", response_model=APIResponse)
async def create_support_case(case: SupportCaseCreate):
    """
    Create a new support or counselling case.
    """
    new_case = {
        "id": f"SC_{str(uuid.uuid4())[:8]}",
        "student_id": case.student_id,
        "subject": case.subject,
        "description": case.description,
        "status": "OPEN",
        "assigned_staff_id": case.assigned_staff_id or "UNASSIGNED",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "notes": None
    }
    SUPPORT_CASES.append(new_case)
    return APIResponse(data=new_case)

@router.get("/support-cases/{caseId}", response_model=APIResponse)
async def get_support_case(caseId: str):
    """
    Retrieve details of a support case.
    Restricted to: Authorized staff only.
    """
    for case in SUPPORT_CASES:
        if case["id"] == caseId:
            return APIResponse(data=case)
    
    raise HTTPException(status_code=404, detail="Support case not found.")

@router.patch("/support-cases/{caseId}", response_model=APIResponse)
async def patch_support_case(caseId: str, update: SupportCasePatch):
    """
    Update a support case (status, notes, or assigned staff).
    """
    for case in SUPPORT_CASES:
        if case["id"] == caseId:
            if update.status:
                case["status"] = update.status
            if update.assigned_staff_id:
                case["assigned_staff_id"] = update.assigned_staff_id
            if update.notes:
                case["notes"] = update.notes
            
            case["updated_at"] = datetime.utcnow()
            return APIResponse(data=case)
    
    raise HTTPException(status_code=404, detail="Support case not found.")
