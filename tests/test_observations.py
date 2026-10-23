"""Tests for observation schemas, the service layer, and the HTTP endpoint."""

from datetime import UTC, datetime, timedelta, timezone

from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import app
from app.repositories.observation_repository import SyntheticObservationRepository
from app.schemas.observation import Observation, ObservationFilter
from app.services import observation_service

client = TestClient(app)


# --- HTTP endpoint ---


def test_list_returns_synthetic_demo_data() -> None:
    response = client.get("/api/v1/observations")

    assert response.status_code == 200
    body = response.json()
    assert body["data_provenance"] == "synthetic_demo"
    assert body["count"] == len(body["data"])
    assert body["count"] == body["total_matching"]
    assert body["total_matching"] > 0


def test_filter_by_sensor() -> None:
    response = client.get("/api/v1/observations", params={"sensor": "VIIRS"})

    assert response.status_code == 200
    body = response.json()
    assert body["total_matching"] > 0
    assert {observation["sensor"] for observation in body["data"]} == {"VIIRS"}


def test_filter_sensor_with_no_matches_returns_empty_list() -> None:
    repository = SyntheticObservationRepository()
    empty_subset = [o for o in repository.list_observations() if o.sensor == "MODIS"][:0]

    collection = observation_service.query_observations(
        empty_subset,
        ObservationFilter(sensor="MODIS", limit=10),
        repository.data_provenance,
    )

    assert collection.data == []
    assert collection.count == 0
    assert collection.total_matching == 0


def test_limit_truncates_result() -> None:
    response = client.get("/api/v1/observations", params={"limit": 2})

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert body["total_matching"] > body["count"]
    assert len(body["data"]) == 2


def test_zero_and_negative_limit_rejected() -> None:
    for invalid_limit in (0, -1):
        response = client.get("/api/v1/observations", params={"limit": invalid_limit})
        assert response.status_code == 422


def test_oversized_limit_rejected() -> None:
    response = client.get("/api/v1/observations", params={"limit": 1001})

    assert response.status_code == 422


def test_unknown_sensor_rejected() -> None:
    response = client.get("/api/v1/observations", params={"sensor": "NOAA"})

    assert response.status_code == 422


def test_non_integer_limit_rejected() -> None:
    response = client.get("/api/v1/observations", params={"limit": "many"})

    assert response.status_code == 422


# --- Schema validation ---


def make_observation(
    latitude: float = 5.0,
    longitude: float = -70.0,
    acquired_at: datetime | None = None,
    frp_mw: float | None = 10.0,
) -> Observation:
    """Return a valid baseline observation for validation boundary tests."""
    return Observation(
        observation_id="SYN-TEST-0001",
        sensor="MODIS",
        latitude=latitude,
        longitude=longitude,
        acquired_at=acquired_at or datetime(2026, 10, 5, 13, 30, tzinfo=UTC),
        frp_mw=frp_mw,
        confidence_raw=80,
        source="synthetic_demo",
    )


def test_latitude_out_of_range_rejected() -> None:
    for invalid_latitude in (-90.1, 90.1):
        try:
            make_observation(latitude=invalid_latitude)
        except ValidationError as error:
            assert "latitude" in str(error)
        else:
            raise AssertionError(f"{invalid_latitude} should have been rejected")


def test_longitude_out_of_range_rejected() -> None:
    for invalid_longitude in (-180.1, 180.1):
        try:
            make_observation(longitude=invalid_longitude)
        except ValidationError as error:
            assert "longitude" in str(error)
        else:
            raise AssertionError(f"{invalid_longitude} should have been rejected")


def test_naive_acquired_at_rejected() -> None:
    naive = datetime(2026, 10, 5, 13, 30)

    try:
        make_observation(acquired_at=naive)
    except ValidationError as error:
        assert "acquired_at" in str(error)
    else:
        raise AssertionError("timezone-less acquired_at should have been rejected")


def test_offset_aware_acquired_at_normalized_to_utc() -> None:
    offset_aware = datetime(2026, 10, 5, 10, 30, tzinfo=timezone(timedelta(hours=-5)))

    observation = make_observation(acquired_at=offset_aware)

    assert observation.acquired_at.utcoffset() == UTC.utcoffset(None)
    assert observation.acquired_at.hour == 15


def test_negative_frp_mw_rejected() -> None:
    try:
        make_observation(frp_mw=-1.0)
    except ValidationError as error:
        assert "frp_mw" in str(error)
    else:
        raise AssertionError("negative frp_mw should have been rejected")
