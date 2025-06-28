import logging
from app.api.routes import router
from fastapi import FastAPI, Request
from app.utils.logging import setup_logging

setup_logging()
logger = logging.getLogger("totp_app")

app = FastAPI(
    title="TOTP Auth Service",
    description="A secure, time-based OTP authentication API",
    version="1.0.0"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url} from {request.client.host}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code} for {request.method} {request.url}")
    return response

# Register routes
app.include_router(router, prefix="/totp")
