# Diccionario de Datos: REPDA Sonora (Uso Agrícola)

## 1. Descripción General
* **Nombre del Dataset:** Concesiones de Agua Subterránea y Superficial - Uso Agrícola (Sonora)
* **Fuente Original:** Registro Público de Derechos de Agua (REPDA) / CONAGUA (Servicio ArcGIS REST API).
* **Ámbito Geográfico:** Estado de Sonora, México (`ESTADO = 26`).
* **Filtro Aplicado:** Registros cuyo uso oficial o homologado corresponde a **AGRÍCOLA**.
* **Unidad de Observación:** Cada registro (fila) representa un **título de concesión o aprovechamiento hídrico** individual registrado ante la autoridad federal.

---

## 2. Estructura de Variables

| Columna / Variable | Tipo de Dato (Pandas/Python) | Descripción Detallada |
| :--- | :--- | :--- |
| **`FID`** | `int64` | Identificador único de la característica (Feature ID) asignado por el servidor geográfico de CONAGUA. |
| **`NUM_TITULO`** | `object` (String) | Número oficial del título de concesión otorgado al usuario. |
| **`NUM_APROVE`** | `object` (String) | Identificador específico del aprovechamiento (pozo, noria, descarga o toma) asociado al título. |
| **`NOMBRE`** | `object` (String) | Nombre del concesionario (persona física, moral, ejido o sociedad de producción rural). |
| **`ESTADO`** | `int64` / `object` | Clave numérica del estado según INEGI/CONAGUA (`26` para Sonora). |
| **`CLAVE_MUN`** | `int64` / `object` | Clave numérica oficial del municipio dentro del estado de Sonora. |
| **`MUNICIPIO`** | `object` (String) | Nombre oficial del municipio donde se ubica físicamente el aprovechamiento. |
| **`LOCALIDAD`** | `object` (String) | Nombre de la localidad, ejido o sitio geográfico de la extracción. |
| **`ACUIFERO`** | `object` (String) | Nombre oficial del acuífero o cuenca hidrológica delimitada por CONAGUA donde se extrae el recurso. |
| **`CUENCA`** | `object` (String) | Región hidrológica o cuenca a la que pertenece el aprovechamiento. |
| **`USO`** / **`USO_SUB`** | `object` (String) | Uso autorizado original reportado en el sistema (ej. *AGRÍCOLA*). |
| **`USO_LIMPIO`** | `object` (String) | *Variable derivada:* Columna estandarizada (mayúsculas, sin acentos ni espacios extra) utilizada para filtrar de forma robusta los registros agrícolas. |
| **`VOL_CONS`** | `float64` | **Volumen concesionado anual** (generalmente expresado en metros cúbicos anuales - $m^3/año$). Variable clave para análisis volumétricos. |
| **`FECHA_HASTA`** | `object` (Datetime) | Fecha de vigencia o caducidad del título de concesión (cuando está disponible en el registro). |
| **`LATITUD`** / **`LONGITUDE`** | `float64` | Coordenadas geográficas del punto de extracción (si el servicio las expone). |

---

## 3. Notas de Calidad y Tipado

* **Limpieza de Cadenas (`USO_LIMPIO`):** Los campos de texto provenientes de APIs gubernamentales suelen presentar inconsistencias de captura. El script incorpora una normalización por compresión ASCII para asegurar que ningún título agrícola quede fuera por errores tipográficos.
* **Valores Nulos o Vacíos (`NaN`):** Es común que algunos campos administrativos (como `LOCALIDAD` específica o fechas de término precisas) contengan valores nulos en el REPDA. Se recomienda validar la integridad de `VOL_CONS` y `MUNICIPIO` antes de realizar agrupaciones estadísticas (`groupby`).
* **Unidades de Volumen:** Asegúrate de verificar si el campo de volumen se encuentra en metros cúbicos ($m^3$) anuales al momento de cruzarlo con los datos climáticos o de superficie sembrada del SIAP.
