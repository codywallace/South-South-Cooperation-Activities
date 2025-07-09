import requests
from pathlib import Path
import json
from ..config.paths import EN_CODELISTS_DIR, FR_CODELISTS_DIR
from ..utils import setup_logger

logger = setup_logger("codelist_loader")

def load_codelist(name: str, lang: str = "en") -> dict:

    directory = EN_CODELISTS_DIR if lang == "en" else FR_CODELISTS_DIR
    codelist_path = directory / f"{name}.json"

    if not codelist_path.exists():
        logger.warning(f"⚠️ Codelist {name} not found locally at {codelist_path}.")
        raise FileNotFoundError(f"Codelist {name} not found at {codelist_path}")

    logger.info(f"✅ Loading local codelist: {codelist_path}")
    try:
        with open(codelist_path, encoding="utf-8") as f:
            data = json.load(f)
            if "data" not in data:
                logger.error(f"❌ Invalid codelist format. Missing 'data' key in {name}.json")
                raise ValueError(f"Invalid codelist format in {name}.json")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"❌ Failed to load codelist {name}.json - Invalid JSON: {e}")
        raise

def get_codelist_label(code: str, list_name: str, lang: str = "en") -> str:
    """
    Retrieve the label of a given code from a specified codelist in the specified language.
    """
    logger.info(f"🔍 Fetching label for code '{code}' from codelist '{list_name}' in language '{lang}'.")
    codelist = load_codelist(list_name, lang=lang)

    for item in codelist.get("data", []):
        if item.get("code") == code:
            name = item.get("name")
            if isinstance(name, dict):
                label = name.get(lang, code)
                logger.info(f"✅ Found label: '{label}' for code '{code}' in '{list_name}'.")
                return label
            elif isinstance(name, str):
                logger.info(f"✅ Found label: '{name}' for code '{code}' in '{list_name}'.")
                return name

    logger.warning(f"⚠️ Code '{code}' not found in codelist '{list_name}'. Returning code as fallback.")
    return code
