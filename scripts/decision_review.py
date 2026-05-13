#!/usr/bin/env python3
"""
Decision Review Agent — Intake, Formalization & Impact Analysis
================================================================
Takes informal human statements and:
  1. Formalizes them into structured Decision records
  2. Cross-references against all governance layers
  3. Identifies conflicts, invalidations, and adaptations needed
  4. Produces a review package for human approval

Usage:
  python3 scripts/decision_review.py --project-root . \
    --statement "We should stop using the P40 at full power, it keeps crashing" \
    --context "GPU thermal monitoring showed repeated hangs above 85C" \
    --author "Infrastructure Lead"

  python3 scripts/decision_review.py --project-root . \
    --file path/to/informal_decision.txt \
    --author "Project Owner"
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Decision Review Agent")
    p.add_argument("--project-root", type=Path, default=Path("."),
                   help="Root directory of the project")
    p.add_argument("--statement", type=str, default=None,
                   help="Informal decision statement (natural language)")
    p.add_argument("--file", type=Path, default=None,
                   help="Path to a text file containing the informal decision")
    p.add_argument("--context", type=str, default="",
                   help="What prompted this decision (optional background)")
    p.add_argument("--author", type=str, default="Unknown",
                   help="Who is making this decision")
    p.add_argument("--apply", action="store_true",
                   help="If set, append the formalized decision to decisions.json")
    return p.parse_args()


def load_json(path):
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def extract_keywords(text):
    """Extract likely governance-relevant terms from informal text."""
    text_lower = text.lower()
    keywords = set()
    # Technical terms
    tech_patterns = [
        r'\b(gpu|cpu|model|inference|thermal|power|vram|memory)\b',
        r'\b(agent|session|workflow|pipeline|daemon|service)\b',
        r'\b(rule|policy|limit|threshold|constraint|require)\b',
        r'\b(deploy|build|test|audit|scan|validate)\b',
        r'\b(route|routing|port|endpoint|api)\b',
    ]
    for pattern in tech_patterns:
        keywords.update(m.group(1) for m in re.finditer(pattern, text_lower))

    # Action verbs that indicate governance intent
    actions = []
    action_patterns = [
        (r'\b(stop|disable|prevent|block|forbid)\b', "MUST_NOT"),
        (r'\b(must|require|always|enforce|mandate)\b', "MUST"),
        (r'\b(should|prefer|recommend|suggest)\b', "SHOULD"),
        (r'\b(allow|may|can|permit|optional)\b', "MAY"),
        (r'\b(deprecate|remove|replace|sunset|retire)\b', "DEPRECATE"),
        (r'\b(override|except|waive|bypass|ignore)\b', "OVERRIDE"),
    ]
    for pattern, modality in action_patterns:
        if re.search(pattern, text_lower):
            actions.append(modality)

    return keywords, actions


def find_matching_concepts(keywords, concepts):
    """Find DataConcepts whose aliases match extracted keywords."""
    matches = []
    for cid, concept in concepts.items():
        aliases = [a.lower() for a in concept.get("aliases", [])]
        name_words = concept.get("name", "").lower().split()
        all_terms = aliases + name_words
        overlap = keywords.intersection(all_terms)
        if overlap:
            matches.append({
                "concept_id": cid,
                "name": concept["name"],
                "matched_on": list(overlap),
                "match_strength": len(overlap),
            })
    matches.sort(key=lambda x: x["match_strength"], reverse=True)
    return matches


def find_conflicting_rules(keywords, actions, rules):
    """Find PDD rules that may conflict with the decision intent."""
    conflicts = []
    for rule in rules:
        scope = rule.get("scope", "").lower()
        title = rule.get("title", "").lower()
        rule_words = set(scope.split() + title.split())
        overlap = keywords.intersection(rule_words)
        if overlap:
            # Check for modality conflicts
            for action in actions:
                if action in ("MUST_NOT", "DEPRECATE", "OVERRIDE"):
                    conflicts.append({
                        "rule_id": rule["rule_id"],
                        "title": rule["title"],
                        "scope": rule["scope"],
                        "matched_on": list(overlap),
                        "potential_conflict": f"Decision may {action.lower()} behavior governed by this rule",
                    })
    return conflicts


def find_affected_decisions(keywords, decisions):
    """Find existing decisions that may be superseded or contradicted."""
    affected = []
    for dec in decisions:
        statement = dec.get("statement", "").lower()
        desc = dec.get("prompted_by", {}).get("description", "").lower()
        all_text = statement + " " + desc
        overlap = keywords.intersection(set(all_text.split()))
        if len(overlap) >= 2:
            affected.append({
                "decision_id": dec["decision_id"],
                "statement_preview": dec.get("statement", "")[:120],
                "matched_on": list(overlap),
                "relationship": "MAY_SUPERSEDE",
            })
    return affected


def infer_decision_type(actions):
    """Infer the decision type from detected action modalities."""
    if "OVERRIDE" in actions:
        return "Override"
    if "DEPRECATE" in actions:
        return "Deprecation"
    if "MUST_NOT" in actions:
        return "Override"
    return "Interpretation"


def infer_context_type(context, statement):
    """Infer what prompted this decision."""
    combined = (context + " " + statement).lower()
    if any(w in combined for w in ["crash", "hang", "fail", "error", "broke", "down"]):
        return "operational_observation"
    if any(w in combined for w in ["rule", "policy", "requirement", "axiom"]):
        return "rule_review"
    if any(w in combined for w in ["drift", "report", "score", "alignment"]):
        return "drift_finding"
    if any(w in combined for w in ["reversa", "found", "observed", "detected"]):
        return "reversa_finding"
    if any(w in combined for w in ["no rule", "gap", "undefined", "unclear"]):
        return "intent_gap"
    return "operational_observation"


def generate_decision_id(concepts, existing_decisions):
    """Generate a unique decision ID."""
    existing_ids = {d.get("decision_id", "") for d in existing_decisions}
    base = "DEC"
    if concepts:
        # Use first matched concept's short name
        concept_name = concepts[0]["concept_id"].replace("DC-", "")
        base = f"DEC-{concept_name}"

    seq = 1
    while f"{base}-{seq:03d}" in existing_ids:
        seq += 1
    return f"{base}-{seq:03d}"


def review(args):
    root = args.project_root.resolve()

    # Get the raw statement
    if args.file:
        raw_statement = args.file.read_text().strip()
    elif args.statement:
        raw_statement = args.statement
    else:
        print("❌ Provide --statement or --file")
        return

    print("=" * 72)
    print("  DECISION REVIEW AGENT — Intake & Impact Analysis")
    print(f"  Project Root: {root}")
    print("=" * 72)

    # Load governance data
    concepts_data = load_json(root / "data" / "data_concepts.json")
    concepts = {c["data_concept_id"]: c for c in concepts_data.get("concepts", [])}
    decisions_data = load_json(root / "data" / "decisions.json")
    existing_decisions = decisions_data.get("decisions", [])

    pdd_rules = []
    pdd_path = root / "pdd" / "load_rules.py"
    if pdd_path.exists():
        for m in re.finditer(r'\("(R-[^"]+)",\s*"([^"]+)",\s*"([^"]+)",', pdd_path.read_text()):
            pdd_rules.append({"rule_id": m.group(1), "scope": m.group(2), "title": m.group(3)})

    # === Phase 1: Extract & Analyze ===
    print(f"\n📝 Raw Statement:")
    print(f"   \"{raw_statement}\"")
    if args.context:
        print(f"\n📋 Context:")
        print(f"   \"{args.context}\"")

    keywords, actions = extract_keywords(raw_statement + " " + args.context)
    print(f"\n🔍 Extracted Keywords: {sorted(keywords)}")
    print(f"   Detected Modalities: {actions if actions else ['(none — will default to Interpretation)']}")

    # === Phase 2: Cross-Reference ===
    print(f"\n{'─' * 72}")
    print("  CROSS-REFERENCE ANALYSIS")
    print(f"{'─' * 72}")

    matched_concepts = find_matching_concepts(keywords, concepts)
    conflicting_rules = find_conflicting_rules(keywords, actions, pdd_rules)
    affected_decisions = find_affected_decisions(keywords, existing_decisions)

    if matched_concepts:
        print(f"\n  📌 Matching DataConcepts ({len(matched_concepts)}):")
        for mc in matched_concepts:
            print(f"     • {mc['concept_id']} — {mc['name']} (matched: {mc['matched_on']})")
    else:
        print(f"\n  ⚠️  No matching DataConcepts found.")
        print(f"     Consider creating a new DataConcept for this area.")

    if conflicting_rules:
        print(f"\n  ⚠️  Potentially Conflicting Rules ({len(conflicting_rules)}):")
        for cr in conflicting_rules:
            print(f"     • {cr['rule_id']} — {cr['title']}")
            print(f"       ↳ {cr['potential_conflict']}")
    else:
        print(f"\n  ✅ No conflicting PDD rules detected.")

    if affected_decisions:
        print(f"\n  🔄 Potentially Superseded Decisions ({len(affected_decisions)}):")
        for ad in affected_decisions:
            print(f"     • {ad['decision_id']} — \"{ad['statement_preview']}...\"")
            print(f"       ↳ Relationship: {ad['relationship']}")
    else:
        print(f"\n  ✅ No existing decisions appear affected.")

    # === Phase 3: Formalize ===
    decision_type = infer_decision_type(actions)
    context_type = infer_context_type(args.context, raw_statement)
    decision_id = generate_decision_id(matched_concepts, existing_decisions)
    bounded_area = matched_concepts[0]["concept_id"] if matched_concepts else "UNANCHORED"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    formalized = {
        "decision_id": decision_id,
        "decision_type": decision_type,
        "prompted_by": {
            "context_type": context_type,
            "description": args.context if args.context else "(no context provided — human should add)",
            "bounded_area": bounded_area,
            "evidence": []
        },
        "statement": raw_statement,
        "authority": args.author,
        "scope": {
            "applies_to": [
                {"entity_type": "DataConcept", "entity_id": mc["concept_id"]}
                for mc in matched_concepts[:3]
            ]
        },
        "effective": {
            "start_date": now,
            "end_date": None
        },
        "enforcement": "BestEffort" if decision_type == "Interpretation" else "Strict",
        "supersedes": [ad["decision_id"] for ad in affected_decisions]
    }

    print(f"\n{'─' * 72}")
    print("  FORMALIZED DECISION (Proposed)")
    print(f"{'─' * 72}")
    print(json.dumps(formalized, indent=2))

    # === Phase 4: Impact Summary ===
    print(f"\n{'─' * 72}")
    print("  IMPACT SUMMARY")
    print(f"{'─' * 72}")

    impacts = []
    if conflicting_rules:
        for cr in conflicting_rules:
            impacts.append(f"⚠️  Rule {cr['rule_id']} ({cr['title']}) may need to be ADAPTED or INVALIDATED")
    if affected_decisions:
        for ad in affected_decisions:
            impacts.append(f"🔄 Decision {ad['decision_id']} may be SUPERSEDED by this decision")
    if bounded_area == "UNANCHORED":
        impacts.append(f"📌 No DataConcept matched — consider creating one before formalizing")
    if not actions:
        impacts.append(f"ℹ️  No governance modality detected — defaulted to '{decision_type}'")

    if impacts:
        for impact in impacts:
            print(f"  {impact}")
    else:
        print(f"  ✅ No downstream impacts detected. Decision is additive.")

    # === Phase 5: Apply (if requested) ===
    if args.apply:
        existing_decisions.append(formalized)
        decisions_data["decisions"] = existing_decisions
        with open(root / "data" / "decisions.json", "w") as f:
            json.dump(decisions_data, f, indent=2)
        print(f"\n  ✅ Decision {decision_id} appended to data/decisions.json")
    else:
        print(f"\n  ℹ️  Dry run. Use --apply to persist this decision.")

    print(f"\n{'=' * 72}")
    return formalized


if __name__ == "__main__":
    args = parse_args()
    review(args)
