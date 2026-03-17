#cosom db (gpt) -11
""" JSON{
  "id": "uuid",
  "event_time": "2026-03-17T10:30:25Z",
  "event_type": "REVIEW.COMMENT.REJECTED",
  
  "actor": {
    "id": "uuid",
    "role": "LEAD_ENG",
    "ip": "192.168.1.xxx"
  },

  "context": {
    "project_id": "uuid",
    "transmittal_id": "uuid",
    "deliverable_id": "uuid",
    "comment_id": "uuid"
  },

  "action": "Engineer rejected AI-generated comment",

  "before_state": {
    "status": "OPEN",
    "risk_tier": "MAJOR"
  },

  "after_state": {
    "status": "REJECTED",
    "risk_tier": "MINOR"
  },

  "correlation_id": "uuid",
  "is_ai_action": false
}"""
"""
PYDANTIC MODEL
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
class Actor(BaseModel):
    id: UUID
    role: str
    ip: str
class Context(BaseModel):
    project_id: Optional[UUID] = None
    transmittal_id: Optional[UUID] = None
    deliverable_id: Optional[UUID] = None
    comment_id: Optional[UUID] = None

class AuditLog(BaseModel):
    id: UUID
    event_time: datetime
    event_type: str

    actor: Actor
    context: Context

    action: str

    before_state: Optional[Dict[str, Any]] = None
    after_state: Optional[Dict[str, Any]] = None

    correlation_id: UUID
    is_ai_action: bool

    class Config:
        orm_mode = True"""