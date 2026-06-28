from fastapi import APIRouter

from api.services.health import health_service

router = APIRouter(tags=["health"])


@router.get("/health")
def health_status():
    return health_service()
