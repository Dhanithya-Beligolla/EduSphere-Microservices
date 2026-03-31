from fastapi import APIRouter, HTTPException
from communication_models.communication_schemas import AlertCreate, APIResponse
from communication_data.communication_mock_data import ALERTS
from datetime import datetime
import uuid

router = APIRouter(prefix="", tags=["Alerts"])

@router.post("/alerts", response_model=APIResponse)
async def create_alert(alert: AlertCreate):
    """
    Create an alert (manual or automated).
    """
    new_alert = {
        "id": f"A_{str(uuid.uuid4())[:8]}",
        "user_id": alert.user_id,
        "type": alert.type,
        "title": alert.title,
        "message": alert.message,
        "priority": alert.priority,
        "is_read": False,
        "created_at": datetime.utcnow()
    }
    ALERTS.append(new_alert)
    return APIResponse(data=new_alert)

@router.get("/users/{userId}/alerts", response_model=APIResponse)
async def get_user_alerts(userId: str):
    """
    Get alerts for a specific user.
    """
    filtered = [a for a in ALERTS if a["user_id"] == userId]
    # Sort by created_at descending
    filtered.sort(key=lambda x: x["created_at"], reverse=True)
    return APIResponse(data=filtered)

# --- Simulation of Event-Driven Alerts ---

@router.post("/simulate/event/{event_name}", include_in_schema=False)
async def simulate_event(event_name: str, user_id: str):
    """
    Hidden endpoint to simulate event-based alert triggers.
    Events: assessment.assignment.published, assessment.submission.missed, assessment.result.published
    """
    event_map = {
        "assessment.assignment.published": {
            "title": "New Assignment",
            "message": "A new assignment has been posted for your class.",
            "priority": "MEDIUM",
            "type": "ASSIGNMENT"
        },
        "assessment.submission.missed": {
            "title": "Assignment Overdue!",
            "message": "You have missed a submission deadline.",
            "priority": "HIGH",
            "type": "ASSIGNMENT"
        },
        "assessment.result.published": {
            "title": "Results Out",
            "message": "The results for your recent assessment are now available.",
            "priority": "MEDIUM",
            "type": "RESULT"
        }
    }
    
    if event_name not in event_map:
        raise HTTPException(status_code=400, detail="Unknown event type.")
    
    event_data = event_map[event_name]
    new_alert = {
        "id": f"A_{str(uuid.uuid4())[:8]}",
        "user_id": user_id,
        "type": event_data["type"],
        "title": event_data["title"],
        "message": event_data["message"],
        "priority": event_data["priority"],
        "is_read": False,
        "created_at": datetime.utcnow()
    }
    ALERTS.append(new_alert)
    return APIResponse(data={"event": event_name, "alert_created": new_alert})
