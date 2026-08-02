from fastapi import APIRouter
from backend.api.endpoints import router as api_router

router = APIRouter()
router.include_router(api_router)
