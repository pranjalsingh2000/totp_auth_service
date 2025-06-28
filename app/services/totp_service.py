import pyotp

def generate_secret() -> str:
    return pyotp.random_base32()

def get_provisioning_uri(username: str, secret: str, issuer: str = "TOTPAuthApp") -> str:
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer)

def verify_otp(secret: str, token: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
