from .router import router


@router.get("/home")
async def home():
    return {"page": "home", "content": "Welcome to Metal Workers"}


@router.get("/about")
async def about():
    return {"page": "about", "content": "About Metal Workers"}
