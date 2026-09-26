from pathlib import Path
import pandas as pd
from config import RAW_DATA_DIR, INTERIM_DATA_DIR, REFERENCES_DIR

import typer

app = typer.Typer(
    help="Comandos para generar los diccionarios de datos del proyecto."
)

# Definir rutas según CCDS
#INTERIM_DATA_DIR = Path("data/interim")
REF_DIR = REFERENCES_DIR #Path("references")


def make_conagua_data_dictionary():
  REF_DIR.mkdir(parents=True, exist_ok=True)
  output_md = REF_DIR / "data_dictionary_conagua_sequia.md"

  # Buscar un archivo procesado de ejemplo para leer las columnas y tipos de datos
  sample_files = list(INTERIM_DATA_DIR.glob("sonora_sequia_*.csv"))

  # Diccionario con descripciones oficiales basadas en los metadatos de CONAGUA
  descriptions = {
      "Cve_Entidad": "Clave oficial de la entidad federativa.",
      "Entidad": "Nombre oficial de la entidad federativa.",
      "Cve_Municipio": "Clave oficial del municipio (INEGI).",
      "Municipio": "Nombre oficial del municipio.",
      "CVE_CONCATENADA": "Clave concatenada única del municipio (Entidad + Municipio).",
      "CVE_ENT": "Clave de la entidad federativa en formato estandarizado.",
      "CVE_MUN": "Clave del municipio en formato estandarizado.",
      "NOMBRE_MUN": "Nombre oficial del municipio en mayúsculas.",
      "ORG_CUENCA": "Organismo de Cuenca donde se localiza el municipio.",
      "CLV_OC": "Clave de Organismo de Cuenca.",
      "CON_CUENCA": "Consejo de Cuenca donde se localiza el municipio.",
      "CVE_CONC": "Clave de Consejo de Cuenca.",
      "fecha": "Fecha correspondiente a la quincena de evaluación del monitor.",
      "categoria_sequia": (
          "Clasificación oficial de sequía (Sin Sequía, D0 a D4)."
      ),
      "Anio": "Año extraído de la fecha de evaluación.",
      "severidad_num": (
          "Escala numérica de severidad asignada (0 = Sin Sequía hasta 5 = D4)."
      ),
  }

  if sample_files:
    print(f"-> Leyendo estructura del archivo modelo: {sample_files[0].name}")
    df_sample = pd.read_csv(sample_files[0])
    column_dtypes = {col: str(df_sample[col].dtype) for col in df_sample.columns}
  else:
    print(
        "[AVISO] No se encontraron archivos procesados. Usando estructura"
        " estándar predefinida..."
    )
    # Estructura por defecto con tipos de datos lógicos estimados
    default_columns = [
        "Cve_Entidad",
        "Entidad",
        "Cve_Municipio",
        "Municipio",
        "CVE_CONCATENADA",
        "CVE_ENT",
        "CVE_MUN",
        "NOMBRE_MUN",
        "ORG_CUENCA",
        "CLV_OC",
        "CON_CUENCA",
        "CVE_CONC",
        "fecha",
        "categoria_sequia",
        "Anio",
        "severidad_num",
    ]
    column_dtypes = {
        col: (
            "int64"
            if "Cve" in col or col == "Anio" or col == "severidad_num"
            else "object"
        )
        for col in default_columns
    }

  # Construcción del contenido en Markdown
  lines = [
      "# Diccionario de Datos: Monitor de Sequía CONAGUA - Sonora\n",
      "## Descripción General",
      "Este documento detalla las variables del dataset transformado a formato largo (Tidy Data) para el análisis de sequía por municipio en Sonora, basado en los reportes del Monitor de Sequía en México de CONAGUA.\n",
      "## Clasificación de Sequía (Monitor de Sequía)",
      "| Categoría | Descripción | Escala Numérica (`severidad_num`) |",
      "| :--- | :--- | :---: |",
      "| **Sin Sequía** | Condición normal sin afectación | `0` |",
      "| **D0** | Anormalmente Seco (preparación para sequía) | `1` |",
      "| **D1** | Sequía Moderada | `2` |",
      "| **D2** | Sequía Severa | `3` |",
      "| **D3** | Sequía Extrema | `4` |",
      "| **D4** | Sequía Excepcional | `5` |\n",
      "## Estructura de Variables del Dataset",
      "| Columna | Tipo de Dato | Descripción / Metadato Oficial |",
      "| :--- | :--- | :--- |",
  ]

  for col, dtype in column_dtypes.items():
    desc = descriptions.get(col, "Variable de metadatos o procesamiento.")
    lines.append(f"| `{col}` | `{dtype}` | {desc} |")

  output_md.write_text("\n".join(lines), encoding="utf-8")
  print(
      f"¡Diccionario de sequía generado con éxito en: {output_md.resolve()}"
  )

