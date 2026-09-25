from pathlib import Path
import pandas as pd
import requests
from loguru import logger
from tqdm import tqdm
import typer
import os  # Para crear las carpetas y construir las rutas de los archivos en el disco.
import requests  # Para realizar la conexión HTTP y descargar los archivos binarios.
import urllib3  # Para deshabilitar los avisos de certificados SSL de páginas de gobierno.
from config import (
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    SONORA_AGRICULTURE_URL,
    CONAGUA_BASE_URL,
    CONAGUA_DROUGHT_URL,
)

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)  # Desactivar avisos de certificados SSL no verificados.

app = typer.Typer()


@app.command()
def download_agriculture_data(start_year: int = 2019, end_year: int = 2024):
    """Descarga los datos de agricultura de Sonora por año."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    years = range(start_year, end_year + 1)

    for year in tqdm(years, total=len(years)):
        url = SONORA_AGRICULTURE_URL.format(year=year)
        dest_file = RAW_DATA_DIR / f"agricultura-sonora-{year}.xlsx"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(dest_file, "wb") as f:
                f.write(response.content)

            # logger.info(f"Downloaded agriculture {year} -> {dest_file}")
            logger.success(f"Año {year}: Descargado con éxito")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to download agriculture {year}: {e}")

    logger.success("Agriculture download complete.")


@app.command()
def download_drought_data(start_year: int = 2019, end_year: int = 2024):
    """Procesa el archivo crudo de sequía de CONAGUA y genera un archivo Tidy por cada año."""
    raw_path = RAW_DATA_DIR / "MunicipiosSequia.xlsx"
    interim_dir = PROCESSED_DATA_DIR.parent / "interim"
    interim_dir.mkdir(parents=True, exist_ok=True)

    # 1. Asegura que la carpeta exista y descarga directamente
    raw_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Iniciando descarga de datos de sequía desde: {CONAGUA_DROUGHT_URL}")

    try:
        raw_path.write_bytes(requests.get(CONAGUA_DROUGHT_URL, timeout=60).content)
        logger.success(f"¡Archivo descargado y guardado con éxito en: {raw_path}!")
    except requests.exceptions.RequestException as e:
        logger.error(f"[ERROR DE RED] No se pudo descargar el archivo: {e}")
        raise
    except Exception as e:
        logger.error(f"[ERROR INESPERADO] Ocurrió un error al guardar el archivo: {e}")
        raise

    # 2. Guarda copia local de archivo crudo
    logger.info(f"Leyendo el archivo crudo de CONAGUA desde {raw_path}...")
    df = pd.read_excel(raw_path, engine="openpyxl")

    # 3. Filtrar Sonora de forma segura (usando clave que empiece con '26')
    cve_col = next((c for c in df.columns if "CVE" in str(c).upper()), None)
    if cve_col:
        df_sonora = df[df[cve_col].astype(str).str.zfill(5).str.startswith("26")].copy()
    elif "Entidad" in df.columns:
        df_sonora = df[df["Entidad"].str.lower() == "sonora"].copy()
    else:
        df_sonora = df.copy()

    # 4. Identificar columnas fijas (metadatos) vs columnas de fechas (quincenas)
    id_vars_candidates = [
        "Cve_Entidad",
        "Entidad",
        "Cve_Municipio",
        "Municipio",
        "CVE_CONCATENADA",
        "CVE_ENT",
        "CVE_MUN",
        "MUNICIPIO",
        "Abrevia",
    ]
    id_vars = [c for c in df_sonora.columns if c in id_vars_candidates]

    # 5. Aplicar melt para pasar a formato largo (Tidy Data)
    logger.info("Transformando a formato largo (Tidy Data)...")
    df_melted = df_sonora.melt(
        id_vars=id_vars, var_name="fecha", value_name="categoria_sequia"
    )

    # 6. Limpiar y convertir fechas
    df_melted["fecha"] = pd.to_datetime(
        df_melted["fecha"], errors="coerce", format="mixed"
    )
    df_melted = df_melted.dropna(subset=["fecha"])

    # 7. Filtrar estrictamente el rango de años
    df_melted["Anio"] = df_melted["fecha"].dt.year
    df_filtered = df_melted[
        (df_melted["Anio"] >= start_year) & (df_melted["Anio"] <= end_year)
    ].copy()

    # 8. Añadir escala numérica de severidad
    severity_map = {"Sin Sequía": 0, "D0": 1, "D1": 2, "D2": 3, "D3": 4, "D4": 5}
    df_filtered["severidad_num"] = (
        df_filtered["categoria_sequia"].map(severity_map).fillna(0).astype(int)
    )

    # 9. Guardar un archivo CSV separado por cada año
    for year, df_year in df_filtered.groupby("Anio"):
        interim_path = INTERIM_DATA_DIR / f"sonora_sequia_{year}.csv"
        df_year.to_csv(interim_path, index=False, encoding="utf-8-sig")
        logger.success(f"Año {year}: Descargado con éxito")
        # logger.success(f"Guardado año {year} -> {interim_path.name} ({len(df_year)} registros)")

    logger.success("¡Proceso de sequía por año completado exitosamente!")


def download_rain_data(start_year: int = 2019, end_year: int = 2024):
    urllib3.disable_warnings(
        urllib3.exceptions.InsecureRequestWarning
    )  # Desactivar avisos de certificados SSL no verificados.

    # Definicion de la URL de la base de datos de lluvia del SMN (Servicio Meteorológico Nacional) de CONAGUA.
    # Ruta para guardar en data/raw/ subiendo un nivel desde la carpeta notebooks/
    # Usamos '..' para salir de notebooks/ hacia la raíz del proyecto

    main_folder = RAW_DATA_DIR
    os.makedirs(main_folder, exist_ok=True)

    # Cabecera HTTP estándar para simular una petición de navegador.
    headers = {"User-Agent": "Mozilla/5.0"}

    # Bucle for para recorrer cada año en el rango definido y descargar los archivos de lluvia correspondientes a cada mes.
    for current_year in range(start_year, end_year):
        year_str = str(current_year)
        logger.info(f"--- Descarga del año: {year_str} ---")
        # Creamos una subcarpeta para cada año (ej. ../data/raw/datos_lluvia_2019_2023/lluvia_2019)
        year_folder = os.path.join(main_folder, "lluvia_" + year_str)
        os.makedirs(year_folder, exist_ok=True)

        # Recorremos los meses del 1 al 12 (enero a diciembre)
        for month in range(1, 13):
            mes_str = str(month).zfill(2)
            file_name = (
                year_str + mes_str + "010000Lluv.csv"
            )  # Formato: [AÑO] + [MES] + 010000Lluv.csv
            file_url = (
                CONAGUA_BASE_URL + "/" + file_name
            )  # Url completa del archivo en el servidor
            local_path = os.path.join(
                year_folder, file_name
            )  # Ruta local final del archivo

            try:
                res = requests.get(
                    file_url, headers=headers, verify=False
                )  # Peticion GET al servidor

                if res.status_code == 200:
                    with open(local_path, "wb") as f:
                        f.write(res.content)
                    logger.success(
                        f"Año {year_str} | Mes {mes_str}: Descargado con éxito"
                    )
                else:
                    # Si el mes no está disponible en el servidor (ej. código 404)
                    logger.warning(
                        f"Año {year_str} | Mes {mes_str}: No disponible (Status {res.status_code})"
                    )
            except Exception as e:
                # Por si se interrumpe la conexión a internet
                logger.error("Error al descargar %s: %s", file_name, e)

    logger.success("Descargas de 2019 a 2023 completadas.")


@app.command()
def data_ingestion_pipeline(start_year: int = 2019, end_year: int = 2024):
    """Ejecuta la descarga de agricultura y el procesamiento de sequía en un solo paso."""
    logger.info("=== Iniciando pipeline completo de datos ===")

    # 1. Ejecutar descarga de datos de agricultura
    logger.info("Paso 1/3: Descargando datos de agricultura...")
    download_agriculture_data(start_year, end_year)

    # 2. Ejecutar descarga y preprocesamiento de sequía
    logger.info("Paso 2/3: Descargando y preprocesando datos de sequía...")
    download_drought_data(start_year, end_year)

    # 3. Ejecutar descarga de datos de lluvia
    logger.info("Paso 3/3: Descargando datos de lluvia...")
    download_rain_data(start_year, end_year)

    logger.success("¡Pipeline completo ejecutado con éxito!")


if __name__ == "__main__":
    app()
