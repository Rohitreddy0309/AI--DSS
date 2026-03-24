import uuid
import enum
from sqlalchemy import (
    Column,String,Text,
    Boolean,Integer,SmallInteger,
    BigInteger,Date,DateTime,Enum,ForeignKey,Index,
    UniqueConstraint,CheckConstraint,Numeric)
from sqlalchemy.dialects.postgresql import (UUID,JSONB)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base 
class AIResult(enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EngineerOverride(enum.Enum):
    ACCEPT_AI = "ACCEPT_AI"
    OVERRIDE_PASS = "OVERRIDE_PASS"
    OVERRIDE_FAIL = "OVERRIDE_FAIL"
    MARK_NOT_APPLICABLE = "MARK_NOT_APPLICABLE"
class Checklist(Base):
        __tablename__ = "checklists"
        id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
        deliverable_id = Column(UUID(as_uuid=True),ForeignKey("deliverables.id"),nullable=False,index=True)
        checklist_id = Column(UUID(as_uuid=True),ForeignKey("checklists.id"),nullable=True)
        checklist_item_id = Column(UUID(as_uuid=True),ForeignKey("checklist_items.id"),nullable=False)
        ai_result = Column(Enum(AIResult, name="ai_result_enum"),nullable=False)
        ai_evidence = Column(Text,nullable=True)
        engineer_override = Column(Enum(EngineerOverride, name="engineer_override_enum"),nullable=True)
        override_justification = Column(Text,nullable=True)
        overridden_by = Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=True)
        created_at = Column(DateTime(timezone=True), nullable=False,server_default=func.now())
        
    # RELATIONSHIPS
        document = relationship("Deliverables")
        checklist = relationship("Checklist", foreign_keys=[checklist_id], remote_side=[id])
        checklist_item = relationship("ChecklistItem", foreign_keys=[checklist_item_id], back_populates="checklists")
        overridden_user = relationship("Users",foreign_keys=[overridden_by])
        
