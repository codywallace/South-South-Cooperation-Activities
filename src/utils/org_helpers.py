from typing import Dict, Any, List
from .text import clean_text
from .codelists import get_codelist_label
from .logging import setup_logger

logger = setup_logger("org_helpers")

def extract_participating_orgs(activity: Dict[str, Any], lang: str = "en") -> List[Dict[str, str]]:
    orgs = []

    refs = activity.get("participating_org_ref", [])
    names = activity.get("participating_org_narrative", [])
    roles = activity.get("participating_org_role", [])
    types = activity.get("participating_org_type", [])

    # fallback from transactions if no orgs present
    if not refs and ("transaction_receiver_org_narrative" in activity or "transaction_provider_org_narrative" in activity):
        tx_receiver_names = activity.get("transaction_receiver_org_narrative", [])
        tx_receiver_refs = activity.get("transaction_receiver_org_ref", [])
        tx_receiver_types = activity.get("transaction_receiver_org_type", [])

        for idx, name in enumerate(tx_receiver_names):
            ref = tx_receiver_refs[idx] if idx < len(tx_receiver_refs) else None
            ref_code = ref.split("-")[0] if ref and "-" in ref else ref

            orgs.append({
                "ref": ref,
                "name": name if isinstance(name, str) else name[0] if isinstance(name, list) and name else "UNKNOWN",
                "role_code": "4",
                "role_label": get_codelist_label("4", "OrganisationRole", lang),
                "type_code": tx_receiver_types[idx] if idx < len(tx_receiver_types) else None,
                "type_label": get_codelist_label(tx_receiver_types[idx], "OrganisationType", lang) if idx < len(tx_receiver_types) else None,
                "registration_agency": get_codelist_label(ref_code, "OrganisationRegistrationAgency", lang) if ref_code else None
            })

        tx_provider_names = activity.get("transaction_provider_org_narrative", [])
        tx_provider_refs = activity.get("transaction_provider_org_ref", [])
        tx_provider_types = activity.get("transaction_provider_org_type", [])

        for idx, name in enumerate(tx_provider_names):
            ref = tx_provider_refs[idx] if idx < len(tx_provider_refs) else None
            ref_code = ref.split("-")[0] if ref and "-" in ref else ref

            orgs.append({
                "ref": ref,
                "name": name if isinstance(name, str) else name[0] if isinstance(name, list) and name else "UNKNOWN",
                "role_code": "1",
                "role_label": get_codelist_label("1", "OrganisationRole", lang),
                "type_code": tx_provider_types[idx] if idx < len(tx_provider_types) else None,
                "type_label": get_codelist_label(tx_provider_types[idx], "OrganisationType", lang) if idx < len(tx_provider_types) else None,
                "registration_agency": get_codelist_label(ref_code, "OrganisationRegistrationAgency", lang) if ref_code else None
            })

        logger.info(f"📅 Extracted {len(orgs)} organizations from transaction fallbacks.")
        return orgs

    for idx, ref in enumerate(refs):
        name = None
        if idx < len(names):
            name_val = names[idx]
            if isinstance(name_val, list) and name_val:
                name = name_val[0]
            elif isinstance(name_val, str):
                name = name_val

        role_code = roles[idx] if idx < len(roles) else None
        type_code = types[idx] if idx < len(types) else None
        agency_code = ref.split("-")[0] if ref and "-" in ref else ref

        orgs.append({
            "ref": ref,
            "name": name or "UNKNOWN",
            "role_code": role_code,
            "role_label": get_codelist_label(role_code, "OrganisationRole", lang) if role_code else None,
            "type_code": type_code,
            "type_label": get_codelist_label(type_code, "OrganisationType", lang) if type_code else None,
            "registration_agency": get_codelist_label(agency_code, "OrganisationRegistrationAgency", lang) if agency_code else None
        })

    logger.info(f"📅 Extracted {len(orgs)} participating organizations.")
    return orgs
