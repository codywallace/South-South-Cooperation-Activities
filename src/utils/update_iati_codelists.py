import requests
import zipfile
import os
import json
from pathlib import Path
from ..config.paths import IATI_CODELISTS_DIR
from ..utils import setup_logger

logger = setup_logger("iati_codelist_updater")

ZIP_URL = "https://github.com/IATI/IATI-Reference-Generator/releases/download/v1.23/downloads.zip"

def update_codelists():
    logger.info("Downloading the latest codelists zip file...")
    response = requests.get(ZIP_URL)

    if response.status_code != 200:
        logger.error(f"Failed to download codelists: {response.status_code}")
        return

    zip_path = IATI_CODELISTS_DIR / "codelists.zip"

    with open(zip_path, "wb") as f:
        f.write(response.content)

    logger.info("Extracting codelists...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(IATI_CODELISTS_DIR)

    # Format all JSON files
    for root, _, files in os.walk(IATI_CODELISTS_DIR):
        for file in files:
            if file.endswith(".json"):
                json_path = Path(root) / file
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Re-save with formatted JSON
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info("✅ Codelists updated and formatted.")


if __name__ == "__main__":
    update_codelists()
