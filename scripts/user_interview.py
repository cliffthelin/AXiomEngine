#!/usr/bin/env python3
"""
AXIOMENGINE USER INTELLIGENCE — "The Interview" (Phase 7)

Captures self-declared job role, expectations, and company-specific lingo
from the human operator, once, and persists it to `user_profile` so every
agent's system persona can be personalized without re-asking.

Usage:
  python3 user_interview.py            # run/redo the interview interactively
  python3 user_interview.py --status   # show whether a profile exists
"""
import asyncio
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

import asyncpg

from user_prompt import prompt_user

PG_DSN = "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"

QUESTIONS = [
    ("job_role", "What is your job role / title?", None),
    ("expectations", "What do you expect this AI system to help you with day-to-day?", None),
    ("lingo_raw", "List any company- or team-specific terms/acronyms and their meaning "
                  "(format: term=meaning, comma-separated; leave blank to skip)", None),
]


def _parse_lingo(raw: str) -> dict:
    lingo = {}
    for pair in raw.split(","):
        pair = pair.strip()
        if not pair or "=" not in pair:
            continue
        term, meaning = pair.split("=", 1)
        term, meaning = term.strip(), meaning.strip()
        if term:
            lingo[term] = meaning
    return lingo


async def run_interview(user_id: str = "default") -> dict:
    answers = {}
    for key, question, options in QUESTIONS:
        answers[key] = prompt_user(question, options)

    job_role = answers["job_role"]
    expectations = answers["expectations"]
    company_lingo = _parse_lingo(answers.get("lingo_raw", ""))

    conn = await asyncpg.connect(PG_DSN)
    try:
        await conn.execute(
            """INSERT INTO user_profile (user_id, job_role, expectations, company_lingo, raw_answers, interviewed_at, updated_at)
               VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
               ON CONFLICT (user_id) DO UPDATE SET
                 job_role = $2, expectations = $3, company_lingo = $4,
                 raw_answers = $5, interviewed_at = NOW(), updated_at = NOW()""",
            user_id, job_role, expectations, json.dumps(company_lingo), json.dumps(answers),
        )
    finally:
        await conn.close()

    print("\nUser Intelligence profile saved.")
    return {
        "job_role": job_role,
        "expectations": expectations,
        "company_lingo": company_lingo,
    }


async def get_profile(user_id: str = "default") -> dict | None:
    """Fetch the stored profile, if any. Used by agents to personalize their persona."""
    conn = await asyncpg.connect(PG_DSN)
    try:
        row = await conn.fetchrow("SELECT * FROM user_profile WHERE user_id = $1", user_id)
    finally:
        await conn.close()
    if not row or not row["interviewed_at"]:
        return None
    return {
        "job_role": row["job_role"],
        "expectations": row["expectations"],
        "company_lingo": json.loads(row["company_lingo"]) if isinstance(row["company_lingo"], str) else row["company_lingo"],
    }


def format_profile_context(profile: dict) -> str:
    """Render a profile as a system-persona injection block."""
    if not profile:
        return ""
    lines = ["<user_context>"]
    if profile.get("job_role"):
        lines.append(f"  Role: {profile['job_role']}")
    if profile.get("expectations"):
        lines.append(f"  Expectations: {profile['expectations']}")
    lingo = profile.get("company_lingo") or {}
    if lingo:
        lines.append("  Company lingo:")
        for term, meaning in lingo.items():
            lines.append(f"    - {term}: {meaning}")
    lines.append("</user_context>")
    return "\n".join(lines)


async def main():
    if "--status" in sys.argv:
        profile = await get_profile()
        if profile:
            print(format_profile_context(profile))
        else:
            print("No interview on file yet. Run without --status to conduct one.")
        return

    await run_interview()


if __name__ == "__main__":
    asyncio.run(main())
