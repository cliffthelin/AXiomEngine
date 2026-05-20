### SOURCE:
### SOURCE:
**Surface Scan**

**Description:** This document provides a high-fidelity high-level mapping of the entire project legacy system.

**License:** MIT

**Compatibility:**
- Claude Code
- Codex
- Cursor
- Gemini CLI and other compatible agents

**Metadata:**
- **author:** sandeco
- **version:** "1.0.0"
- **framework:** reversa
- **phase:** Recognition

**Contents:**
## Structure of the Project Legacy

**Source:**
---
name: reversa-scout
description: Map the complete surface of the legacy system.

# TODO: This is a placeholder for instructions.

license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI and other compatible agents
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: Recognition
---

**Before Starting**

- Open `state.json` -> `output_folder` (default: `_reversa_sdd`) and `doc_level` (default: `essential`). Use `output_folder` as the output folder for all subsequent stages.

**Process:**

**1. Project Structure**
- List all the directory tree levels, excluding:
  - `node_modules`
  - `.git`
  - `_reversa_sdd`
  - `dist`
  - `build`
  - `coverage`
  - `__pycache__`
  - `cache`

**2. Technologies and Frameworks**
- Identify technologies and frameworks from configuration files:
  - Language (file extension — count)
  - Main frameworks and libraries from `package.json`
  - Critical dependencies versions
  - Packaging managers (Dockerfile, docker-compose.yml)

**3. Input Points**
- List the application input files (`main`, `index`, `app`, `server`, `bootstrap`)
- List configuration files (`.env.example`, `config/`, `settings`)
- List CI/CD files (`.github/workflows/**`, `Jenkinsfile`, `.gitlab-ci.yml`)
- `Dockerfile` and `docker-compose.yml`
- `package.json` scripts (start, build, test, deploy)

**4. Database Schema (Superficial)**
- If DDL, migrations, or ORM models exist, list them. The `reversa-data-master` file performs a detailed analysis.

**5. Testing Coverage**
- Identify frameworks supporting unit testing
- Provide an estimate of coverage (files `*.test.*`, `*.spec.*`)

**6. Recommendation for Spec Organization**
- Generate the `organization_suggestion` field in `surface.json` using the following heuristics in the order they appear:
  - First priority: `endpoint`
  - Second priority: `module`
  - Third priority: `use-case`
  - If no priority applies, use `feature`
- For the `feature` case, list the identified features in `organization_suggestion.features`

**Output**

**_reversa_sdd/**:
- `inventory.md` — Comprehensive inventory
- `dependencies.md` — Dependencies with versions

**`.reversa/context/`**:
- `surface.json` — Structured data for other agents

**Checkpoint:**
- Finalize by reporting generated files (relative paths)
- Provide a brief summary of the mapping