# Definir rutas según CCDS
#INTERIM_DATA_DIR = Path("data/interim")
REF_DIR = REFERENCES_DIR #Path("references")


def make_inegi_hidrografia_data_dictionary():
  REF_DIR.mkdir(parents=True, exist_ok=True)
  output_md = REF_DIR / "data_dictionary_inegi_hidrografia.md"

  # Buscar un archivo geoespacial procesado de ejemplo en interim o raw
  sample_files = list(INTERIM_DATA_DIR.glob("*rios*.geojson")) + list(
      INTERIM_DATA_DIR.glob("*hidrografia*.geojson")
  )

  # Diccionario con descripciones estándar de la Red Hidrográfica de INEGI
  descriptions = {
        "FID": "Identificador único del segmento de red hidrográfica.",
        "OBJECTID": "Identificador único del segmento de red hidrográfica.",
        "CVE": "Clave geoestadística o hidrográfica del elemento.",
        "NOMBRE": (
            "Nombre oficial del río, arroyo o cuerpo de agua (cuando aplica)."
        ),
        "TIPO": (
            "Condición de la corriente (Perenne, Intermitente, Canal, Cuerpo de"
            " agua)."
        ),
        "ORDEN": "Orden de la corriente según la jerarquía de Strahler.",
        "LONGITUD": "Longitud geométrica del segmento en metros o kilómetros.",
        "CVE_ENT": "Clave de la entidad federativa (Sonora = 26).",
        "geometry": (
            "Geometría vectorial lineal o poligonal (LineString / MultiLineString)"
            " en Sistema de Coordenadas WGS84 (EPSG:4326)."
        ),
  }

  if sample_files:
    print(
        f"-> Leyendo estructura del archivo geográfico modelo:"
        f" {sample_files[0].name}"
    )
    import geopandas as gpd

    df_sample = gpd.read_file(sample_files[0], rows=5)
    column_dtypes = {col: str(df_sample[col].dtype) for col in df_sample.columns}
  else:
    print(
        "[AVISO] No se encontró capa vectorial procesada. Usando estructura"
        " estándar de Red Hidrográfica INEGI..."
    )
    column_dtypes = {
        "FID": "int64",
        "NOMBRE": "object",
        "TIPO": "object",
        "ORDEN": "int64",
        "LONGITUD": "float64",
        "CVE_ENT": "object",
        "geometry": "geometry (LineString)",
    }

  # Construcción del contenido en Markdown
  lines = [
      "# Diccionario de Datos: Red Hidrográfica (INEGI) - Sonora\n",
      "## 1. Guía de Extracción Manual (Archivos Pesados)",
      "Debido al volumen de los datos vectoriales de INEGI (Escala 1:50,000), la ingesta recomendada sigue este flujo manual controlado:",
      "1. **Descarga:** Acceder al [Banco de Información Geoespacial de INEGI](https://www.inegi.org.mx/app/mapas/).",
      "2. **Capa Temática:** Seleccionar **Hidrografía** -> **Red Hidrográfica Edición 2.0** para el estado de Sonora.",
      "3. **Almacenamiento:** Descomprimir el paquete vectorial dentro de la ruta `data/raw/inegi_hidrografia/` de tu proyecto.",
      "4. **Procesamiento:** Utilizar `geopandas` en Python para recortar las capas utilizando los polígonos municipales de la Denominación de Origen del Bacanora.\n",
      "## 2. Estructura de Variables del Vector Hidrográfico",
      "| Columna / Atributo | Tipo de Dato | Descripción Técnica |",
      "| :--- | :--- | :--- |",
  ]

  for col, dtype in column_dtypes.items():
    desc = descriptions.get(
        col, "Atributo geoespacial secundario de la red."
    )
    lines.append(f"| `{col}` | `{dtype}` | {desc} |")

  output_md.write_text("\n".join(lines), encoding="utf-8")
  print(
      f"¡Diccionario de Hidrografía generado con éxito en:"
      f" {output_md.resolve()}"
  )

