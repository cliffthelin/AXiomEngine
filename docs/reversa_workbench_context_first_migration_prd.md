# PRD: Reversa Workbench Migration — From PowerShell WinForms Manager to Context-First Agentic Application

**Document status:** Draft for review  
**Prepared date:** 2026-05-19  
**Working product name:** Reversa Workbench  
**Source baseline:** Existing PowerShell WinForms Reversa Manager / Add-On Features Agnostic Bundle  
**Strategic theme:** Context defines the application; code becomes a governed artifact generated, maintained, and validated from context.

---

## 1. Executive Summary

The current Reversa add-on ecosystem has grown beyond a PowerShell WinForms manager. It now includes GUI tooling, helper scripts, traceability/provenance utilities, Reversa instance management, database grounding helpers, migration artifacts, approval concepts, and markdown-driven agent/skill behaviors.

The next product evolution should migrate the current PowerShell WinForms tool into an agnostic, web-based, modular workbench while preserving the existing toolkit as an execution backend during early phases. Over time, the product should move toward a **context-first architecture** where application intent, governance, policy, skill behavior, workflows, acceptance criteria, and output contracts are managed as versioned context assets. The code layer should become a generated or implementation-specific artifact that follows technical policy and is validated against the higher-level context.

The long-term goal is not merely to rewrite the UI in a newer framework. The goal is to create a durable **Context Asset Manager and Workflow Console** that can manage Reversa-style agentic systems across runtimes, projects, models, and execution environments.

---

## 2. Background and Current State

The current bundle already demonstrates several important capabilities:

- Reversa instance discovery and management.
- Install/update actions.
- Generated artifact browsing.
- Markdown preview and editing.
- Bulk Markdown-to-HTML conversion.
- Provenance status review.
- Database grounding artifact review.
- Copyable query IDs and cancel commands.
- Scripts for git safety, pre-commit checks, schema extraction, lineage enrichment, report indexing, monitoring, pipeline execution, prerequisite verification, traceability snapshots, and provenance stamping.
- Early thinking around front-door/gallery management for multiple Reversa/add-on instances.
- A stated principle that summarization is not the sole source of truth and that code remains ground truth for current implementation behavior.
- A forward-looking PRD recognizing that the PowerShell GUI is becoming too large and should evolve into a workflow console.

The current system should be treated as a working proof of concept and operator toolkit, not as the final architecture.

---

## 3. Problem Statement

The existing PowerShell WinForms implementation is effective as a local operator dashboard, but it is reaching structural limits:

1. **Single-file or script-heavy UI complexity**
   - UI state, workflow logic, command execution, and artifact browsing are too tightly coupled.

2. **Platform dependency**
   - PowerShell WinForms is Windows-centered and not ideal for cross-platform, web-based, multi-user, or containerized usage.

3. **Limited workflow orchestration**
   - Many Reversa behaviors are still represented as files and scripts rather than first-class workflow states.

4. **Prompt-governed safety is not enough**
   - Markdown instructions can guide agents, but risky actions need external workflow gates, approval records, and validators.

5. **No normalized context asset registry**
   - Skills, prompts, PRDs, PDDs, migration documents, provenance outputs, test rubrics, and generated artifacts need a common management model.

6. **Insufficient evaluation and model comparison**
   - The system should eventually test the same skill/context against multiple local and cloud models, record outputs, and compare results.

7. **Blurred boundary between intent and implementation**
   - User intent, business policy, governance, workflow rules, and technical implementation are currently too easy to mix together. The future system should separate these layers intentionally.

---

## 4. Product Vision

Create a web-based, runtime-agnostic Reversa Workbench that manages:

- Application profiles.
- Reversa/add-on instances.
- Agent and skill profiles.
- Context assets.
- Workflow runs.
- Human-in-the-middle approvals.
- Provenance and traceability artifacts.
- Model comparison results.
- Version history and promotion status.
- Generated code and technical artifacts.

The product should evolve from:

```text
PowerShell WinForms Manager
```

to:

```text
Web-based Workflow Console
```

to:

```text
Context Asset Manager for Agentic Applications
```

to:

```text
Context-first application factory where code is a governed artifact of context.
```

---

## 5. Product Philosophy

### 5.1 Context First, Code as Artifact

The long-term philosophy is:

```text
Application intent, policy, governance, workflows, skills, output contracts,
and acceptance tests should be expressed as versioned context assets.

Code should implement, render, execute, or validate those context assets.
```

This does not mean code is unimportant. It means code should not be the first or only place where user intent, policy, and governance are embedded.

### 5.2 Layer Separation

The system should distinguish between:

1. **Intent Layer**
   - User goals.
   - Desired outcomes.
   - Application purpose.
   - Business meaning.

2. **Policy and Governance Layer**
   - What is allowed.
   - What is prohibited.
   - Approval rules.
   - Compliance requirements.
   - Promotion gates.

3. **Context/Skill Layer**
   - Agent personas.
   - Reusable instructions.
   - Output formats.
   - Examples.
   - Restrictions.
   - Test scenarios.

4. **Workflow Layer**
   - Process sequencing.
   - Checkpoints.
   - HITM approvals.
   - Retry/resume behavior.
   - State transitions.

5. **Technical Code Layer**
   - UI implementation.
   - APIs.
   - adapters.
   - data stores.
   - execution wrappers.
   - validators.
   - generated artifacts.

