"""HTTP routes for observation queries.

Routes stay thin: validate request parameters and delegate to the
service layer. Scientific interpretation of observations must not live
here.
"""

from typing import Annotated

from fastapi import APIRouter, Query

from app.repositories.observation_repository import (
    ObservationRepository,
    SyntheticObservationRepository,
)
from app.schemas.observation import (
    DEFAULT_LIMIT,
    MAX_LIMIT,
    ObservationCollection,
    ObservationFilter,
    Sensor,
)
from app.services import observation_service

router = APIRouter(prefix="/api/v1", tags=["observations"])

repository: ObservationRepository = SyntheticObservationRepository()


@router.get(
    "/observations",
    summary="List demo observations with optional sensor filter.",
    response_model=ObservationCollection,
)
def get_observations(
    sensor: Annotated[
        Sensor | None, Query(description="Filter observations by source sensor.")
    ] = None,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=MAX_LIMIT,
            description="Maximum number of records returned (v0.1: truncation, no pagination).",
        ),
    ] = DEFAULT_LIMIT,
) -> ObservationCollection:
    """Return observations matching the requested filter."""
    query = ObservationFilter(sensor=sensor, limit=limit)
    return observation_service.query_observations(
        repository.list_observations(),
        query,
        repository.data_provenance,
    )
