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
class Discipline(enum.Enum):
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


class RiskTier(enum.Enum):
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
class HistoricalComments(Base):
    __tablename__= "historical_comments"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    comment_text = Column(Text,nullable=False)
    discipline = Column(Enum(Discipline, name="kb_discipline_enum"),nullable=False,index=True)
    deliverable_type = Column(Enum(DeliverableType, name="kb_deliverable_type_enum"),nullable=False,index=True)
    equipment_type_tags = Column(JSONB,nullable=False)
    comment_category = Column(String(100),nullable=False,index=True)
    risk_tier = Column(Enum(RiskTier, name="kb_risk_tier_enum"),nullable=False,index=True)
    standard_reference = Column(String(300),nullable=True)
    occurrence_count = Column(Integer,nullable=False,default=1)
    acceptance_rate = Column(Numeric(5, 2),  nullable=False)
    source_project_count = Column(Integer,nullable=False)
    is_verified_best_practice = Column(Boolean,nullable=False,default=False)
    embedding_ref = Column(String(300),nullable=True)
    created_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now(),onupdate=func.now())

