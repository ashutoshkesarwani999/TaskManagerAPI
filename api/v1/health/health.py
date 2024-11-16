from fastapi import APIRouter, Depends, Body


health_router = APIRouter()

@health_router.get("/",
                   summary="Health Check",
                   description="Health Check",
                   status_code=200)
async def health_check():
    return {
        "status": "healthy" 
    }