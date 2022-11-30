from fastapi import APIRouter
from src.routes.employee import router as employee
from src.routes.organisation import router as organisation


router = APIRouter()

router.include_router(employee)
router.include_router(organisation)

