from pydantic import BaseModel
from datetime import datetime

class TOTPCreate(BaseModel):
    username: str

class TOTPVerify(BaseModel):
    username: str
    otp: str

class TOTPResponse(BaseModel):
    username: str
    created_at: datetime
    verified_once: bool
    provisioning_uri: str
    qr_code_base64: str

    class Config:
        orm_mode = True
