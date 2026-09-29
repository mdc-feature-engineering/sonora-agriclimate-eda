from pathlib import Path
import pandas as pd
import requests
from loguru import logger
from tqdm import tqdm
import typer
import os
import urllib3
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import io

from config import (
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    SONORA_AGRICULTURE_URL,
    CONAGUA_BASE_URL,
    CONAGUA_DROUGHT_URL,
    REPDA_URL_QUERY,
)

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)  # Disable warnings for unverified SSL certificates.

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

    output_dir = INTERIM_DATA_DIR / "sonora_sequia"

    # 1. Create the folder dynamically if it does not exist (with parents=True and exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
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

    # 2. Save a local copy of the raw file.
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

    # 4. Identify fixed columns (metadata) vs. date columns (fortnightly periods)
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

    # 5. Apply `melt` to convert to long format (Tidy Data).
    logger.info("Transformando a formato largo (Tidy Data)...")
    df_melted = df_sonora.melt(
        id_vars=id_vars, var_name="fecha", value_name="categoria_sequia"
    )

    # 6. Clean and convert dates
    df_melted["fecha"] = pd.to_datetime(
        df_melted["fecha"], errors="coerce", format="mixed"
    )
    df_melted = df_melted.dropna(subset=["fecha"])

    # 7. Filtrar estrictamente el rango de años
    df_melted["Anio"] = df_melted["fecha"].dt.year
    df_filtered = df_melted[
        (df_melted["Anio"] >= start_year) & (df_melted["Anio"] <= end_year)
    ].copy()

    # 8. Strictly filter the year range
    severity_map = {"Sin Sequía": 0, "D0": 1, "D1": 2, "D2": 3, "D3": 4, "D4": 5}
    df_filtered["severidad_num"] = (
        df_filtered["categoria_sequia"].map(severity_map).fillna(0).astype(int)
    )

    # 9. Save a separate CSV file for each year
    for year, df_year in df_filtered.groupby("Anio"):
        output_csv = output_dir / f"sonora_sequia_{year}.csv"
        df_year.to_csv(output_csv, index=False, encoding="utf-8-sig")
        logger.success(f"Año {year}: Descargado con éxito")

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
def download_temperature_data(start_year: int = 2019, end_year: int = 2024):
    """Descarga los archivos mensuales de temperatura media (TMed) directamente en data/raw/."""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # 1. Asegurar que la carpeta data/raw exista
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Cabeceras con Referer para evitar rechazos o Status 500 del servidor
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"),
        "Referer": (
            "https://smn.conagua.gob.mx/es/climatologia/temperaturas-y-lluvias/resumenes-mensuales-de-temperaturas-y-lluvias"
        ),
    }

    # 3. Recorrido por años y meses
    for current_year in range(start_year, end_year):
        year_str = str(current_year)
        logger.info(f"--- Descarga de temperatura del año: {year_str} ---")

        # Se crea directamente en data/raw/temperatura_XXXX
        year_folder = RAW_DATA_DIR / f"temperatura_{year_str}"
        year_folder.mkdir(parents=True, exist_ok=True)

        for month in range(1, 13):
            mes_str = str(month).zfill(2)
            file_name = f"{year_str}{mes_str}010000TMed.csv"
            file_url = f"{CONAGUA_BASE_URL.rstrip('/')}/{file_name}"
            local_path = year_folder / file_name

            # Si el archivo ya existe localmente, se omite
            if local_path.exists() and local_path.stat().st_size > 0:
                logger.info(f"Año {year_str} | Mes {mes_str}: Ya existe localmente")
                continue

            try:
                res = requests.get(file_url, headers=headers, verify=False, timeout=20)

                if res.status_code == 200:
                    with open(local_path, "wb") as f:
                        f.write(res.content)
                    logger.success(
                        f"Año {year_str} | Mes {mes_str}: Descargado con éxito"
                    )
                else:
                    logger.warning(
                        f"Año {year_str} | Mes {mes_str}: No disponible (Status"
                        f" {res.status_code})"
                    )

                # Pausa de cortesía para no saturar al SMN
                time.sleep(0.5)

            except Exception as e:
                logger.error(f"Error al descargar {file_name}: {e}")

    logger.success("Descargas de temperatura media completadas.")