6. **Evidence Layer**
   - Logs.
   - run results.
   - snapshots.
   - diffs.
   - provenance.
   - test evidence.
   - model comparison outputs.

Each layer can guide or validate another layer, but the boundaries should remain explicit.

### 5.3 Increment Discipline

Bug fixes may occur incrementally in the code layer.

Major feature changes should be driven by context changes:

```text
Context change → tests/rubrics updated → generated/implemented code updated → validation evidence produced → promotion decision.
```

This prevents the application from drifting into ungoverned feature accretion.

---

## 6. Target Users

### Primary Users

- Reversa operators managing multiple project instances.
- Agentic workflow builders.
- Developers maintaining Reversa-style systems.
- Analysts reviewing generated artifacts, traceability, and grounding outputs.

### Secondary Users

- Governance reviewers.
- QA/validation agents.
- Data stewards.
- Migration strategists.
- Developers consuming generated context or code artifacts.

---

## 7. Goals

### Functional Goals

- Replace the PowerShell WinForms manager with a modular web-based interface.
- Preserve current working capabilities during migration.
- Support multiple Reversa/add-on instances.
- Manage context assets, skills, agents, artifacts, and workflows.
- Add guided workflow execution with explicit approval gates.
- Support provenance and traceability as first-class views.
- Support skill/version management.
- Support model comparison and test-driving of agent skills.
- Support gradual migration away from script-first architecture.

### Architectural Goals

- Separate UI, workflow orchestration, execution adapters, context registry, and evidence storage.
- Keep PowerShell scripts callable during early phases.
- Introduce a normalized manifest/schema model.
- Make all major assets diffable, versioned, and testable.
- Enable future re-rendering or rebuilding of the application from context definitions.

### Governance Goals

- Keep business/user intent out of the hidden code layer where possible.
- Keep code policies technical and implementation-focused.
- Maintain clear promotion gates.
- Require tests and evidence for major behavior changes.
- Preserve traceability from context to generated artifacts to runtime results.

---

## 8. Non-Goals

### Initial Non-Goals

- Immediate rewrite of every PowerShell script.
- Immediate cloud-hosted multi-user deployment.
- Immediate replacement of Reversa CLI behavior.
- Immediate AI-only generation of production code.
- Storing secrets in context files.
- Removing command-line access for power users.

### Long-Term Non-Goals

- Treating generated code as unreviewable truth.
- Allowing agentic systems to bypass governance.
- Merging business policy, runtime implementation, and UI code into one unstructured layer.
- Treating markdown summaries as authoritative when executable code, tests, or source artifacts contradict them.

---

## 9. Recommended Target Architecture

### 9.1 High-Level Architecture

```text
Reversa Workbench
  ├── Web UI
  ├── API / Service Layer
  ├── Context Asset Registry
  ├── Workflow Orchestrator
  ├── Runtime Adapters
  ├── Script Execution Adapter
  ├── Evidence Store
  ├── Version Store
  ├── Model Evaluation Harness
  └── Project/Instance Connectors
```

### 9.2 Suggested Technology Direction

The PRD should remain language-agnostic, but the following stack is practical:

#### Preferred Web UI Options

- React + TypeScript + Vite.
- Next.js if server-rendered routes and integrated API are desired.
- Tauri if a local desktop shell is needed while keeping web technologies.
- Electron only if native desktop integration is critical and heavier footprint is acceptable.

#### Preferred API Options

- FastAPI / Python if script orchestration, filesystem tooling, and AI workflow integration are priorities.
- Node.js / TypeScript if sharing schemas/types with the UI is the priority.
- .NET if Windows enterprise integration is the priority.

#### Preferred Data Options

- SQLite for local-first MVP.
- Postgres for multi-user or server deployment.
- Git-backed file storage for promoted context assets.
- JSON/YAML/Markdown files for portable source-of-truth context assets.

#### Preferred Validation Options

- JSON Schema for structured context assets.
- Markdown linting for context documents.
- Promptfoo / DeepEval for model/skill testing.
- Unit/integration tests for adapters and execution wrappers.
- Snapshot testing for rendered prompts, generated code, and output formats.

---

## 10. Canonical Object Model

The future system should normalize current files/scripts/artifacts into explicit objects.

### 10.1 ApplicationProfile

Represents a managed application or project context.

Checklist:

- [ ] Has stable `id`.
- [ ] Has display name.
- [ ] Has root path or repository reference.
- [ ] Defines associated Reversa instances.
- [ ] Defines allowed runtimes.
- [ ] Defines allowed model providers.
- [ ] Defines policy references.
- [ ] Defines default artifact locations.
- [ ] Defines approval requirements.
- [ ] Defines promotion rules.
- [ ] Defines technical stack references where applicable.

### 10.2 ReversaInstance

Represents one installed Reversa/add-on instance.

Checklist:

- [ ] Has stable `id`.
- [ ] Has root path.
- [ ] Has detected installed capabilities.
- [ ] Tracks `.reversa` or equivalent state path.
- [ ] Tracks `_reversa_sdd` or equivalent output path.
- [ ] Tracks progress/migration directories.
- [ ] Tracks installed scripts/toolkit paths.
- [ ] Tracks health status.
- [ ] Tracks last scan timestamp.
- [ ] Tracks source manifests.

### 10.3 ContextAsset

Represents any meaningful instruction, artifact, policy, plan, output, or evidence item.

Types may include:

