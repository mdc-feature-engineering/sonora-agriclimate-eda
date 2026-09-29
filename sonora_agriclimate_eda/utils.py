from pathlib import Path
import pandas as pd
from config import RAW_DATA_DIR, INTERIM_DATA_DIR, REFERENCES_DIR
import typer

app = typer.Typer(help="Comandos para generar los diccionarios de datos del proyecto.")

REF_DIR = REFERENCES_DIR


def make_sequia_conagua_data_dictionary():
    REF_DIR.mkdir(parents=True, exist_ok=True)
    output_md = REF_DIR / "data_dictionary_conagua_sequia.md"

    sample_files = list(INTERIM_DATA_DIR.glob("sonora_sequia_*.csv"))

    descriptions = {
        "Cve_Entidad": "Clave oficial de la entidad federativa.",
        "Entidad": "Nombre oficial de la entidad federativa.",
        "Cve_Municipio": "Clave oficial del municipio (INEGI).",
        "Municipio": "Nombre oficial del municipio.",
        "CVE_CONCATENADA": (
            "Clave concatenada única del municipio (Entidad + Municipio)."
        ),
        "CVE_ENT": "Clave de la entidad federativa en formato estandarizado.",
        "CVE_MUN": "Clave del municipio en formato estandarizado.",
        "NOMBRE_MUN": "Nombre oficial del municipio en mayúsculas.",
        "ORG_CUENCA": "Organismo de Cuenca donde se localiza el municipio.",
        "CLV_OC": "Clave de Organismo de Cuenca.",
        "CON_CUENCA": "Consejo de Cuenca donde se localiza el municipio.",
        "CVE_CONC": "Clave de Consejo de Cuenca.",
        "fecha": "Fecha correspondiente a la quincena de evaluación del monitor.",
        "categoria_sequia": ("Clasificación oficial de sequía (Sin Sequía, D0 a D4)."),
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
    print(f"¡Diccionario de sequía generado con éxito en: {output_md.resolve()}")


def make_hidrico_data_dictionary():
    REF_DIR.mkdir(parents=True, exist_ok=True)
    output_md = REF_DIR / "data_dictionary_hidrico_sonora.md"

    sample_files = list(RAW_DATA_DIR.glob("hidrico_sonora*.xlsx"))

    descriptions = {
        "Clave": (
            "Clave de la presa. Identifica la clave de una presa junto a su"
            " descripción (Catálogo_estatal)."
        ),
        "Fecha": "Fecha de captura de los recursos hídricos, en formato dd/mm/aaaa.",
        "Almacenamiento(hm³)": (
            "Volumen de agua en las presas, en hectómetros cúbicos (hm³)."
        ),
    }

    if sample_files:
        print(f"-> Leyendo estructura del archivo modelo: {sample_files[0].name}")
        df_sample = pd.read_excel(sample_files[0])
        column_dtypes = {col: str(df_sample[col].dtype) for col in df_sample.columns}
    else:
        print(
            "[AVISO] No se encontró archivo de recursos hídricos descargado. Usando"
            " estructura estándar predefinida..."
        )
        column_dtypes = {
            "Clave": "object",
            "Fecha": "datetime64[ns]",
            "Almacenamiento(hm³)": "float64",
        }

    lines = [
        "# Diccionario de Datos: Recursos Hídricos de Sonora\n",
        "## Descripción General",
        "Este documento detalla las variables del archivo de recursos hídricos de Sonora, que contiene el registro histórico de almacenamiento de agua en presas del estado.\n",
        "## Estructura de Variables del Dataset",
        "| Columna | Tipo de Dato | Descripción / Metadato Oficial |",
        "| :--- | :--- | :--- |",
    ]

    for col, dtype in column_dtypes.items():
        desc = descriptions.get(col, "Variable de metadatos o procesamiento.")
        lines.append(f"| `{col}` | `{dtype}` | {desc} |")

    output_md.write_text("\n".join(lines), encoding="utf-8")
    print(
        f"¡Diccionario de recursos hídricos generado con éxito en:"
        f" {output_md.resolve()}"
    )


def make_siap_agricola_data_dictionary():
    REF_DIR.mkdir(parents=True, exist_ok=True)
    output_md = REF_DIR / "data_dictionary_siap_agricola.md"

    sample_files = list(INTERIM_DATA_DIR.glob("*siap*.csv")) + list(
        INTERIM_DATA_DIR.glob("*produccion_agricola*.csv")
    )

    col_metadata = {
        "Anio": {
            "desc": "Año agrícola de cierre de producción.",
            "notes": (
                "• Rango válido: 2000 a presente.<br>• Sin valores nulos.<br>•"
                " En raw puede aparecer como `ANIO`."
            ),
        },
        "IdEstado": {
            "desc": "Clave numérica de la entidad federativa.",
            "notes": (
                "• Para Sonora es **estrictamente `26`**.<br>• Filtro primario de"
                " ingesta."
            ),
        },
        "Estado": {
            "desc": "Nombre oficial de la entidad federativa.",
            "notes": '• Texto estandarizado (ej. `"Sonora"`).',
        },
        "IdDdr": {
            "desc": "Clave del Distrito de Desarrollo Rural.",
            "notes": "• Identificador numérico SADER.",
        },
        "Ddr": {
            "desc": "Nombre del Distrito de Desarrollo Rural.",
            "notes": "• Inconsistencias ortográficas ocasionales.",
        },
        "IdMunicipio": {
            "desc": "Clave numérica del municipio (INEGI).",
            "notes": (
                "• Rango de 1 a 72 en Sonora.<br>• Base para la clave de cruce"
                " `CVE_MUN` (`26` + `IdMunicipio`)."
            ),
        },
        "Municipio": {
            "desc": "Nombre oficial del municipio.",
            "notes": "• Sensible a acentuación según el año agrícola.",
        },
        "Ciclo": {
            "desc": "Ciclo agrícola de producción.",
            "notes": (
                '• Valores esperados: `"Otoño-Invierno"`, `"Primavera-Verano"`,'
                ' `"Perennes"`.'
            ),
        },
        "Modalidad": {
            "desc": "Condición hídrica de siembra.",
            "notes": (
                '• Valores esperados: `"Riego"` o `"Temporal"`.<br>• Predominio'
                " de Riego en Sonora."
            ),
        },
        "Cultivo": {
            "desc": "Nombre específico del cultivo registrado.",
            "notes": '• Cadena de texto (ej. `"Trigo grano"`, `"Uva"`).',
        },
        "Sembrada": {
            "desc": "Superficie total sembrada expresada en hectáreas (ha).",
            "notes": "• Numérico `>= 0.0`. Sin comas de miles.",
        },
        "Cosechada": {
            "desc": "Superficie total cosechada expresada en hectáreas (ha).",
            "notes": "• Numérico `>= 0.0`. Regla: `Cosechada <= Sembrada`.",
        },
        "Siniestrada": {
            "desc": "Superficie afectada o siniestrada expresada en hectáreas (ha).",
            "notes": (
                "• Numérico `>= 0.0`. Indicador directo de afectación por"
                " sequía.<br>• Regla: `Sembrada ≈ Cosechada + Siniestrada`."
            ),
        },
        "Produccion": {
            "desc": "Volumen total de producción obtenido expresado en toneladas (ton).",
            "notes": "• Numérico `>= 0.0`. Si `Cosechada == 0`, debe ser `0.0`.",
        },
        "Rendimiento": {
            "desc": "Rendimiento medio obtenido por hectárea cosechada (ton/ha).",
            "notes": "• Numérico `>= 0.0`. Calculado como `Produccion / Cosechada`.",
        },
        "Pmr": {
            "desc": "Precio Medio Rural (MXN / tonelada).",
            "notes": "• Numérico `>= 0.0`.",
        },
        "Valor": {
            "desc": "Valor total de la producción (en miles de pesos mexicanos).",
            "notes": (
                "• Numérico `>= 0.0`. Calculado como `(Produccion * Pmr) / 1000`."
            ),
        },
    }

    if sample_files:
        print(f"-> Leyendo estructura del archivo modelo: {sample_files[0].name}")
        df_sample = pd.read_csv(sample_files[0], encoding="utf-8-sig")
        column_dtypes = {col: str(df_sample[col].dtype) for col in df_sample.columns}
    else:
        print(
            "[AVISO] No se encontró archivo SIAP procesado. Usando estructura"
            " estándar predefinida..."
        )
        column_dtypes = {
            "Anio": "int64",
            "IdEstado": "int64",
            "Estado": "object",
            "IdMunicipio": "int64",
            "Municipio": "object",
            "Ciclo": "object",
            "Modalidad": "object",
            "Cultivo": "object",
            "Sembrada": "float64",
            "Cosechada": "float64",
            "Siniestrada": "float64",
            "Produccion": "float64",
            "Rendimiento": "float64",
            "Valor": "float64",
        }

    lines = [
        "# Diccionario de Datos: Cierre de Producción Agrícola (SIAP - SADER)\n",
        "## Descripción general",
        (
            "Este conjunto de datos recopila la estadística oficial del Servicio"
            " de Información Agroalimentaria y Pesquera (SIAP) de la SADER."
            " Contiene el cierre de producción agrícola a nivel municipal"
            " desglosado por ciclo, modalidad hídrica y cultivo específico para"
            " el estado de Sonora.\n"
        ),
        "* **Fuente:** SIAP - SADER (Datos Abiertos / Cierre Agrícola).",
        "* **Cobertura espacial:** Municipios del estado de Sonora.",
        "* **Granularidad:** Municipal por cultivo, ciclo y modalidad.\n",
        "---\n",
        "## Estructura de variables\n",
        (
            "| Columna | Tipo de Dato | Descripción Detallada | Notas de Calidad y"
            " Validaciones |"
        ),
        "| :--- | :--- | :--- | :--- |",
    ]

    for col, dtype in column_dtypes.items():
        meta = col_metadata.get(
            col,
            {
                "desc": "Variable agrícola de producción.",
                "notes": "• Sin notas específicas registradas.",
            },
        )
        lines.append(f"| `{col}` | `{dtype}` | {meta['desc']} | {meta['notes']} |")

    lines.extend(
        [
            "\n---",
            "## Notas de calidad y tipado\n",
            (
                "1. **Tipado numérico (`float64` / `int64`):** Eliminar comas de"
                ' miles (ej. `"1,250.50"`) antes del moldeo. Las columnas de'
                " superficie, volumen y valor se fuerzan a `float64`, mientras que"
                " años y claves numéricas van como `int64`."
            ),
            (
                "2. **Codificación de caracteres (`UTF-8`):** Los archivos raw"
                " del SIAP suelen distribuirse en `latin1` o `cp1252`. Al generar el"
                " dataframe transformado, guardar explícitamente en `UTF-8`"
                " (`encoding='utf-8-sig'`) para evitar corrupción de caracteres con"
                ' tilde (ej. `"Bácum"`, `"Otoño-Invierno"`).'
            ),
            (
                "3. **Limpieza de textos (`object`):** Aplicar `.str.strip()` en"
                " variables categóricas (`Municipio`, `Cultivo`, `Ciclo`,"
                " `Modalidad`) para remover espacios iniciales o finales accidentalmente"
                " agregados en los registros del SIAP."
            ),
            (
                "4. **Estandarización clave INEGI (`CVE_MUN`):** Para realizar"
                " cruces con datasets climáticos o de sequía (CONAGUA), concatenar"
                " `IdEstado` (`26`) e `IdMunicipio` rellenado a 3 dígitos con ceros"
                " a la izquierda (ej. `26001` para Hermosillo)."
            ),
        ]
    )

    output_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"¡Diccionario SIAP Agrícola generado con éxito en: {output_md.resolve()}")


@app.command()
def conagua_dictionary():
    """Genera el diccionario de datos de CONAGUA (Sequía)."""
    make_sequia_conagua_data_dictionary()


@app.command()
def hidrico_dictionary():
    """Genera el diccionario de datos de recursos hídricos (presas)."""
    make_hidrico_data_dictionary()


@app.command()
def siap_dictionary():
    """Genera el diccionario de datos de SIAP."""
    make_siap_agricola_data_dictionary()


@app.command()
def all():
    """Genera todos los diccionarios del proyecto."""
    make_sequia_conagua_data_dictionary()
    make_hidrico_data_dictionary()
    make_siap_agricola_data_dictionary()


if __name__ == "__main__":
    app()
