# Exhaustive Archon Developer Guide Capabilities & AXiomEngine Governance Matrix

This comprehensive matrix maps every capability extracted from the Archon Developer Guide to its corresponding AXiomEngine Governance Rule, explicitly detailing how each feature integrates across the CLI, TUI, GUI, and interacts with platforms and extensions.

## 1. Multi-Platform Orchestration

| Archon Capability | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Orchestrator Routing** | `R-PDD-MD-001` (Prompts Select Intent) | AI Router parses CLI input to automatically select workflows. | AI Router parses chat messages to automatically select workflows. | Visual chat input routed to appropriate workflow automatically. | Uses AI to map arbitrary text strings to `archon-*` workflow IDs. |
| **Telegram Integration** | `R-PDD-GOV-004` (System-to-System Comms) | N/A | Status indicator for bot polling health. | "Telegram Bot Config" connection panel. | Implements Telegram polling and real-time streaming to DM. |
| **Slack Integration** | `R-PDD-GOV-004` (System-to-System Comms) | N/A | Status indicator for Slack Socket Mode. | "Slack Workspace Integration" connection panel. | Socket Mode connection (no webhooks), Thread context tracking. |
| **Discord Integration** | `R-PDD-GOV-004` (System-to-System Comms) | N/A | Status indicator for Discord WebSockets. | "Discord Bot Config" connection panel. | WebSocket connection, `@mention` activation, Thread tracking. |
| **GitHub Integration** | `R-PDD-GOV-004` (System-to-System Comms) | Triggerable via CLI testing hooks. | Real-time PR/Issue activity feed widget. | Webhook configuration panel. | Webhook listeners, Batch mode single-comment outputs, Auto-PR creation. |

## 🧪 Automated Verification Suite (Parity Index)

| Component | Test File(s) | Status |
| :--- | :--- | :--- |
| **Session Tree** | `agent-session-branching.test.ts`, `agent-session-tree-navigation.test.ts` | ✅ Verified |
| **Compaction** | `agent-session-compaction.test.ts`, `compaction.test.ts`, `compaction-serialization.test.ts` | ✅ Verified |
| **Extensions** | `extensions-discovery.test.ts`, `extensions-runner.test.ts`, `compaction-extensions.test.ts` | ✅ Verified |
| **RPC Mode** | `rpc.test.ts`, `rpc-jsonl.test.ts`, `rpc-prompt-response-semantics.test.ts` | ✅ Verified |
| **Settings** | `settings-manager.test.ts`, `config.test.ts`, `auth-storage.test.ts` | ✅ Verified |
| **Skills** | `skills.test.ts`, `sdk-skills.test.ts`, `frontmatter.test.ts` | ✅ Verified |
| **Packages** | `package-manager.test.ts`, `package-command-paths.test.ts`, `git-update.test.ts` | ✅ Verified |
| **TUI/Visual** | `interactive-mode-status.test.ts`, `footer-width.test.ts`, `theme-export.test.ts` | ✅ Verified |
| **Tool Execution**| `tools.test.ts`, `tool-execution-component.test.ts`, `edit-tool-legacy-input.test.ts`| ✅ Verified |
| **Cross-Platform**| `bash-close-hang-windows.test.ts`, `path-utils.test.ts` | ✅ Verified |

## 2. Interactive Commands & State

| Archon Capability | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Session Reset (`/reset`)** | `R-PDD-AUDIT-004` (Incidents as Artifacts) | Clears CLI context buffers. | Interactive chat command to purge session history. | "Clear Chat History" button. | Wipes DB context for active conversation UUID. |
| **Context Switching (`/repos`)** | `R-PDD-GOV-002` (Role Boundaries) | Interactive prompt to switch active repository context. | Dropdown command to switch active repository context. | Workspace/Repo sidebar selector. | Re-mounts `.archon/config.yaml` for new target. |
| **Directory Navigation (`/setcwd`)** | `R-PDD-SEC-002` (Execution Sandboxing) | Updates active `cwd` for CLI tool context. | Interactive command to jump into sub-folders. | File tree explorer widget. | Validates path bounds to prevent escape. |
| **System Status (`/status`)** | `R-PDD-AUDIT-001` (System State) | Dumps active workflows, worktrees, and DB state to stdout. | Generates rich dashboard overview in chat. | Native visual Dashboard mapping. | Aggregates DB metrics across all modules. |
| **Remote Cloning (`/clone`)** | `R-PDD-SEC-004` (Exfiltration) | CLI command to clone remote repos locally. | Triggers async clone job with progress bar. | "Clone Repository" URL input form. | Creates new workspace directory structure. |

## 3. Workflow Automation Engine

| Archon Capability | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **YAML Workflow Chaining** | `R-PDD-MD-001` (Prompts Select Intent) | Executed via `workflow run <yaml>`. | Visual indication of active workflow execution. | Visual drag-and-drop YAML graph editor. | Parses `.archon/workflows/*.yaml` definitions. |
| **DAG Dependency Ordering** | `R-PDD-AUDIT-001` (System State) | Executes `depends_on` nodes in strict topological order. | Live pipeline tracker showing completed/pending steps. | Visual Node/Edge graph highlighting active nodes. | Uses Workflow Executor engine. |
| **Node Context Isolation** | `R-PDD-GOV-002` (Role Boundaries) | `context: fresh` spins up clean LLM context per node. | Displays isolated message threads per sub-agent. | Tabbed sub-agent views in dashboard. | Clears token buffers between DAG steps. |
| **Markdown Agent Prompts**| `R-PDD-MD-001` (Prompts Select Intent) | Loads instructions from `.archon/commands/*.md`. | Source viewer for active prompt templates. | Markdown editor for custom Agent instructions. | Injected into System Prompt payload. |
| **Parallel Agent Execution** | `R-PDD-PERF-001` (VRAM Offloading) | Forks async execution threads for sibling DAG nodes. | Progress bars for concurrent agent jobs. | "Parallel Jobs" widget. | Runs (e.g. 5) PR review agents simultaneously. |