def download_repda_data(batch_size=2000, max_workers=5):
    """Descarga de forma masiva y en paralelo las concesiones del REPDA para Sonora (ESTADO = 26)."""
    complete_csv_output = RAW_DATA_DIR / "repda_sonora_completo.csv"
    agricultural_csv_output = INTERIM_DATA_DIR / "repda_sonora_agricola.csv"
    output_parquet = RAW_DATA_DIR / "repda_sonora_completo.parquet"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://sigagis.conagua.gob.mx/",
    }
    where_clause = "ESTADO = 26"

    # 1. Check the total number of exact records
    logger.info("Consultando el número total de registros en Sonora...")
    count_params = {"where": where_clause, "returnCountOnly": "true", "f": "json"}
    try:
        r = requests.get(
            REPDA_URL_QUERY,
            params=count_params,
            headers=headers,
            verify=False,
            timeout=15,
        )
        total_records = r.json().get("count", 0)
    except Exception as e:
        logger.warning(f"Error al conectar con la API para obtener el conteo: {e}")
        return []

    logger.info(f"Total de registros a descargar: {total_records}")
    if total_records == 0:
        return []

    # 2. Internal function to download an individual batch with retries
    def fetch_chunk(offset):
        params = {
            "where": where_clause,
            "outFields": "*",
            "f": "json",
            "returnGeometry": "false",
            "resultRecordCount": batch_size,
            "resultOffset": offset,
            "orderByFields": "FID",
        }
        for _ in range(3):
            try:
                resp = requests.get(
                    REPDA_URL_QUERY,
                    params=params,
                    headers=headers,
                    verify=False,
                    timeout=20,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return [feat["attributes"] for feat in data.get("features", [])]
            except Exception:
                time.sleep(1)
        return []

    # 3. Perform bulk download using threads
    offsets = list(range(0, total_records, batch_size))
    all_features = []

    logger.info("Descargando todo Sonora en paralelo...")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_chunk, off): off for off in offsets}
        for future in as_completed(futures):
            res = future.result()
            if res:
                all_features.extend(res)
            logger.info(
                f"Registros descargados: {len(all_features)} / {total_records}",
                end="\r",
            )

    logger.success(
        "\n¡Descarga finalizada con éxito! Total de registros obtenidos:"
        f" {len(all_features)}"
    )

    if all_features:
        df_sonora = pd.DataFrame(all_features)

        if "FID" in df_sonora.columns:
            df_sonora = df_sonora.drop_duplicates(subset=["FID"])

        # 4. Save full data backup
        df_sonora.to_csv(complete_csv_output, index=False, encoding="utf-8-sig")
        df_sonora.to_parquet(output_parquet, index=False)
        logger.info(f"[1/2] Archivo completo guardado en: {complete_csv_output.name}")

        # 5. Detect water usage column and normalize text
        col_uso = None
        for c in ["USO_SUB", "USO", "USO_EXTRACCION"]:
            if c in df_sonora.columns:
                col_uso = c
                break

        if col_uso:
            df_sonora["USO_LIMPIO"] = (
                df_sonora[col_uso]
                .astype(str)
                .str.upper()
                .str.normalize("NFKD")
                .str.encode("ascii", errors="ignore")
                .str.decode("utf-8")
                .str.strip()
            )
            df_agricola = df_sonora[
                df_sonora["USO_LIMPIO"].str.contains("AGRICOLA", na=False)
            ].copy()
        else:
            df_agricola = df_sonora.copy()

        # 6. Save filtered file for agriculture
        df_agricola.to_csv(agricultural_csv_output, index=False, encoding="utf-8-sig")
        logger.info(
            f"[2/2] Archivo agrícola guardado en: {agricultural_csv_output.name}"
        )
        logger.info(f"Total de títulos con uso agrícola: {len(df_agricola)}")

    else:
        logger.warning("No se obtuvieron registros para procesar.")


def download_data_aquifers():
    """Descarga datos de mantos acuiferos en Sonora."""
    output_csv = RAW_DATA_DIR / "acuiferos_sonora.csv"

    url = "https://sigagis.conagua.gob.mx/gas1/sections/Edos/sonora/sonora.html"

    # 1. Headers to simulate a web browser and avoid blocking/redirection
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
            " like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        logger.info("Descargando página de CONAGUA...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verify that the request is successful (code 200)

        # 2. Use io.StringIO to read the HTML content downloaded with requests
        tables = pd.read_html(io.StringIO(response.text))

        if tables:
            # 3. Select the main aquifer table
            df_aquifers = tables[0]

            # 4. Save as CSV
            df_aquifers.to_csv(output_csv, index=False, encoding="utf-8-sig")
            logger.success(
                "\nArchivo guardado exitosamente como 'acuiferos_sonora.csv'"
            )
        else:
            logger.warning("No se encontraron tablas HTML en la página.")

    except Exception as e:
        logger.warning(f"Ocurrió un error al procesar la solicitud: {e}")


@app.command()
def data_ingestion_pipeline(start_year: int = 2019, end_year: int = 2024):
    """Ejecuta la descarga de agricultura y el procesamiento de sequía en un solo paso."""
    logger.info("=== Iniciando pipeline completo de datos ===")

    logger.info("Paso 1/6: Descargando datos de agricultura...")
    download_agriculture_data(start_year, end_year)

    logger.info("Paso 2/6: Descargando y preprocesando datos de sequía...")
    download_drought_data(start_year, end_year)

    logger.info("Paso 3/6: Descargando datos de lluvia...")
    download_rain_data(start_year, end_year)

    logger.info("Paso 4/6: Descargando datos de temperatura media...")
    download_temperature_data(start_year, end_year)

    logger.info("Paso 5/6: Descargando y preprocesando datos de REPDA...")
    download_repda_data()

    logger.info("Paso 6/6: Descargando y preprocesando datos de acuíferos...")
    download_data_aquifers()

    logger.success("¡Pipeline completo ejecutado con éxito!")


if __name__ == "__main__":
    app()