- Skill markdown.
- Agent persona.
- PRD.
- PDD rule.
- Governance rule.
- Migration plan.
- Output format contract.
- Test rubric.
- Provenance report.
- Traceability snapshot.
- Database grounding artifact.
- Model run result.
- Generated code artifact.

Checklist:

- [ ] Has stable `id`.
- [ ] Has type.
- [ ] Has source path.
- [ ] Has content hash.
- [ ] Has version.
- [ ] Has status: draft, active, promoted, deprecated, blocked, archived.
- [ ] Has ownership metadata.
- [ ] Has provenance metadata.
- [ ] Has source references.
- [ ] Has validation status.
- [ ] Has related application profile.
- [ ] Has related workflow run when applicable.
- [ ] Has related tests when applicable.

### 10.4 SkillProfile

Represents a normalized agent/skill definition that can render to Markdown or runtime-specific formats.

Checklist:

- [ ] Defines persona.
- [ ] Defines intent.
- [ ] Defines scope.
- [ ] Defines allowed actions.
- [ ] Defines denied actions.
- [ ] Defines required inputs.
- [ ] Defines required outputs.
- [ ] Defines output format.
- [ ] Defines examples.
- [ ] Defines anti-examples.
- [ ] Defines acceptance tests.
- [ ] Defines runtime adapters.
- [ ] Defines model compatibility notes.
- [ ] Defines safety restrictions.
- [ ] Defines promotion status.
- [ ] Can render to Reversa `SKILL.md`.
- [ ] Can render to PI/Archon/Hermes-specific formats if needed.
- [ ] Can render to generic `AGENTS.md` style instructions.

### 10.5 WorkflowRun

Represents an execution or review session.

Checklist:

- [ ] Has run ID.
- [ ] Has application profile ID.
- [ ] Has initiating user or agent.
- [ ] Has selected context assets.
- [ ] Has selected skill/profile.
- [ ] Has selected runtime/model.
- [ ] Has start/end timestamps.
- [ ] Has status.
- [ ] Has approval gates.
- [ ] Has generated artifacts.
- [ ] Has logs.
- [ ] Has test results.
- [ ] Has evidence bundle.
- [ ] Has resume/checkpoint data.

### 10.6 ApprovalGate

Represents a decision checkpoint.

Checklist:

- [ ] Defines gate type.
- [ ] Defines required approver.
- [ ] Defines required evidence.
- [ ] Defines allowed outcomes: approve, reject, defer, request changes.
- [ ] Captures decision timestamp.
- [ ] Captures rationale.
- [ ] Captures related artifacts.
- [ ] Blocks workflow until satisfied.
- [ ] Is included in evidence export.

### 10.7 EvidenceArtifact

Represents proof that something happened or was validated.

Checklist:

- [ ] Has stable ID.
- [ ] Has artifact type.
- [ ] Has content hash.
- [ ] Has source references.
- [ ] Has line/file references where possible.
- [ ] Has generated timestamp.
- [ ] Has producer.
- [ ] Has validation status.
- [ ] Is immutable after finalization.
- [ ] Can be exported in an evidence bundle.

---

## 11. Phase Plan

## Phase 0 — Baseline Inventory and Safety Freeze

### Objective

Capture the current PowerShell WinForms manager and add-on toolkit as a governed baseline before migration begins.

### Deliverables

- Current-state inventory.
- Script manifest.
- GUI feature map.
- Known workflows list.
- Known risks list.
- Baseline screenshots or recordings.
- Baseline test checklist.
- Current limitations statement.

### Checklist

#### Inventory

- [ ] Identify all PowerShell scripts used by the current GUI.
- [ ] Identify all helper scripts in categorized folders.
- [ ] Identify all generated artifact locations.
- [ ] Identify all progress/state directories.
- [ ] Identify all migration documents.
- [ ] Identify all provenance/traceability scripts.
- [ ] Identify all database grounding scripts.
- [ ] Identify all install/update scripts.
- [ ] Identify all hidden assumptions in the current GUI.
- [ ] Identify all hard-coded paths.
- [ ] Identify all Windows-only assumptions.
- [ ] Identify all scripts that can modify files.
- [ ] Identify all scripts that can access databases.
- [ ] Identify all scripts that can execute long-running operations.

#### Safety

- [ ] Add a migration freeze note to the current tool.
- [ ] Require backups before modifying the current manager.
- [ ] Create a Git branch/tag for the current baseline.
- [ ] Generate hashes for all current scripts.
- [ ] Create an initial evidence bundle for the baseline.
- [ ] Document how to restore the current working PowerShell version.
- [ ] Confirm no migration work deletes existing scripts.
- [ ] Confirm no new tool bypasses existing safety checks.

#### Acceptance Criteria

- [ ] A reviewer can see what exists today.
- [ ] A reviewer can restore the current PowerShell manager.
- [ ] A reviewer can distinguish current working features from planned features.
- [ ] No current capability is removed.
- [ ] No unmanaged database execution is introduced.

---

## Phase 1 — Manifest and Schema Foundation

### Objective

Create a structured manifest layer that describes current applications, instances, scripts, artifacts, and workflows without replacing the current UI yet.

### Deliverables

- `application-profile.schema.json`
- `reversa-instance.schema.json`
- `context-asset.schema.json`
- `skill-profile.schema.json`
- `workflow-run.schema.json`
- `approval-gate.schema.json`
- `evidence-artifact.schema.json`
- Example manifests for at least one current Reversa instance.
- Validation CLI or script.

### Checklist

#### Manifest Design

