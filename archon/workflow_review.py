#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

# Add project root and scripts to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "scripts"))

try:
    from scripts.search_context import search_context
    from archon.archon import Archon
except ImportError as e:
    print(f"Import error: {e}")
    print("Ensure you are running this from the axiomengine root or have PYTHONPATH set.")
    sys.exit(1)

async def run_review(topic: str):
    archon = Archon()
    print(f"\n[WORKFLOW] Starting Automated Review: '{topic}'")
    print("-" * 60)
    
    # 1. Semantic Search for Context
    print("Step 1: Retrieving semantic context (files + rules)...")
    try:
        context = await search_context(topic, limit=3)
    except Exception as e:
        print(f"Search failed: {e}")
        return
    
    context_text = "### RELEVANT PDD RULES\n"
    for r in context['pdd_rules']:
        context_text += f"- **[{r['rule_id']}] {r['title']}**: {r['content']}\n"
    
    context_text += "\n### RELEVANT PROJECT FILES\n"
    for p in context['projects']:
        context_text += f"#### FILE: {p['path']} (Similarity: {p['similarity']:.3f})\n"
        context_text += "```\n" + p['snippet'] + "\n```\n"

    # 2. Execute Archon Planning / Review
    print("Step 2: Dispatching to ARCHON for architectural review...")
    
    review_prompt = (
        f"TASK: Perform a COMPREHENSIVE ARCHITECTURAL REVIEW for the topic: '{topic}'.\n\n"
        "GOVERNANCE CHECKLIST:\n"
        "1. Does the code/context violate any PDD rules cited below?\n"
        "2. Is the hardware isolation protocol maintained?\n"
        "3. Are there any 'silent failure' risks (R-PDD-CORE-004)?\n\n"
        f"{context_text}\n\n"
        "OUTPUT: Provide a 'PASS/FAIL' assessment followed by detailed architectural recommendations."
    )
    
    # Archon.plan_task prints the output to console
    archon.plan_task(review_prompt)

if __name__ == "__main__":
    # Default topic if none provided
    target_topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "GPU temperature monitoring and safety"
    asyncio.run(run_review(target_topic))
