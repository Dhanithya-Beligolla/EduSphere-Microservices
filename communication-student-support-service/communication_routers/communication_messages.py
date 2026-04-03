from fastapi import APIRouter, HTTPException
from communication_models.communication_schemas import MessageCreate, APIResponse
from communication_data.communication_mock_data import MESSAGES
from datetime import datetime
import uuid

router = APIRouter(prefix="", tags=["Messages"])

@router.post("/messages", response_model=APIResponse)
async def send_message(msg: MessageCreate):
    """
    Send a message.
    """
    # Simulate conversation logic
    conv_id = msg.conversation_id or f"CONV_{str(uuid.uuid4())[:8]}"
    
    new_msg = {
        "id": f"M_{str(uuid.uuid4())[:8]}",
        "sender_id": msg.sender_id,
        "receiver_id": msg.receiver_id,
        "content": msg.content,
        "timestamp": datetime.utcnow(),
        "conversation_id": conv_id
    }
    MESSAGES.append(new_msg)
    return APIResponse(data=new_msg)

@router.get("/conversations/{conversationId}/messages", response_model=APIResponse)
async def get_conversation_messages(conversationId: str):
    """
    Get messages for a specific conversation.
    """
    filtered = [m for m in MESSAGES if m["conversation_id"] == conversationId]
    if not filtered:
         raise HTTPException(status_code=404, detail="Conversation not found or empty.")
    
    # Sort by timestamp
    filtered.sort(key=lambda x: x["timestamp"])
    return APIResponse(data=filtered)
