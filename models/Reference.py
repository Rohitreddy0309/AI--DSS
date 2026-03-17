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
class DocumentType(enum.Enum):
    STANDARD = "STANDARD"
    SPECIFICATION = "SPECIFICATION"
    PROCEDURE = "PROCEDURE"
    GUIDELINE = "GUIDELINE"
    CODE = "CODE"


class IngestionStatus(enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
class ReferenceDocument(Base):
    __tablename__ = "reference_documents"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    document_code = Column(String(100),nullable=False,unique=True)
    title = Column( String(500), nullable=False )
    doc_type = Column(Enum(DocumentType, name="ref_doc_type_enum"),nullable=False,index=True)
    discipline_scope = Column(JSONB,nullable=False)
    deliverable_type_scope = Column(JSONB,nullable=False)
    version = Column(String(20),nullable=False)
    effective_date = Column(Date,nullable=False)
    project_id = Column(UUID(as_uuid=True),ForeignKey("projects.id"),nullable=True)
    supersedes_id = Column(UUID(as_uuid=True),ForeignKey("reference_documents.id"),nullable=True)
    blob_url = Column(Text,nullable=False)
    sha256_hash = Column(String(64),nullable=False)
    ai_search_index = Column(String(200),nullable=False)
    chunk_count = Column(Integer,nullable=True)
    ingestion_status = Column( Enum(IngestionStatus, name="ingestion_status_enum"),nullable=False,index=True)
    uploaded_by = Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now())
      # RELATIONSHIPS
    project = relationship("Project")
    uploader = relationship("User",foreign_keys=[uploaded_by] )
    superseded_document = relationship( "ReferenceDocument", remote_side=[id])
