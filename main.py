from fastapi import FastAPI
from accounts import router as accounts_router
from pages import router as pages_router
from settings import settings

app = FastAPI(title=settings.APP_NAME, version="0.1.0", debug=settings.DEBUG)

app.include_router(accounts_router)
app.include_router(pages_router)
