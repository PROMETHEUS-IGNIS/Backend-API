"""Data access for observations, isolated from HTTP routes and services.

The concrete repository for the MVP is backed by in-memory synthetic
records that are clearly labeled as demonstration data. Real data
ingestion (ROADMAP.md, F3/HU-008) must be added behind the same
interface without rewriting routes or services.
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Protocol

from app.schemas.observation import DataProvenance, Observation


class ObservationRepository(Protocol):
    """Interface that any data source must satisfy."""

    data_provenance: DataProvenance

    def list_observations(self) -> Sequence[Observation]:
        """Return all available observations; filtering is done by the service."""
        ...


class SyntheticObservationRepository:
    """Demo repository with a small fixed set of synthetic records.

    Every record in the returned data is SYNTHETIC and demonstrative; it
    must never be presented as a real NASA observation.
    """

    data_provenance: DataProvenance = "synthetic_demo"

    def __init__(self) -> None:
        self._observations: tuple[Observation, ...] = _build_synthetic_observations()

    def list_observations(self) -> Sequence[Observation]:
        return self._observations


def _build_synthetic_observations() -> tuple[Observation, ...]:
    """Build the fixed synthetic demo dataset (Colombian region as showcase)."""
    return (
        Observation(
            observation_id="SYN-MOD-0001",
            sensor="MODIS",
            latitude=5.8412,
            longitude=-68.5031,
            acquired_at=datetime(2026, 10, 5, 13, 30, tzinfo=UTC),
            frp_mw=42.1,
            confidence_raw=80,
            source="synthetic_demo",
        ),
        Observation(
            observation_id="SYN-MOD-0002",
            sensor="MODIS",
            latitude=4.5120,
            longitude=-69.9102,
            acquired_at=datetime(2026, 10, 6, 10, 30, tzinfo=UTC),
            frp_mw=11.4,
            confidence_raw=65,
            source="synthetic_demo",
        ),
        Observation(
            observation_id="SYN-MOD-0003",
            sensor="MODIS",
            latitude=2.9330,
            longitude=-73.4117,
            acquired_at=datetime(2026, 10, 8, 22, 30, tzinfo=UTC),
            frp_mw=None,
            confidence_raw=91,
            source="synthetic_demo",
        ),
        Observation(
            observation_id="SYN-MOD-0004",
            sensor="MODIS",
            latitude=6.1050,
            longitude=-71.7880,
            acquired_at=datetime(2026, 10, 9, 13, 25, tzinfo=UTC),
            frp_mw=7.8,
            confidence_raw=50,
            source="synthetic_demo",
        ),
        Observation(
            observation_id="SYN-VIR-0001",
            sensor="VIIRS",
            latitude=5.9021,
            longitude=-68.6110,
            acquired_at=datetime(2026, 10, 5, 13, 45, tzinfo=UTC),
            frp_mw=30.2,
            confidence_raw="h",
            source="synthetic_demo",
        ),
        Observation(
            observation_id="SYN-VIR-0002",
            sensor="VIIRS",
            latitude=4.3210,
            longitude=-70.2255,
            acquired_at=datetime(2026, 10, 7, 13, 45, tzinfo=UTC),
            frp_mw=None,
            confidence_raw="n",
            source="synthetic_demo",
        ),
        Observation(
            observation_id="SYN-VIR-0003",
            sensor="VIIRS",
            latitude=6.7801,
            longitude=-70.8942,
            acquired_at=datetime(2026, 10, 9, 13, 48, tzinfo=UTC),
            frp_mw=4.6,
            confidence_raw="l",
            source="synthetic_demo",
        ),
        Observation(
            observation_id="SYN-VIR-0004",
            sensor="VIIRS",
            latitude=3.4102,
            longitude=-72.2071,
            acquired_at=datetime(2026, 10, 10, 13, 50, tzinfo=UTC),
            frp_mw=18.9,
            confidence_raw="h",
            source="synthetic_demo",
        ),
    )
