from sqlalchemy.orm import Session
from app.utils.auth import verify_api_key
from fastapi import APIRouter, Depends, HTTPException, status, Request

from app.models.schemas import TOTPCreate, TOTPVerify, TOTPResponse
from app.repository import totp_repository
from app.services import crypto_service, totp_service
from app.utils import qr
from app.utils.response import handle_errors
from app.db import get_db

router = APIRouter()

@router.post("/register", dependencies=[Depends(verify_api_key)], response_model=TOTPResponse, status_code=201)
@handle_errors
def register(payload: TOTPCreate, db: Session = Depends(get_db), request: Request = None):
    if totp_repository.get_totp_secret(db, payload.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered"
        )

    secret = totp_service.generate_secret()
    encrypted = crypto_service.encrypt_secret(secret)
    saved = totp_repository.save_totp_secret(db, payload.username, encrypted)
    uri = totp_service.get_provisioning_uri(payload.username, secret)
    qr_code = qr.generate_qr_code_base64(uri)

    totp_repository.log_event(
        db=db,
        username=payload.username,
        event_type="register",
        ip=request.client.host
    )

    return TOTPResponse(
        username=saved.username,
        created_at=saved.created_at,
        verified_once=saved.verified_once,
        provisioning_uri=uri,
        qr_code_base64=qr_code
    )


@router.post("/verify", dependencies=[Depends(verify_api_key)], status_code=200)
@handle_errors
def verify(payload: TOTPVerify, db: Session = Depends(get_db), request: Request = None, dependencies=[Depends(verify_api_key)]):
    entry = totp_repository.get_totp_secret(db, payload.username)
    if not entry:
        raise HTTPException(status_code=404, detail="User not found")

    secret = crypto_service.decrypt_secret(entry.encrypted_secret)
    if not totp_service.verify_otp(secret, payload.otp):
        raise HTTPException(status_code=401, detail="Invalid OTP")

    totp_repository.mark_verified(db, payload.username)

    totp_repository.log_event(
        db=db,
        username=payload.username,
        event_type="verify",
        ip=request.client.host
    )
    
    totp_repository.mark_verified(db, payload.username)

    return {
        "message": "OTP is valid",
        "username": payload.username,
        "status": "success"
    }
