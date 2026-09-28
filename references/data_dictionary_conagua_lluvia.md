# Diccionario de Datos: Agricultura de Sonora

## Descripción general

Este diccionario describe las variables disponibles en los archivos de lluvias nacionales(`AÑO-MES-01.csv`). El dataset contiene información sobre la precipitación mensual (mm) registrada en distintas estaciones regionales de todo México. 

## Estructura de variables

| Variable | Tipo de dato | Formato | Unidad de medida | Descripción | Obligatoriedad | Catálogo de referencia | Identificador de valores nulos | Ejemplo de dato |
|---|---|---|---|---|---|---|---|---|
| `lon` | Numérico | `float` | grados decimales | longitud de la ubicación de la estación. | No especificado | — | No especificado | `-102.309722` |
| `lat` | Numérico | `float` | grados decimales | latitud de la ubicación de la estación. | No especificado | — | No especificado | `22.188611` |
| `edo` | Texto | `AAA` | — | entidad federativa. | No especificado | — | No especificado | `SON` |
| `clave` | Texto | `AAAAA` | — | clave de identificación única de la estación meteorológica. | No especificado | — | No especificado | `ALMAG` |
| `estacion` | Texto | Texto alfanumérico(`[Nombre], [Abrev_Estado] [Red/Operador]*`) | — | nombre toponímico de la estación de monitoreo y su abreviatura estatal. | No especificado | — | No especificado | `Calvillo, Ags. SMN*` |
| `precipitacion_mm` | Numérico | `float` | milímetros (mm) | Precipitación mensual acumulada registrada. | No especificado | — | No especificado |`11.50`|
| `periodo` | Texto | `mes-aa` | — | norme original del mes y año del resgistro del SMN | No especificado | — | No especificado |`ene-19`|
| `archivo_origen` | Texto | `aammdd*.csv` | — | nombre del archivo crudo CSV descargado del SMN | No especificado | — | No especificado |`201901010000Lluv.csv`|
| `anio` | Numérico | `int` | `AAAA` | año de la observación | No especificado | — | No especificado |`2021`|
| `mes` | Numérico | `int` | `1 a 12` | mes de la observación | No especificado | — | No especificado |`2`|
| `fecha` | Fecha/Hora | `datetime` | `AAAA-MM-DD` | Fecha normalizada al primer día del mes| No especificado | — | No especificado |`2020-01-01`|

## Notas de calidad y tipado

- **Variables temporales derivadas:** Las variables `anio`, `mes` y `fecha` fueron construidas a partir de los metadatos contenidos en el nombre de `archivo_origen` para asegurar consistencia cronológica en el análisis de series de tiempo.
- **Normalización de mediciones:** La variable `precipitacion_mm` corresponde a la columna que en el archivo crudo variaba dinámicamente de nombre (ej. `ene-19`, `feb-19`). Se estandarizó su nombre y se respaldó la etiqueta original en la columna `periodo`.
- **Tratamiento de nulos:** Los registros sin medición de precipitación o con valores atípicos de lectura se preservan como `NaN` en Pandas para no sesgar el cálculo de medias y acumulados.
