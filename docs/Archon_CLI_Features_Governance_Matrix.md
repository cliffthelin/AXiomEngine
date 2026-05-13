# Exhaustive Archon CLI Capabilities & AXiomEngine Governance Matrix

This comprehensive matrix maps every feature extracted from the Archon CLI technical reference to its corresponding AXiomEngine Governance Rule, and explicitly details how each feature is integrated across the CLI, TUI, GUI, and how it interacts with external packages and extensions.

## 1. Environment & Setup Management

| Archon CLI Feature | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Env Var Sanitization** | `R-PDD-SEC-004` (Exfiltration) | `stripCwdEnv()` removes `CLAUDE_CODE_*` and auto-loaded `<cwd>/.env*` keys. | Warns user of stripped variables during boot. | "Environment Sanitized" status indicator. | Extensions receive clean `process.env`. |
| **Hierarchical Env Loading** | `R-PDD-GOV-002` (Role Boundaries) | Loads `~/.archon/.env` then overrides with `<cwd>/.archon/.env`. | Displays active config source in footer. | "Workspace Environment" configuration panel. | `loadArchonEnv(cwd)` accessible to plugins. |
| **Git Repository Validation** | `R-PDD-AUDIT-001` (System State) | Validates `.git` root; exits 1 if not found. Auto-resolves subdirectory paths to repo root. | Shows warning dialog if launched outside a git repo. | Disables Archon-specific widgets if no git repo is linked. | Bypassed for `version`, `help`, `setup`, `chat`. |
| **Setup Wizard (`archon setup`)** | `R-PDD-GOV-001` (Human-in-the-Loop) | Interactive prompts to initialize `.archon/` directory. | Setup modal with guided steps. | Onboarding wizard component. | Generates default config JSONs. |
| **Database Auto-Initialization** | `R-PDD-AUDIT-004` (Artifacts) | Defaults to SQLite at `~/.archon/archon.db`. Supports PostgreSQL via `DATABASE_URL`. | Shows active DB connection state in status bar. | "Database Configuration" tab in settings. | Uses `@archon/core/db/connection.ts` (`closeDatabase`). |

## 2. Workflow Discovery & Execution

| Archon CLI Feature | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Workflow Discovery (`list`)**| `R-PDD-MD-001` (Prompts Select Intent) | `archon workflow list [--json]`. Parses `.archon/workflows/` and bundled defaults. | Interactive list of available workflows. | Workflow catalog grid with descriptions. | `discoverWorkflowsWithConfig(cwd, config)` |
| **Workflow Overrides** | `R-PDD-GOV-002` (Role Boundaries) | Repo-scoped YAML overrides bundled default workflows by name. | Warns when a bundled workflow is shadowed by local config. | Shows "Custom Override" badge on workflow cards. | Driven by `@archon/workflows/workflow-discovery`. |
| **Workflow Execution (`run`)** | `R-PDD-GOV-001` (Human-in-the-Loop) | `archon workflow run <name> [message]`. Streams responses to stdout via `CLIAdapter`. | Dedicated execution pane with live streaming. | Real-time chat/log viewer. | Uses `executeWorkflow()` from `@archon/workflows/executor`. |
| **Workflow Validation** | `R-PDD-SEC-001` (Tool Verification) | `archon validate`. Checks syntax of custom workflows. | Pre-flight validation checks before running. | Linting errors displayed in workflow editor. | Implemented in `src/commands/validate.ts`. |
| **Conversation Tracking** | `R-PDD-AUDIT-002` (Immutable Logs) | Uses ID format `cli-{timestamp}-{random}`. Logs to `conversationDb`. | Associates TUI sessions with unique DB IDs. | History panel driven by `conversationDb` queries. | `CLIAdapter.sendMessage(convId, msg)` |
| **Event Emission (`emit`)** | `R-PDD-AUDIT-001` (System State) | `archon workflow event emit --run-id <uuid> --type <type> --data <json>`. | Background system event bus. | Background system event bus. | Fire-and-forget storage via `createWorkflowEvent()`. |

