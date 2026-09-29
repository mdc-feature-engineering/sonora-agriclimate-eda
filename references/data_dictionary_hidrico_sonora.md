# Diccionario de Datos: Recursos Hídricos de Sonora

## Descripción general

Este diccionario describe las variables disponibles en el archivo de recursos hídricos de Sonora (`hidrico_sonora_2020-actualidad2024.xlsx`), que contiene el registro histórico de almacenamiento de agua en presas del estado.

## Estructura de variables

| Variable | Tipo de dato | Formato | Unidad de medida | Descripción | Identificadores | Catálogo de referencia | Detalle de relación con catálogos | Identificador de valores nulos | Ejemplo de dato |
|---|---|---|---|---|---|---|---|---|---|
| `Clave` | Texto | — | — | Clave de la presa. | `Clave` | `Catálogo_estatal` | Identifica la clave de una presa junto a su descripción. | Vacío | `LCDSO` |
| `Fecha` | Fecha | `dd/mm/aaaa` | — | Fecha de captura de los recursos hídricos. | — | — | — | Vacío | `01/01/2020` |
| `Almacenamiento(hm³)` | Numérico | — | Hectómetros cúbicos | Volumen de agua en las presas. | — | — | — | Vacío | `738.54` |

## Notas de calidad y tipado

- La columna `Almacenamiento(hm³)` contiene un símbolo especial en el nombre; al validarla con Pydantic se expone como `almacenamiento_hm3` mediante un alias.
- `Fecha` se documenta en formato `dd/mm/aaaa`; debe parsearse con día primero (`dayfirst=True`) para evitar confundir día y mes.
- `Clave` identifica la presa y debe cruzarse con el catálogo estatal de presas para obtener su nombre completo.
