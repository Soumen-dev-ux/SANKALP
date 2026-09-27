from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func

from app.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(100), nullable=True)
    ip_address = Column(String(100), nullable=True)
    user_agent = Column(String(500), nullable=True)
    meta_data = Column("metadata", JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
