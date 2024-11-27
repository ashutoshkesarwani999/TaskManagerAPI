from fastapi import APIRouter

user_router = APIRouter()


#
@user_router.post("/users/create")
async def create_user():
    return {"message": "User created"}