from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from accounts import router as accounts_router
from pages import router as pages_router
from newsletter import router as newsletter_router
from site_visitor import SiteVisitorMiddleware
from settings import settings
from sqlmodel import SQLModel
from db import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    debug=settings.DEBUG,
)

app.add_middleware(SiteVisitorMiddleware)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Mount static files
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# Templates
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

app.include_router(accounts_router)
app.include_router(pages_router)
app.include_router(newsletter_router)
 