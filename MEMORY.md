# MEMORY.md — NASA Fire Harmonization API
Memoria del proyecto entre sesiones. Máximo ~50 líneas: resume o elimina lo que ya no
aporte.
## Estado actual
- F1 (fundamentos) y F2 (observaciones, HU-006 sin HU-007) completadas: FastAPI
  ejecutable, `GET /api/v1/health` y `GET /api/v1/observations` con datos
  sintéticos etiquetados; 15 pruebas pasando; Ruff configurado y limpio.
- Entorno: Python 3.13.17 con launcher `py`; venv `.venv` creado;
  dependencias fijadas (fastapi 0.161.1, uvicorn 0.54.0, pydantic 2.14.1,
  pytest 9.1.1, httpx 0.28.1, ruff 0.17.2).
- Contratos documentados en `docs/api-contracts.md` (health + observations).
## Decisiones (qué cambió y por qué)
- Python 3.13 en lugar de 3.12: el usuario instaló la última estable y
  `AGENTS.md` fue actualizado para reflejar el entorno real.
- `confidence_raw` es union `int | str` para preservar el valor original
  de cada producto (MODIS 0–100, VIIRS l/n/h) sin reinterpretación.
- `confidence_score` NO existe: esperando método aprobado por Science/
  Data (regla de dominio). No inventar.
- Repositorio sintético (`synthetic_demo`) como clase con `Protocol`
  `ObservationRepository`: la ingesta real (F3) entra por la misma
  interfaz sin tocar rutas ni servicios.
- Normalización a UTC dentro del validador del esquema; fechas sin zona
  horaria se rechazan.
- Filtrado por sensor + `limit` (1–1000) en el servicio; `total_matching`
  expone el truncamiento sin paginación (documentado).
## Aprendizajes y errores a evitar
- Windows necesita el paquete `tzdata` para zonas con nombre en
  `zoneinfo` (ej. America/Bogota); pruebas usan offsets fijos, no añadir
  `tzdata` sin autorización.
- Ruff B008 no distingue `Query()` de FastAPI: usar estilo
  `Annotated[..., Query(...)]` desde el inicio.
- Tests de filtros: usar `total_matching > count` (dataset puede crecer),
  no igualar a constantes.
## Próximos pasos
- HU-007: filtros temporales y bounding box (acordar formato con
  Frontend).
- F3/HU-008: ingesta de datos reales vía el Protocol del repositorio
  cuando Data/Geospatial entregue archivos; verificar `confidence_raw`
  y `acquired_at` contra muestras reales.
- F4/F5: calendar/harmonization/analytics bloqueados hasta definición
  científica; no simular aprobaciones.
- Opcional: Ruff en pre-commit/git hooks y README de instalación.