- [ ] Define `ApplicationProfile` schema.
- [ ] Define `ReversaInstance` schema.
- [ ] Define `ContextAsset` schema.
- [ ] Define `SkillProfile` schema.
- [ ] Define `WorkflowRun` schema.
- [ ] Define `ApprovalGate` schema.
- [ ] Define `EvidenceArtifact` schema.
- [ ] Define status enums.
- [ ] Define version fields.
- [ ] Define provenance fields.
- [ ] Define hash fields.
- [ ] Define source reference format.
- [ ] Define artifact relationship fields.

#### Current-State Mapping

- [ ] Map current PowerShell GUI functions to manifest capabilities.
- [ ] Map current scripts to `ContextAsset` or `ExecutionAdapter` entries.
- [ ] Map current progress documents to `ContextAsset` entries.
- [ ] Map current migration documents to `ContextAsset` entries.
- [ ] Map current provenance outputs to `EvidenceArtifact` entries.
- [ ] Map current traceability snapshots to `EvidenceArtifact` entries.
- [ ] Map current Reversa instance path assumptions into `ReversaInstance`.

#### Validation

- [ ] Create schema validation script.
- [ ] Validate sample manifests.
- [ ] Fail validation for missing IDs.
- [ ] Fail validation for invalid status values.
- [ ] Fail validation for missing source paths.
- [ ] Fail validation for missing hashes where required.
- [ ] Produce human-readable validation report.
- [ ] Produce machine-readable validation report.

#### Acceptance Criteria

- [ ] The current system can be described without changing it.
- [ ] At least one real Reversa instance is represented by manifests.
- [ ] All manifests validate.
- [ ] Invalid manifests fail with clear messages.
- [ ] The manifest layer can be used by both old and future UIs.

---

## Phase 2 — Web Workbench Skeleton

### Objective

Build a web-based read-only workbench that can browse the same information currently surfaced by the PowerShell GUI.

### Deliverables

- Web UI skeleton.
- API/service layer.
- Local filesystem connector.
- Manifest browser.
- Instance dashboard.
- Artifact browser.
- Read-only markdown viewer.
- Basic health/status page.

### Checklist

#### UI Foundation

- [ ] Create web application project.
- [ ] Create layout shell.
- [ ] Add application switcher.
- [ ] Add Reversa instance list.
- [ ] Add navigation for Applications, Instances, Assets, Workflows, Evidence, Settings.
- [ ] Add responsive layout.
- [ ] Add dark/light mode if practical.
- [ ] Add error boundary.
- [ ] Add empty states.
- [ ] Add loading states.

#### API Foundation

- [ ] Create API/service layer.
- [ ] Add endpoint to list application profiles.
- [ ] Add endpoint to list Reversa instances.
- [ ] Add endpoint to read manifests.
- [ ] Add endpoint to list context assets.
- [ ] Add endpoint to read artifact metadata.
- [ ] Add endpoint to read markdown content.
- [ ] Add endpoint to compute health summary.
- [ ] Add structured error responses.
- [ ] Add request logging.
- [ ] Add path safety checks.

#### Read-Only Safety

- [ ] Ensure Phase 2 cannot modify project files.
- [ ] Ensure Phase 2 cannot execute scripts.
- [ ] Ensure Phase 2 cannot access databases.
- [ ] Ensure Phase 2 cannot write approval records.
- [ ] Show read-only banner.
- [ ] Log all attempted unsafe actions as blocked.

#### Acceptance Criteria

- [ ] User can open web workbench locally.
- [ ] User can see current Reversa instances.
- [ ] User can browse artifacts.
- [ ] User can preview markdown.
- [ ] User can view manifest validation status.
- [ ] No files are modified.
- [ ] No scripts are executed.
- [ ] No risky operations are available.

---

## Phase 3 — Feature Parity with Current Manager

### Objective

Reach functional parity with the current PowerShell manager while keeping execution behind safe adapters.

### Deliverables

- Artifact browsing parity.
- Markdown preview/edit parity.
- HTML conversion parity.
- Provenance review parity.
- Database grounding artifact review parity.
- Copyable query/cancel command parity.
- Existing script launch adapter in guarded mode.

### Checklist

#### Artifact Management

- [ ] Browse generated artifacts by instance.
- [ ] Filter artifacts by type.
- [ ] Search artifacts.
- [ ] Open markdown artifacts.
- [ ] Open JSON/CSV/text artifacts.
- [ ] Show source path.
- [ ] Show provenance status.
- [ ] Show content hash.
- [ ] Show last modified timestamp.
- [ ] Show related workflow if known.

#### Markdown Editing

- [ ] Add editable markdown view.
- [ ] Add diff preview before save.
- [ ] Add backup-before-save.
- [ ] Add provenance header preservation.
- [ ] Add validation before save.
- [ ] Add save reason field.
- [ ] Add version record on save.
- [ ] Add rollback to previous saved version.
- [ ] Prevent editing promoted/locked assets without explicit unlock.

#### HTML Conversion

- [ ] Support one-file markdown-to-HTML conversion.
- [ ] Support bulk conversion.
- [ ] Preserve source references.
- [ ] Generate output manifest.
- [ ] Show conversion result.
- [ ] Capture errors.

#### Script Adapter

- [ ] Register current PowerShell scripts as executable actions.
- [ ] Mark each action as read-only, write, long-running, or risky.
- [ ] Require confirmation before execution.
- [ ] Require working directory selection.
- [ ] Capture stdout/stderr.
- [ ] Capture exit code.
- [ ] Capture duration.
- [ ] Store execution evidence.
- [ ] Support dry-run where script supports it.
- [ ] Do not execute unregistered scripts.

