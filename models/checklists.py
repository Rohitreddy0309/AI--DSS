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
        deliverable_id = Column(UUID(as_uuid=True),ForeignKey("documents.id"),nullable=False,index=True)
        checklist_id = Column(UUID(as_uuid=True),ForeignKey("checklists.id"),nullable=False)
        checklist_item_id = Column(UUID(as_uuid=True),ForeignKey("checklists.id"),nullable=False)
        ai_result = Column(Enum(AIResult, name="ai_result_enum"),nullable=False)
        ai_evidence = Column(Text,nullable=True)
        engineer_override = Column(Enum(EngineerOverride, name="engineer_override_enum"),nullable=True)
        override_justification = Column(Text,nullable=True)
        overridden_by = Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=True)
        created_at = Column(DateTime(timezone=True), nullable=False,server_default=func.now())
        
    # RELATIONSHIPS
        document = relationship("Document")
        checklist = relationship("Checklist")
        checklist_item = relationship("ChecklistItem")
        overridden_user = relationship("User",foreign_keys=[overridden_by])
        
