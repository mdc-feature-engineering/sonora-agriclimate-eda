from pathlib import Path
import pandas as pd
import requests
from loguru import logger
from tqdm import tqdm
import typer

from sonora_agriclimate_eda.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def download_agriculture(
    start_year: int = 2019,
    end_year: int = 2023,
):
    """Descarga los datos de agricultura de Sonora por año."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    agricultura_sonora = (
        "https://datos.sonora.gob.mx/dataset/3e17a7e8-c8d4-49c4-a426-4dec099cd0cd/"
        "resource/9e455a9c-1733-490e-ba3d-6117ffe4ffe5/download/"
        "agricultura-sonora-{year}.xlsx"
    )

    years = range(start_year, end_year + 1)

    for year in tqdm(years, total=len(years)):
        url = agricultura_sonora.format(year=year)
        dest_file = RAW_DATA_DIR / f"agricultura-sonora-{year}.xlsx"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(dest_file, "wb") as f:
                f.write(response.content)

            logger.info(f"Downloaded agriculture {year} -> {dest_file}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to download agriculture {year}: {e}")

    logger.success("Agriculture download complete.")


@app.command()
def process_drought(
    start_year: int = 2018,
    end_year: int = 2025,
):
    """Procesa el archivo crudo de sequía de CONAGUA y lo convierte a formato Tidy."""
    raw_path = RAW_DATA_DIR / "MunicipiosSequia.xlsx"
    interim_dir = PROCESSED_DATA_DIR.parent / "interim"
    interim_dir.mkdir(parents=True, exist_ok=True)
    interim_path = interim_dir / "sonora_sequia_tidy.csv"

    if not raw_path.exists():
        logger.error(
            f"No se encontró el archivo de sequía en {raw_path}. Asegúrate de"
            " colocarlo en data/raw/."
        )
        raise typer.Exit(code=1)

    logger.info(f"Leyendo el archivo crudo de CONAGUA desde {raw_path}...")
    df = pd.read_excel(raw_path, engine="openpyxl")

    # 1. Filtrar Sonora de forma segura (usando clave que empiece con '26')
    cve_col = next((c for c in df.columns if "CVE" in str(c).upper()), None)
    if cve_col:
        df_sonora = df[df[cve_col].astype(str).str.zfill(5).str.startswith("26")].copy()
    elif "Entidad" in df.columns:
        df_sonora = df[df["Entidad"].str.lower() == "sonora"].copy()
    else:
        df_sonora = df.copy()

    # 2. Identificar columnas fijas (metadatos) vs columnas de fechas (quincenas)
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

    # 3. Aplicar melt para pasar a formato largo (Tidy Data)
    logger.info("Transformando a formato largo (Tidy Data)...")
    df_melted = df_sonora.melt(
        id_vars=id_vars, var_name="fecha", value_name="categoria_sequia"
    )

    # Limpiar y convertir fechas
    df_melted["fecha"] = pd.to_datetime(df_melted["fecha"], errors="coerce")
    df_melted = df_melted.dropna(subset=["fecha"])

    # 4. Filtrar estrictamente el rango de años
    df_melted["Anio"] = df_melted["fecha"].dt.year
    df_filtered = df_melted[
        (df_melted["Anio"] >= start_year) & (df_melted["Anio"] <= end_year)
    ].copy()

    # 5. Añadir escala numérica de severidad
    severity_map = {"Sin Sequía": 0, "D0": 1, "D1": 2, "D2": 3, "D3": 4, "D4": 5}
    df_filtered["severidad_num"] = (
        df_filtered["categoria_sequia"].map(severity_map).fillna(0).astype(int)
    )

    # 6. Guardar en la capa interim
    df_filtered.to_csv(interim_path, index=False, encoding="utf-8-sig")
    logger.success(
        f"¡Datos de sequía procesados y guardados con éxito en: {interim_path}!"
        f"\nDimensiones finales: {df_filtered.shape}"
    )


if __name__ == "__main__":
    app()
