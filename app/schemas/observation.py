"""Pydantic models for the observation contract.

These models implement the preliminary contract from PROJECT_CONTEXT.md.
The final schema must still be verified against real MODIS/VIIRS product
files once the Data/Geospatial team delivers samples (ROADMAP.md, F3/HU-001).
"""

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

Sensor = Literal["MODIS", "VIIRS"]

DataProvenance = Literal["synthetic_demo"]

DEFAULT_LIMIT: int = 100
MAX_LIMIT: int = 1000


class Observation(BaseModel):
    """Normalized hot-spot observation from a single satellite sensor pass."""

    observation_id: str = Field(min_length=1)
    sensor: Sensor
    latitude: float = Field(ge=-90.0, le=90.0, description="Decimal degrees.")
    longitude: float = Field(ge=-180.0, le=180.0, description="Decimal degrees.")
    acquired_at: datetime = Field(description="Acquisition instant with explicit timezone.")
    frp_mw: float | None = Field(
        default=None,
        ge=0.0,
        description="Fire radiative power in MW; None when the source product does not provide it.",
    )
    confidence_raw: int | str = Field(
        description=(
            "Original confidence value or category of the source product, preserved "
            "without reinterpretation (MODIS: 0-100; VIIRS: l/n/h letter)."
        ),
    )
    source: str = Field(
        min_length=1,
        description="Source product or provenance of the record.",
    )

    @field_validator("acquired_at")
    @classmethod
    def require_explicit_timezone_and_utc(cls, value: datetime) -> datetime:
        """Reject timezone-less values and normalize explicit offsets to UTC."""
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("acquired_at must include an explicit timezone")
        return value.astimezone(UTC)


class ObservationFilter(BaseModel):
    """Query parameters accepted by the observations endpoint."""

    sensor: Sensor | None = None
    limit: int = Field(default=DEFAULT_LIMIT, ge=1, le=MAX_LIMIT)


class ObservationCollection(BaseModel):
    """Paginated response envelope for observation queries."""

    data: list[Observation]
    count: int = Field(ge=0, description="Number of records returned after applying the limit.")
    total_matching: int = Field(
        description="Total records matching the filter before applying the limit.",
    )
    data_provenance: DataProvenance
