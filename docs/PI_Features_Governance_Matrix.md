# Exhaustive PI Capabilities & AXiomEngine Governance Matrix

This comprehensive matrix maps every feature extracted from the `pi.dev` ecosystem to its corresponding AXiomEngine Governance Rule, and explicitly details how each feature is integrated across the CLI, TUI, GUI, and how it interacts with external packages and extensions.

## 1. Core Session & Execution Management

| PI Feature | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Plannotator Integration** | `R-PDD-GOV-005` (Visual Feedback) | `pi --plannotator` | `/plannotator-review` command. | Hotkey to trigger visual overlay. | "Visual Review" dashboard tab. |
| **Encrypted Sharing** | `R-PDD-SEC-004` (Exfiltration) | CLI approval prompt | TUI modal for approval | GUI toggle in settings | End-to-end encrypted shortlinks. |
| **Interactive Shell Loop** | `R-PDD-GOV-001` (Human-in-the-Loop) | Execute `pi` to block and read stdin. | `rich` layout with streaming text regions. | WebSocket streaming into Chat Widget. | Hooked via `pi.on("session_start")` |
| **Session Auto-Save** | `R-PDD-AUDIT-004` (Incidents as Artifacts) | Implicit save to `.pi/agent/sessions/` on exit. | Live footer indicator of active session ID. | Left-hand sidebar updating in real-time. | `ctx.sessionManager.getSessionFile()` |
| **Session Resumption (`-c` / `-r`)** | `R-PDD-AUDIT-001` (System State) | `pi -c` (continue last) or `pi -r` (fzf list). | `/resume` opens interactive overlay picker. | "Recent Sessions" dashboard panel. | Emits `session_before_switch` |
| **Ephemeral Sessions (`--no-session`)** | `R-PDD-SEC-004` (Exfiltration) | `pi --no-session` | Flag toggle at startup or in `/settings`. | "Incognito Mode" toggle on chat start. | Extensions cannot access `SessionManager`. |
| **Session Tree Branching (`/fork`)** | `R-PDD-AUDIT-002` (Immutable Logs) | `pi --fork <id>` | Select message -> `f` hotkey to fork. | Visual graph tree node -> Right Click -> Fork. | Emits `session_before_fork` |
| **Session Cloning (`/clone`)** | `R-PDD-AUDIT-002` (Immutable Logs) | `pi --clone` | `/clone` duplicates branch to new file. | "Duplicate Session" action button. | Generates new UUID for `ExtensionContext`. |
| **Tree Visualization (`/tree`)** | `R-PDD-AUDIT-001` (System State) | `pi --tree` prints ASCII representation. | Modal window rendering branched lines. | Interactive D3.js or Vis.js diagram. | Extensions can hook `session_before_tree`. |
| **Context Compaction (`/compact`)** | `R-PDD-PERF-001` (VRAM Offloading) | `pi --compact [prompt]` | `/compact` summarizes active branch. | "Optimize Memory" one-click button. | Hooks `session_before_compact`. |
| **Steering Messages (Queue)** | `R-PDD-GOV-003` (Emergency Abort) | POST to running Valkey task. | `Enter` while agent is thinking. | "Interrupt & Steer" button. | Pauses `tool_execution` loop. |
| **Follow-Up Messages (Queue)** | `R-PDD-GOV-001` (Human-in-the-Loop) | Append JSON to running Valkey task. | `Alt+Enter` or `Shift+Enter`. | Queued Task List widget. | Stored in `ExtensionCommandContext`. |
| **Agent Core Loop** | `R-PDD-GOV-001` (Event Streaming) | `pi --mode json` streams loop events. | Live updates via `AgentLoopEvent` stream (inc. thinking). | WebSocket streams structured loop events to GUI. | Core `agent_loop()` generator logic. |
| **AI Abstraction Layer** | `R-PDD-GOV-002` (Unified Providers) | `--model` switch across providers. | Sidebar updates model metadata; live cost tracking. | Model selection dropdown in GUI. | `pi_ai.py` unified API; Cross-Provider Handoffs. |
| **Tool Validation** | `R-PDD-SEC-001` (Safe Execution) | Blocks and errors on invalid JSON schema. | Red error messages for validation failures. | Audit log captures validation rejections. | `jsonschema` enforcement in loop. |
| **Cross-Provider Handoffs**| `R-PDD-GOV-002` (Unified Providers) | Implicit conversion on model switch. | Thinking blocks serialized to tags mid-stream. | Transparent context transformation in gateway. | `_transform_context` in `pi_ai.py`. |
| **AI Compatibility Layer**| `R-PDD-MD-001` (Intent Capture) | CLI flags for compat settings. | Auto-detects provider capabilities (e.g. DeepSeek). | GUI settings for per-model compat flags. | `OpenAICompletionsCompat` schema. |
| **Session Compaction** | `R-PDD-PERF-001` (VRAM Offloading) | `/compact` manual command. | Auto-summarization on context threshold. | One-click "Optimize Memory" in dashboard. | `CompactionManager` with PI summary spec. |
| **JSON Event Stream** | `R-PDD-AUDIT-001` (System State) | `pi --mode json` outputs official events. | N/A (Console mode). | Consumed by GUI WebSocket for real-time state. | Official `AgentSessionEvent` schema. |
| **Debug Logging** | `R-PDD-AUDIT-004` (Diagnostics) | `/debug` writes to `~/.pi/agent/pi-debug.log`. | Status bar reflects debug state. | Debug logs viewable via `/ws/logs`. | `pi_config.py` diagnostic helper. |
| **Extension Events** | `R-PDD-AUDIT-001` (System State) | `session_start` emitted on boot. | `turn_end` triggers dashboard refreshes. | WebSocket streams extension-specific updates. | `pi.on()` event system. |
| **UI Modals (ctx.ui)**| `R-PDD-GOV-001` (Human-in-the-Loop) | Blocks CLI with `[y/N]` prompt. | Renders Rich modal dialog in terminal. | Triggers browser-native `<dialog>` via WS. | `ExtensionUI` bridge logic. |
| **Termux Clipboard** | `R-PDD-SEC-004` (Exfiltration) | `termux-clipboard-set` detection. | Syncs clipboard to Android system. | Syncs clipboard to browser session. | `clipboard_utils.py` cross-platform helper. |
| **Custom Keybindings** | `R-PDD-GOV-003` (Interaction) | N/A (CLI uses standard readline). | `keybindings.json` overrides TUI map. | Customizable hotkeys in dashboard settings. | `get_keybindings()` in `pi_config.py`. |
| **Shell Stability** | `R-PDD-EXEC-001` (Authoritative) | Auto-detects Git Bash/WSL on Windows. | N/A (Tool execution is background). | N/A (Managed by remote worker). | `get_bash_path()` in `shell_utils.py`. |
| **Custom Model Reg.** | `R-PDD-GOV-002` (Unified Providers) | `models.json` loads custom APIs. | Custom models show in `/model` list. | GUI dropdown reflects `models.json` entries. | `AIRegistry.load_custom_models()`. |
| **PI Package Reg.** | `R-PDD-GOV-004` (Ecosystem) | `pi install` for npm/git/local. | Packages inject tools/commands. | GUI dashboard lists installed packages. | `PackageManager` with post-install hooks. |
| **Dependency Iso.** | `R-PDD-SEC-002` (Isolation) | Project-local `.pi/` overrides global. | Extensions scoped to package root. | Settings resolution preserves isolation. | `_get_package_paths()` logic. |

