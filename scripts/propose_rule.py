#!/usr/bin/env python3
import asyncpg
import asyncio
import sys
from typing import Optional

PG_DSN = "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"

async def propose_rule(
    rule_id: str,
    agent_name: str,
    change_type: str,
    content: str,
    rationale: str,
    title: Optional[str] = None
):
    """Submit a proposal for a rule mutation."""
    conn = await asyncpg.connect(PG_DSN)
    try:
        pid = await conn.fetchval(
            """INSERT INTO pdd_proposals (rule_id, agent_name, change_type, title, content, rationale)
               VALUES ($1, $2, $3, $4, $5, $6) RETURNING proposal_id""",
            rule_id, agent_name, change_type, title, content, rationale
        )
        print(f"✅ Proposal {pid} submitted for rule {rule_id} ({change_type})")
        return pid
    finally:
        await conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 5:
        # Simple CLI for testing
        asyncio.run(propose_rule(
            rule_id=sys.argv[1],
            agent_name=sys.argv[2],
            change_type=sys.argv[3],
            content=sys.argv[4],
            rationale=sys.argv[5],
            title=sys.argv[6] if len(sys.argv) > 6 else None
        ))
    else:
        print("Usage: python propose_rule.py <rule_id> <agent_name> <new|update|delete> <content> <rationale> [title]")
