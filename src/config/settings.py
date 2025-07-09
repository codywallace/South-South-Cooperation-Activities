from dotenv import load_dotenv
import os
import sys

load_dotenv(".env.local")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("API_KEY not found in environment variables.")
    sys.exit(1)

search_terms = [
    "mine action",
    "risk education",
    "victims assistance",
    "explosive ordnance",
    "explosive remnants of war",
    "ERW",
    "improvised explosive device",
    "IEDs",
    "explosive hazards",
    "landmine",
    "demining",
    "de-mining",
    "humanitarian mine action",
    "humanitarian demining",
    "explosive hazard clearance",
    "survey and clearance"
]

sector_code = 15250
