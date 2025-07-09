
import requests
import json
import time

from src.config.settings import search_terms, API_KEY #sector_code
from src.config.paths import *
from src.utils import slugify, safe_filename, setup_logger


class SouthSouthCooperationExtractor:
    def __init__(self, api_key=API_KEY, base_url=None, rows=1000, delay=0.5):
        if not api_key:
            raise ValueError("API_KEY was not set successfully.")
        
        self.api_key = api_key
        self.activity_url = base_url or "https://api.iatistandard.org/datastore/activity/select?"
        self.rows = rows
        self.delay = delay
        self.logger = setup_logger("extract_south_south_cooperation_activities")
        
    def build_query(self, terms):
        fields = [
            "title_narrative",
            "description_narrative",
            "transaction_description_narrative",
            "transaction_sector_narrative",
            "result_indicator_description_narrative",
            "policy_marker_narrative",
            "participating_org_narrative"
        ]
        narrative_queries = [f'{field}:"{term}"' for term in terms for field in fields]
        narrative_query = " OR ".join(narrative_queries)
        return f"({narrative_query})"
    
    def fetch_activities(self, query):
        all_docs = []
        unique_ids = set()
        unique_publishers = set()
        start = 0
        
        while True:
            params = {
                "q": query,
                "rows": self.rows,
                "start": start,
                "wt": "json",
                "subscription-key": self.api_key
            }
            
            self.logger.info(f"Fetching rows {start} to {start + self.rows}...")
            response = requests.get(self.activity_url, params=params)
            self.logger.info(f"Request URL: {response.url}")
            
            if response.status_code != 200:
                self.logger.error(f"Failed to fetch: {response.status_code} - {response.text}")
                raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
            
            data = response.json()
            docs = data.get("response", {}).get("docs", [])
            
            if not docs:
                break
            
            all_docs.extend(docs)
            unique_ids.update(doc.get("iati_identifier") for doc in docs if "iati_identifier" in doc)
            unique_publishers.update(doc.get("reporting_org_ref") for doc in docs if "reporting_org_ref" in doc)
            
            start += self.rows
            time.sleep(self.delay)
            
        self.logger.info(f"✅ Total records fetched: {len(all_docs)}")
        self.logger.info(f"🆔 Unique IATI Identifiers: {len(unique_ids)}")
        self.logger.info(f"🏢 Unique Publishers: {len(unique_publishers)}")        
        
        return all_docs 
    
    def save_raw_activities(self, docs):
        if not docs:
            self.logger.warning("No documents to save.")
            return
        
        for activity in docs:
            publisher = activity.get("reporting_org_ref", "unknown")
            publisher_slug = slugify(publisher) or "unknown"
            publisher_dir = RAW_ACTIVITIES_DIR / publisher_slug
            publisher_dir.mkdir(parents=True, exist_ok=True)
            
            iati_id = activity.get("iati_identifier", f"unknown_{int(time.time())}")
            filename = f"{safe_filename(iati_id)}.json"
            file_path = publisher_dir / filename
            
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(activity, f, ensure_ascii=False, indent=2)
                self.logger.info(f"Saved: {file_path}")
            except Exception as e:
                self.logger.error(f"Error saving {file_path}: {e}")
                
    def run(self):
        query = self.build_query(search_terms)
        activities = self.fetch_activities(query)
        self.save_raw_activities(activities)
        self.logger.info(f"Data extraction completed and saved to {RAW_ACTIVITIES_DIR}")
        
if __name__ == "__main__":
    extractor = SouthSouthCooperationExtractor()
    extractor.run()
    
    