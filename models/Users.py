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
class UserRole(enum.Enum):
    SYS_ADMIN = "SYS_ADMIN"
    DOC_CTRL = "DOC_CTRL"
    LEAD_ENG = "LEAD_ENG"
    PROJ_MGR = "PROJ_MGR"
    CONTRACTOR = "CONTRACTOR"
    AUDITOR = "AUDITOR"

class Discipline(enum.Enum):
    MECHANICAL = "MECHANICAL"
    INSTRUMENTATION = "INSTRUMENTATION"
    ELECTRICAL = "ELECTRICAL"
    CIVIL = "CIVIL"
    MULTI = "MULTI"
class Users(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    email = Column(String(255),nullable=False,unique=True)
    full_name = Column(String(200),nullable=False)
    role = Column(Enum(UserRole, name="user_role_enum"),nullable=False,index=True)
    discipline = Column(Enum(Discipline, name="discipline_enum"),nullable=True,index=True)
    azure_oid = Column(String(100),nullable=True,unique=True)
    password_hash = Column(String(255),nullable=True)
    contractor_company_id = Column(UUID(as_uuid=True),ForeignKey("contractor_companies.id"), nullable=True)
    is_active = Column(Boolean,nullable=False,default=True,index=True)
    last_login_at = Column(DateTime(timezone=True),nullable=True)
    created_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now(),onupdate=func.now())    
    # RELATIONSHIPS
    contractor_company = relationship(
        "ContractorCompany",
        back_populates="users"
    )
