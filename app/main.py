from fastapi import FastAPI
from app.api.routes import router
from app.db import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TOTP Auth Service",
    description="A secure, time-based OTP authentication API",
    version="1.0.0"
)

# Register routes
app.include_router(router, prefix="/totp")
