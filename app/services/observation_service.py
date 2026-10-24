"""Application logic for observation queries, independent of FastAPI."""

from collections.abc import Sequence

from app.schemas.observation import (
    DataProvenance,
    Observation,
    ObservationCollection,
    ObservationFilter,
)


def query_observations(
    observations: Sequence[Observation],
    query: ObservationFilter,
    data_provenance: DataProvenance,
) -> ObservationCollection:
    """Filter observations and apply the result limit without scientific reinterpretation."""
    matching = [
        observation
        for observation in observations
        if query.sensor is None or observation.sensor == query.sensor
    ]
    selected = matching[: query.limit]
    return ObservationCollection(
        data=selected,
        count=len(selected),
        total_matching=len(matching),
        data_provenance=data_provenance,
    )
