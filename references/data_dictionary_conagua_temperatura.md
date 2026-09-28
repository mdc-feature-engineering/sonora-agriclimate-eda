# Diccionario de Datos: Temperatura Media Nacional (CONAGUA / SMN)

## Descripción general

Este diccionario describe las variables disponibles en los archivos de temperatura media nacional (`AÑO-MES-01.csv`). El dataset contiene información sobre la temperatura media mensual (°C) registrada en distintas estaciones regionales de todo México, donde cada renglón representa el registro de una estación para el periodo correspondiente.

## Estructura de variables

| Variable | Tipo de dato | Formato | Unidad de medida | Descripción | Obligatoriedad | Catálogo de referencia | Identificador de valores nulos | Ejemplo de dato |
|---|---|---|---|---|---|---|---|---|
| `lon` | Numérico | `float` | grados decimales | longitud de la ubicación de la estación. | No especificado | — | No especificado | `-99.75` |
| `lat` | Numérico | `float` | grados decimales | latitud de la ubicación de la estación. | No especificado | — | No especificado | `16.76` |
| `clave` | Texto | `AAAAA` | — | clave de identificación única de la estación meteorológica. | No especificado | — | No especificado | `76805` |
| `edo` | Texto | `AAA` | — | entidad federativa. | No especificado | — | No especificado | `GRO` |
| `est` | Texto | Texto alfanumérico | — | nombre toponímico de la estación meteorológica. | No especificado | — | No especificado | `ACAPULCO` |
| `temp_promedio` | Numérico | `float` | grados Celsius (°C) | Temperatura media mensual registrada en la estación. | No especificado | — | No especificado | `27.441935` |
| `archivo_origen` | Texto | `aammdd*.csv` | — | nombre del archivo crudo CSV descargado del SMN | No especificado | — | No especificado | `201901010000TMed.csv` |
| `anio` | Numérico | `int` | `AAAA` | año de la observación | No especificado | — | No especificado | `2019` |
| `mes` | Numérico | `int` | `1 a 12` | mes de la observación | No especificado | — | No especificado | `1` |
| `fecha` | Temporal | `datetime` | `AAAA-MM-DD` | Fecha normalizada al primer día del mes | No especificado | — | No especificado | `2019-01-01` |

## Notas de calidad y tipado

- Cada fila o renglón corresponde a la observación puntual de una estación meteorológica durante el mes de análisis.
- Las variables `anio`, `mes` y `fecha` fueron derivadas a partir del nombre de `archivo_origen`.
- La variable `temp_promedio` almacena la medición de temperatura media mensual reportada para cada estación.