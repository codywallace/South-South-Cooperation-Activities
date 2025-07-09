from collections import OrderedDict
import numpy as np 

DPORTAL_URL = "https://dportal.org/q.html?aid={}"

# Core headers
HEADERS = OrderedDict({
    'iati_identifier': str,
    'title': str,
    'reporting_org': str,
    'reporting_org_type': str,
    'aid_type': str,
    'finance_type': str,
    'flow_type': str,
    'provider_org': str,
    'provider_org_type': str,
    'receiver_org': str,
    'receiver_org_type': str,
    'transaction_type': str,
    'value_original': str,
    'currency_original': str,
    'value_usd': np.float64,
    'value_eur': np.float64,
    'value_local': np.float64,
    'exchange_rate_date': str,
    'exchange_rate': str,
    'transaction_date': str,
    'country_code': str,
    'multi-country': np.int32,
    'sector_code': str,
    'sector_category': str,
    'humanitarian': np.int32,
    'fiscal_year': np.int32,
    'fiscal_quarter': np.int32,
    'fiscal_year_quarter': str,
    'url': str 
})

MULTILANG_HEADERS = [
    'title',
    'reporting_org',
    'provider_org',
    'receiver_org'
]

# Activity-level headers
ACTIVITY_HEADERS = OrderedDict({
    'iati_identifier': str,
    'title': str,
    'description': str,
    'reporting_org': str,
    'reporting_org_ref': str,
    'location': str,
    'start_date': str,
    'end_date': str,
    'status_code': str,
    'humanitarian': np.int32,
    'default_currency': str,
    'default_aid_type': str,
    'default_finance_type': str,
    'default_flow_type': str,
    'activity_scope_code': str,
    'collaboration_type_code': str,
    'recipient_country_code': str,
    'recipient_region_code': str,
    'capital_spend': str,
    'conditions_attached': bool
})

ACTIVITY_MULTILANG_HEADERS = [
    'title',
    'description',
    'reporting_org'
]

# Budget headers
BUDGET_HEADERS = OrderedDict({
    'iati_identifier': str,
    'budget_type': str,
    'budget_status': str,
    'value': np.float64,
    'currency': str,
    'value_date': str,
    'start_date': str,
    'end_date': str
})

# Transaction-level headers
TRANSACTION_HEADERS = OrderedDict({
    'transaction_ref': str,
    'transaction_type': str,
    'transaction_date': str,
    'value': np.float64,
    'value_date': str,
    'currency': str,
    'provider_org': str,
    'provider_org_type': str,
    'receiver_org': str,
    'receiver_org_type': str,
    'sector_code': str,
    'sector_vocabulary': str,
    'recipient_country_code': str,
    'recipient_region_code': str,
    'aid_type': str,
    'finance_type': str,
    'flow_type': str,
    'tied_status': str,
    'disbursement_channel': str,
    'description': str
})

# Result indicator headers
RESULT_HEADERS = OrderedDict({
    'iati_identifier': str,
    'result_type': str,
    'result_title': str,
    'result_indicator_title': str,
    'result_indicator_description': str,
    'result_indicator_measure': str,
    'aggregation_status': str,
    'baseline': str,
    'indicator': str,
    'period_start': str,
    'period_end': str,
    'target_value': str,
    'actual_value': str
})

RESULT_MULTILANG_HEADERS = [
    'result_title',
    'result_indicator_title',
    'result_indicator_description'
]

# Document link headers
DOCUMENT_LINK_HEADERS = OrderedDict({
    'iati_identifier': str,
    'document_url': str,
    'document_format': str,
    'document_title': str,
    'document_language': str,
    'document_category': str
})

DOCUMENT_MULTILANG_HEADERS = [
    'document_title'
]

# Location headers
LOCATION_HEADERS = OrderedDict({
    'location_reach_code': str,
    'location_id_code': str,
    'location_id_vocabulary': str,
    'location_class_code': str,
    'exactness_code': str,
    'location_name': str,
    'location_description': str,
    'activity_description': str,
    'admin_level_1': str,
    'admin_level_2': str,
    'point_pos': str,
    'point_srs_name': str,
    'gazetteer_uri': str
})

# Policy marker headers
POLICY_MARKER_HEADERS = OrderedDict({
    'policy_marker_code': str,
    'policy_marker_vocabulary': str,
    'policy_marker_significance': str,
    'policy_marker_narrative': str,
    'policy_marker_narrative_xml_lang': str,
    'policy_marker_vocabulary_uri': str
})

# Participating organisation headers
PARTICIPATING_ORG_HEADERS = OrderedDict({
    'iati_identifier': str,
    'org_ref': str,
    'org_narrative': str,
    'org_type': str,
    'org_role': str,
    'crs_channel_code': str
})

PARTICIPATING_ORG_MULTILANG_HEADERS = [
    'org_narrative'
]

# Tag headers
TAG_HEADERS = OrderedDict({
    'iati_identifier': str,
    'tag_code': str,
    'tag_vocabulary': str,
    'tag_vocabulary_uri': str,
    'tag_narrative': str
})

TAG_MULTILANG_HEADERS = [
    'tag_narrative'
]

# Humanitarian scope headers
HUMANITARIAN_SCOPE_HEADERS = OrderedDict({
    'iati_identifier': str,
    'humanitarian_scope_type': str,
    'humanitarian_scope_code': str,
    'humanitarian_scope_vocabulary': str,
    'humanitarian_scope_narrative': str
})

HUMANITARIAN_SCOPE_MULTILANG_HEADERS = [
    'humanitarian_scope_narrative'
]

def headers(langs):
    out = []
    for header in HEADERS.keys():
        if header in MULTILANG_HEADERS:
            out += [f'{header}#{lang}' for lang in langs]
        else:
            out += [header]
    return out

def activity_headers(langs):
    out = [] 
    for header in ACTIVITY_HEADERS.keys():
        if header in ACTIVITY_MULTILANG_HEADERS:
            out += [f'{header}#{lang}' for lang in langs]
        else:
            out += [header]
    return out

def budget_headers():
    return list(BUDGET_HEADERS.keys())

def result_headers(langs):
    out = []
    for header in RESULT_HEADERS.keys():
        if header in RESULT_MULTILANG_HEADERS:
            out += [f'{header}#{lang}' for lang in langs]
        else:
            out += [header]
    return out

def document_link_headers(langs):
    out = []
    for header in DOCUMENT_LINK_HEADERS.keys():
        if header in DOCUMENT_MULTILANG_HEADERS:
            out += [f'{header}#{lang}' for lang in langs]
        else:
            out += [header]
    return out

def participating_org_headers(langs):
    out = []
    for header in PARTICIPATING_ORG_HEADERS.keys():
        if header in PARTICIPATING_ORG_MULTILANG_HEADERS:
            out += [f'{header}#{lang}' for lang in langs]
        else:
            out += [header]
    return out

def tag_headers(langs):
    out = []
    for header in TAG_HEADERS.keys():
        if header in TAG_MULTILANG_HEADERS:
            out += [f'{header}#{lang}' for lang in langs]
        else:
            out += [header]
    return out

def humanitarian_scope_headers(langs):
    out = []
    for header in HUMANITARIAN_SCOPE_HEADERS.keys():
        if header in HUMANITARIAN_SCOPE_MULTILANG_HEADERS:
            out += [f'{header}#{lang}' for lang in langs]
        else:
            out += [header]
    return out
