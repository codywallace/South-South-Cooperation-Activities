import pytest
from src.utils.policy_marker_helpers import extract_policy_markers


def test_extract_policy_markers_basic():
    activity = {
        "policy_marker_code": ["1", "8"],
        "policy_marker_vocabulary": ["1", "2"],
        "policy_marker_significance": ["1", "2"]
    }

    result = extract_policy_markers(activity, lang="en")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["label"] == "Gender Equality"
    assert result[0]["vocabulary_label"] == "OECD DAC CRS"
    assert "significance_label" in result[0]


def test_extract_policy_markers_missing_fields():
    activity = {
        "policy_marker_code": ["2"]
        # Missing vocabulary and significance
    }

    result = extract_policy_markers(activity, lang="en")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["label"] == "Aid to Environment"
    assert result[0]["vocabulary_label"] is None
    assert result[0]["significance_label"] is None