#### Acceptance Criteria

- [ ] Current PowerShell manager can remain available as fallback.
- [ ] Web workbench can perform core existing manager tasks.
- [ ] Every write action creates a backup or version record.
- [ ] Every script action is registered and classified.
- [ ] Risky actions require confirmation.
- [ ] Execution results are captured as evidence.

---

## Phase 4 — Guided Workflow Console

### Objective

Move beyond manager parity into first-class workflow orchestration.

### Deliverables

- Workflow definitions.
- Guided runs.
- Checkpoint/resume.
- HITM approval gates.
- Run timeline.
- Evidence bundle per run.
- Workflow status dashboard.

### Checklist

#### Workflow Model

- [ ] Define workflow schema.
- [ ] Define step schema.
- [ ] Define checkpoint schema.
- [ ] Define approval gate schema.
- [ ] Define artifact input/output contract.
- [ ] Define retry behavior.
- [ ] Define resume behavior.
- [ ] Define blocked state.
- [ ] Define completed state.
- [ ] Define failed state.

#### UI Workflow Runner

- [ ] Show workflow catalog.
- [ ] Show workflow purpose.
- [ ] Show required inputs.
- [ ] Show required approvals.
- [ ] Show expected outputs.
- [ ] Start workflow run.
- [ ] Pause workflow run.
- [ ] Resume workflow run.
- [ ] Cancel workflow run.
- [ ] Show current step.
- [ ] Show completed steps.
- [ ] Show blocked steps.
- [ ] Show approval requests.
- [ ] Show generated artifacts.

#### Approval Gates

- [ ] Add DB access approval gate.
- [ ] Add server/access approval gate.
- [ ] Add explain-plan approval gate.
- [ ] Add pilot-table approval gate.
- [ ] Add full execution approval gate.
- [ ] Add file modification approval gate.
- [ ] Add skill promotion approval gate.
- [ ] Capture approver.
- [ ] Capture rationale.
- [ ] Capture decision timestamp.
- [ ] Include approvals in evidence bundle.

#### Acceptance Criteria

- [ ] A workflow can be run from start to finish.
- [ ] A workflow can pause and resume.
- [ ] A risky step cannot proceed without approval.
- [ ] Workflow artifacts are linked to the run.
- [ ] Approval decisions are preserved.
- [ ] Failed workflows can be inspected after failure.
- [ ] A reviewer can understand what happened without reading raw logs first.

---

## Phase 5 — Context Asset Registry

### Objective

Create the central registry for context assets, including skills, PRDs, PDDs, workflows, policies, output contracts, migration plans, and generated artifacts.

### Deliverables

- Context Asset Registry.
- Asset type taxonomy.
- Search/filter/tagging.
- Version history.
- Diff viewer.
- Promotion states.
- Relationship graph.

### Checklist

#### Asset Registry

- [ ] Register markdown skill files.
- [ ] Register PRDs.
- [ ] Register PDD rules.
- [ ] Register migration documents.
- [ ] Register workflow definitions.
- [ ] Register policy documents.
- [ ] Register output contracts.
- [ ] Register generated artifacts.
- [ ] Register evidence artifacts.
- [ ] Register test rubrics.
- [ ] Register model comparison outputs.

#### Asset Metadata

- [ ] Add ID.
- [ ] Add type.
- [ ] Add title.
- [ ] Add status.
- [ ] Add version.
- [ ] Add owner.
- [ ] Add source path.
- [ ] Add content hash.
- [ ] Add created timestamp.
- [ ] Add modified timestamp.
- [ ] Add application profile reference.
- [ ] Add related workflow references.
- [ ] Add related test references.
- [ ] Add related generated code references.

#### Registry UI

- [ ] Search assets.
- [ ] Filter by application.
- [ ] Filter by type.
- [ ] Filter by status.
- [ ] Filter by owner.
- [ ] Filter by changed date.
- [ ] Show asset dependencies.
- [ ] Show asset consumers.
- [ ] Show validation status.
- [ ] Show promotion history.
- [ ] Show version diff.

#### Acceptance Criteria

- [ ] Every managed context artifact can be found.
- [ ] Every asset has a type and status.
- [ ] Every promoted asset has version history.
- [ ] Every generated artifact can reference its source context.
- [ ] The registry can identify stale or unvalidated assets.
- [ ] The registry can export an index.

---

## Phase 6 — Skill Profile Manager

### Objective

Normalize Reversa/PI/Archon/Hermes skills into structured, versioned, testable Skill Profiles.

### Deliverables

- Skill Profile schema.
- Skill editor.
- Markdown renderers.
- Runtime adapters.
- Interview-assisted skill creation.
- Version history.
- Promotion workflow.

### Checklist

#### Skill Schema

- [ ] Define persona field.
- [ ] Define intent field.
- [ ] Define scope field.
- [ ] Define allowed actions.
- [ ] Define denied actions.
- [ ] Define input contract.
- [ ] Define output contract.
- [ ] Define required examples.
- [ ] Define anti-examples.
- [ ] Define test scenarios.
- [ ] Define runtime render targets.
- [ ] Define model compatibility.
- [ ] Define restrictions.
- [ ] Define promotion status.
- [ ] Define deprecation status.

#### Skill Editor

