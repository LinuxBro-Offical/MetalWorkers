from .router import router


@router.get("/profile")
async def get_profile():
    return {"user": {"id": 1, "name": "Jane Doe"}}


@router.post("/login")
async def login():
    return {"message": "Logged in"} 