from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError

from app.core.rate_limit import is_allowed
from app.core.logger import logger
from app.core.security import SECRET_KEY, ALGORITHM


class SecurityMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        ip = request.client.host
        token = None
        user = None

        # Extract token
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user = payload.get("sub")
            except JWTError:
                logger.warning("Invalid token used")

        # Apply multi-layer rate limiting
        allowed, reason = is_allowed(ip, user, token)

        if not allowed:
            logger.warning(f"Blocked request: {ip}, user={user}, reason={reason}")
            return JSONResponse(
                status_code=429,
                content={"detail": reason}
            )

        response = await call_next(request)
        return response