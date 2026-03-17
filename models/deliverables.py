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

class DocumentDiscipline(enum.Enum):
    MECHANICAL = "MECHANICAL"
    INSTRUMENTATION = "INSTRUMENTATION"
    ELECTRICAL = "ELECTRICAL"
    CIVIL = "CIVIL"
    MULTI = "MULTI"


class DeliverableType(enum.Enum):
    DRAWING = "DRAWING"
    SPECIFICATION = "SPECIFICATION"
    REPORT = "REPORT"
    CALCULATION = "CALCULATION"
    OTHER = "OTHER"


class ReviewStatus(enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_REVIEW = "IN_REVIEW"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class AIVerdict(enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"


class FinalVerdict(enum.Enum):
    APPROVED = "APPROVED"
    APPROVED_WITH_COMMENTS = "APPROVED_WITH_COMMENTS"
    REJECTED = "REJECTED"

class Deliverables(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    document_number = Column(String(150),nullable=False,index=True)
    revision = Column( String(20), nullable=False)
    title = Column(String(500),nullable=False)
    discipline = Column(Enum(DocumentDiscipline, name="document_discipline_enum"), nullable=False, index=True)
    deliverable_type = Column(Enum(DeliverableType, name="deliverable_type_enum"),nullable=False, index=True)
    transmittal_id = Column( UUID(as_uuid=True), ForeignKey("transmittals.id"), nullable=False, index=True)
    project_id = Column( UUID(as_uuid=True),ForeignKey("projects.id"),nullable=False,index=True)
    assigned_engineer_id = Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=True,index=True)
    previous_revision_id = Column( UUID(as_uuid=True), ForeignKey("documents.id"),nullable=True)
    file_name = Column(String(300), nullable=False)
    blob_url = Column(Text,nullable=False)
    file_size_bytes = Column( BigInteger,nullable=False)
    sha256_hash = Column( String(64),nullable=False )
    parsed_content_ref = Column(String(300),nullable=True)
    review_status = Column(Enum(ReviewStatus, name="review_status_enum"), nullable=False, index=True)
    ai_verdict = Column(Enum(AIVerdict, name="ai_verdict_enum"), nullable=True)
    final_verdict = Column(Enum(FinalVerdict, name="final_verdict_enum"),nullable=True,index=True )
    ai_comment_count = Column(SmallInteger, nullable=True)
    critical_count = Column(SmallInteger, nullable=True)
    major_count = Column(SmallInteger,nullable=True)
    minor_count = Column(SmallInteger,nullable=True)
    ai_processing_started_at = Column( DateTime(timezone=True), nullable=True)
    ai_processing_completed_at = Column(DateTime(timezone=True),nullable=True)
    engineer_review_started_at = Column( DateTime(timezone=True), nullable=True)
    engineer_review_submitted_at = Column(DateTime(timezone=True),nullable=True )
    pm_approved_at = Column( DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at = Column( DateTime(timezone=True), nullable=False,server_default=func.now(),onupdate=func.now())
    # RELATIONSHIPS
    transmittal = relationship("Transmittal")
    project = relationship("Project")
    assigned_engineer = relationship("User",foreign_keys=[assigned_engineer_id])
    previous_revision = relationship("Document",remote_side=[id])

