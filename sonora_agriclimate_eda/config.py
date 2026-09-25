from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# --- URLs de Fuentes Externas ---
SONORA_AGRICULTURE_URL = (
    "https://datos.sonora.gob.mx/dataset/3e17a7e8-c8d4-49c4-a426-4dec099cd0cd/"
    "resource/9e455a9c-1733-490e-ba3d-6117ffe4ffe5/download/"
    "agricultura-sonora-{year}.xlsx"
)

CONAGUA_BASE_URL = "https://smn.conagua.gob.mx/tools/RESOURCES/com_archivo_datos_resumenes"

CONAGUA_DROUGHT_URL = (
    "https://smn.conagua.gob.mx/tools/RESOURCES/"
    "Monitor de Sequia en Mexico/MunicipiosSequia.xlsx"
)

# --- Metadatos y Columnas ---
ID_VARS_CANDIDATES = [
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



# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
