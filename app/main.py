from fastapi import FastAPI, Depends
import logging

from app.db.database import Base, engine
from app.api.deps import oauth2_scheme

# routers
from app.api.routes import (
    employee,
    attendance,
    auth,
    department,
    designation,
    leave,
    report,
    payroll
)

# import all models (important for SQLAlchemy)
import app.models


# ---------------------------
# Logging setup
# ---------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()


# ---------------------------
# Startup event (SAFE)
# ---------------------------
@app.on_event("startup")
def startup_event():
    logger.info("🚀 App starting...")

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database connected & tables created")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")


# ---------------------------
# Routers
# ---------------------------
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(employee.router, tags=["Employee"])
app.include_router(attendance.router, tags=["Attendance"])
app.include_router(department.router, tags=["Department"])
app.include_router(designation.router, tags=["Designation"])
app.include_router(leave.router, tags=["Leave"])
app.include_router(report.router, tags=["Reports"])
app.include_router(payroll.router, tags=["Payroll"])


# ---------------------------
# Test route
# ---------------------------
@app.get("/test-auth")
def test_auth(token: str = Depends(oauth2_scheme)):
    return {"token": token}


# ---------------------------
# Health check (VERY IMPORTANT for Render)
# ---------------------------
@app.get("/")
def root():
    return {"status": "running"}