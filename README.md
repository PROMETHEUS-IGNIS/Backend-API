# NASA Fire Harmonization API

Backend de la **NASA Space Apps Challenge 2026** para el reto
**Harmonization of MODIS and VIIRS Hot Spots**.

API HTTP construida con FastAPI que expone observaciones de puntos
calientes satelitales (MODIS/VIIRS) para su exploración desde el
frontend: consultas filtradas, contrato de observaciones estables y
documentación OpenAPI interactiva.

> ⚠️ **Estado de los datos:** todos los datos servidos actualmente son
> **sintéticos y demostrativos** (`data_provenance: "synthetic_demo"`).
> NO son observaciones reales de NASA. La ingesta de datos reales está
> planificada en el roadmap (fase F3) y se integrará sin cambiar rutas
> ni contratos.

## Requisitos

- **Python 3.13** o superior (entorno de desarrollo actual: 3.13.17,
  con el launcher `py` disponible).
- Windows con PowerShell (comandos probados en este entorno).

## Instalación

Desde la raíz del repositorio (la carpeta que contiene `app/` y
`requirements.txt`):

``` powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ejecución en desarrollo

``` powershell
python -m uvicorn app.main:app --reload
```

Documentación interactiva (con el servidor en ejecución):

- Swagger UI: <http://127.0.0.1:8000/docs>
- Esquema OpenAPI: <http://127.0.0.1:8000/openapi.json>

## Endpoints (v0.1.0)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/v1/health` | Comprobación de estado (`{"status": "ok"}`) |
| `GET` | `/api/v1/observations` | Observaciones normalizadas, filtro opcional |

**Parámetros de `GET /api/v1/observations`:**

| Parámetro | Tipo | Rango | Por defecto |
|---|---|---|---|
| `sensor` | string | `MODIS` \| `VIIRS` | (sin filtro) |
| `limit` | int | 1–1000 | 100 |

Ejemplo:

``` powershell
curl "http://127.0.0.1:8000/api/v1/observations?sensor=VIIRS&limit=2"
```

``` json
{
  "data": [
    {
      "observation_id": "SYN-VIR-0001",
      "sensor": "VIIRS",
      "latitude": 5.9021,
      "longitude": -68.611,
      "acquired_at": "2026-10-05T13:45:00Z",
      "frp_mw": 30.2,
      "confidence_raw": "h",
      "source": "synthetic_demo"
    }
  ],
  "count": 2,
  "total_matching": 4,
  "data_provenance": "synthetic_demo"
}
```

Parámetros inválidos (sensor desconocido, `limit` fuera de rango)
devuelven **422**. Consultas válidas sin resultados devuelven 200 con
`data: []`.

📄 La referencia oficial de contratos compartida con el frontend y el
equipo científico es **`docs/api-contracts.md`**.

## Reglas de dominio (resumen)

- MODIS y VIIRS **no son fuentes intercambiables**: no se suman sus
  conteos ni se asume equivalencia de campos, resolución o confianza.
- `confidence_raw` conserva el valor/categoría **original** del
  producto sin reinterpretar. No existe `confidence_score` todavía:
  solo se añadirá cuando Science Lead y Data/ML/Statistics aprueben un
  método y una escala.
- Una ausencia de registros no implica cero actividad; cero
  detecciones y datos faltantes se distinguen en los contratos según lo
  permita la fuente.

## Pruebas

``` powershell
python -m pytest -v
python -m pytest tests/test_observations.py -v
```

Las pruebas no requieren servicios externos ni credenciales.

## Lint y formato

``` powershell
ruff check .
ruff format --check .
```

## Estructura del proyecto

``` text
backend/
├── app/
│   ├── main.py                   # Aplicación FastAPI
│   ├── api/routes/               # health.py, observations.py
│   ├── schemas/                  # Contratos Pydantic (health, observation)
│   ├── services/                 # Lógica de aplicación (sin HTTP)
│   └── repositories/             # Acceso a datos (sintético por ahora)
├── tests/                        # pytest + TestClient
├── docs/
│   └── api-contracts.md          # Contratos compartidos con el equipo
├── requirements.txt
├── pyproject.toml                # Configuración de Ruff y pytest
├── PROJECT_CONTEXT.md            # Contexto de producto y dominio
├── AGENTS.md                     # Convenciones del agente/código
└── ROADMAP.md                    # Fases e historias de usuario
```

## Hoja de ruta

El plan de fases y los criterios de aceptación están en `ROADMAP.md`.
Estado vivo, decisiones y aprendizajes del proyecto en `MEMORY.md`.
Fases pendientes inmediatas: filtros temporales/espaciales (HU-007),
ingesta de datos reales (F3) e integración con el módulo científico
(F4).

## Licencia y atribución

Proyecto del equipo Semillero de Astronomía para la NASA Space Apps
Challenge 2026. Los datos sintéticos incluidos son exclusivamente de
demostración.