- [ ] Create structured editor.
- [ ] Support raw markdown view.
- [ ] Support structured field view.
- [ ] Support preview rendered output.
- [ ] Support diff before save.
- [ ] Support save reason.
- [ ] Support version bump.
- [ ] Support clone.
- [ ] Support archive.
- [ ] Support restore.
- [ ] Support compare versions.

#### Interview Mode

- [ ] Ask what the skill should do.
- [ ] Ask what it should never do.
- [ ] Ask what inputs it receives.
- [ ] Ask what outputs it must produce.
- [ ] Ask for good examples.
- [ ] Ask for bad examples.
- [ ] Ask applicable application profile.
- [ ] Ask applicable runtimes.
- [ ] Ask required restrictions.
- [ ] Ask required tests.
- [ ] Generate draft Skill Profile.
- [ ] Generate draft rendered markdown.
- [ ] Mark output as draft until reviewed.

#### Runtime Rendering

- [ ] Render to Reversa `SKILL.md`.
- [ ] Render to PI-compatible format.
- [ ] Render to Archon-compatible format.
- [ ] Render to Hermes-compatible format.
- [ ] Render to generic `AGENTS.md`.
- [ ] Render to prompt/test harness format.
- [ ] Store render output hash.
- [ ] Detect render drift.
- [ ] Require review before publishing render to runtime.

#### Acceptance Criteria

- [ ] A markdown skill can be imported into a Skill Profile.
- [ ] A Skill Profile can render back to markdown.
- [ ] A Skill Profile can be versioned.
- [ ] A Skill Profile can be tested.
- [ ] A Skill Profile can be promoted.
- [ ] Runtime-specific files are treated as renders, not the canonical source.
- [ ] Draft skills cannot overwrite promoted skills without approval.

---

## Phase 7 — Testing, Evaluation, and Model Comparison

### Objective

Add formal skill/context testing across local and cloud models.

### Deliverables

- Test scenario schema.
- Evaluation runner.
- Model provider registry.
- Result comparison UI.
- Pass/fail rubric support.
- Regression suite.

### Checklist

#### Model Registry

- [ ] Register local models.
- [ ] Register cloud models.
- [ ] Register provider endpoints.
- [ ] Register model capabilities.
- [ ] Register context length.
- [ ] Register cost metadata where applicable.
- [ ] Register privacy classification.
- [ ] Register allowed application profiles.
- [ ] Register blocked application profiles.

#### Test Scenarios

- [ ] Define scenario ID.
- [ ] Define input prompt.
- [ ] Define required context assets.
- [ ] Define expected behavior.
- [ ] Define forbidden behavior.
- [ ] Define expected output schema.
- [ ] Define rubric.
- [ ] Define pass/fail checks.
- [ ] Define human review flag.
- [ ] Define regression criticality.

#### Evaluation Runner

- [ ] Run one skill against one model.
- [ ] Run one skill against multiple models.
- [ ] Run multiple skill versions against one model.
- [ ] Run multiple skill versions against multiple models.
- [ ] Capture raw prompt.
- [ ] Capture raw response.
- [ ] Capture model metadata.
- [ ] Capture timing.
- [ ] Capture token counts if available.
- [ ] Capture evaluator result.
- [ ] Capture human feedback.
- [ ] Store results indefinitely or per retention policy.

#### Comparison UI

- [ ] Side-by-side outputs.
- [ ] Highlight format violations.
- [ ] Highlight forbidden behavior.
- [ ] Highlight missing required sections.
- [ ] Show evaluator score.
- [ ] Show human rating.
- [ ] Show regression trend.
- [ ] Show recommended winner.
- [ ] Allow promotion from successful test.

#### Acceptance Criteria

- [ ] Same skill can be tested across multiple models.
- [ ] Results are stored and searchable.
- [ ] Failures block promotion when marked critical.
- [ ] Human reviewers can override with rationale.
- [ ] Model comparison results can be exported.
- [ ] Regression tests can run in CI or local automation.

---

## Phase 8 — Context-Driven Build and Regeneration

### Objective

Begin practicing the long-term principle: significant application behavior should be rebuilt or regenerated from context definitions and tested against those definitions.

### Deliverables

- Context-to-code generation pipeline prototype.
- Generated component or workflow prototype.
- Context change detection.
- Rebuild trigger.
- Generated artifact tracking.
- Validation report.

### Checklist

#### Context-to-Code Boundary

- [ ] Identify which features are safe to generate from context.
- [ ] Identify which features must remain hand-coded.
- [ ] Identify which policies apply to context.
- [ ] Identify which policies apply to generated code.
- [ ] Identify which policies apply to runtime.
- [ ] Identify which policies only guide or validate.
- [ ] Document the separation explicitly.

#### Generation Prototype

- [ ] Select one low-risk feature.
- [ ] Define feature context.
- [ ] Define UI context.
- [ ] Define workflow context.
- [ ] Define acceptance tests.
- [ ] Generate implementation artifact.
- [ ] Run tests.
- [ ] Compare generated output to context.
- [ ] Store generated artifact metadata.
- [ ] Store generation prompt/context bundle.
- [ ] Require human review before adoption.

#### Change Management

- [ ] Detect context changes.
- [ ] Identify affected code artifacts.
- [ ] Identify affected tests.
- [ ] Identify affected workflows.
- [ ] Require regeneration or explicit no-op decision.
- [ ] Capture rationale.
- [ ] Capture evidence.

#### Acceptance Criteria

