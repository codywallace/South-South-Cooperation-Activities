from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
RAW_ACTIVITIES_DIR = RAW_DATA_DIR / "activities"
RAW_ACTIVITIES_DIR.mkdir(parents=True, exist_ok=True) 
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"
IATI_CODELISTS_DIR = DATA_DIR / "codelists"
EN_CODELISTS_DIR = IATI_CODELISTS_DIR / "203" / "codelists" / "downloads" / "clv3" / "json" / "en"
FR_CODELISTS_DIR = IATI_CODELISTS_DIR / "203" / "codelists" / "downloads" / "clv3" / "json" / "fr"

SRC_DIR = BASE_DIR / "src"

TESTS_DIR = BASE_DIR / "tests"

MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"
# CHECKPOINT_DIR = MODEL_DIR / "checkpoints"
