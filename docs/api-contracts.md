# API Contracts — NASA Fire Harmonization API

Contratos compartidos entre Backend/API, Frontend/Map/UX, Data/Geospatial,
Data/ML/Statistics y Science Lead. Este documento debe mantenerse
sincronizado con el comportamiento real de la API; si cambian los
endpoints o los esquemas, se actualiza este archivo y sus pruebas.

## Versión 0.1.0 (MVP — datos sintéticos)

### Convenciones generales

- Base URL local: `http://127.0.0.1:8000`
- Prefijo de versiones: `/api/v1`
- Todas las fechas y horas se expresan en **UTC** (ISO 8601) y se
  clasifican como **adquisición** (`acquired_at`). La semántica exacta
  debe verificarse contra los productos reales.
- Coordenadas en grados decimales: latitud [-90, 90], longitud [-180, 180].
- **Procedencia de los datos:** todos los datos actuales son
  **sintéticos y demostrativos**; no son observaciones reales de NASA.
  El campo `data_provenance` y el texto `source` lo identifican
  explícitamente. Al incorporar datos reales (ROADMAP.md, F3), estos
  campos cambiarán y se anunciará el cambio aquí.

### GET /api/v1/health

Comprobación de estado del servicio.

**Respuesta 200:**

```json
{
  "status": "ok",
  "api_version": "0.1.0"
}
```

### GET /api/v1/observations

Consulta de observaciones de puntos calientes normalizadas.

**Parámetros de consulta:**

| Parámetro | Tipo | Requerido | Rango / valores | Descripción |
|---|---|---|---|---|
| `sensor` | string | No | `MODIS` \| `VIIRS` | Filtro por sensor de origen |
| `limit` | int | No | 1–1000, por defecto 100 | Máximo de registros a devolver (truncamiento simple; sin paginación en v0.1) |

**Respuesta 200:**

```json
{
  "data": [
    {
      "observation_id": "SYN-MOD-0001",
      "sensor": "MODIS",
      "latitude": 5.8412,
      "longitude": -68.5031,
      "acquired_at": "2026-10-05T13:30:00Z",
      "frp_mw": 42.1,
      "confidence_raw": 80,
      "source": "synthetic_demo"
    }
  ],
  "count": 1,
  "total_matching": 1,
  "data_provenance": "synthetic_demo"
}
```

**Descripción de `Observation`:**

| Campo | Tipo | Semántica | Condición |
|---|---|---|---|
| `observation_id` | string | Identificador del registro en el sistema | Requerido |
| `sensor` | string | Sensor de origen: `MODIS` o `VIIRS`. No son fuentes intercambiables ni sus conteos se suman | Requerido |
| `latitude` | float | Grados decimales | Requerido, [-90, 90] |
| `longitude` | float | Grados decimales | Requerido, [-180, 180] |
| `acquired_at` | string (ISO 8601, UTC) | Instante de adquisición con zona horaria explícita | Requerido |
| `frp_mw` | float \| null | Potencia radiativa del fuego en MW; `null` cuando el producto de origen no la proporciona | Opcional |
| `confidence_raw` | int \| string | Valor o categoría de confianza **original** del producto sin reinterpretar. Convención provisional: para MODIS un entero 0–100; para VIIRS una letra `l`/`n`/`h`. La correspondencia definitiva debe verificarse contra archivos reales | Requerido |
| `source` | string | Producto o procedencia del registro (`synthetic_demo` hasta confirmar productos reales) | Requerido |

**Descripción del envoltorio `ObservationCollection`:**

| Campo | Tipo | Semántica |
|---|---|---|
| `data` | array de `Observation` | Registros tras aplicar `limit` |
| `count` | int | Registros devueltos (= `len(data)`) |
| `total_matching` | int | Total de coincidencias **antes** de aplicar `limit`; útil para detectar truncamiento |
| `data_provenance` | string | `synthetic_demo` mientras los datos sean de demostración |

**Errores:**

- Parámetros inválidos (sensor desconocido, `limit` fuera de 1–1000,
  tipos incorrectos): **422** con el formato de error de FastAPI.
- No se encontraron registros: **200** con `data: []`.

### Decisiones pendientes (bloqueos registrados)

- **Esquema definitivo:** el contrato anterior se debe contrastar con
  los archivos reales de MCD14ML/VNP14 (o los productos que confirme el
  equipo) para validar nombres de columnas, unidades y semántica de
  `confidence_raw` y `acquired_at`.
- **`confidence_score`:** NO se incluye hasta que Science Lead y
  Data/ML/Statistics definan y aprueben un método y una escala de
  normalización (ROADMAP.md, HU-002).
- **Filtros temporales y espaciales** (rango de fechas, bounding box):
  pendientes de HU-007 y de coordinar el formato con el frontend.
- **Calendario (`/calendar`), armonización (`/harmonization`) y
  analítica (`/analytics`):** bloqueadas hasta que exista una
  definición científica aprobada del método y las métricas.
