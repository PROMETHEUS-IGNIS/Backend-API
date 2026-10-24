"""Pydantic models for the health endpoint contract."""

from typing import Literal

from pydantic import BaseModel


class HealthStatus(BaseModel):
    """Stable health response body documented in docs/api-contracts.md."""

    status: Literal["ok"]
    api_version: str