def make_repda_data_dictionary():
  REF_DIR.mkdir(parents=True, exist_ok=True)
  output_md = REF_DIR / "data_dictionary_repda_concesiones.md"

  # Buscar un archivo procesado de ejemplo del REPDA en interim
  sample_files = list(INTERIM_DATA_DIR.glob("*repda*.csv")) + list(
      INTERIM_DATA_DIR.glob("*concesiones*.csv")
  )

  # Diccionario con descripciones oficiales basadas en los atributos del MapServer de CONAGUA
  descriptions = {
      "FID": "Identificador único de registro del servidor cartográfico.",
      "ESTADO": "Clave o nombre de la entidad federativa (Sonora = 26).",
      "MUNICIPIO": "Nombre o clave del municipio de ubicación del aprovechamiento.",
      "USO_SUB": (
          "Uso oficial asignado al agua subterránea (Agrícola, Pecuario,"
          " Público Urbano, etc.)."
      ),
      "VOL_CONS": (
          "Volumen anual total concesionado para extracción (metros cúbicos /"
          " m³)."
      ),
      "TITULAR": "Nombre del titular, ejidatario o razón social de la concesión.",
      "NUMAUTORIZ": "Número de título o autorizaciones oficiales de derechos.",
      "FECHA_HASTA": "Fecha de vigencia o caducidad legal del título.",
      "ACUFERO": "Nombre oficial del acuífero regulado por CONAGUA.",
      "USO_LIMPIO": (
          "Variable derivada del pipeline para estandarizar y limpiar"
          " variaciones tipográficas en los usos durante el EDA."
      ),
  }

  if sample_files:
    print(f"-> Leyendo estructura del archivo modelo: {sample_files[0].name}")
    df_sample = pd.read_csv(sample_files[0])
    column_dtypes = {col: str(df_sample[col].dtype) for col in df_sample.columns}
  else:
    print(
        "[AVISO] No se encontró archivo REPDA procesado. Usando estructura"
        " estándar esperada..."
    )
    column_dtypes = {
        "FID": "int64",
        "ESTADO": "object",
        "MUNICIPIO": "object",
        "USO_SUB": "object",
        "VOL_CONS": "float64",
        "TITULAR": "object",
        "ACUFERO": "object",
        "USO_LIMPIO": "object",
    }

  # Construcción del contenido en Markdown
  lines = [
      "# Diccionario de Datos: REPDA - Concesiones de Agua Subterránea (CONAGUA)\n",
      "## 1. Contexto y Enfoque Analítico",
      "Este documento detalla la estructura del dataset de concesiones de agua subterránea extraído del REPDA (Registro Público de Derechos de Agua) para el estado de Sonora. Su propósito principal es permitir el filtrado por los municipios serranos con Denominación de Origen del Bacanora (DOT) para cuantificar títulos menores, volúmenes y presión hídrica en actividades agrícolas y pecuarias.\n",
      "## 2. Estructura de Variables del Dataset",
      "| Columna | Tipo de Dato | Descripción Técnica |",
      "| :--- | :--- | :--- |",
  ]

  for col, dtype in column_dtypes.items():
    desc = descriptions.get(
        col, "Variable de metadatos o atributos del título concesionado."
    )
    lines.append(f"| `{col}` | `{dtype}` | {desc} |")

  output_md.write_text("\n".join(lines), encoding="utf-8")
  print(
      f"¡Diccionario de REPDA generado con éxito en: {output_md.resolve()}"
  )

@app.command()
def conagua():
  """Genera el diccionario de datos de CONAGUA (Sequía)."""
  make_conagua_data_dictionary()


@app.command()
def inegi():
  """Genera el diccionario de datos de INEGI (Hidrografía)."""
  make_inegi_hidrografia_data_dictionary()


@app.command()
def repda():
  """Genera el diccionario de datos de REPDA (Concesiones)."""
  make_repda_data_dictionary()


@app.command()
def all():
  """Genera todos los diccionarios del proyecto."""
  make_conagua_data_dictionary()
  make_inegi_hidrografia_data_dictionary()
  make_repda_data_dictionary()


if __name__ == "__main__":
  app()