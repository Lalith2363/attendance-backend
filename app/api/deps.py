from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM
from datetime import datetime

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 🔐 Get current user from JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # ✅ Validate expiration properly
        exp = payload.get("exp")
        if not exp:
            raise HTTPException(status_code=401, detail="Token missing expiration")

        if datetime.utcnow().timestamp() > exp:
            raise HTTPException(status_code=401, detail="Token expired")

        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# 🔐 Admin-only access
def require_admin(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# 🔐 Employee (or admin) access
def require_employee(user=Depends(get_current_user)):
    if user.get("role") not in ["employee", "admin"]:
        raise HTTPException(status_code=403, detail="Employee access required")
    return user