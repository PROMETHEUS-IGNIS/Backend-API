"""HTTP routes for the health endpoint."""

from fastapi import APIRouter

from app import API_VERSION
from app.schemas.health import HealthStatus

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get(
    "/health",
    summary="Check that the API is running.",
    response_model=HealthStatus,
)
def get_health() -> HealthStatus:
    """Return a stable health status body."""
    return HealthStatus(status="ok", api_version=API_VERSION)
