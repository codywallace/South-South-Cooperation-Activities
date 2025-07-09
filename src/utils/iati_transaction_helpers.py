from typing import Dict, Any, List
from collections import defaultdict
from utils.date_utils import get_date
from utils.exchange_rates import value_in_usd
from utils.text import get_first


def get_codes_from_transactions(transactions, exchange_rates):
    unique_codes = set(t[0] for t in transactions)
    if len(unique_codes) == 1:
        return [{'code': next(iter(unique_codes)), 'percentage': 100.0}]

    unique_currencies = set(t[1] for t in transactions)
    if len(unique_currencies) != 1:
        transactions = [
            (
                code,
                'USD',
                value_in_usd(value=val, currency=cur, value_date=get_date(date), exchange_rates=exchange_rates),
                date
            )
            for code, cur, val, date in transactions
        ]

    total_value = sum(float(t[2]) for t in transactions)
    code_totals = defaultdict(float)
    for code, _, value, _ in transactions:
        code_totals[code] += (value / total_value) * 100.0

    return [{'code': code, 'percentage': pct} for code, pct in code_totals.items()]


def get_sectors_from_transactions(activity, default_currency, exchange_rates):
    txs = activity.get("transactions", [])
    filtered = [
        (tx.get("sector_code"), tx.get("currency", default_currency), float(tx.get("value", 0)), tx.get("value_date"))
        for tx in txs
        if tx.get("transaction_type") in ["2", "11"] and tx.get("sector_code")
    ]
    if not filtered:
        return [{'code': '', 'percentage': 100.0}]
    return get_codes_from_transactions(filtered, exchange_rates)


def get_countries_from_transactions(activity, default_currency, exchange_rates):
    txs = activity.get("transactions", [])
    filtered = [
        (
            tx.get("recipient_country_code") or tx.get("recipient_region_code"),
            tx.get("currency", default_currency),
            float(tx.get("value", 0)),
            tx.get("value_date")
        )
        for tx in txs
        if tx.get("transaction_type") in ["2", "11"] and (tx.get("recipient_country_code") or tx.get("recipient_region_code"))
    ]
    if not filtered:
        return []
    return get_codes_from_transactions(filtered, exchange_rates)


def get_classification_from_transactions(activity, default_currency, exchange_rates, field_name):
    field_map = {
        'aid_type': 'aid_type',
        'flow_type': 'flow_type',
        'finance_type': 'finance_type'
    }
    field_key = field_map.get(field_name)
    txs = activity.get("transactions", [])
    filtered = [
        (
            tx.get(field_key),
            tx.get("currency", default_currency),
            float(tx.get("value", 0)),
            tx.get("value_date")
        )
        for tx in txs
        if tx.get("transaction_type") in ["2", "11"] and tx.get(field_key)
    ]
    if not filtered:
        return [{'code': '', 'percentage': 100.0}]
    return get_codes_from_transactions(filtered, exchange_rates)


def normalize_transactions(activity: Dict[str, Any]) -> List[Dict[str, Any]]:
    transactions = []

    values = activity.get("transaction_value", [])
    dates = activity.get("transaction_transaction_date_iso_date", [])
    value_dates = activity.get("transaction_value_value_date", [])
    currencies = activity.get("default_currency", "")
    types = activity.get("transaction_transaction_type_code", [])

    sectors = activity.get("transaction_sector_code", []) or activity.get("sector_code", [])
    sector_vocab = activity.get("transaction_sector_vocabulary", []) or activity.get("sector_vocabulary", [])

    recipient_countries = activity.get("transaction_recipient_country_code", []) or activity.get("recipient_country_code", [])
    recipient_regions = activity.get("transaction_recipient_region_code", []) or activity.get("recipient_region_code", [])

    aid_types = activity.get("default_aid_type_code", [None])
    finance_type = activity.get("default_finance_type_code")
    flow_type = activity.get("default_flow_type_code")
    tied_statuses = activity.get("transaction_tied_status_code", [])
    default_tied_status = activity.get("default_tied_status_code")

    disbursement_channels = activity.get("transaction_disbursement_channel_code", [])
    descriptions = activity.get("transaction_description_narrative", [])

    provider_orgs = activity.get("reporting_org_ref", "")
    provider_org_type = activity.get("reporting_org_type")
    receiver_orgs = activity.get("transaction_receiver_org_narrative", [])
    receiver_org_type = activity.get("transaction_receiver_org_type", [])
    transaction_refs = activity.get("transaction_ref", [None] * len(values))

    for idx, value in enumerate(values):
        tx = {
            "transaction_ref": transaction_refs[idx] if idx < len(transaction_refs) else None,
            "transaction_type": types[idx] if idx < len(types) else None,
            "transaction_date": dates[idx] if idx < len(dates) else None,
            "value": value,
            "value_date": value_dates[idx] if idx < len(value_dates) else None,
            "currency": currencies,
            "receiver_org": receiver_orgs[idx] if idx < len(receiver_orgs) else None,
            "receiver_org_type": receiver_org_type[idx] if idx < len(receiver_org_type) else None,
            "provider_org": provider_orgs,
            "provider_org_type": provider_org_type,
            "sector_code": sectors[idx] if idx < len(sectors) else None,
            "sector_vocabulary": sector_vocab[idx] if idx < len(sector_vocab) else None,
            "recipient_country_code": recipient_countries[idx] if idx < len(recipient_countries) else None,
            "recipient_region_code": recipient_regions[idx] if idx < len(recipient_regions) else None,
            "aid_type": aid_types[0],
            "finance_type": finance_type,
            "flow_type": flow_type,
            "tied_status": tied_statuses[idx] if idx < len(tied_statuses) else default_tied_status,
            "disbursement_channel": disbursement_channels[idx] if idx < len(disbursement_channels) else None,
            "description": descriptions[idx] if idx < len(descriptions) else None
        }
        transactions.append(tx)

    return transactions
