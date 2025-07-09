import pytest
from src.utils.org_helpers import extract_participating_orgs

def test_extract_participating_orgs_basic():
    activity = {
        "participating_org_ref": ["AT-3", "ORG-456"],
        "participating_org_narrative": [["Federal Government of Austria"], ["Org Two"]],
        "participating_org_role": ["1", "2"],
        "participating_org_type": ["10", "21"]
    }

    result = extract_participating_orgs(activity, lang="en")

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0]["ref"] == "AT-3"
    assert result[0]["name"] == "Federal Government of Austria"
    assert result[0]["role_code"] == "1"
    assert result[0]["role_label"] == "Funding"
    assert result[0]["type_code"] == "10"
    assert result[0]["type_label"] == "Government"

    assert result[1]["ref"] == "ORG-456"
    assert result[1]["name"] == "Org Two"
    assert result[1]["role_code"] == "2"
    assert result[1]["role_label"] == "Accountable"
    assert result[1]["type_code"] == "21"
    assert result[1]["type_label"] == "International NGO"

def test_extract_participating_orgs_partial_data():
    activity = {
        "participating_org_ref": ["ORG-789"],
        "participating_org_narrative": [[]],
        "participating_org_role": ["2"]
    }

    result = extract_participating_orgs(activity)
    assert len(result) == 1
    assert result[0]["ref"] == "ORG-789"
    assert result[0]["name"] == "UNKNOWN"
    assert result[0]["role_code"] == "2"
    assert result[0]["role_label"] == "Accountable"

def test_extract_participating_orgs_no_data_infer_from_transactions():
    activity = {
        "transaction_receiver_org_ref": ["halo"],
        "transaction_receiver_org_narrative": ["Halo Trust"],
        "transaction_receiver_org_type": ["21"],
        "transaction_provider_org_ref": ["US-GOV-1"],
        "transaction_provider_org_narrative": ["USAID"],
        "transaction_provider_org_type": ["10"]
    }

    result = extract_participating_orgs(activity)

    assert isinstance(result, list)
    assert len(result) == 2

    implementer = next((org for org in result if org["role_code"] == "4"), None)
    funder = next((org for org in result if org["role_code"] == "1"), None)

    assert implementer is not None
    assert implementer["name"] == "Halo Trust"
    assert implementer["type_code"] == "21"
    assert implementer["type_label"] == "International NGO"

    assert funder is not None
    assert funder["name"] == "USAID"
    assert funder["type_code"] == "10"
    assert funder["type_label"] == "Government"

def test_extract_participating_orgs_invalid_codes():
    activity = {
        "participating_org_ref": ["XX-999"],
        "participating_org_narrative": [["Unknown Org"]],
        "participating_org_role": ["999"],
        "participating_org_type": ["999"]
    }

    result = extract_participating_orgs(activity)
    assert len(result) == 1
    assert result[0]["ref"] == "XX-999"
    assert result[0]["name"] == "Unknown Org"
    assert result[0]["role_code"] == "999"
    assert result[0]["role_label"] == "999"
    assert result[0]["type_code"] == "999"
    assert result[0]["type_label"] == "999"
