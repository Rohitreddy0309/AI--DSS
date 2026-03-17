from sqlalchemy import Boolean, Column, DateTime, Integer, String,Text
from sqlalchemy.sql import func

from core.database import Base

class Vendors(Base):
    __tablename__ = "sample_adss"

    file_id = Column(Integer, primary_key=True, index=True, autoincrement=True)    
    vendor_name = Column(String)
    created_date = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    File_name = Column(String, nullable=True)
    comments = Column(Text)