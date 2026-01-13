from fastapi import APIRouter

from app.api.v1.routes import health, projects

router = APIRouter(prefix="/v1")
router.include_router(health.router)
router.include_router(projects.router)
