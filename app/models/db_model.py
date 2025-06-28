# app/models/db_model.py
from sqlalchemy import Column, String, DateTime, Boolean, Integer
from datetime import datetime
from app.db import Base

class TOTPSecret(Base):
    __tablename__ = "totp_secrets"

    username = Column(String, primary_key=True, index=True)
    encrypted_secret = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    verified_once = Column(Boolean, default=False)
    last_verified_at = Column(DateTime, nullable=True)


# app/models/db_model.py

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    event_type = Column(String)  # "register" | "verify"
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, nullable=True)  # optional
    device_id = Column(String, nullable=True)   # optional
