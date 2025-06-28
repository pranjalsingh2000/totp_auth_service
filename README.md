# 🔐 TOTP Authentication Service

A secure, modular FastAPI service for generating and verifying **Time-Based One-Time Passwords (TOTP)** — suitable for MFA integrations.

---

## 📦 Features

- ✅ User registration with QR code and provisioning URI
- ✅ OTP verification (TOTP RFC 6238)
- 🔐 AES-encrypted secrets
- 📜 Audit logging
- ⚙️ Modular design (routes, services, repo)
- 🔑 API key authentication (JWT planned)
- 🧪 Swagger docs enabled

---

## 🚀 Quickstart

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd totp_auth_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure .env
Create a .env file in the project root:
DATABASE_URL=sqlite:///./totp.db
SECRET_KEY=your-32-byte-secret-key
API_KEY=your-static-api-key
SECRET_KEY must be exactly 32 bytes (AES-256)
### 3. Run the App
```bash
uvicorn app.main:app --reload
```
App: `http://localhost:8000`
Docs: `http://localhost:8000/docs`
## 📘 API Endpoints
POST `/totp/register`
Registers a user and returns TOTP provisioning URI + QR code (base64).
Headers:
```X-API-Key: your-static-api-key```
Body:
```bash
{
  "username": "example_user"
}
```
Response:
```bash
{
  "username": "example_user",
  "created_at": "...",
  "verified_once": false,
  "provisioning_uri": "otpauth://totp/...",
  "qr_code_base64": "data:image/png;base64,..."
}
```
POST `/totp/verify`
Verifies the OTP for a registered user.
Headers:
```bash
X-API-Key: your-static-api-key
```
Body:
```bash
{
  "username": "example_user",
  "otp": "123456"
}
```
```bash
Response:
{
  "message": "OTP is valid",
  "username": "example_user",
  "status": "success"
}
```
🧾 Audit Logging
Each action (register, verify) is logged with:
Username
Event type
IP address
Timestamp
Stored in the audit_logs table.
🔐 Authentication
✅ API Key via X-API-Key header
❌ JWT not yet implemented (planned)
🧱 Folder Structure
```bash
app/
├── api/             # Routes
├── models/          # DB & schemas
├── repository/      # DB access layer
├── services/        # Business logic (TOTP, crypto)
├── utils/           # QR gen, decorators, auth
├── config.py
├── db.py
└── main.py
```
📦 Requirements
fastapi
sqlalchemy
pyotp
pycryptodome
qrcode
python-dotenv
pydantic-settings
📜 License
MIT License – Use freely, modify responsibly.