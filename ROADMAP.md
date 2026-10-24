# ROADMAP.md — NASA Fire Harmonization API

## 1. Propósito

Este roadmap organiza el desarrollo del backend/API para el reto NASA Space Apps Challenge 2026 **Harmonization of MODIS and VIIRS Hot Spots**. Divide el trabajo en fases, historias de usuario (HU), criterios de aceptación y tareas pequeñas que pueden delegarse a agentes de código.

El objetivo es entregar un backend funcional, verificable y fácil de integrar con el módulo científico y el frontend. Este documento es un plan de ejecución: no reemplaza `PROJECT_CONTEXT.md`, `AGENTS.md`, los contratos de datos aprobados ni las decisiones del equipo científico.

## 2. Cómo utilizar este roadmap

- Trabaja en orden de dependencias. Una fase puede avanzar en paralelo cuando sus contratos de entrada y salida estén acordados.
- Cada tarea delegable debe tener un objetivo claro, archivos o módulos esperados, criterios de aceptación y verificaciones.
- Antes de asignar una tarea a un agente, proporciónale `AGENTS.md`, `PROJECT_CONTEXT.md` y la HU correspondiente.
- Asigna una HU por agente o una tarea pequeña por agente. Evita que dos agentes modifiquen simultáneamente el mismo archivo.
- No permitas que un agente invente datos, campos de origen, fórmulas científicas o métricas para completar una tarea.
- Mantén una rama o un conjunto de cambios aislado por tarea cuando el flujo de Git del equipo lo permita.
- Integra los cambios mediante revisión humana; los agentes no deben hacer commits, pushes ni despliegues salvo autorización explícita.
- Si una decisión científica o un contrato público no está definido, registra el bloqueo y continúa con trabajo independiente.

### Prioridad

- **P0 — Imprescindible:** necesario para tener un backend demostrable.
- **P1 — Importante:** aporta la funcionalidad principal y una integración robusta.
- **P2 — Opcional:** solo abordar si el tiempo, los datos y los contratos lo permiten.

### Definition of Ready (DoR)

Una HU está lista para asignarse cuando:
1. Su objetivo y resultado esperado están claros.
2. Las dependencias y los contratos relevantes están disponibles o se indica explícitamente qué está simulado.
3. Los criterios de aceptación pueden verificarse.
4. No depende de una decisión científica pendiente sin una alternativa provisional autorizada.

### Definition of Done (DoD)

Una HU se considera terminada cuando:
1. Cumple todos los criterios de aceptación.
2. Incluye pruebas adecuadas para el comportamiento nuevo o modificado.
3. Las verificaciones aplicables se ejecutaron y sus resultados se informaron con honestidad.
4. La documentación y los contratos se actualizaron si corresponde.
5. No introduce secretos, datos sintéticos presentados como reales ni cambios ajenos a la HU.
6. El cambio fue revisado e integrado por la persona responsable.

---

## 3. Resumen de fases

| Fase | Objetivo | Prioridad | Dependencias | Entregable |
|---|---|---:|---|---|
| F0. Alineación y contratos | Acordar límites del MVP, fuentes y contratos | P0 | Ninguna | Contratos iniciales aprobados |
| F1. Fundamentos del backend | Crear aplicación ejecutable y verificable | P0 | F0 parcial | API mínima con health check |
| F2. Esquemas y observaciones | Validar y consultar observaciones normalizadas | P0 | F0, F1 | Endpoint de observaciones |
| F3. Adaptador de datos reales | Integrar la fuente/archivos disponibles | P0 | F2, entrega del equipo de datos | Datos reales accesibles |
| F4. Contrato de armonización | Integrar salidas del procesamiento científico | P0 | F0, F2, integrante científico | Resultados armonizados consultables |
| F5. Calendario y analítica | Entregar actividad temporal y métricas acordadas | P0/P1 | F4 | API del calendario |
| F6. Integración con frontend | Validar flujos completos con el mapa y la interfaz | P0 | F2, F5, frontend disponible | Integración funcional |
| F7. Robustez y calidad | Manejar errores, límites y casos faltantes | P1 | F2–F6 | API más confiable |
| F8. Documentación y demo | Preparar entrega reproducible para jueces | P0 | F1–F7, según alcance | Backend documentado y demostrable |
| F9. Extensiones | Funcionalidades no esenciales | P2 | MVP estable | Mejoras opcionales |

