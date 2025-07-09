import re
import unicodedata

import re

def clean_text(text: str) -> str:
    """
    Clean the text by removing extra spaces and other unwanted characters.
    
    """
    if not isinstance(text, str):
        return ""
    return re.sub(r'\s+', ' ', text).strip()


def slugify(text: str) -> str:
    """
    Converting string to URL slug
    """
    text = str(text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)

def safe_filename(text: str) -> str:
    """
    Convert a string to a safe filename by removing invalid characters.
    """
    text = str(text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[\\/:\*\?\"<>\|]", "_", text)     
    text = re.sub(r"\s+", "-", text)                 
    return text.strip().lower()   

def normalize(text: str) -> str:
    """
    Normalize the text by removing extra spaces and converting to lowercase.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()

def normalize_url(url: str) -> str:
    """
    Normalize the URL by removing trailing slashes and converting to lowercase.
    """
    url = url.rstrip("/")
    return url.lower()

