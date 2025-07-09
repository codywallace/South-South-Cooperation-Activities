import os
import sys
import json
import time
import requests
from dotenv import load_dotenv
from pathlib import Path

# 🧭 Add src/ to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config.settings import search_terms, sector_code
from src.config.paths import RAW_ACTIVITIES_DIR
from src.utils.text import slugify

load_dotenv(".env.local")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set.")

# 🔗 IATI API endpoint
activity_url = "https://api.iatistandard.org/datastore/activity/select?"
rows = 1000
format = "json"

# 🧠 Build search query
def build_mine_action_activity_query(terms, sector_code):
    fields = [
        "title_narrative",
        "description_narrative",
        "transaction_description_narrative",
        "transaction_sector_narrative"
    ]
    narrative_queries = [f'{field}:"{term}"' for term in terms for field in fields]
    narrative_query = " OR ".join(narrative_queries)
    return f"({narrative_query}) AND (sector_code:{sector_code} OR transaction_sector_code:{sector_code})"

# 🌍 Paginated IATI fetcher
def fetch_mine_action_activities(query):
    all_docs = []
    start = 0
    page_size = 1000

    while True:
        params = {
            "q": query,
            "rows": page_size,
            "start": start,
            "wt": format,
            "subscription-key": API_KEY
        }

        print(f"Fetching rows {start} to {start + page_size}...")
        response = requests.get(activity_url, params=params)
        print("Request URL:", response.url)

        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

        data = response.json()
        docs = data.get("response", {}).get("docs", [])
        if not docs:
            break

        all_docs.extend(docs)
        start += page_size
        time.sleep(0.5)

    print(f"Total records fetched: {len(all_docs)}")
    return {"response": {"docs": all_docs}}

# 🧪 Test: count unique IATI identifiers
def test_unique_iati_identifiers():
    query = build_mine_action_activity_query(search_terms, sector_code)
    data = fetch_mine_action_activities(query)

    docs = data.get("response", {}).get("docs", [])
    identifiers = [doc.get("iati_identifier") for doc in docs if "iati_identifier" in doc]
    unique_ids = set(identifiers)

    result = {
        "total_activities": len(docs),
        "unique_iati_identifiers": len(unique_ids)
    }

    print(json.dumps(result, indent=2))
    assert len(unique_ids) > 0

# 🧪 Test: save a single activity to disk
def test_sample_activity():
    query = build_mine_action_activity_query(search_terms, sector_code)
    data = fetch_mine_action_activities(query)
    
    docs = data.get("response", {}).get("docs", [])
    if not docs:
        print("No activity records found.")
        return

    activity = docs[1]  # Grab just one

    publisher = activity.get("reporting_org_ref", "UNKNOWN")
    publisher_slug = slugify(publisher) or "unknown"

    publisher_dir = RAW_ACTIVITIES_DIR / publisher_slug
    publisher_dir.mkdir(parents=True, exist_ok=True)

    iati_id = activity.get("iati_identifier", f"unknown_{int(time.time())}")
    filename = f"{iati_id}.json"
    filepath = publisher_dir / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(activity, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved activity {iati_id} to {filepath}")
    except Exception as e:
        print(f"❌ Error writing file {filepath}: {e}")
        assert False