Las fases F3 y F4 pueden avanzar en paralelo si los contratos están acordados. No debe bloquearse el desarrollo de la API por la disponibilidad inmediata de los datos reales: puede usarse un repositorio sintético claramente etiquetado mientras tanto.

---

# 4. Fases, historias de usuario y tareas delegables

## F0 — Alineación del alcance y contratos

**Objetivo:** reducir ambigüedades antes de que los agentes implementen código.

### HU-001 — Definir los contratos de observación

**Como** responsable de Backend/API, **quiero** un esquema común para observaciones MODIS y VIIRS, **para** integrar datos de distintas fuentes sin perder procedencia ni significado.

**Prioridad:** P0.

**Criterios de aceptación**
- Existe un contrato JSON documentado con tipos, unidades, campos requeridos y opcionales.
- Se conserva el valor de confianza original y se distingue de cualquier puntuación normalizada.
- La fecha tiene una semántica explícita y zona horaria definida.
- El contrato se contrasta con muestras reales de los datos disponibles.
- Los responsables de datos y ciencia revisan el contrato.

**Tareas delegables**
- **T001.1 — Inventariar los campos disponibles.** Revisar muestras y documentación de los productos fuente entregados por Data/Geospatial. No inventar campos ausentes.
- **T001.2 — Proponer el esquema Pydantic.** Preparar el modelo de observación con validaciones de tipos, coordenadas y campos opcionales.
- **T001.3 — Crear ejemplos JSON.** Añadir ejemplos sintéticos claramente etiquetados y, cuando existan, ejemplos anonimizados o representativos de datos reales.
- **T001.4 — Documentar decisiones pendientes.** Registrar campos, unidades, identificadores y conversiones que requieran aprobación.

**Agente recomendado:** agente de backend/Pydantic; revisión de Data/Geospatial y Science Lead.

### HU-002 — Definir el contrato de resultados armonizados

**Como** backend y frontend, **quiero** un formato común para los resultados del algoritmo, **para** consumirlos sin depender de los detalles internos del procesamiento.

**Prioridad:** P0.

**Criterios de aceptación**
- El contrato diferencia los resultados originales por sensor y las métricas armonizadas.
- Cada métrica tiene definición, unidad, período y método/versionado cuando aplique.
- Se indica cuándo un valor no está disponible.
- El contrato recibe aprobación de Science Lead y Data/ML/Statistics.

**Tareas delegables**
- **T002.1 — Diseñar el esquema de resultados.** Crear una propuesta basada en las salidas reales previstas del módulo científico.
- **T002.2 — Definir metadatos de ejecución.** Proponer campos para versión del método, período analizado, estado y procedencia.
- **T002.3 — Documentar semántica de valores ausentes.** Diferenciar cero actividad, datos ausentes, cobertura desconocida y procesamiento incompleto cuando la fuente permita distinguirlos.
- **T002.4 — Acordar el contrato con frontend.** Validar que el esquema sirva para mapa, calendario y gráficos.

**Bloqueo:** no definir una fórmula de armonización ni una puntuación de calidad sin aprobación científica.

### HU-003 — Acordar alcance y criterios del MVP

**Como** equipo, **queremos** priorizar un conjunto pequeño de capacidades, **para** completar una demostración coherente durante la hackathon.

**Prioridad:** P0.

**Criterios de aceptación**
- El equipo acuerda qué región, período y caso de uso demostrará.
- Se identifican las fuentes disponibles y sus restricciones.
- Se define el flujo principal desde datos hasta visualización.
- Las funcionalidades opcionales quedan fuera del MVP.

