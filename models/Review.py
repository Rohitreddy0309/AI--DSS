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
class CommentSource(enum.Enum):
    AI = "AI"
    ENGINEER = "ENGINEER"
    IMPORTED = "IMPORTED"


class RiskTier(enum.Enum):
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"


class EngineerAction(enum.Enum):
    ACCEPT = "ACCEPT"
    MODIFY = "MODIFY"
    REJECT = "REJECT"


class CommentStatus(enum.Enum):
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class Comments(Base):
    __tablename__ = "comments"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    deliverable_id = Column(UUID(as_uuid=True),ForeignKey("deliverables.id"),nullable=False,index=True)
    comment_number = Column(SmallInteger,nullable=False)
    source = Column(Enum(CommentSource, name="comment_source_enum"),nullable=False,index=True)
    location_reference = Column(String(300),nullable=False)
    comment_text = Column( Text, nullable=False)
    risk_tier = Column(Enum(RiskTier, name="risk_tier_enum"),nullable=False,index=True)
    standard_reference = Column( String(300), nullable=True)
    sop_reference = Column(String(200),nullable=True)
    historical_comment_id = Column(UUID(as_uuid=True),ForeignKey("comments.id"),nullable=True)
    ai_confidence_score = Column(Numeric(4, 3),nullable=True)
    is_low_confidence = Column( Boolean, nullable=False, default=False)
    engineer_action = Column(Enum(EngineerAction, name="engineer_action_enum"),nullable=True,index=True)
    engineer_note = Column(Text,nullable=True )
    engineer_modified_text = Column(Text,nullable=True)
    engineer_modified_risk = Column(Enum(RiskTier, name="engineer_modified_risk_enum"),nullable=True)
    reviewed_by = Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=True)
    reviewed_at = Column(DateTime(timezone=True),nullable=True)
    status = Column(Enum(CommentStatus, name="comment_status_enum"),nullable=False,index=True)
    carried_forward_from_id = Column( UUID(as_uuid=True), ForeignKey("comments.id"), nullable=True)
    created_at = Column( DateTime(timezone=True),nullable=False,server_default=func.now())
       # RELATIONSHIPS
    deliverable = relationship("Deliverables", back_populates="comments")
    reviewer = relationship("Users",foreign_keys=[reviewed_by],backref="reviewed_comments")
    historical_comment = relationship("Comments",remote_side=[id],foreign_keys=[historical_comment_id])
    carried_forward = relationship( "Comments",remote_side=[id],foreign_keys=[carried_forward_from_id])


