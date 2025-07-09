from typing import List, Dict, Any
from .codelists import get_codelist_label
from ..utils import setup_logger

logger = setup_logger("policy_marker_helpers")

def extract_policy_markers(activity: dict, lang: str = "en") -> list:
    codes = activity.get("policy_marker_code", [])
    vocabs = activity.get("policy_marker_vocabulary", [])
    sigs = activity.get("policy_significance", [])
    
    markers = []
    
    for idx, code in enumerate(codes):
        vocab = vocabs[idx] if idx < len(vocabs) else None
        sig = sigs[idx] if idx < len(sigs) else None
        
        marker_label = get_codelist_label(code, "PolicyMarker", lang)
        vocab_label = get_codelist_label(vocab, "PolicyMarkerVocabulary", lang) if vocab else None
        sig_label = get_codelist_label(sig, "PolicySignificance", lang) if sig else None
        
        marker = {
            "code": code,
            "label": marker_label,
            "vocabulary": vocab,
            "vocabulary_label": vocab_label or vocab,
            "significance": sig,
            "significance_label": sig_label or sig
        }
    
        markers.append(marker)
        
    logger.info(f"🧩 Extracted {len(markers)} policy markers from activity.")
    return markers