**Tareas delegables**
- **T003.1 — Redactar el alcance técnico.** Listar endpoints mínimos y dependencias.
- **T003.2 — Elaborar un diagrama de flujo.** Mostrar fuente → normalización → procesamiento → API → frontend.
- **T003.3 — Crear una matriz de dependencias.** Identificar entregables de cada integrante y fecha objetivo.

---

## F1 — Fundamentos del backend

**Objetivo:** tener una API ejecutable, documentada y con pruebas desde el comienzo.

### HU-004 — Ejecutar la API localmente

**Como** desarrollador del equipo, **quiero** iniciar el backend de forma reproducible, **para** trabajar y probar funcionalidades desde cualquier máquina del equipo.

**Prioridad:** P0.

**Criterios de aceptación**
- La aplicación inicia con el comando documentado.
- `GET /api/v1/health` devuelve estado HTTP 200 y una respuesta estable.
- La documentación OpenAPI está disponible en `/docs`.
- El proyecto puede instalar sus dependencias en un entorno virtual limpio.

**Tareas delegables**
- **T004.1 — Crear el esqueleto mínimo.** Configurar `app/main.py`, paquetes y router de salud.
- **T004.2 — Definir dependencias iniciales.** Registrar FastAPI, Uvicorn, pytest y HTTPX según la política del repositorio.
- **T004.3 — Añadir configuración básica.** Documentar cómo ejecutar la aplicación y qué variables de entorno, si las hay, necesita.
- **T004.4 — Crear prueba de salud.** Probar estado y cuerpo de la respuesta.

**Agente recomendado:** agente de backend Python.

### HU-005 — Establecer la base de pruebas y estilo

**Como** responsable del backend, **quiero** una verificación automatizada consistente, **para** detectar regresiones antes de integrar cambios.

**Prioridad:** P0.

**Criterios de aceptación**
- pytest descubre y ejecuta las pruebas.
- Hay una guía clara de comandos.
- Las pruebas no dependen de servicios externos ni credenciales.
- Si se incorpora lint/formato, está configurado y documentado.

**Tareas delegables**
- **T005.1 — Configurar pytest.** Añadir pruebas mínimas y revisar la estructura de importación.
- **T005.2 — Evaluar Ruff.** Proponer configuración y dependencias; pedir autorización antes de añadirlas si no estaban aprobadas.
- **T005.3 — Revisar `.gitignore`.** Excluir `.venv`, cachés, archivos `.env` y resultados locales que no deban versionarse.
- **T005.4 — Documentar comandos.** Mantenerlos sincronizados con `AGENTS.md`.

---

## F2 — Esquemas y consulta de observaciones

**Objetivo:** publicar el primer contrato útil para el frontend.

### HU-006 — Consultar observaciones

**Como** usuario del sistema, **quiero** consultar observaciones satelitales normalizadas, **para** explorar detecciones en la interfaz.

**Prioridad:** P0.

**Endpoint propuesto:** `GET /api/v1/observations`.

**Criterios de aceptación**
- Devuelve una lista con un esquema estable.
- El modelo valida sensores y coordenadas.
- Los filtros implementados están documentados.
- Los datos de demostración se identifican como sintéticos.
- Los casos de lista vacía y parámetros inválidos están probados.

**Tareas delegables**
- **T006.1 — Implementar `Observation` con Pydantic.** Aplicar el contrato aprobado, no asumir que el esquema preliminar es definitivo.
- **T006.2 — Crear repositorio temporal.** Proporcionar registros sintéticos claramente identificados.
- **T006.3 — Crear servicio de consulta.** Filtrar y limitar resultados sin depender de FastAPI.
- **T006.4 — Implementar endpoint.** Delegar la lógica al servicio y documentar parámetros.
- **T006.5 — Añadir pruebas.** Cubrir respuesta normal, filtro por sensor, límites, lista vacía y valores inválidos.

### HU-007 — Filtrar por tiempo y región

**Como** usuario del mapa, **quiero** filtrar observaciones por intervalo de fechas y área geográfica, **para** centrar el análisis en una zona y período relevantes.

**Prioridad:** P0.