## 2. Command & UI Systems

| PI Feature | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Slash Commands (`/`)** | `R-PDD-MD-001` (Prompts Select Intent) | User types `/command args`. | Autocomplete floating window. | Command Palette (Cmd+K). | `pi.registerCommand("name", handler)` |
| **Custom Shortcuts** | `R-PDD-GOV-001` (Human-in-the-Loop) | Configured in `keybindings.json`. | Captured via standard curses/prompt-toolkit. | Customizable keyboard shortcuts panel. | `pi.registerShortcut("ctrl+x", handler)` |
| **CLI Flags (`--flag`)** | `R-PDD-MD-001` (Prompts Select Intent) | Passthrough to sys.argv. | Translates to internal state flags. | Toggles in the Settings form. | `pi.registerFlag("my-flag", options)` |
| **Theme Overrides** | `R-PDD-MD-002` (System Aesthetics) | `--theme <path>` | Loads `.theme` JSON for ANSI colors. | Applies CSS variable overrides dynamically. | Extensions bundle `.theme` files. |
| **UI Context Modals** | `R-PDD-GOV-001` (Human-in-the-Loop) | Blocks terminal awaiting `[y/N]`. | Renders centered modal overlay box. | Triggers browser-native `<dialog>` or React modal. | `ctx.ui.confirm("Title", "Message")` |
| **UI Notifications** | `R-PDD-AUDIT-001` (System State) | Prints `[LEVEL] Message` to stdout. | Renders temporary toast in bottom-right. | React hot-toast in top-right. | `ctx.ui.notify("Msg", "success")` |
| **Status Footers** | `R-PDD-AUDIT-001` (System State) | Appends to CLI output periodically. | Live-updating bottom bar (Tokens, VRAM). | Fixed footer bar across all pages. | `ctx.ui.setStatus("ext_id", "msg")` |
| **UI Widgets** | `R-PDD-AUDIT-001` (System State) | N/A (Console doesn't support fixed widgets). | Fixed text box above the input editor. | React component injected into Dashboard. | `ctx.ui.setWidget("ext_id", ["L1", "L2"])` |
| **Custom TUI Components** | `R-PDD-MD-002` (System Aesthetics) | N/A | Full layout engine capturing raw keystrokes. | iFrame or sandboxed React component. | `ctx.ui.custom()` |

## 3. Extensibility & Plugins

| PI Feature | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Typescript/Python Extensions** | `R-PDD-SEC-002` (Execution Sandboxing) | Loaded via `-e path.ts` or `extensions/` dir. | Listed in startup banner. | Extensions Marketplace / Registry View. | Can import `ExtensionAPI` and `node:fs`. |
| **Lifecycle Hook: `session_start`**| `R-PDD-AUDIT-001` (System State) | Daemon logs execution. | Daemon logs execution. | Visual indicator of Extension boot. | `pi.on("session_start")` |
| **Lifecycle Hook: `tool_call`** | `R-PDD-SEC-001` (Tool Verification) | Blocks execution on LLM invocation. | Triggers permission checks mid-turn. | Audit log captures intercepted calls. | `pi.on("tool_call")` returns `{block: True}`. |
| **Lifecycle Hook: `turn_end`** | `R-PDD-AUDIT-001` (System State) | Logs metrics. | Updates metrics overlay. | Refreshes VRAM usage graphs. | `pi.on("turn_end")` |
| **Custom Tool Registration** | `R-PDD-SEC-001` (Tool Verification) | Added to JSON Schema block dynamically. | Shows in `/tools` command. | Listed in "Available LLM Tools". | `pi.registerTool({ name: "greet", ... })` |
| **Custom Message Renderers** | `R-PDD-MD-002` (System Aesthetics) | Applies ANSI formatting. | Uses Rich to format custom markdown tags. | Uses React components to render payload data. | `pi.registerMessageRenderer(type, func)` |
| **Package Management (`npm`/`git`)**| `R-PDD-SEC-003` (Dependency Auditing) | `pi install <git-url>` | Managed via `/settings` package tab. | "Install Package" button in Marketplace. | Discovers `skills/` and `extensions/` within packages. |

## 4. Context & Governance Loading

| PI Feature | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Global Prompts (`AGENTS.md`)** | `R-PDD-GOV-002` (Role Boundaries) | Loads `~/.pi/agent/AGENTS.md`. | Context tag visible in header. | "Global Settings -> Prompts" editor. | Modifies baseline system instruction. |
| **Project Prompts (`SYSTEM.md`)**| `R-PDD-GOV-002` (Role Boundaries) | Loads `./.pi/SYSTEM.md` recursively. | Overrides global context tag. | "Workspace Context" side-panel. | Hooks `ctx.getSystemPrompt()`. |
| **Prompt Templates (`/template`)** | `R-PDD-MD-001` (Prompts Select Intent) | Type `/template` to inject text. | Auto-expands in editor block. | Clickable buttons to insert into chatbox. | Scanned during `resources_discover`. |
| **Agent Skills (`SKILL.md`)** | `R-PDD-MD-001` (Prompts Select Intent) | Loads `./skills/` directory. | Type `/skill:name` to explicitly load. | "Active Skills" toggles on right sidebar. | Frontmatter (`name`, `description`) parsed dynamically. |
| **Progressive Skill Loading** | `R-PDD-PERF-001` (VRAM Offloading) | System prompt gets brief skill descriptions. | Full `SKILL.md` injected when `read` tool used. | Transparent to user; saves context. | Built-in `read` tool intercepts paths. |
| **Output Truncation** | `R-PDD-PERF-001` (VRAM Offloading) | Limits stdout capture for LLM feedback. | Ellipses long tool responses dynamically. | "Expand to see full output" dropdown. | Handled in MCP Bridge core logic. |

## 5. Providers, Models & External API

| PI Feature | AXiomEngine Governance Rule | CLI Implementation | TUI Implementation | GUI Implementation | Integration & Extensions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dynamic Model Switching** | `R-PDD-PERF-001` (VRAM Offloading) | `--model <name>` | `Ctrl+P` opens model selection fuzzy finder. | Top-right navigation dropdown. | `pi.setModel()` inside extension logic. |
| **Custom Providers** | `R-PDD-SEC-004` (Exfiltration) | `pi.registerProvider("custom", config)` | Available in model fuzzy finder. | "Add API Key/Endpoint" in Settings GUI. | Async factory fetches remote models on boot. |
| **Thinking Levels Toggling** | `R-PDD-PERF-001` (VRAM Offloading) | `--thinking high` | Keyboard shortcut toggles `<think>` context. | Dedicated toggle switch near send button. | `pi.setThinkingLevel(level)` |
| **RPC Mode (JSONL Stdin)** | `R-PDD-GOV-004` (System-to-System Comms) | `echo "{}" \| pi --mode rpc` | Disabled in TUI. | Backend pipeline capability only. | Bypasses UI context hooks. |
| **JSON Event Stream** | `R-PDD-AUDIT-001` (System State) | `pi --mode json` | Disabled in TUI. | Used to stream data directly to frontend Websocket. | Emits raw `tool_call` and `chunk` events natively. |
| **Session Export (`/export`)** | `R-PDD-AUDIT-004` (Incidents as Artifacts) | `pi --export out.html` | `/export` saves static UI representation. | "Export as HTML/PDF" button. | Uses internal renderer to serialize state. |
| **Session Share (`/share`)** | `R-PDD-SEC-004` (Exfiltration) | `pi --share` (pushes to Gist). | `/share` triggers Gist OAuth prompt. | "Publish to GitHub Gist" button. | Triggers validation hook before network call. |
