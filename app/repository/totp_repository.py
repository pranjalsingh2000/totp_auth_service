# app/repository/totp_repository.py

from sqlalchemy.orm import Session
from app.models.db_model import AuditLog, TOTPSecret
from datetime import datetime

def save_totp_secret(db: Session, username: str, encrypted_secret: str):
    db_entry = TOTPSecret(
        username=username,
        encrypted_secret=encrypted_secret,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        verified_once=False
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_totp_secret(db: Session, username: str):
    return db.query(TOTPSecret).filter(TOTPSecret.username == username).first()

def mark_verified(db: Session, username: str):
    entry = db.query(TOTPSecret).filter(TOTPSecret.username == username).first()
    if entry:
        entry.verified_once = True
        entry.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(entry)
    return entry

def log_event(db: Session, username: str, event_type: str, ip: str = None, device_id: str = None):
    event = AuditLog(
        username=username,
        event_type=event_type,
        ip_address=ip,
        device_id=device_id,
        timestamp=datetime.utcnow()
    )
    db.add(event)
    db.commit()