**Criterios de aceptación**
- Los parámetros temporales tienen semántica y zona horaria documentadas.
- Los límites geográficos están validados.
- Se especifica si los límites del área se incluyen.
- Los filtros se aplican de forma consistente y se prueban.
- La API limita el tamaño de la respuesta o documenta una estrategia de paginación cuando el volumen lo requiera.

**Tareas delegables**
- **T007.1 — Definir el contrato de filtros.** Acordar fechas, bounding box y combinación de parámetros con el frontend.
- **T007.2 — Implementar validación de filtros.** Rechazar intervalos invertidos y coordenadas fuera de rango.
- **T007.3 — Añadir filtrado al servicio/repositorio.** Evitar lógica duplicada en las rutas.
- **T007.4 — Probar límites y combinaciones.** Incluir zona horaria, límites de fecha y cajas geográficas inválidas.

**Dependencia:** confirmar el formato espacial de los datos reales y las necesidades del mapa.

---

## F3 — Ingesta y acceso a datos reales

**Objetivo:** sustituir gradualmente el repositorio sintético por datos del equipo.

### HU-008 — Cargar los datos de origen

**Como** responsable de backend, **quiero** acceder a los archivos o a la fuente real acordada, **para** alimentar la API con observaciones verificables.

**Prioridad:** P0.

**Criterios de aceptación**
- La fuente y la versión/producto se documentan.
- Los datos se pueden cargar de forma reproducible.
- Los errores de lectura o registros inválidos se detectan y reportan.
- La ingesta no requiere secretos versionados.
- Existen pruebas con muestras pequeñas y seguras.

**Tareas delegables**
- **T008.1 — Inspeccionar los archivos entregados.** Documentar formato, columnas, unidades, sistema de coordenadas y limitaciones.
- **T008.2 — Proponer adaptador de fuente.** Definir una interfaz interna para desacoplar la fuente del servicio.
- **T008.3 — Implementar lector del formato aprobado.** CSV/JSON/Parquet u otro formato confirmado por el equipo.
- **T008.4 — Normalizar campos.** Convertir solo campos cuya semántica esté confirmada; conservar valores originales relevantes.
- **T008.5 — Añadir pruebas de ingesta.** Probar archivo válido, archivo vacío, columnas faltantes y registros inválidos.

**Nota:** si la fuente es NASA FIRMS mediante API, confirmar antes las condiciones de acceso, los límites de consulta y la forma de autenticación. No asumir que el equipo necesita consumir el servicio en tiempo real; archivos descargados pueden ser suficientes para el MVP.

### HU-009 — Informar procedencia y calidad de la ingesta

**Como** usuario técnico, **quiero** conocer la procedencia y el estado de los datos, **para** interpretar los resultados de forma responsable.

**Prioridad:** P1.

**Criterios de aceptación**
- Se conoce la fuente, el período y el momento de procesamiento cuando esos datos están disponibles.
- Los registros rechazados o incompletos se contabilizan sin ocultar el problema.
- No se modifican silenciosamente valores originales.
- Los datos sintéticos no se mezclan sin identificación con los reales.

**Tareas delegables**
- **T009.1 — Definir metadatos de ingesta.**
- **T009.2 — Registrar resumen de validación.**
- **T009.3 — Añadir pruebas para datos incompletos.**
- **T009.4 — Documentar limitaciones de cobertura.**

---

## F4 — Integración con el módulo científico

**Objetivo:** hacer accesibles los resultados producidos por el algoritmo aprobado.

### HU-010 — Consultar resultados armonizados

**Como** usuario de la aplicación, **quiero** consultar resultados armonizados para un período y área, **para** comparar la actividad de los sensores con una metodología explícita.

**Prioridad:** P0.

**Endpoint candidato:** `GET /api/v1/harmonization`.

**Criterios de aceptación**
- El endpoint usa el contrato aprobado por Science Lead y Data/ML/Statistics.
- Incluye período y área consultados, método/versionado cuando corresponda y estado del resultado.
- Los valores ausentes no se convierten automáticamente en cero.
- Los resultados pueden rastrearse hasta su fuente o ejecución cuando los metadatos estén disponibles.
- Hay pruebas con resultados conocidos o fixtures aprobados.

