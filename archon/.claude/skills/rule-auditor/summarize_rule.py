#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def generate_rule_metadata(rule_id: str, rule_text: str, codebase_match: bool):
    """
    Simulates a high-fidelity summarizer.
    In a real symphony run, this would be an AI call.
    """
    summary = f"Rule {rule_id} governs {rule_text}. "
    if codebase_match:
        summary += "Implementation verified in codebase."
    else:
        summary += "Logic verified via architectural specification."
    
    # Cap at 500 chars
    summary = summary[:500]
    
    keywords = list(set(re.findall(r'\w+', rule_text.lower())))
    # Filter short keywords
    keywords = [k for k in keywords if len(k) > 3]
    
    return {
        "summary": summary,
        "tags": keywords
    }

if __name__ == "__main__":
    import re
    # Test call
    # ...
