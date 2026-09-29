# Diccionario de Datos: Monitor de Sequía CONAGUA - Sonora

## Descripción General
Este documento detalla las variables del dataset transformado a formato largo (Tidy Data) para el análisis de sequía por municipio en Sonora, basado en los reportes del Monitor de Sequía en México de CONAGUA.

## Clasificación de Sequía (Monitor de Sequía)
| Categoría | Descripción | Escala Numérica (`severidad_num`) |
| :--- | :--- | :---: |
| **Sin Sequía** | Condición normal sin afectación | `0` |
| **D0** | Anormalmente Seco (preparación para sequía) | `1` |
| **D1** | Sequía Moderada | `2` |
| **D2** | Sequía Severa | `3` |
| **D3** | Sequía Extrema | `4` |
| **D4** | Sequía Excepcional | `5` |

## Estructura de Variables del Dataset
| Columna | Tipo de Dato | Descripción / Metadato Oficial |
| :--- | :--- | :--- |
| `CVE_CONCATENADA` | `int64` | Clave concatenada única del municipio (Entidad + Municipio). |
| `CVE_ENT` | `int64` | Clave de la entidad federativa en formato estandarizado. |
| `CVE_MUN` | `int64` | Clave del municipio en formato estandarizado. |
| `fecha` | `str` | Fecha correspondiente a la quincena de evaluación del monitor. |
| `categoria_sequia` | `str` | Clasificación oficial de sequía (Sin Sequía, D0 a D4). |
| `Anio` | `int64` | Año extraído de la fecha de evaluación. |
| `severidad_num` | `int64` | Escala numérica de severidad asignada (0 = Sin Sequía hasta 5 = D4). |