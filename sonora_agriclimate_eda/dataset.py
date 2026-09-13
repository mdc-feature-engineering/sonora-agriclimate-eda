from pathlib import Path

import requests
from loguru import logger
from tqdm import tqdm
import typer

from sonora_agriclimate_eda.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR,
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    # ----------------------------------------------
    start_year: int = 2019,
    end_year: int = 2023,
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    input_path.mkdir(parents=True, exist_ok=True)

    #DATOS AGRICULTURA SONORA (Fuente: https://datos.sonora.gob.mx/dataset/agricultura-sonora)
    agricultura_sonora = (
        "https://datos.sonora.gob.mx/dataset/3e17a7e8-c8d4-49c4-a426-4dec099cd0cd/"
        "resource/9e455a9c-1733-490e-ba3d-6117ffe4ffe5/download/"
        "agricultura-sonora-{year}.xlsx"
    )

    years = range(start_year, end_year + 1)

    for year in tqdm(years, total=len(years)):
        url = agricultura_sonora.format(year=year)
        dest_file = input_path / f"agricultura-sonora-{year}.xlsx"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(dest_file, "wb") as f:
                f.write(response.content)

            logger.info(f"Downloaded {year} -> {dest_file}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to download {year}: {e}")

    logger.success("Processing dataset complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()