- [ ] At least one feature can be regenerated from context.
- [ ] Generated code is not treated as automatically promoted.
- [ ] Tests validate generated behavior.
- [ ] Context changes can identify affected artifacts.
- [ ] The system distinguishes context governance from code governance.
- [ ] Reviewers can trace from context to generated code.

---

## Phase 9 — Policy and Governance Layer Separation

### Objective

Formalize layered governance so that intent, policy, context, workflow, code, and evidence each have appropriate rules.

### Deliverables

- Governance layer model.
- Policy taxonomy.
- Rule applicability matrix.
- Validation engine.
- Promotion gate rules.
- Audit report.

### Checklist

#### Layer Model

- [ ] Define Intent Layer.
- [ ] Define Business Policy Layer.
- [ ] Define Governance Layer.
- [ ] Define Context/Skill Layer.
- [ ] Define Workflow Layer.
- [ ] Define Technical Code Layer.
- [ ] Define Evidence Layer.
- [ ] Define Runtime Adapter Layer.
- [ ] Define Model Policy Layer.

#### Rule Applicability

- [ ] Mark rules as direct enforcement, guidance, validation, or advisory.
- [ ] Identify rules that apply before code generation.
- [ ] Identify rules that apply during implementation.
- [ ] Identify rules that apply after execution.
- [ ] Identify rules that apply only to humans.
- [ ] Identify rules that apply only to agents.
- [ ] Identify rules that apply to both.
- [ ] Prevent business intent from being hidden only in implementation code.
- [ ] Prevent technical-only rules from overriding higher-level policy without approval.

#### Validation

- [ ] Validate context assets against context policy.
- [ ] Validate workflow runs against workflow policy.
- [ ] Validate generated code against technical policy.
- [ ] Validate outputs against evidence policy.
- [ ] Validate promotions against governance gates.
- [ ] Produce audit-ready report.
- [ ] Record exceptions with rationale.

#### Acceptance Criteria

- [ ] Every rule has a declared layer.
- [ ] Every rule has declared enforcement mode.
- [ ] Promotions require appropriate layer checks.
- [ ] Exceptions are explicit.
- [ ] Audit report shows what governed what.
- [ ] Code-layer changes cannot silently redefine user intent.

---

## Phase 10 — Multi-User / Server / Enterprise Readiness

### Objective

Prepare the system for broader use beyond one local operator.

### Deliverables

- Authentication plan.
- Role-based permissions.
- Multi-user audit log.
- Server deployment option.
- Secure secrets handling.
- Backup/restore plan.
- Environment promotion model.

### Checklist

#### Identity and Access

- [ ] Define user roles.
- [ ] Define agent roles.
- [ ] Define admin role.
- [ ] Define reviewer role.
- [ ] Define operator role.
- [ ] Define read-only analyst role.
- [ ] Add authentication.
- [ ] Add authorization checks.
- [ ] Add role-based action visibility.
- [ ] Add approval delegation.

#### Security

- [ ] Do not store secrets in context files.
- [ ] Use secret manager or environment-specific secure storage.
- [ ] Restrict filesystem access.
- [ ] Restrict script execution.
- [ ] Restrict database access.
- [ ] Restrict network access.
- [ ] Log privileged operations.
- [ ] Require explicit approval for risky actions.
- [ ] Add security review checklist.

#### Deployment

- [ ] Support local-only deployment.
- [ ] Support containerized deployment.
- [ ] Support server deployment.
- [ ] Support database-backed deployment.
- [ ] Support Git-backed context store.
- [ ] Support backup/restore.
- [ ] Support environment promotion: dev, test, prod.
- [ ] Support audit export.

#### Acceptance Criteria

- [ ] Users only see actions they are allowed to perform.
- [ ] Secrets are not stored in managed context assets.
- [ ] Risky actions are auditable.
- [ ] System can be backed up and restored.
- [ ] Deployment mode is documented.
- [ ] Multi-user usage does not break provenance/history.

---

## Phase 11 — Long-Term Context-First Application Factory

### Objective

Evolve the workbench into a system where applications and features are primarily defined by context, then implemented, generated, tested, and governed through technical artifacts.

### Deliverables

- Application context schema.
- Feature context schema.
- Policy context schema.
- Workflow context schema.
- UI context schema.
- Code generation/adaptation pipeline.
- Validation and promotion pipeline.
- Rebuild-from-context process.

### Checklist

#### Context-Defined Applications

- [ ] Define application intent.
- [ ] Define users.
- [ ] Define workflows.
- [ ] Define policies.
- [ ] Define permissions.
- [ ] Define data contracts.
- [ ] Define output contracts.
- [ ] Define UI behaviors.
- [ ] Define evidence requirements.
- [ ] Define acceptance tests.
- [ ] Define model policies.
- [ ] Define integration points.

#### Code as Artifact

- [ ] Mark generated code as an artifact.
- [ ] Track source context for each generated artifact.
- [ ] Track generation method.
- [ ] Track model/tool used if applicable.
- [ ] Track review status.
- [ ] Track test status.
- [ ] Track promotion status.
- [ ] Track divergence from context.
- [ ] Flag manual edits.
- [ ] Require reconciliation when code diverges from source context.

#### Release Governance

- [ ] Minor release allows bug fixes within existing context.
- [ ] Major release requires context changes.
- [ ] Context changes require tests.
- [ ] Tests must pass or be explicitly deferred with approval.
- [ ] Promotion requires evidence bundle.
- [ ] Rollback restores context and artifact versions.
- [ ] Release notes generated from context and evidence.

