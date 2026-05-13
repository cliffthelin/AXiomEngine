#!/usr/bin/env python3
"""
PDD Rules Loader — Ingest PDD chapter markdown files into Postgres pgvector
Run once after 00_install_base.sh to populate the pdd_rules table.
"""
import asyncio
import re
import sys
from pathlib import Path

PDD_DIR = Path(__file__).parent.parent / ".context" / "pdd"
PG_DSN = "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"

# The 5 PDD rule files from your normalized chapter document
# Key: rule_id pattern, Value: (scope, title, content)
INLINE_RULES = [
    ("R-PDD-CORE-001", "core",  "AI Does Not Infer Intent",
     "AI tools do not reason about intent unless it is explicitly retrievable. "
     "They generate probabilistically based on context given at the exact moment of generation."),

    ("R-PDD-CORE-002", "core",  "Folder Structure is Not Authority",
     "Folder structure does not signal authority to an AI. A folder name is just a string. "
     "Authority must be explicitly declared and retrieved, not inferred from placement."),

    ("R-PDD-CORE-003", "core",  "Developer is a Context Orchestrator",
     "Developers are responsible for explicitly shaping AI context. "
     "Governing Markdown must be kept open, or explicitly referenced in AI prompts to force retrieval."),

    ("R-PDD-CORE-004", "core",  "Missing Intent Leads to Silent Failure",
     "Context loss is a system failure, not a human error. Without explicit intent, "
     "AI will produce output that is behaviorally plausible but policy-incorrect."),

    ("R-PDD-MD-001",   "md",    "Prompts Select Intent, Markdown Contains It",
     "Prompts are selectors of intent, not containers of intent. "
     "Prompts must reference durable, authoritative artifacts that live in the repository."),

    ("R-PDD-MD-002",   "md",    "Structure of Authoritative Markdown",
     "Every authoritative document must follow Declare → Constrain → Verify pattern "
     "with: Purpose, Definitions, Rules, Non-Goals, Validation."),

    ("R-PDD-MD-003",   "md",    "Stable Identifiers",
     "Authoritative Markdown must define named rule IDs (e.g., R-PDD-MD-003) "
     "rather than relying on narrative references."),

    ("R-PDD-EXEC-001", "exec",  "Prompts as Versioned Artifacts",
     "Prompts that influence production behavior must be stored as Markdown, "
     "code-reviewed, versioned, and explicitly referenced. Ad-hoc chats are forbidden."),

    ("R-PDD-EXEC-002", "exec",  "Role-Separated Prompt Chaining",
     "Planning Prompts: analyze, cannot modify code. "
     "Execution Prompts: generate using explicit scope, must halt if intent missing. "
     "Review Prompts: evaluate drift, cannot introduce new behavior."),

    ("R-PDD-EXEC-003", "exec",  "Stop-the-Line Pipelines",
     "Pipelines must enforce strict gates. If a prompt omits required intent, "
     "expands scope, or violates review criteria, the workflow must halt immediately."),

    ("R-PDD-GOV-001",  "gov",   "Single Source of Truth",
     "Authoritative organizational intent lives in exactly one maintained system. "
     "If two documents disagree, only one is allowed to be authoritative."),

    ("R-PDD-GOV-002",  "gov",   "Role Boundaries",
     "AI agents must never author or mutate intent. "
     "Roles: Intent Author (defines rules), Executor (complies), "
     "Reviewer (validates), Governor (enforces)."),

    ("R-PDD-GOV-003",  "gov",   "Interface Standardization",
     "Governance standardizes rule identifiers, required structural anchors, "
     "and validation semantics. Must not standardize prose style."),

    ("R-PDD-AUDIT-001","audit", "Computational Audit Trails",
     "The system must log: prompt identity and version, governing intent references, "
     "model versions, context inputs, and review outcomes."),

    ("R-PDD-AUDIT-002","audit", "Governance Metrics",
     "Every metric must map to: Correctness (intent alignment), "
     "Stability (semantic drift), or Risk Exposure (hallucination flags)."),

    ("R-PDD-AUDIT-003","audit", "Intervention Controls",
     "Unstructured interventions (ad-hoc prompt tweaks) are forbidden. "
     "Allowed: Observation-only, Containment (rollback), Corrective (structural fix)."),

    ("R-PDD-AUDIT-004","audit", "Incidents as Durable Artifacts",
     "If an incident does not improve an artifact (intent, prompt, or constraint), "
     "it did not improve the system. Changes must be hypothesis-driven and reversible."),

    # Hardware-specific rules
    ("R-HW-GPU-001",   "hw",    "P40 Thermal Limit",
     "Tesla P40 temperature MUST NOT exceed 85°C under sustained inference. "
     "At 85°C: reduce load. At 90°C: stop all inference."),

    ("R-HW-GPU-002",   "hw",    "Display GPU Assignment",
     "AMD Raphael iGPU MUST be the display adapter in Modes 1, 2, and 3. "
     "RTX 3070 and Tesla P40 are reserved for AI compute in these modes."),

    ("R-HW-GPU-003",   "hw",    "CUDA Architecture Targets",
     "All CUDA builds must target both sm_60 (Pascal/P40) and sm_86 (Ampere/3070). "
     "Flag: -DCMAKE_CUDA_ARCHITECTURES=60;86"),

    # Swarm rules
    ("R-PDD-SWARM-001", "swarm", "Agent Swarm Orchestration",
     "Complex goals MUST be broken down into atomic sub-tasks. "
     "Sub-agents MUST NOT spawn further sub-agents unless explicitly authorized. "
     "Every sub-task MUST inherit the root session's PDD context."),

    # Atlas Code rules
    ("R-PDD-ATLAS-001", "atlas", "AI Atlas Code Engineering",
     "Atlas Code is authorized to manage end-to-end pipelines. "
     "Must use AXiomEngine Router (9001) for all inference. "
     "Must respect sandbox and VGPU quotas."),

    # Symphony rules
    ("R-PDD-SYMPHONY-001", "symphony", "Autonomous Issue Orchestration",
     "Symphony is the authorized orchestrator for tracker issues. "
     "Must use deterministic workspaces and bounded concurrency. "
     "Must respect backoff and eligibility rules."),

    ("R-PDD-SEC-001", "core", "Workspace Security Scanning",
     "Every newly provisioned workspace MUST undergo a security scan. "
     "Failures must block execution."),
    
    ("R-PDD-GIT-001", "pi", "Automated Version Control",
     "Commits must include Swarm and Issue IDs for traceability."),
    
    ("R-PDD-KG-001", "archon", "Knowledge Graph Maintenance",
     "Stale nodes older than 90 days must be pruned as background tasks."),
]


async def load_rules():
    try:
        import asyncpg
    except ImportError:
        print("Installing asyncpg...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "asyncpg", "-q"])
        import asyncpg

    print(f"Connecting to Postgres...")
    conn = await asyncpg.connect(PG_DSN)

    inserted = 0
    skipped = 0
    for rule_id, scope, title, content in INLINE_RULES:
        existing = await conn.fetchval(
            "SELECT rule_id FROM pdd_rules WHERE rule_id=$1", rule_id
        )
        if existing:
            skipped += 1
            continue
        await conn.execute(
            """INSERT INTO pdd_rules (rule_id, scope, title, content)
               VALUES ($1, $2, $3, $4)""",
            rule_id, scope, title, content
        )
        inserted += 1
        print(f"  ✅ {rule_id}: {title}")

    count = await conn.fetchval("SELECT COUNT(*) FROM pdd_rules")
    await conn.close()
    print(f"\nDone: {inserted} inserted, {skipped} already existed ({count} total)")


if __name__ == "__main__":
    asyncio.run(load_rules())
