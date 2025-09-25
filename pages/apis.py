from .router import router
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from settings import settings

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
 