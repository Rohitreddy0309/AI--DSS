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
class Companies(Base):
    __tablename__ = "contractor_companies"
    
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    company_name = Column(String(300),nullable=False,unique=True)
    company_code = Column(String(50),nullable=False,unique=True)
    registration_number = Column( String(100),nullable=True)
    primary_contact_email = Column(String(255),nullable=False)
    primary_contact_name = Column(String(200),nullable=True)
    is_active = Column( Boolean,nullable=False,default=True,index=True)
    created_at = Column( DateTime(timezone=True), nullable=False, server_default=func.now())
    # RELATIONSHIPS
    users = relationship(
        "User",
        back_populates="contractor_company",
        cascade="all, delete-orphan"
    )
