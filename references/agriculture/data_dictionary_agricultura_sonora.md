# Diccionario de Datos: Agricultura de Sonora

## Descripción general

Este diccionario describe las variables disponibles en los archivos de agricultura de Sonora (`agricultura-sonora-AAAA.xlsx`). El dataset contiene información de superficie sembrada, cosechada y siniestrada, producción, rendimiento y valor económico de los cultivos registrados en el estado.

Los campos de catálogo, obligatoriedad, identificador de valores nulos y ejemplos de dato se documentan como `No especificado` cuando no fueron incluidos en la fuente proporcionada.

## Estructura de variables

| Variable | Tipo de dato | Formato | Unidad de medida | Descripción | Obligatoriedad | Catálogo de referencia | Identificador de valores nulos | Ejemplo de dato |
|---|---|---|---|---|---|---|---|---|
| `ANO` | Texto | `AAAA` | — | Año del registro de cultivo. | No especificado | — | No especificado | `2024` |
| `CIERREYAVAN` | Numérico | — | Cierre o avance de producción agrícola `AAAA` | Indica si el registro del cultivo corresponde a un dato de cierre o de avance de producción del año `AAAA`. | No especificado | — | No especificado | `CIERRE DE PRODUCCION AGRICOLA 2024` |
| `CICLO` | Numérico | `Int` | — | Código del ciclo de producción del cultivo registrado. | No especificado | `1` = Otoño-invierno; `2` = Primavera-verano; `3` = Perennes | No especificado | `3` |
| `CDDR` | Texto | `Int` | `CCC` | Clave numérica del Distrito de Desarrollo Rural (DDR) donde se registra el cultivo. | No especificado | — | No especificado | `001` |
| `NDDR` | Numérico | — | — | Descripción o nombre del Distrito de Desarrollo Rural (DDR) donde se registra el cultivo. | No especificado | — | No especificado | `Caborca` |
| `CMUN` | Texto | `Int` | `CC` | Clave numérica del municipio donde se registra el cultivo. | No especificado | — | No especificado | `01` |
| `NMUN` | Numérico | — | — | Nombre del municipio donde se registra el cultivo. | No especificado | — | No especificado | `Aconchi` |
| `CVMES` | Texto | `Int` | `CC` | Clave numérica del mes en que se registra el cultivo. | No especificado | — | No especificado | `01` |
| `NMES` | Numérico | — | — | Nombre del mes en que se registra el cultivo. | No especificado | — | No especificado | `Enero` |
| `CVECUL` | Texto | `Int` | — | Clave identificadora del cultivo. | No especificado | — | No especificado | `101` |
| `CULTIVO` | Numérico | — | — | Nombre del cultivo. | No especificado | — | No especificado | `Maíz grano` |
| `CVEVAR` | Texto | `Int` | — | Clave identificadora de la variedad del cultivo. | No especificado | — | No especificado | `001` |
| `DESVAR` | Numérico | — | — | Nombre o descripción de la variedad del cultivo. | No especificado | — | No especificado | `Blanco` |
| `SUPSEM` | Numérico | `Float` | Hectáreas | Cantidad de hectáreas sembradas. | No especificado | — | No especificado | `1250.50` |
| `SUPCOSE` | Numérico | `Float` | Hectáreas | Cantidad de hectáreas cosechadas. | No especificado | — | No especificado | `1200.00` |
| `SUPSINI` | Numérico | `Float` | Hectáreas | Cantidad de hectáreas siniestradas. | No especificado | — | No especificado | `50.50` |
| `PRODTON` | Numérico | `Float` | Toneladas | Producción total obtenida. | No especificado | — | No especificado | `3600.75` |
| `RENDMNTO` | Numérico | `Float` | Toneladas por hectárea | Rendimiento del cultivo, calculado como la producción obtenida por hectárea sembrada. | No especificado | — | No especificado | `3.00` |
| `PMR` | Numérico | `Float` | Pesos por tonelada | Precio Medio Rural (PMR). Se calcula como el cociente entre el valor total de producción y la producción obtenida en toneladas. | No especificado | — | No especificado | `4500.00` |
| `VALPROD` | No especificado | `Float` | Miles de pesos MXN | Valor total producido por cultivo. | No especificado | — | No especificado | `16203.38` |

## Notas de calidad y tipado

- Las variables `NDDR`, `NMUN`, `NMES`, `CULTIVO` y `DESVAR` fueron proporcionadas con tipo `Numérico`, aunque su descripción indica que contienen nombres o textos. Se recomienda verificar el tipo real leyendo los archivos Excel antes de realizar conversiones.
- `CIERREYAVAN` fue proporcionada como `Numérico`, pero su unidad y descripción indican que puede contener etiquetas textuales de cierre o avance. Se recomienda inspeccionar sus valores únicos.
- `VALPROD` no incluye tipo de dato en la información original; únicamente se especifica el formato `Float`.
- Las claves con ceros a la izquierda, como `CDDR`, `CMUN`, `CVMES` y `CVEVAR`, deben conservarse como texto para evitar perder su formato durante la lectura o exportación.
- Las unidades y categorías deben validarse contra los valores reales de cada archivo anual antes de usarlas en análisis o modelos.