**Tareas delegables**
- **T010.1 — Inspeccionar la interfaz del módulo científico.** Determinar si entrega una función Python, un archivo o un servicio.
- **T010.2 — Definir el adaptador de armonización.** Evitar que las rutas dependan de detalles internos del algoritmo.
- **T010.3 — Implementar el servicio de consulta.**
- **T010.4 — Exponer el endpoint y su esquema de respuesta.**
- **T010.5 — Añadir pruebas de integración.**

**Bloqueo científico:** no crear un algoritmo sustituto ni inventar resultados para desbloquear el endpoint. Mientras no haya implementación, usar fixtures claramente sintéticos solo para validar el contrato y la interfaz.

### HU-011 — Consultar métricas y anomalías

**Como** analista, **quiero** consultar las métricas acordadas y los períodos inusuales, **para** interpretar patrones sin replicar cálculos en el frontend.

**Prioridad:** P1.

**Criterios de aceptación**
- Cada métrica tiene definición, unidad, período y método documentados.
- Los umbrales de anomalía están definidos por el equipo científico.
- La respuesta distingue ausencia de resultado de un valor numérico cero.
- Los resultados se pueden relacionar con su período y área.

**Tareas delegables**
- **T011.1 — Documentar métricas aprobadas.**
- **T011.2 — Definir el esquema de respuesta.**
- **T011.3 — Integrar resultados calculados por el módulo científico.**
- **T011.4 — Añadir pruebas de casos normales y extremos.**

No implementes detección estadística de anomalías por intuición. Si el método no está definido, deja esta HU bloqueada o fuera del MVP.

---

## F5 — Calendario y analítica temporal

**Objetivo:** entregar al frontend la estructura que necesita para representar actividad diaria.

### HU-012 — Consultar el calendario de actividad

**Como** usuario, **quiero** ver la actividad por día en un intervalo, **para** identificar períodos de mayor o menor actividad y días que requieren revisión.

**Prioridad:** P0 si el calendario es la visualización central del reto; en caso contrario, P1.

**Endpoint candidato:** `GET /api/v1/calendar?start=YYYY-MM-DD&end=YYYY-MM-DD`.

**Criterios de aceptación**
- Devuelve un resultado por fecha según el contrato acordado.
- La respuesta indica el área y el período consultado.
- La definición de actividad armonizada está documentada.
- Se diferencia cero actividad de datos ausentes cuando sea posible.
- Los días sin observaciones se manejan de acuerdo con la política aprobada.
- El frontend puede representar la respuesta sin recalcular métricas científicas.

**Tareas delegables**
- **T012.1 — Acordar el contrato con frontend y ciencia.**
- **T012.2 — Crear esquemas Pydantic del calendario.**
- **T012.3 — Implementar el servicio de consulta temporal.**
- **T012.4 — Implementar filtros de fecha y área.**
- **T012.5 — Añadir pruebas de intervalos, días faltantes y límites.**
- **T012.6 — Publicar un ejemplo de respuesta en la documentación.**

### HU-013 — Consultar resumen de un período

**Como** usuario, **quiero** obtener un resumen de la actividad en un período, **para** comparar períodos y contextualizar la visualización.

**Prioridad:** P1.

**Endpoint candidato:** `GET /api/v1/analytics`.

**Criterios de aceptación**
- Devuelve solo métricas definidas y aprobadas.
- Cada valor tiene una unidad o una definición clara.
- Se documentan las limitaciones y la cobertura del período.
- El resumen coincide con el resultado del módulo científico.

**Tareas delegables**
- **T013.1 — Acordar las métricas mínimas del MVP.**
- **T013.2 — Crear el esquema de resumen.**
- **T013.3 — Integrar resultados existentes, sin duplicar el algoritmo.**
- **T013.4 — Verificar consistencia entre calendario y resumen.**

---

