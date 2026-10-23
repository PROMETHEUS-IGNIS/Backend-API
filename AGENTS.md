# AGENTS.md --- NASA Fire Harmonization API

Backend modular para apoyar el reto NASA Space Apps Challenge 2026
**Harmonization of MODIS and VIIRS Hot Spots**. Su objetivo es exponer
datos y resultados de armonización mediante una API estable para que el
frontend explore observaciones, actividad temporal y métricas
geográficas.

## Stack y estructura

### Tecnologías y versiones clave

-   **Python:** 3.12 o superior, salvo que el entorno del equipo exija
    otra versión compatible.
-   **FastAPI:** API HTTP y documentación OpenAPI.
-   **Pydantic v2:** validación y serialización de esquemas.
-   **Uvicorn:** servidor ASGI de desarrollo.
-   **pytest + HTTPX:** pruebas unitarias y de endpoints mediante
    `TestClient`.
-   **Ruff:** formato y análisis estático recomendado. Si no está
    instalado/configurado, consulta antes de introducirlo como
    dependencia del proyecto.
-   **Datos científicos:** Pandas, NumPy o GeoPandas solo cuando una
    tarea real los necesite; no añadirlos preventivamente.

Las versiones exactas deben quedar fijadas en los archivos de
dependencias del repositorio una vez acordadas. No afirmes que una
versión está instalada sin comprobarlo.

### Estructura prevista

``` text
backend/
├── app/
│   ├── main.py
│   ├── api/routes/
│   │   ├── health.py
│   │   ├── observations.py
│   │   └── calendar.py
│   ├── schemas/
│   │   ├── observation.py
│   │   └── calendar.py
│   ├── services/
│   │   ├── observation_service.py
│   │   └── calendar_service.py
│   └── repositories/
│       └── observation_repository.py
├── tests/
├── docs/
│   └── api-contracts.md
├── requirements.txt
├── .gitignore
├── PROJECT_CONTEXT.md
└── AGENTS.md
```

Esta estructura es la referencia objetivo, no una autorización para
crear todos los archivos de inmediato. Respeta la estructura existente
del repositorio y crea solo lo necesario para la tarea aprobada.

-   `app/main.py`: crea la aplicación FastAPI, registra routers y
    configura metadatos.
-   `app/api/routes/`: endpoints HTTP; no debe concentrar lógica
    científica ni acceso directo a archivos.
-   `app/schemas/`: modelos Pydantic que definen y validan entradas y
    salidas.
-   `app/services/`: lógica de aplicación y coordinación entre
    componentes.
-   `app/repositories/`: acceso a datos y adaptadores para desacoplar la
    fuente de almacenamiento.
-   `tests/`: pruebas automatizadas.
-   `docs/api-contracts.md`: contratos compartidos con los demás
    integrantes.
-   `PROJECT_CONTEXT.md`: contexto de producto, dominio y
    responsabilidad del agente.

## Comandos

Ejecutar desde la raíz del repositorio (la carpeta que contiene `app/` y
`requirements.txt`). En Windows PowerShell:

``` powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Si el proyecto aún no tiene `requirements.txt`, no inventes sus
contenidos ni supongas que existe: consulta el estado del repositorio y
solicita autorización o propone el archivo antes de crearlo.

Documentación interactiva local, con el servidor en ejecución:

``` text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/openapi.json
```

Ejecutar pruebas:

``` powershell
python -m pytest -v
```

Ejecutar una prueba concreta:

``` powershell
python -m pytest tests/test_observations.py -v
```

Lint y formato, si Ruff ya está configurado e instalado:

``` powershell
ruff check .
ruff format --check .
```

Aplicar formato, solo cuando la tarea lo requiera:

``` powershell
ruff format .
```

Si no hay configuración de Ruff, no reformatees todo el repositorio.
Propón una configuración mínima y pide autorización antes de añadir la
herramienta o cambiar dependencias.

Para registrar las versiones instaladas en el entorno:

``` powershell
python -m pip freeze
```

No sobrescribas archivos de dependencias o bloqueos sin revisar primero
cómo se gestionan en el repositorio.

## Convenciones

-   Código, identificadores, nombres de carpetas, funciones, clases,
    variables y comentarios técnicos: **inglés**.
-   Documentación de equipo y explicaciones al responsable humano:
    **español**, salvo que se acuerde otra cosa.
-   Nombres: `snake_case` para módulos, funciones y variables;
    `PascalCase` para clases; constantes en `UPPER_SNAKE_CASE`.
-   Añade anotaciones de tipos a funciones públicas y modelos de datos.
-   Prefiere funciones pequeñas, nombres descriptivos y retornos
    explícitos.
-   Usa modelos Pydantic para contratos de API; evita devolver
    diccionarios arbitrarios cuando exista un esquema conocido.
-   Mantén las rutas HTTP delgadas y delega la lógica a servicios.
-   Mantén la lógica científica independiente de FastAPI.
-   Aísla la lectura de archivos y el acceso a datos en
    repositorios/adaptadores.
-   Usa inyección explícita de dependencias cuando simplifique las
    pruebas; evita patrones de infraestructura innecesarios para el MVP.
-   Las fechas y horas deben tener una zona horaria explícita. Normaliza
    a UTC en los límites del sistema cuando sea apropiado.
-   Conserva unidades y procedencia de los datos.
-   Usa `pytest` para pruebas. Incluye casos normales, entradas
    inválidas y límites relevantes.
-   No añadas comentarios que repitan literalmente lo que el código ya
    expresa. Documenta el motivo cuando no sea obvio.
-   Archivo de referencia para contexto y reglas de dominio:
    `PROJECT_CONTEXT.md`. Para contratos compartidos, usa
    `docs/api-contracts.md` si existe.

## Reglas de dominio / trampas conocidas

-   MODIS y VIIRS no deben tratarse como fuentes intercambiables. Sus
    resoluciones, horarios de observación, campos y categorías de
    confianza pueden diferir.
-   No sumes conteos por sensor ni declares una cifra de actividad
    armonizada sin una definición científica acordada.
-   No conviertas niveles de confianza originales a una escala común sin
    un método aprobado y documentado.
-   Conserva los valores originales de confianza y otros campos fuente
    relevantes; los campos normalizados deben ser adicionales y tener
    una definición clara.
-   Distingue entre cero detecciones, datos faltantes, cobertura no
    disponible y procesamiento incompleto cuando la fuente permita
    hacerlo.
-   No supongas que una detección corresponde a un incendio único, ni
    que dos detecciones cercanas son el mismo evento, sin una regla
    validada.
-   No inventes registros, métricas, fuentes o resultados científicos.
    Los datos sintéticos deben identificarse como demostrativos y no
    deben presentarse como observaciones reales de NASA.
-   Usa coordenadas geográficas en grados decimales y valida rangos:
    latitud \[-90, 90\], longitud \[-180, 180\]. Confirma el sistema de
    referencia espacial de cualquier archivo real.
-   No mezcles fechas locales y UTC de forma implícita. Documenta el
    significado de las fechas: adquisición, recepción o procesamiento.
-   No asumas que `frp_mw` está disponible en todas las fuentes; debe
    ser opcional cuando el producto de origen no lo proporcione.
-   La definición final del esquema debe verificarse contra los archivos
    y metadatos reales, no solo contra ejemplos de documentación.
-   El método de armonización y los criterios de validación corresponden
    al Science Lead y al responsable de Data/ML/Statistics. El backend
    los integra; no los inventa.
-   No incluyas claves API ni credenciales en el código, ejemplos, logs,
    pruebas o archivos versionados.

## Forma de trabajar

1.  Lee `PROJECT_CONTEXT.md`, este archivo y los archivos directamente
    relacionados antes de actuar.
2.  Inspecciona el repositorio y su estado actual. No supongas que la
    estructura prevista ya existe.
3.  Para cambios pequeños y locales, implementa directamente si el
    objetivo y los criterios están claros.
4.  Antes de cambios que afecten arquitectura, contratos públicos,
    dependencias, almacenamiento, seguridad o varios módulos, presenta
    un plan breve y espera aprobación.
5.  Divide el trabajo en cambios pequeños, coherentes y fáciles de
    revisar. Evita refactorizaciones ajenas a la tarea.
6.  No reemplaces datos reales por datos sintéticos ni cambies contratos
    para hacer pasar pruebas.
7.  Añade o modifica pruebas para cada comportamiento nuevo o corregido.
8.  Ejecuta las verificaciones pertinentes antes de terminar. Si no
    puedes ejecutarlas, indícalo explícitamente.
9.  Actualiza documentación y contratos cuando cambie el comportamiento
    público.
10. Al finalizar, explica: resumen, archivos modificados, decisiones y
    supuestos, comandos de verificación con resultados reales y
    pendientes/riesgos.

## Memoria
- Al empezar, lee `MEMORY.md` para conocer el estado del proyecto y las decisiones
tomadas.
- Al terminar una tarea, actualízalo: estado actual, decisiones importantes (con su
porqué) y errores a evitar.
- Mantenlo breve (máximo ~50 líneas): resume o elimina lo que ya no aporte.
- Si algo se convierte en una regla permanente, propón moverlo a `AGENTS.md` en lugar de
dejarlo en la memoria.
- No guardes nunca datos sensibles (claves, tokens, datos personales). 

## Límites

### ✅ Siempre

-   Validar las entradas externas y usar esquemas tipados.
-   Mantener la separación entre rutas, servicios y repositorios.
-   Preservar procedencia, unidades y valores fuente relevantes.
-   Añadir pruebas para cambios de comportamiento.
-   Usar datos sintéticos solo con identificación explícita.
-   Mantener los secretos fuera del repositorio.
-   Informar claramente de incertidumbres científicas y técnicas.
-   Mantener la documentación alineada con el comportamiento real.
-   Actualizar `MEMORY.md` al terminar cada tarea. 

### ⚠️ Pregunta antes

-   Añadir, quitar o actualizar dependencias.
-   Crear una base de datos, incorporar servicios externos o introducir
    Docker, caché, colas o infraestructura cloud.
-   Crear archivos de configuración global, workflows CI/CD o nuevos
    mecanismos de despliegue.
-   Crear archivos nuevos fuera de la estructura ya acordada o hacer
    refactorizaciones amplias.
-   Cambiar el formato, nombres, tipos, unidades o semántica de un
    contrato JSON público.
-   Definir o modificar algoritmos de armonización, umbrales de
    anomalías, equivalencias de confianza o métricas científicas.
-   Cambiar la versión mínima de Python o la estrategia de bloqueo de
    dependencias.
-   Eliminar archivos, migrar datos o realizar cambios destructivos.

Si una de estas decisiones es imprescindible, explica la necesidad, las
alternativas y el impacto, y solicita aprobación antes de actuar.

### 🚫 Nunca

-   Inventar resultados científicos o presentar datos de demostración
    como datos reales.
-   Afirmar que una prueba, lint o integración pasó si no se ejecutó.
-   Introducir credenciales, tokens o claves privadas en el repositorio.
-   Eliminar o relajar pruebas para ocultar fallos.
-   Cambiar contratos públicos silenciosamente.
-   Modificar el algoritmo científico por intuición o por conveniencia
    de la interfaz.
-   Añadir dependencias o infraestructura "por si acaso".
-   Ejecutar comandos destructivos o sobrescribir trabajo ajeno sin
    autorización.
-   Hacer commits, pushes, releases o despliegues sin una solicitud
    explícita del responsable humano.

## Verificación

Antes de declarar una tarea terminada:

1.  Comprueba que el cambio cumple los criterios de aceptación.

2.  Ejecuta las pruebas relevantes:

    ``` powershell
    python -m pytest -v
    ```

3.  Si Ruff está instalado y configurado, ejecuta:

    ``` powershell
    ruff check .
    ruff format --check .
    ```

4.  Para cambios en rutas o esquemas, verifica la respuesta HTTP, el
    código de estado y la documentación OpenAPI. Prueba entradas
    inválidas y límites.

5.  Para cambios de contratos, actualiza `docs/api-contracts.md` y
    comprueba que los ejemplos coincidan con los modelos y respuestas
    reales.

6.  Para cambios científicos, comprueba que el método aprobado esté
    documentado y que existan pruebas con casos conocidos; las pruebas
    de software por sí solas no demuestran validez científica.

7.  Revisa `git diff` para detectar cambios accidentales, secretos,
    archivos temporales o modificaciones no relacionadas.

8.  Reporta exactamente qué comandos se ejecutaron, cuáles pasaron,
    cuáles fallaron y cuáles no se pudieron ejecutar.

No declares una tarea terminada si hay fallos relevantes sin explicar o
si falta una decisión de dominio necesaria para validar el resultado.
