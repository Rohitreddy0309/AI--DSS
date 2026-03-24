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

class Revision(Base):
    __tablename__ = "revision_comparisons"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    current_deliverable_id = Column(UUID(as_uuid=True),ForeignKey("deliverables.id"),nullable=False,index=True)
    prior_deliverable_id = Column(UUID(as_uuid=True),ForeignKey("deliverables.id"),nullable=False)
    diff_json_ref = Column(String(300),nullable=False)
    added_fields_count = Column(SmallInteger,nullable=False)
    deleted_fields_count = Column(SmallInteger,nullable=False)
    modified_fields_count = Column(SmallInteger, nullable=False)
    prior_comments_total = Column(SmallInteger,nullable=False)
    prior_comments_resolved = Column(SmallInteger,nullable=False)
    prior_comments_unresolved = Column(SmallInteger,nullable=False)
    new_issues_introduced = Column(SmallInteger,nullable=False)
    comparison_summary = Column(Text,nullable=True)
    created_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    
    # RELATIONSHIPS
    current_document = relationship("Deliverables",foreign_keys=[current_deliverable_id])
    prior_document = relationship("Deliverables",foreign_keys=[prior_deliverable_id])
