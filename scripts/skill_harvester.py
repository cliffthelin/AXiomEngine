#!/usr/bin/env python3
"""
AXIOMENGINE GOVERNED SKILL HARVESTER (Phase 7)

Mines `agent_audit` for workflows an agent has repeated successfully
(no drift, same rules cited, same agent) and drafts them into candidate
SKILL.md files. Nothing is auto-installed:

  1. `harvest()` finds recurring successful patterns and drafts a Skill.
  2. Each draft is run through `Governor.validate_proposal` (scripts/governor.py)
     so a harvested skill must itself be PDD-compliant before it can even
     be staged.
  3. Compliant drafts are written to `.pi/skills_pending/<name>/SKILL.md`
     (never into an active skills directory) and recorded in
     `skill_harvest_candidates` with status='pending'.
  4. `approve()` is the ONLY path that promotes a staged skill into the
     active `.pi/skills/` directory, and it must be invoked explicitly
     (CLI `--approve <name>` or a human action via the dashboard) —
     there is no auto-approval.
"""
import asyncio
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

import asyncpg

from governor import Governor

PG_DSN = "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"
STAGING_DIR = PROJECT_ROOT / ".pi" / "skills_pending"
ACTIVE_DIR = PROJECT_ROOT / ".pi" / "skills"
MIN_OCCURRENCES = 3  # a workflow must repeat this many times, drift-free, to qualify


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "harvested-skill"


class SkillHarvester:
    def __init__(self):
        self.governor = Governor(session_id="skill_harvest_session")

    async def find_candidates(self, conn) -> list[dict]:
        """Group non-drift audit rows by (agent_name, rules_cited) and keep
        combinations that repeated at least MIN_OCCURRENCES times."""
        rows = await conn.fetch(
            "SELECT agent_name, rules_cited FROM agent_audit "
            "WHERE drift_flag = FALSE AND agent_name IS NOT NULL"
        )
        counts = Counter((r["agent_name"], tuple(r["rules_cited"] or [])) for r in rows)
        return [
            {"agent_name": agent, "rules_cited": list(rules), "count": count}
            for (agent, rules), count in counts.items()
            if count >= MIN_OCCURRENCES
        ]

    def draft_skill_md(self, agent_name: str, rules_cited: list[str], count: int) -> tuple[str, str, str]:
        """Return (name, description, full SKILL.md content) for a candidate."""
        name = _slugify(f"{agent_name}-workflow")
        description = (
            f"Auto-harvested from {count} PDD-compliant runs of {agent_name}, "
            f"citing rules: {', '.join(rules_cited) if rules_cited else 'none'}."
        )
        content = (
            "---\n"
            f"name: {name}\n"
            f"description: {description}\n"
            "disable-model-invocation: true\n"  # staged skills never auto-trigger
            "---\n\n"
            f"# {name}\n\n"
            f"Harvested candidate from agent `{agent_name}`. This workflow succeeded "
            f"{count} consecutive times under PDD rules {rules_cited or '(none cited)'} "
            "without triggering drift.\n\n"
            "> This skill is a harvested DRAFT. It is not active until a human approves it "
            "via `skill_harvester.py --approve <name>`.\n"
        )
        return name, description, content

    async def harvest(self):
        conn = await asyncpg.connect(PG_DSN)
        try:
            candidates = await self.find_candidates(conn)
            print(f"SkillHarvester: found {len(candidates)} recurring workflow(s).")

            for c in candidates:
                name, description, content = self.draft_skill_md(
                    c["agent_name"], c["rules_cited"], c["count"]
                )

                existing = await conn.fetchval(
                    "SELECT candidate_id FROM skill_harvest_candidates WHERE name = $1 AND status = 'pending'",
                    name,
                )
                if existing:
                    print(f"SkillHarvester: '{name}' already pending, skipping.")
                    continue

                verdict = await self.governor.validate_proposal(
                    agent_name="SkillHarvester",
                    task=f"Harvest workflow skill for {c['agent_name']}",
                    proposal=content,
                )

                staged_path = None
                if verdict.strip().upper().startswith("PASS"):
                    skill_dir = STAGING_DIR / name
                    skill_dir.mkdir(parents=True, exist_ok=True)
                    (skill_dir / "SKILL.md").write_text(content)
                    staged_path = str(skill_dir / "SKILL.md")
                    print(f"SkillHarvester: staged '{name}' at {staged_path} (pending human approval).")
                else:
                    print(f"SkillHarvester: '{name}' rejected by Governor: {verdict}")

                await conn.execute(
                    """INSERT INTO skill_harvest_candidates
                       (name, description, source_agent, rules_cited, pattern_count,
                        content, staged_path, governor_verdict, status)
                       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)""",
                    name, description, c["agent_name"], c["rules_cited"], c["count"],
                    content, staged_path, verdict,
                    "pending" if staged_path else "rejected",
                )
        finally:
            await conn.close()

    async def approve(self, name: str):
        """Promote a staged, pending skill into the active skills directory.
        This is the only mutation of ACTIVE_DIR performed by this module, and
        it only runs when explicitly called."""
        conn = await asyncpg.connect(PG_DSN)
        try:
            row = await conn.fetchrow(
                "SELECT * FROM skill_harvest_candidates WHERE name = $1 AND status = 'pending' "
                "ORDER BY created_at DESC LIMIT 1",
                name,
            )
            if not row:
                print(f"No pending candidate named '{name}'.")
                return

            staged = Path(row["staged_path"])
            if not staged.exists():
                print(f"Staged file missing: {staged}")
                return

            active_dir = ACTIVE_DIR / name
            active_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(staged, active_dir / "SKILL.md")

            await conn.execute(
                "UPDATE skill_harvest_candidates SET status = 'approved', updated_at = NOW() WHERE candidate_id = $1",
                row["candidate_id"],
            )
            print(f"Approved and activated skill '{name}' at {active_dir / 'SKILL.md'}")
        finally:
            await conn.close()


async def main():
    harvester = SkillHarvester()
    if len(sys.argv) > 2 and sys.argv[1] == "--approve":
        await harvester.approve(sys.argv[2])
    else:
        await harvester.harvest()


if __name__ == "__main__":
    asyncio.run(main())
