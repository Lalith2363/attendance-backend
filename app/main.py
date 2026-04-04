from fastapi import FastAPI
from app.api.routes import employee, attendance, auth
from app.db.database import Base, engine
from fastapi import Depends
from app.api.deps import oauth2_scheme
from app.middleware.security import SecurityMiddleware
from app.api.routes import department,designation,leave
from app.api.routes import report
from app.models.employee import Employee
from app.models.department import Department
from app.models.designation import Designation
from app.models.attendance import Attendance
from app.models.leave import Leave
from app.models.user import User
from app.models.shift import Shift
from app.api.routes import payroll
from app.api.routes import auth


app = FastAPI()

Base.metadata.create_all(bind=engine)

# include routers
app.include_router(employee.router)
app.include_router(attendance.router)
app.include_router(auth.router)
app.add_middleware(SecurityMiddleware)
app.include_router(department.router)
app.include_router(designation.router)
app.include_router(leave.router)
app.include_router(report.router)
app.include_router(payroll.router)
app.include_router(auth.router)


@app.get("/test-auth")
def test_auth(token: str = Depends(oauth2_scheme)):
    return {"token": token}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)