## F6 — Integración con frontend y mapa

**Objetivo:** asegurar que los contratos funcionan en la aplicación real.

### HU-014 — Integrar el mapa con la API

**Como** usuario de la interfaz, **quiero** visualizar observaciones filtradas por región y período, **para** explorar espacialmente la actividad.

**Prioridad:** P0.

**Criterios de aceptación**
- El frontend puede consumir los endpoints desde su entorno de desarrollo.
- El contrato de coordenadas coincide con el formato esperado por el mapa.
- Los filtros producen resultados coherentes.
- Los errores de red o respuestas vacías se manejan sin bloquear la interfaz.
- CORS se configura para los orígenes de desarrollo aprobados, sin usar comodines innecesarios en producción.

**Tareas delegables**
- **T014.1 — Acordar URL base y rutas con frontend.**
- **T014.2 — Configurar CORS con orígenes explícitos.**
- **T014.3 — Probar el flujo de filtros de mapa.**
- **T014.4 — Verificar coordenadas, fechas y esquema de respuesta.**
- **T014.5 — Documentar pasos de integración local.**

### HU-015 — Integrar calendario y gráficos

**Como** usuario, **quiero** que el calendario y los gráficos consuman resultados consistentes, **para** explorar cambios temporales sin discrepancias entre componentes.

**Prioridad:** P0/P1 según el alcance visual acordado.

**Criterios de aceptación**
- Los componentes consumen los contratos publicados.
- El backend no requiere que el frontend implemente cálculos científicos.
- Las fechas, unidades y estados de datos faltantes son coherentes entre endpoints.
- Los errores y estados vacíos tienen respuestas previsibles.

**Tareas delegables**
- **T015.1 — Revisar los modelos usados por el frontend.**
- **T015.2 — Probar la respuesta del calendario con datos de prueba.**
- **T015.3 — Corregir incompatibilidades mediante cambios coordinados.**
- **T015.4 — Ejecutar una prueba integral del flujo principal.**

No cambies un contrato público solo para resolver una incompatibilidad local. Primero acuerda el ajuste con frontend y actualiza la documentación y pruebas.

---

## F7 — Robustez, seguridad y calidad

**Objetivo:** evitar que datos incompletos o solicitudes incorrectas produzcan resultados engañosos o errores difíciles de diagnosticar.

### HU-016 — Gestionar errores de forma consistente

**Como** consumidor de la API, **quiero** errores claros y predecibles, **para** saber si la solicitud es incorrecta, si faltan datos o si el servicio falló.

**Prioridad:** P1.

**Criterios de aceptación**
- Los errores de validación devuelven códigos HTTP apropiados.
- Los errores internos no exponen trazas ni secretos.
- La estructura de error se documenta si se personaliza.
- Las pruebas cubren los casos más relevantes.

**Tareas delegables**
- **T016.1 — Inventariar errores esperados.**
- **T016.2 — Definir el formato de error, si es necesario.**
- **T016.3 — Implementar manejadores consistentes.**
- **T016.4 — Añadir pruebas de entradas inválidas y fallos controlados.**

### HU-017 — Controlar volumen y rendimiento

**Como** consumidor de la API, **quiero** que las consultas grandes se gestionen de forma predecible, **para** evitar respuestas excesivas o tiempos de espera innecesarios.

**Prioridad:** P1.

**Criterios de aceptación**
- Los endpoints que devuelven listas tienen límites o paginación apropiados.
- Los límites están documentados.
- No se carga repetidamente todo un archivo grande en cada petición si el volumen real lo vuelve ineficiente.
- Las decisiones se basan en el volumen real del MVP.

**Tareas delegables**
- **T017.1 — Medir el tamaño y patrón de acceso de los datos disponibles.**
- **T017.2 — Proponer paginación o filtros adicionales si hacen falta.**
- **T017.3 — Implementar y probar la estrategia aprobada.**

### HU-018 — Proteger configuración y secretos

**Como** responsable del proyecto, **quiero** mantener credenciales y configuración fuera del código, **para** reducir el riesgo de exposición accidental.

