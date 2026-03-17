
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

class TransmittalPurpose(enum.Enum):
    SUBMISSION = "SUBMISSION"
    REVIEW = "REVIEW"
    APPROVAL = "APPROVAL"
    INFORMATION = "INFORMATION"


class TransmittalStatus(enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"
    
class Transmittals(Base):

    __tablename__ = "transmittals"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    trn = Column(String(50),nullable=False,unique=True)
    project_id = Column(UUID(as_uuid=True),ForeignKey("projects.id"),nullable=False,index=True)
    contractor_company_id = Column(UUID(as_uuid=True),ForeignKey("contractor_companies.id"),nullable=False,index=True)
    submitted_by = Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    submitted_at = Column( DateTime(timezone=True), nullable=False, index=True)
    purpose = Column(Enum(TransmittalPurpose, name="transmittal_purpose_enum"),nullable=False)
    document_count = Column(SmallInteger,nullable=False)
    status = Column( Enum(TransmittalStatus, name="transmittal_status_enum"), nullable=False,index=True)
    doc_ctrl_assigned_at = Column(DateTime(timezone=True),nullable=True)
    doc_ctrl_id = Column( UUID(as_uuid=True),ForeignKey("users.id"),nullable=True)
    official_response_issued_at = Column(DateTime(timezone=True),nullable=True)
    created_at = Column( DateTime(timezone=True), nullable=False, server_default=func.now())
    # RELATIONSHIPS
    project = relationship("Project")
    contractor_company = relationship("ContractorCompany")
    submitted_user = relationship("User",foreign_keys=[submitted_by])
    doc_controller = relationship("User",foreign_keys=[doc_ctrl_id])
