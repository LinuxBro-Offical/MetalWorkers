from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from sqlmodel import Session
from db import engine
from .models import SiteVisitor


class SiteVisitorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith("/static") and not request.url.path.startswith("/favicon.ico"):
            with Session(engine) as session:
                visitor = SiteVisitor(
                    ip_address=request.client.host,
                    user_agent=request.headers.get("user-agent"),
                )
                session.add(visitor)
                session.commit()
        response = await call_next(request)
        return response 