from typing import Dict, Any
from utils.text import clean_text
from utils.variables import ACTIVITY_HEADERS
from utils.iati_transaction_helpers import normalize_transactions
from utils.iati_budget_helpers import normalize_budgets
from utils.org_helpers import extract_participating_orgs
from utils.geo_utils import extract_location_data
from utils.document_helpers import extract_documents
from utils.result_helpers import extract_results
from utils.policy_marker_helpers import extract_policy_markers
from utils.tag_helpers import extract_tags
from utils.humanitarian_scope_helpers import extract_humanitarian_scope


def normalize_activity(activity: Dict[str, Any]) -> Dict[str, Any]:

    iati_id = activity.get("iati_identifier", "UNKNOWN")
    reporting_org_id = activity.get("reporting_org_ref", "UNKNOWN")
    reporting_org_type = activity.get("reporting_org_type")

    reporting_org = clean_text(
        activity.get("reporting_org_narrative", [None])[0] 
        if activity.get("reporting_org_narrative") else None
    )

    title = clean_text(
        activity.get("title_narrative", [None])[0]
        if activity.get("title_narrative") else None
    )

    description = clean_text(
        activity.get("description_narrative", [None])[0]
        if activity.get("description_narrative") else None
    )

    normalized = {
        "iati_identifier": iati_id,
        "reporting_org": reporting_org,
        "reporting_org_type": reporting_org_type,
        "title": title,
        "description": description,
        "default_currency": activity.get("default_currency"),
        "default_flow_type": activity.get("default_flow_type_code"),
        "default_aid_type": activity.get("default_aid_type_code", [None])[0],
        "default_finance_type": activity.get("default_finance_type_code"),
        "default_tied_status": activity.get("default_tied_status_code"),
        "activity_scope_code": activity.get("activity_scope_code"),
        "collaboration_type_code": activity.get("collaboration_type_code"),
        "recipient_country_code": activity.get("recipient_country_code", [None])[0],
        "recipient_region_code": activity.get("recipient_region_code", [None])[0] if "recipient_region_code" in activity else None,
        "conditions_attached": activity.get("conditions_attached", False),
        "status_code": activity.get("activity_status_code"),
        "start_date": activity.get("activity_date_iso_date", [None])[0],
        "end_date": activity.get("activity_date_iso_date", [None])[1] if len(activity.get("activity_date_iso_date", [])) > 1 else None
    }

    # Normalize transactions
    normalized["transactions"] = normalize_transactions(activity)

    # Budgets
    normalized["budgets"] = normalize_budgets(activity)

    # Participating orgs
    normalized["participating_orgs"] = extract_participating_orgs(activity)

    # Locations
    normalized["locations"] = extract_location_data(activity)

    # Documents
    normalized["documents"] = extract_documents(activity)

    # Results
    normalized["results"] = extract_results(activity)

    # Policy markers
    normalized["policy_markers"] = extract_policy_markers(activity)

    # Tags
    normalized["tags"] = extract_tags(activity)

    # Humanitarian Scope
    normalized["humanitarian_scope"] = extract_humanitarian_scope(activity)

    return normalized
