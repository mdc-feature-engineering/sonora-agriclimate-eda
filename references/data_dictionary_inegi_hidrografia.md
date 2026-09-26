# Diccionario de Datos: Red Hidrográfica (INEGI) - Sonora

## 1. Guía de Extracción Manual (Archivos Pesados)
Debido al volumen de los datos vectoriales de INEGI (Escala 1:50,000), la ingesta recomendada sigue este flujo manual controlado:
1. **Descarga:** Acceder al [Banco de Información Geoespacial de INEGI](https://www.inegi.org.mx/app/mapas/).
2. **Capa Temática:** Seleccionar **Hidrografía** -> **Red Hidrográfica Edición 2.0** para el estado de Sonora.
3. **Almacenamiento:** Descomprimir el paquete vectorial dentro de la ruta `data/raw/inegi_hidrografia/` de tu proyecto.
4. **Procesamiento:** Utilizar `geopandas` en Python para recortar las capas utilizando los polígonos municipales de la Denominación de Origen del Bacanora.

## 2. Estructura de Variables del Vector Hidrográfico
| Columna / Atributo | Tipo de Dato | Descripción Técnica |
| :--- | :--- | :--- |
| `FID` | `int64` | Identificador único del segmento de red hidrográfica. |
| `NOMBRE` | `object` | Nombre oficial del río, arroyo o cuerpo de agua (cuando aplica). |
| `TIPO` | `object` | Condición de la corriente (Perenne, Intermitente, Canal, Cuerpo de agua). |
| `ORDEN` | `int64` | Orden de la corriente según la jerarquía de Strahler. |
| `LONGITUD` | `float64` | Longitud geométrica del segmento en metros o kilómetros. |
| `CVE_ENT` | `object` | Clave de la entidad federativa (Sonora = 26). |
| `geometry` | `geometry (LineString)` | Geometría vectorial lineal o poligonal (LineString / MultiLineString) en Sistema de Coordenadas WGS84 (EPSG:4326). |