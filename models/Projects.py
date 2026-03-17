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
class ProjectSector(enum.Enum):
    OIL_GAS = "OIL_GAS"
    ENERGY = "ENERGY"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    MANUFACTURING = "MANUFACTURING"
    OTHER = "OTHER"


class ProjectStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Project(Base):
    __tablename__ = "projects"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    project_code = Column(String(50),nullable=False,unique=True)
    project_name = Column( String(300), nullable=False)
    client_name = Column(String(200),nullable=False)
    sector = Column(Enum(ProjectSector, name="project_sector_enum"),nullable=False,index=True)
    project_manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    doc_numbering_pattern = Column(String(200),nullable=False)
    review_sla_days_internal = Column(SmallInteger,nullable=False)
    review_sla_days_external = Column(SmallInteger,nullable=False)
    status = Column(Enum(ProjectStatus, name="project_status_enum"),nullable=False,index=True)
    start_date = Column(Date,nullable=False)
    end_date = Column(Date, nullable=True)
    created_by = Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    created_at = Column( DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now(),onupdate=func.now())
    
    # RELATIONSHIPS
    project_manager = relationship("User",foreign_keys=[project_manager_id])
    creator = relationship("User",foreign_keys=[created_by])