#### Acceptance Criteria

- [ ] A feature can be defined in context before code exists.
- [ ] A generated implementation can be traced back to context.
- [ ] Manual implementation can also be traced back to context.
- [ ] Major releases are context-driven.
- [ ] Code divergence is detectable.
- [ ] Evidence proves the implementation matches the context.
- [ ] The system practices its own philosophy.

---

## 12. Cross-Cutting Requirements

## 12.1 Provenance

Checklist:

- [ ] Every generated artifact declares source context.
- [ ] Every generated artifact includes hash or version references.
- [ ] Every modified artifact records who/what modified it.
- [ ] Every run records selected context.
- [ ] Every workflow records input and output artifacts.
- [ ] Every promotion records evidence.
- [ ] Provenance can be exported.

## 12.2 Traceability

Checklist:

- [ ] Trace from application profile to skills.
- [ ] Trace from skill to rendered runtime files.
- [ ] Trace from context to generated code.
- [ ] Trace from workflow to artifacts.
- [ ] Trace from tests to requirements.
- [ ] Trace from policy to validation result.
- [ ] Trace from model output to prompt/context bundle.
- [ ] Trace from release to evidence bundle.

## 12.3 Safety

Checklist:

- [ ] Risky actions are classified.
- [ ] Risky actions require approval.
- [ ] Database operations require staged approval.
- [ ] File modifications require backup/version record.
- [ ] Runtime adapters use path allowlists.
- [ ] Shell execution is disabled by default.
- [ ] Unregistered scripts cannot run.
- [ ] Dry-run is preferred where available.
- [ ] Dangerous actions are logged and reviewable.

## 12.4 Testability

Checklist:

- [ ] Unit tests for schema validation.
- [ ] Unit tests for path safety.
- [ ] Unit tests for manifest parsing.
- [ ] Unit tests for artifact indexing.
- [ ] Integration tests for script adapter.
- [ ] Integration tests for workflow runner.
- [ ] Snapshot tests for rendered skills.
- [ ] Evaluation tests for model outputs.
- [ ] Regression tests for promoted skills.
- [ ] UI tests for approval gates.

## 12.5 Portability

Checklist:

- [ ] No hard dependency on Windows UI.
- [ ] PowerShell scripts callable as adapters, not core UI.
- [ ] Support Linux paths where possible.
- [ ] Support containerized runtime where possible.
- [ ] Store context in portable text formats.
- [ ] Keep runtime-specific renders separate from canonical context.
- [ ] Avoid embedding environment-specific paths in canonical assets.

---

## 13. Migration Strategy

### Recommended Migration Pattern

Use a strangler-fig migration:

```text
Current PowerShell WinForms Manager
  ↓
Web read-only workbench
  ↓
Web parity workbench with guarded script execution
  ↓
Workflow console
  ↓
Context asset registry
  ↓
Skill/profile manager
  ↓
Context-driven application factory
```

### Preservation Rule

No working PowerShell capability should be removed until the web workbench has equivalent or better behavior, test evidence, and rollback instructions.

### Adapter Rule

Existing scripts should initially be wrapped as registered actions rather than rewritten immediately.

### Promotion Rule

New functionality should be promoted only when:

- Context definition exists.
- Tests exist.
- Evidence exists.
- Rollback path exists.
- Reviewer approval exists for major behavior.

---

## 14. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Migration becomes a rewrite | Use parity phases and preserve current tool as fallback |
| PowerShell assumptions leak into new architecture | Put scripts behind explicit adapters |
| Context layer becomes vague documentation | Require schemas, tests, promotion states, and evidence |
| AI-generated code drifts from intent | Trace generated code to source context and test against context |
| Too much governance slows prototype | Separate prototype/draft states from promoted states |
| UI rebuild loses current capabilities | Baseline inventory and parity checklist |
| Risky DB/file operations become easier to trigger | Approval gates and action classification |
| Multi-runtime support becomes chaotic | Canonical Skill Profile with runtime-specific renders |
| Context/code boundary becomes blurred | Layer applicability matrix and validation |
| Long-term vision delays useful MVP | Phase read-only and parity work first |

---

## 15. Definition of Done

A phase is complete only when:

- [ ] Deliverables are present.
- [ ] Checklists are reviewed.
- [ ] Tests pass or deferrals are explicitly approved.
- [ ] Evidence bundle exists.
- [ ] Documentation is updated.
- [ ] Rollback path exists.
- [ ] Known gaps are recorded.
- [ ] No prior working capability is lost without approval.

---

## 16. Suggested Immediate Next Actions

1. Create the baseline inventory and freeze tag.
2. Define the manifest schemas.
3. Generate manifests for one current Reversa instance.
4. Build a read-only web workbench that consumes those manifests.
5. Add artifact browsing and markdown preview.
6. Add guarded script execution only after read-only parity is stable.
7. Add Skill Profile schema after core instance/artifact management works.
8. Add model comparison after skills are normalized.
9. Add context-to-code generation only after the system can validate context assets reliably.

---

## 17. Strategic Principle to Preserve

The workbench should embody this rule:

```text
The application is defined by governed context.
The code is an implementation artifact.
The evidence proves the code still matches the context.
```

This principle should guide long-term architecture, but it should not prevent practical early migration. The correct path is:

```text
Framework and function first.
Context normalization second.
Context-driven regeneration third.
Governed application factory last.
```
