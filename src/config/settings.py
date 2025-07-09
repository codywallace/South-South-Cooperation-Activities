from dotenv import load_dotenv
import os
import sys

load_dotenv(".env.local")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("API_KEY not found in environment variables.")
    sys.exit(1)

search_terms = [
    "south south cooperation",
    "south-south cooperation",
    "south south triangular cooperation",
    "south-south triangular cooperation",
    "sstc",
    "south south and triangular cooperation",
    "south-south and triangular cooperation"
]

sector_code = 15250