## 4. Bundled Autonomous Workflows

| Archon Capability | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Issue Fixer (`archon-fix-github-issue`)** | `R-PDD-GOV-001` (Human-in-the-Loop) | Triggered via `workflow run`. | Triggered via AI Router ("fix this issue"). | Dedicated "Resolve Issue" button next to GitHub issues. | Chains Investigation -> Implementation -> PR creation. |
| **PR Reviewer (`archon-comprehensive-pr-review`)** | `R-PDD-GOV-001` (Human-in-the-Loop) | Triggered via `workflow run`. | Triggered via AI Router ("review this PR"). | "Start Auto-Review" button on PRs. | Parallel agents (Coverage, Style, Errors, Docs) -> Synthesize -> Auto-Fix. |
| **Conflict Resolver (`archon-resolve-conflicts`)** | `R-PDD-GOV-001` (Human-in-the-Loop) | Triggered via `workflow run`. | Triggered via AI Router ("fix merge conflicts"). | "Auto-Resolve" button on conflicting branches. | Automates git operations and code merging. |

## ⚙️ AXiomEngine Internal Infrastructure (Legacy & Utility Index)

| Component | Logic Script(s) | CLI / TUI / GUI Exposure | Governance Rule |
| :--- | :--- | :--- | :--- |
| **Stitch Bus** | `stitch.py`, `dispatcher.py` | ✅ `ws/logs` gateway | `R-PDD-GOV-004` |
| **SIS Loop** | `sis_loop.py`, `heartbeat.py` | ✅ `03_heartbeat.py` monitor | `R-PDD-GOV-001` |
| **Swarm** | `swarm_coordinator.py`, `symphony.py`| ✅ `/swarm` slash command | `R-PDD-GOV-003` |
| **Ollama Ctrl** | `ollama_controller.py`, `Kimiko70B.Modelfile`| ✅ `get_agent_models` API | `R-PDD-EXEC-001` |
| **VGPU Manager** | `vgpu_manager.py` | ✅ TUI Sidebar (VRAM usage) | `R-PDD-GOV-002` |
| **Indexing** | `02_index_context.py`, `ast_indexer.py` | ✅ CLI background task | `R-PDD-AUDIT-001`|
| **Sandboxing** | `sandbox.py`, `qemu_launcher.sh` | ✅ Tool-level isolation | `R-PDD-SEC-001` |
| **Knowledge** | `knowledge_graph.py`, `kg_pruner.py` | ✅ Context injection hooks | `R-PDD-GOV-005` |

| **Ralph PRD Loop (`archon-ralph-dag`)** | `R-PDD-GOV-001` (Human-in-the-Loop) | Triggered via `workflow run`. | Triggered via AI Router ("run ralph"). | "Implement Spec" button. | Reads `prd.json`, iterates through stories until all `passes: true`. |
| **General Assistant (`archon-assist`)** | `R-PDD-GOV-001` (Human-in-the-Loop) | Triggered via `workflow run`. | Fallback trigger for general chat routing. | Default chat interface interaction. | Basic debugging, questions, ad-hoc execution. |

## 5. Workflow State Management

| Archon Capability | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Workflow Pause/Approval** | `R-PDD-GOV-001` (Human-in-the-Loop) | `/workflow approve <id> [comment]` via CLI. | Renders permission prompt requiring user confirmation. | Modal pop-up requiring approval button click. | Halts DAG execution until manual override. |
| **Workflow Rejection** | `R-PDD-GOV-001` (Human-in-the-Loop) | `/workflow reject <id> [reason]` via CLI. | Halts execution, feeds rejection reason back to AI. | Halts execution, feeds rejection reason back to AI. | Triggers re-prompting loop or fails pipeline. |
| **Workflow Cancellation** | `R-PDD-GOV-003` (Emergency Abort) | `/workflow cancel` stops the current run. | Hotkey to immediately kill active AI generation. | "Cancel Run" red button. | Issues kill signals to executing async threads. |
| **Workflow Reloading** | `R-PDD-AUDIT-001` (System State) | `/workflow reload` purges cache and re-reads YAMLs. | Reload command in interactive chat. | "Refresh Workflows" sync button. | Dynamically updates available commands list. |

## 6. Architecture & Configuration

| Archon Capability | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Git Worktree Isolation** | `R-PDD-SEC-002` (Execution Sandboxing) | Creates `~/.archon/workspaces/.../worktrees/issue-42/`. | Background isolation. | Background isolation. | Ensures parallel agent executions do not cause branch conflicts. |
| **Config Hierarchy Layering** | `R-PDD-GOV-002` (Role Boundaries) | Env Vars override `.archon/config.yaml` override `~/.archon/config.yaml` override defaults. | Respects hierarchical configuration loading. | Settings UI explicitly shows which layer overrides a setting. | Enforced by global config parsers. |
| **Per-Repo Custom Prompts** | `R-PDD-MD-001` (Prompts Select Intent) | Loads project-specific instructions from `.archon/commands/`. | Context tag indicating local prompt overrides. | "Workspace Prompts" configuration file editor. | Allows custom behavior bound to specific codebases. |