**Prioridad:** P1.

**Criterios de aceptación**
- No hay secretos versionados.
- Los parámetros sensibles se reciben por configuración segura.
- Los ejemplos usan valores ficticios o placeholders.
- `.gitignore` excluye archivos locales sensibles.

**Tareas delegables**
- **T018.1 — Revisar archivos de configuración.**
- **T018.2 — Verificar `.gitignore`.**
- **T018.3 — Documentar variables necesarias y ejemplos seguros.**
- **T018.4 — Revisar el diff en busca de credenciales o datos locales.**

---

## F8 — Documentación y demostración

**Objetivo:** permitir que otra persona ejecute, pruebe y comprenda el backend durante la evaluación.

### HU-019 — Documentar instalación y API

**Como** integrante del equipo o evaluador técnico, **quiero** instrucciones reproducibles, **para** ejecutar el backend y comprender sus endpoints sin depender de explicaciones verbales.

**Prioridad:** P0.

**Criterios de aceptación**
- `README.md` explica requisitos, instalación, configuración, ejecución y pruebas.
- La documentación distingue datos reales de datos sintéticos.
- Los endpoints, filtros, respuestas y errores relevantes están documentados.
- Los contratos coinciden con el comportamiento real.
- Una persona distinta del autor puede seguir los pasos en un entorno limpio.

**Tareas delegables**
- **T019.1 — Escribir instrucciones de instalación.**
- **T019.2 — Documentar endpoints y ejemplos.**
- **T019.3 — Actualizar `docs/api-contracts.md`.**
- **T019.4 — Revisar coherencia entre `README.md`, `AGENTS.md` y los comandos reales.**

### HU-020 — Preparar una demostración reproducible

**Como** equipo de Space Apps, **queremos** demostrar el flujo principal de extremo a extremo, **para** explicar el valor de la solución y las limitaciones de forma transparente.

**Prioridad:** P0.

**Criterios de aceptación**
- La demo puede ejecutarse siguiendo instrucciones escritas.
- El flujo muestra fuente, procesamiento, API y visualización.
- Los datos de demostración están etiquetados.
- Se explican las limitaciones del método y qué está validado.
- No se presenta una prueba técnica como validación científica.

**Tareas delegables**
- **T020.1 — Definir el escenario de demo.**
- **T020.2 — Preparar un conjunto pequeño y reproducible de datos de prueba.**
- **T020.3 — Verificar el flujo completo desde una instalación limpia.**
- **T020.4 — Preparar una lista de comprobación previa a la presentación.**

---

## F9 — Extensiones opcionales

Solo abordar después de que el MVP completo funcione.

### HU-021 — Persistencia de resultados

**Prioridad:** P2.

Agregar persistencia si los datos, el tamaño o los requisitos de la demo lo justifican.

Tareas:
- Evaluar el volumen real y los patrones de consulta.
- Comparar archivos estructurados con una base de datos.
- Proponer la opción más simple.
- Solicitar aprobación antes de añadir infraestructura o dependencias.
- Añadir pruebas y documentación de configuración.

### HU-022 — Consultas asíncronas o procesamiento pesado

**Prioridad:** P2.

Considerar tareas en segundo plano solo si el procesamiento no puede ejecutarse razonablemente durante una solicitud normal.

Tareas:
- Medir duración y memoria del procesamiento real.
- Identificar límites de la petición HTTP.
- Proponer una solución proporcional.
- Solicitar aprobación antes de introducir colas, workers o servicios externos.

### HU-023 — Caché de consultas frecuentes

**Prioridad:** P2.

Considerar caché únicamente si hay consultas repetidas y una necesidad demostrada.

Tareas:
- Identificar endpoints costosos.
- Definir cómo invalidar resultados al cambiar datos o método.
- Evaluar alternativas sin infraestructura adicional.
- Solicitar aprobación antes de incorporar un sistema de caché externo.

---

# 5. Orden recomendado de delegación

Este es el orden práctico para trabajar con agentes de código:

