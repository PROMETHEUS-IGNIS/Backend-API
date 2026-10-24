"""FastAPI application for the NASA Fire Harmonization backend."""

from fastapi import FastAPI

from app import API_VERSION
from app.api.routes import health, observations

app = FastAPI(
    title="NASA Fire Harmonization API",
    version=API_VERSION,
    description=(
        "Backend for the NASA Space Apps Challenge 2026 challenge "
        "'Harmonization of MODIS and VIIRS Hot Spots'. "
        "Current data is SYNTHETIC and demonstrative, not real NASA observations."
    ),
)

app.include_router(health.router)
app.include_router(observations.router)
