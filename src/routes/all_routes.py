from fastapi import APIRouter
from src.routes.employee import router as employee

router = APIRouter()

router.include_router(employee)
