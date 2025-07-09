import os
import sys
import json
import pytest
from pathlib import Path

# 🧭 Add src/ to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.codelists import load_codelist, get_codelist_label
from src.config.paths import EN_CODELISTS_DIR, FR_CODELISTS_DIR


# ✅ Test: Load local codelist
def test_load_codelist():
    codelist_name = "TransactionType"

    # Load the codelist
    data = load_codelist(codelist_name)

    assert isinstance(data, dict)
    assert "data" in data

    # Verify known code exists
    codes = [item["code"] for item in data["data"]]
    assert "3" in codes

    print(f"✅ Successfully loaded codelist: {codelist_name}")


# ✅ Test: Get label for a known code
def test_get_codelist_label():
    label = get_codelist_label("3", "TransactionType", lang="en")
    assert label == "Disbursement"

    label_fr = get_codelist_label("3", "TransactionType", lang="fr")
    assert label_fr == "Décaissement"

    # Test for a non-existent code
    missing_label = get_codelist_label("9999", "TransactionType")
    assert missing_label == "9999"

    print("✅ Successfully retrieved codelist labels.")