## 3. Worktree Isolation Environments

| Archon CLI Feature | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Worktree Creation** | `R-PDD-SEC-002` (Execution Sandboxing) | `provider.create()` makes isolated git worktree at `~/.archon/workspaces/<owner>/<repo>/worktrees/<branch>/`. | "Creating Isolation Environment..." spinner. | Sandboxed terminal execution context. | `@archon/isolation/src/providers/worktree.ts` |
| **Branch Targeting (`--branch`)** | `R-PDD-AUDIT-001` (System State) | Auto-registers codebase and checks out specified branch. | Branch selector dropdown before workflow run. | "Target Branch" input field in execution form. | Managed by `isolationDb.findActiveByWorkflow()`. |
| **Base Branch (`--from`)** | `R-PDD-AUDIT-001` (System State) | Determines base branch when creating a new worktree. | Selectable base branch in Git integration UI. | Selectable base branch in Git integration UI. | Passes `fromBranch` to `provider.create()`. |
| **Worktree Reuse** | `R-PDD-PERF-001` (VRAM Offloading) | If existing worktree is healthy (`provider.healthCheck(path)`), reuses it. | Skipped creation step if healthy cache exists. | Fast-boot indicators for cached environments. | Warns if `--from` specified but existing worktree used. |
| **In-Place Execution (`--no-worktree`)** | `R-PDD-GOV-001` (Human-in-the-Loop) | Skips worktree creation; uses `cwd` as-is. Checks out branch in place. | Checkbox toggle for "Run in Current Directory". | "Disable Sandboxing" toggle. | Dangerous mode; logs explicit user override. |

## 4. Isolation Cleanup & Lifecycle

| Archon CLI Feature | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **List Environments (`list`)** | `R-PDD-AUDIT-001` (System State) | `archon isolation list`. Queries `isolationDb` and prints grouped table. | Interactive table of active sandboxes. | "Active Environments" dashboard view. | `isolationDb.listAllActiveWithCodebase()` |
| **Stale Cleanup (`cleanup`)** | `R-PDD-PERF-001` (VRAM Offloading) | `archon isolation cleanup [days]`. Defaults to 7 days. | "Purge Stale Environments" action. | "Storage Management" tab button. | `isolationDb.findStaleEnvironments(days)` |
| **Merged Branch Cleanup** | `R-PDD-AUDIT-001` (System State) | `archon isolation cleanup --merged`. Uses three-signal union to verify safety. | Included in periodic garbage collection. | "Clean Merged PRs" action. | Uses `@archon/core/src/services/cleanup-service.ts`. |
| **Git Fast-Forward Signal** | `R-PDD-AUDIT-001` (System State) | `isBranchMerged()` checks native git ancestry. | N/A (Backend logic). | N/A (Backend logic). | Short-circuits further checks if true. |
| **Git Cherry/Squash Signal** | `R-PDD-AUDIT-001` (System State) | `isPatchEquivalent()` checks if squashed to main. | N/A (Backend logic). | N/A (Backend logic). | `@archon/git/src/branch.ts` |
| **GitHub PR Signal (`gh` CLI)** | `R-PDD-GOV-004` (System Comms) | `getPrState()` queries `gh` CLI (MERGED/CLOSED/OPEN/NONE). | Soft dependency gracefully degrades if `gh` missing. | GitHub integration status indicator. | Skips removal if state is OPEN. |

## 5. Adapters & Outputs

| Archon CLI Feature | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CLIAdapter Streaming** | `R-PDD-AUDIT-001` (System State) | `sendMessage(convId, msg)` streams directly to `stdout`. | Custom `IPlatformAdapter` routing to UI buffers. | Websocket adapter implementation. | Extensions can hook stream chunks. |
| **Exit Code Enforcement** | `R-PDD-AUDIT-003` (Intervention) | Exits `0` on success, `1` on error (logs to `stderr`). | Captures exit codes to render error states. | Triggers global alert banners on exit `1`. | `cli.ts` wraps all handlers in try/catch. |
