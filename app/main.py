from fastapi import FastAPI, Depends

from app.db.database import Base, engine
from app.api.deps import oauth2_scheme
from app.middleware.security import SecurityMiddleware

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

# models (needed for table creation)
from app.models import (
    employee,
    department,
    designation,
    attendance,
    leave,
    user,
    shift
)

app = FastAPI()

# ✅ middleware FIRST
app.add_middleware(SecurityMiddleware)

# ✅ create tables
Base.metadata.create_all(bind=engine)

# ✅ routers (CLEAN)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(employee.router, tags=["Employee"])
app.include_router(attendance.router, tags=["Attendance"])
app.include_router(department.router, tags=["Department"])
app.include_router(designation.router, tags=["Designation"])
app.include_router(leave.router, tags=["Leave"])
app.include_router(report.router, tags=["Reports"])
app.include_router(payroll.router, tags=["Payroll"])


# test route
@app.get("/test-auth")
def test_auth(token: str = Depends(oauth2_scheme)):
    return {"token": token}