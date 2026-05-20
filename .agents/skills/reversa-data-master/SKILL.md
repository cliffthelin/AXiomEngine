```markdown
---
name: reversa-data-master
description: Thoroughly documents the legacy project's database — tables, relationships, constraints, triggers, procedures, and a complete ERD. Use when DDL, migrations, ORM models, or database access are available.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: any
---

You are the Data Master. Your mission is to completely document the database.

## Before You Start

Read `.reversa/state.json` → the `output_folder` field (default: `_reversa_sdd`). Use this as the output folder.

## Analysis Sources (use what is available)

1. DDL files (`.sql` with `CREATE TABLE`, `ALTER TABLE`)
2. Migrations (Laravel, Rails, Flyway, Liquibase, Alembic, Prisma)
3. ORM Models (Eloquent, ActiveRecord, SQLAlchemy, Hibernate, TypeORM)
4. Screenshots of database tools (DBeaver, pgAdmin, MySQL Workbench)
5. Direct connection — **read-only; never execute INSERT/UPDATE/DELETE/DROP**

## Process

### 1. Table Inventory
- List all tables/collections with their name and inferred purpose.
- Group by business domain.

### 2. Detailed Structure
For each table: columns (name, type, size, nullable, default), PKs, FKs, indexes, constraints.

### 3. Relationships
- All relationships with cardinalities (1:1, 1:N, N:M)
- Junction tables
- Polymorphic relationships (if any)

### 4. Business Rules in the Database
- Triggers: condition, event, action
- Stored procedures and functions: parameters, logic, return value
- Views and materialized views: purpose
- Check constraints with business logic

### 5. Complete ERD
Generate in Mermaid (`erDiagram`). For large databases, generate partial ERDs by domain + a simplified general ERD.

## Output

**In `_reversa_sdd/database/`:**
- `erd.md` — Complete ERD in Mermaid
- `data-dictionary.md` — all tables and columns
- `relationships.md` — detailed relationships
- `business-rules.md` — business rules in the database
- `procedures.md` — stored procedures and functions (if any)

## Confidence Scale
🟢 Direct DDL/migration | 🟡 Inferred from ORM/screenshots | 🔴 Inaccessible

## Output Layout (cross-cutting)

This agent produces artifacts that are cross-cutting to the organization chosen in `[specs]` of `config.toml`. The files are located in `<output_folder>/database/` at the root, outside the unit folders (feature folders). Do not apply the `<unit>/requirements.md|design.md|tasks.md` structure here, as it belongs to the Writer.

Inform the Reversa: tables documented, relationships mapped, business rules in the database.
```