1. **Agente A — Fundamentos:** HU-004 y HU-005. Crear la aplicación mínima, comandos y pruebas.
2. **Agente B — Contrato de observaciones:** HU-001 y parte de HU-006. Trabajar primero en esquemas y validaciones; no duplicar cambios en `main.py`.
3. **Agente C — Consulta de observaciones:** HU-006, una vez acordado el contrato. Implementar repositorio, servicio, ruta y pruebas.
4. **Agente D — Integración de datos:** HU-008 y HU-009 cuando el equipo entregue archivos y metadatos.
5. **Agente E — Integración científica:** HU-002, HU-010 y HU-011 según la disponibilidad del método y sus resultados.
6. **Agente F — Calendario:** HU-012 y HU-013 después de aprobar los contratos científicos y temporales.
7. **Agente G — Integración frontend:** HU-014 y HU-015 con participación del responsable de frontend.
8. **Agente de revisión/documentación:** HU-016 a HU-020 según los cambios integrados.

Los agentes pueden coincidir en el tiempo si trabajan en módulos distintos. Sin embargo, una sola persona debe ser responsable de integrar cambios que afecten los mismos contratos o archivos centrales.

## 6. Plantilla para asignar tareas a un agente

Copia y completa esta plantilla al delegar una tarea:

```text
Lee AGENTS.md, PROJECT_CONTEXT.md y la HU asignada en ROADMAP.md.

Tarea: [ID y título de la HU/tarea]
Objetivo: [resultado concreto]
Contexto existente: [archivos, contratos o módulos relevantes]
Alcance permitido: [archivos o componentes que puede modificar]
Fuera de alcance: [qué no debe cambiar]
Criterios de aceptación:
- [criterio 1]
- [criterio 2]
- [criterio 3]

Pruebas requeridas:
- [casos normales]
- [casos inválidos/límites]

Antes de implementar:
- Inspecciona el estado real del repositorio.
- Si falta una decisión de dominio o el cambio afecta contratos,
  detente y solicita aclaración.
- Para cambios amplios, presenta un plan breve antes de editar.

Al terminar:
- Resume los cambios.
- Enumera los archivos modificados.
- Explica decisiones y supuestos.
- Indica comandos ejecutados y resultados reales.
- Señala pendientes, riesgos y pruebas no ejecutadas.
- No hagas commit, push ni despliegue.
```

## 7. Dependencias críticas y bloqueos

| Decisión o insumo | Responsable principal | Bloquea |
|---|---|---|
| Muestras reales y columnas de los archivos | Data/Geospatial | Finalización del esquema y adaptador real |
| Método de armonización y métricas | Science Lead + Data/ML/Statistics | HU-002, HU-010, HU-011 y parte de HU-012 |
| Región y período de la demo | Equipo | Filtros, volumen y escenario de demostración |
| Campos que necesita el mapa | Frontend/Map/UX | Contrato final de observaciones y filtros |
| Entorno y dependencias aprobadas | Responsable Backend/API | Instalación reproducible y herramientas adicionales |

Cuando un bloqueo esté pendiente, marca la HU como **Bloqueada**, documenta qué decisión falta y avanza en tareas independientes. No simules una aprobación ni ocultes la incertidumbre.

## 8. Criterio de éxito del MVP

El backend está listo para la demostración cuando:

- Se puede instalar y ejecutar siguiendo el README.
- La API publica su documentación OpenAPI.
- Los endpoints principales de observaciones y calendario tienen contratos estables.
- La fuente de datos usada está identificada y los datos sintéticos, si existen, están etiquetados.
- El módulo científico se integra sin duplicar ni inventar su lógica.
- El frontend consume los endpoints principales con filtros funcionales.
- Las pruebas relevantes pasan y los fallos conocidos están documentados.
- El equipo puede explicar qué resultados son datos observados, cuáles son cálculos del método y cuáles son solo demostraciones.

**Regla final:** prioriza un flujo pequeño, trazable y reproducible de datos → procesamiento aprobado → API → visualización, antes que añadir más endpoints o infraestructura.