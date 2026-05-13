# PI Deep Governance Library

| Rule ID | Section | Rule Description | Source File |
| :--- | :--- | :--- | :--- |
| G-PI-AGENTS-001 | Conversational Style | Keep answers short and concise | AGENTS.md |
| G-PI-AGENTS-002 | Conversational Style | No emojis in commits, issues, PR comments, or code | AGENTS.md |
| G-PI-AGENTS-003 | Conversational Style | No fluff or cheerful filler text | AGENTS.md |
| G-PI-AGENTS-004 | Conversational Style | Technical prose only, be kind but direct (e.g., "Thanks @user" not "Thanks so much @user!") | AGENTS.md |
| G-PI-AGENTS-005 | Code Quality | No `any` types unless absolutely necessary | AGENTS.md |
| G-PI-AGENTS-006 | Code Quality | Check node_modules for external API type definitions instead of guessing | AGENTS.md |
| G-PI-AGENTS-007 | Code Quality | NEVER use inline imports  no `await import("./foo.js")`, no `import("pkg").Type` in type positions, no dynamic imports for types. Always use standard toplevel imports. | AGENTS.md |
| G-PI-AGENTS-008 | Code Quality | NEVER remove or downgrade code to fix type errors from outdated dependencies; upgrade the dependency instead | AGENTS.md |
| G-PI-AGENTS-009 | Code Quality | Always ask before removing functionality or code that appears to be intentional | AGENTS.md |
| G-PI-AGENTS-010 | Code Quality | Do not preserve backward compatibility unless the user explicitly asks for it | AGENTS.md |
| G-PI-AGENTS-011 | Code Quality | Never hardcode key checks with, eg. `matchesKey(keyData, "ctrl+x")`. All keybindings must be configurable. Add default to matching object (`DEFAULT_EDITOR_KEYBINDINGS` or `DEFAULT_APP_KEYBINDINGS`) | AGENTS.md |
| G-PI-AGENTS-012 | Code Quality | NEVER modify `packages/ai/src/models.generated.ts` directly. Update `packages/ai/scripts/generatemodels.ts` instead. | AGENTS.md |
| G-PI-AGENTS-013 | Commands | After code changes (not documentation changes): `npm run check` (get full output, no tail). Fix all errors, warnings, and infos before committing. | AGENTS.md |
| G-PI-AGENTS-014 | Commands | Note: `npm run check` does not run tests. | AGENTS.md |
| G-PI-AGENTS-015 | Commands | NEVER run: `npm run dev`, `npm run build`, `npm test` | AGENTS.md |
| G-PI-AGENTS-016 | Commands | Only run specific tests if user instructs: `npx tsx ../../node_modules/vitest/dist/cli.js run test/specific.test.ts` | AGENTS.md |
| G-PI-AGENTS-017 | Commands | Run tests from the package root, not the repo root. | AGENTS.md |
| G-PI-AGENTS-018 | Commands | If you create or modify a test file, you MUST run that test file and iterate until it passes. | AGENTS.md |
| G-PI-AGENTS-019 | Commands | When writing tests, run them, identify issues in either the test or implementation, and iterate until fixed. | AGENTS.md |
| G-PI-AGENTS-020 | Commands | For `packages/codingagent/test/suite/`, use `test/suite/harness.ts` plus the faux provider. Do not use real provider APIs, real API keys, or paid tokens. | AGENTS.md |
| G-PI-AGENTS-021 | Commands | Put issuespecific regressions under `packages/codingagent/test/suite/regressions/` and name them `<issuenumber><shortslug>.test.ts`. | AGENTS.md |
| G-PI-AGENTS-022 | Commands | NEVER commit unless user asks | AGENTS.md |
| G-PI-AGENTS-023 | Contribution Gate | New issues from new contributors are autoclosed by `.github/workflows/issuegate.yml` | AGENTS.md |
| G-PI-AGENTS-024 | Contribution Gate | New PRs from new contributors without PR rights are autoclosed by `.github/workflows/prgate.yml` | AGENTS.md |
| G-PI-AGENTS-025 | Contribution Gate | Maintainer approval comments are handled by `.github/workflows/approvecontributor.yml` | AGENTS.md |
| G-PI-AGENTS-026 | Contribution Gate | Maintainers review autoclosed issues daily | AGENTS.md |
| G-PI-AGENTS-027 | Contribution Gate | Issues that do not meet the quality bar in `CONTRIBUTING.md` are not reopened and do not receive a reply | AGENTS.md |
| G-PI-AGENTS-028 | Contribution Gate | `lgtmi` approves future issues | AGENTS.md |
| G-PI-AGENTS-029 | Contribution Gate | `lgtm` approves future issues and rights to submit PRs | AGENTS.md |
| G-PI-AGENTS-030 | Contribution Gate | Add `pkg:` labels to indicate which package(s) the issue affects | AGENTS.md |
| G-PI-AGENTS-031 | Contribution Gate | Available labels: `pkg:agent`, `pkg:ai`, `pkg:codingagent`, `pkg:tui`, `pkg:webui` | AGENTS.md |
| G-PI-AGENTS-032 | Contribution Gate | If an issue spans multiple packages, add all relevant labels | AGENTS.md |
| G-PI-AGENTS-033 | Contribution Gate | Write the full comment to a temp file and use `gh issue comment bodyfile` or `gh pr comment bodyfile` | AGENTS.md |
| G-PI-AGENTS-034 | Contribution Gate | Never pass multiline markdown directly via `body` in shell commands | AGENTS.md |
| G-PI-AGENTS-035 | Contribution Gate | Preview the exact comment text before posting | AGENTS.md |
| G-PI-AGENTS-036 | Contribution Gate | Post exactly one final comment unless the user explicitly asks for multiple comments | AGENTS.md |
| G-PI-AGENTS-037 | Contribution Gate | If a comment is malformed, delete it immediately, then post one corrected comment | AGENTS.md |
| G-PI-AGENTS-038 | Contribution Gate | Keep comments concise, technical, and in the user's tone | AGENTS.md |
| G-PI-AGENTS-039 | Contribution Gate | Include `fixes #<number>` or `closes #<number>` in the commit message | AGENTS.md |
| G-PI-AGENTS-040 | Contribution Gate | This automatically closes the issue when the commit is merged | AGENTS.md |
| G-PI-AGENTS-041 | PR Workflow | Analyze PRs without pulling locally first | AGENTS.md |
| G-PI-AGENTS-042 | PR Workflow | If the user approves: create a feature branch, pull PR, rebase on main, apply adjustments, commit, merge into main, push, close PR, and leave a comment in the user's tone | AGENTS.md |
| G-PI-AGENTS-043 | PR Workflow | You never open PRs yourself. We work in feature branches until everything is according to the user's requirements, then merge into main, and push. | AGENTS.md |
| G-PI-AGENTS-044 | Format | `### Breaking Changes`  API changes requiring migration | AGENTS.md |
| G-PI-AGENTS-045 | Format | `### Added`  New features | AGENTS.md |
| G-PI-AGENTS-046 | Format | `### Changed`  Changes to existing functionality | AGENTS.md |
| G-PI-AGENTS-047 | Format | `### Fixed`  Bug fixes | AGENTS.md |
| G-PI-AGENTS-048 | Format | `### Removed`  Removed features | AGENTS.md |
| G-PI-AGENTS-049 | Rules | Before adding entries, read the full `[Unreleased]` section to see which subsections already exist | AGENTS.md |
| G-PI-AGENTS-050 | Rules | New entries ALWAYS go under `## [Unreleased]` section | AGENTS.md |
| G-PI-AGENTS-051 | Rules | Append to existing subsections (e.g., `### Fixed`), do not create duplicates | AGENTS.md |
| G-PI-AGENTS-052 | Rules | NEVER modify alreadyreleased version sections (e.g., `## [0.12.2]`) | AGENTS.md |
| G-PI-AGENTS-053 | Rules | Each version section is immutable once released | AGENTS.md |
| G-PI-AGENTS-054 | Attribution | Internal changes (from issues): `Fixed foo bar ([#123](https://github.com/badlogic/pimono/issues/123))` | AGENTS.md |
| G-PI-AGENTS-055 | Attribution | External contributions: `Added feature X ([#456](https://github.com/badlogic/pimono/pull/456) by [@username](https://github.com/username))` | AGENTS.md |
| G-PI-AGENTS-056 | 1. Core Types (`packages/ai/src/types.ts`) | Add API identifier to `Api` type union (e.g., `"bedrockconversestream"`) | AGENTS.md |
| G-PI-AGENTS-057 | 1. Core Types (`packages/ai/src/types.ts`) | Create options interface extending `StreamOptions` | AGENTS.md |
| G-PI-AGENTS-058 | 1. Core Types (`packages/ai/src/types.ts`) | Add mapping to `ApiOptionsMap` | AGENTS.md |
| G-PI-AGENTS-059 | 1. Core Types (`packages/ai/src/types.ts`) | Add provider name to `KnownProvider` type union | AGENTS.md |
| G-PI-AGENTS-060 | 2. Provider Implementation (`packages/ai/src/providers/`) | `stream<Provider>()` function returning `AssistantMessageEventStream` | AGENTS.md |
| G-PI-AGENTS-061 | 2. Provider Implementation (`packages/ai/src/providers/`) | `streamSimple<Provider>()` for `SimpleStreamOptions` mapping | AGENTS.md |
| G-PI-AGENTS-062 | 2. Provider Implementation (`packages/ai/src/providers/`) | Providerspecific options interface | AGENTS.md |
| G-PI-AGENTS-063 | 2. Provider Implementation (`packages/ai/src/providers/`) | Message/tool conversion functions | AGENTS.md |
| G-PI-AGENTS-064 | 2. Provider Implementation (`packages/ai/src/providers/`) | Response parsing emitting standardized events (`text`, `tool_call`, `thinking`, `usage`, `stop`) | AGENTS.md |
| G-PI-AGENTS-065 | 3. Provider Exports and Lazy Registration | Add a package subpath export in `packages/ai/package.json` pointing at `./dist/providers/<provider>.js` | AGENTS.md |
| G-PI-AGENTS-066 | 3. Provider Exports and Lazy Registration | Add `export type` reexports in `packages/ai/src/index.ts` for provider option types that should remain available from the root entry | AGENTS.md |
| G-PI-AGENTS-067 | 3. Provider Exports and Lazy Registration | Register the provider in `packages/ai/src/providers/registerbuiltins.ts` via lazy loader wrappers, do not statically import provider implementation modules there | AGENTS.md |
| G-PI-AGENTS-068 | 3. Provider Exports and Lazy Registration | Add credential detection in `packages/ai/src/envapikeys.ts` | AGENTS.md |
| G-PI-AGENTS-069 | 4. Model Generation (`packages/ai/scripts/generate-models.ts`) | Add logic to fetch/parse models from provider source | AGENTS.md |
| G-PI-AGENTS-070 | 4. Model Generation (`packages/ai/scripts/generate-models.ts`) | Map to standardized `Model` interface | AGENTS.md |
| G-PI-AGENTS-071 | 5. Tests (`packages/ai/test/`) | Always add the provider to `stream.test.ts` with at least one representative model, even if it reuses an existing API implementation such as `openaicompletions`. | AGENTS.md |
| G-PI-AGENTS-072 | 5. Tests (`packages/ai/test/`) | Add the provider to the broader provider matrix where applicable: `tokens.test.ts`, `abort.test.ts`, `empty.test.ts`, `contextoverflow.test.ts`, `imagelimits.test.ts`, `unicodesurrogate.test.ts`, `toolcallwithoutresult.test.ts`, `imagetoolresult.test.ts`, `totaltokens.test.ts`, `crossproviderhandoff.test.ts`. | AGENTS.md |
| G-PI-AGENTS-073 | 5. Tests (`packages/ai/test/`) | For `crossproviderhandoff.test.ts`, add at least one provider/model pair. If the provider exposes multiple model families (for example GPT and Claude), add at least one pair per family. | AGENTS.md |
| G-PI-AGENTS-074 | 5. Tests (`packages/ai/test/`) | For nonstandard auth, create utility (e.g., `bedrockutils.ts`) with credential detection. | AGENTS.md |
| G-PI-AGENTS-075 | 6. Coding Agent (`packages/coding-agent/`) | `src/core/modelresolver.ts`: Add default model ID to `defaultModelPerProvider` | AGENTS.md |
| G-PI-AGENTS-076 | 6. Coding Agent (`packages/coding-agent/`) | `src/core/providerdisplaynames.ts`: Add APIkey login display name so `/login` and related UI show the provider for builtin APIkey auth. | AGENTS.md |
| G-PI-AGENTS-077 | 6. Coding Agent (`packages/coding-agent/`) | `src/cli/args.ts`: Add env var documentation | AGENTS.md |
| G-PI-AGENTS-078 | 6. Coding Agent (`packages/coding-agent/`) | `README.md`: Add provider setup instructions | AGENTS.md |
| G-PI-AGENTS-079 | 6. Coding Agent (`packages/coding-agent/`) | `docs/providers.md`: Add setup instructions, env var, and `auth.json` key | AGENTS.md |
| G-PI-AGENTS-080 | 7. Documentation | `packages/ai/README.md`: Add to providers table, document options/auth, add env vars | AGENTS.md |
| G-PI-AGENTS-081 | 7. Documentation | `packages/ai/CHANGELOG.md`: Add entry under `## [Unreleased]` | AGENTS.md |
| G-PI-AGENTS-082 | Releasing | Lockstep versioning: All packages always share the same version number. Every release updates all packages together. | AGENTS.md |
| G-PI-AGENTS-083 | Releasing | Version semantics (no major releases): | AGENTS.md |
| G-PI-AGENTS-084 | Releasing | `patch`: Bug fixes and new features | AGENTS.md |
| G-PI-AGENTS-085 | Releasing | `minor`: API breaking changes | AGENTS.md |
| G-PI-AGENTS-086 | Committing | ONLY commit files YOU changed in THIS session | AGENTS.md |
| G-PI-AGENTS-087 | Committing | ALWAYS include `fixes #<number>` or `closes #<number>` in the commit message when there is a related issue or PR | AGENTS.md |
| G-PI-AGENTS-088 | Committing | NEVER use `git add A` or `git add .`  these sweep up changes from other agents | AGENTS.md |
| G-PI-AGENTS-089 | Committing | ALWAYS use `git add <specificfilepaths>` listing only files you modified | AGENTS.md |
| G-PI-AGENTS-090 | Committing | Before committing, run `git status` and verify you are only staging YOUR files | AGENTS.md |
| G-PI-AGENTS-091 | Committing | Track which files you created/modified/deleted during the session | AGENTS.md |
| G-PI-AGENTS-092 | Committing | It is always fine to include `packages/ai/src/models.generated.ts` in a commit alongside the actual files you want to commit | AGENTS.md |
| G-PI-AGENTS-093 | Forbidden Git Operations | `git reset hard`  destroys uncommitted changes | AGENTS.md |
| G-PI-AGENTS-094 | Forbidden Git Operations | `git checkout .`  destroys uncommitted changes | AGENTS.md |
| G-PI-AGENTS-095 | Forbidden Git Operations | `git clean fd`  deletes untracked files | AGENTS.md |
| G-PI-AGENTS-096 | Forbidden Git Operations | `git stash`  stashes ALL changes including other agents' work | AGENTS.md |
| G-PI-AGENTS-097 | Forbidden Git Operations | `git add A` / `git add .`  stages other agents' uncommitted work | AGENTS.md |
| G-PI-AGENTS-098 | Forbidden Git Operations | `git commit noverify`  bypasses required checks and is never allowed | AGENTS.md |
| G-PI-AGENTS-099 | If Rebase Conflicts Occur | Resolve conflicts in YOUR files only | AGENTS.md |
| G-PI-AGENTS-100 | If Rebase Conflicts Occur | If conflict is in a file you didn't modify, abort and ask the user | AGENTS.md |
| G-PI-AGENTS-101 | If Rebase Conflicts Occur | NEVER force push | AGENTS.md |
| G-PI-CONTRIBUTING-001 | The One Rule | You must understand your code. If you cannot explain what your changes do and how they interact with the rest of the system, your PR will be closed. | CONTRIBUTING.md |
| G-PI-CONTRIBUTING-002 | Contribution Gate | `lgtmi`: your future issues will not be autoclosed | CONTRIBUTING.md |
| G-PI-CONTRIBUTING-003 | Contribution Gate | `lgtm`: your future issues and PRs will not be autoclosed | CONTRIBUTING.md |
| G-PI-CONTRIBUTING-004 | Quality Bar For Issues | Keep it concise. If it does not fit on one screen, it is too long. | CONTRIBUTING.md |
| G-PI-CONTRIBUTING-005 | Quality Bar For Issues | Write in your own voice. | CONTRIBUTING.md |
| G-PI-CONTRIBUTING-006 | Quality Bar For Issues | State the bug or request clearly. | CONTRIBUTING.md |
| G-PI-CONTRIBUTING-007 | Quality Bar For Issues | Explain why it matters. | CONTRIBUTING.md |
| G-PI-CONTRIBUTING-008 | Quality Bar For Issues | If you want to implement the change yourself, say so. | CONTRIBUTING.md |
| G-PI-README-001 | Share your OSS coding agent sessions | [badlogicgames/pimono on Hugging Face](https://huggingface.co/datasets/badlogicgames/pimono) | README.md |
| G-PI-CHANGELOG-001 | Added | Added `shouldStopAfterTurn` to the lowlevel agent loop config for gracefully exiting after a completed turn before polling queued messages or starting another LLM call. | CHANGELOG.md |
| G-PI-CHANGELOG-002 | Breaking Changes | Migrated public TypeBoxfacing types and examples from `@sinclair/typebox` 0.34.x to `typebox` 1.x. Install and import from `typebox` instead of relying on `@sinclair/typebox` transitively ([#3112](https://github.com/badlogic/pimono/issues/3112)) | CHANGELOG.md |
| G-PI-CHANGELOG-003 | Added | Added `terminate: true` toolresult hints to skip the automatic followup LLM call when every finalized tool result in the current batch opts into early termination ([#3525](https://github.com/badlogic/pimono/issues/3525)) | CHANGELOG.md |
| G-PI-CHANGELOG-004 | Fixed | Fixed `streamProxy()` to preserve the proxysafe serializable subset of stream options, including session, transport, retrydelay, metadata, header, cacheretention, and thinkingbudget settings ([#3512](https://github.com/badlogic/pimono/issues/3512)) | CHANGELOG.md |
| G-PI-CHANGELOG-005 | Fixed | Fixed parallel tool execution to emit `tool_execution_end` as soon as each tool is finalized, while still emitting persisted toolresult messages in assistant source order ([#3503](https://github.com/badlogic/pimono/issues/3503)) | CHANGELOG.md |
| G-PI-CHANGELOG-006 | Changed | Clarified parallel tool execution ordering docs to specify that final tool lifecycle and toolresult artifacts are emitted in tool completion order. | CHANGELOG.md |
| G-PI-CHANGELOG-007 | Fixed | Fixed parallel toolcall finalization to convert `afterToolCall` hook throws into error tool results instead of aborting the batch ([#3084](https://github.com/badlogic/pimono/issues/3084)) | CHANGELOG.md |
| G-PI-CHANGELOG-008 | Breaking Changes | `AgentState` has been reshaped: | CHANGELOG.md |
| G-PI-CHANGELOG-009 | Breaking Changes | `streamMessage` was renamed to `streamingMessage` | CHANGELOG.md |
| G-PI-CHANGELOG-010 | Breaking Changes | `error` was renamed to `errorMessage` | CHANGELOG.md |
| G-PI-CHANGELOG-011 | Breaking Changes | `isStreaming`, `streamingMessage`, `pendingToolCalls`, and `errorMessage` are now readonly in the public API | CHANGELOG.md |
| G-PI-CHANGELOG-012 | Breaking Changes | `pendingToolCalls` is now typed as `ReadonlySet<string>` | CHANGELOG.md |
| G-PI-CHANGELOG-013 | Breaking Changes | `tools` and `messages` are now accessor properties, and assigning either field copies the provided toplevel array instead of preserving array identity | CHANGELOG.md |
| G-PI-CHANGELOG-014 | Breaking Changes | `AgentOptions.initialState` no longer accepts runtimeowned fields. Remove `isStreaming`, `streamingMessage`, `pendingToolCalls`, and `errorMessage` from `initialState` values. | CHANGELOG.md |
| G-PI-CHANGELOG-015 | Breaking Changes | Removed `Agent` mutator methods in favor of direct property access: | CHANGELOG.md |
| G-PI-CHANGELOG-016 | Breaking Changes | `agent.setSystemPrompt(value)` > `agent.state.systemPrompt = value` | CHANGELOG.md |
| G-PI-CHANGELOG-017 | Breaking Changes | `agent.setModel(model)` > `agent.state.model = model` | CHANGELOG.md |
| G-PI-CHANGELOG-018 | Breaking Changes | `agent.setThinkingLevel(level)` > `agent.state.thinkingLevel = level` | CHANGELOG.md |
| G-PI-CHANGELOG-019 | Breaking Changes | `agent.setTools(tools)` > `agent.state.tools = tools` | CHANGELOG.md |
| G-PI-CHANGELOG-020 | Breaking Changes | `agent.replaceMessages(messages)` > `agent.state.messages = messages` | CHANGELOG.md |
| G-PI-CHANGELOG-021 | Breaking Changes | `agent.appendMessage(message)` > `agent.state.messages.push(message)` | CHANGELOG.md |
| G-PI-CHANGELOG-022 | Breaking Changes | `agent.clearMessages()` > `agent.state.messages = []` | CHANGELOG.md |
| G-PI-CHANGELOG-023 | Breaking Changes | `agent.setToolExecution(mode)` > `agent.toolExecution = mode` | CHANGELOG.md |
| G-PI-CHANGELOG-024 | Breaking Changes | `agent.setBeforeToolCall(fn)` > `agent.beforeToolCall = fn` | CHANGELOG.md |
| G-PI-CHANGELOG-025 | Breaking Changes | `agent.setAfterToolCall(fn)` > `agent.afterToolCall = fn` | CHANGELOG.md |
| G-PI-CHANGELOG-026 | Breaking Changes | `agent.setTransport(transport)` > `agent.transport = transport` | CHANGELOG.md |
| G-PI-CHANGELOG-027 | Breaking Changes | Removed queue mode getter/setter methods in favor of properties: | CHANGELOG.md |
| G-PI-CHANGELOG-028 | Breaking Changes | `agent.setSteeringMode(mode)` > `agent.steeringMode = mode` | CHANGELOG.md |
| G-PI-CHANGELOG-029 | Breaking Changes | `agent.getSteeringMode()` > `agent.steeringMode` | CHANGELOG.md |
| G-PI-CHANGELOG-030 | Breaking Changes | `agent.setFollowUpMode(mode)` > `agent.followUpMode = mode` | CHANGELOG.md |
| G-PI-CHANGELOG-031 | Breaking Changes | `agent.getFollowUpMode()` > `agent.followUpMode` | CHANGELOG.md |
| G-PI-CHANGELOG-032 | Breaking Changes | `Agent.subscribe()` listeners are now awaited and receive the active `AbortSignal`: | CHANGELOG.md |
| G-PI-CHANGELOG-033 | Breaking Changes | `agent.subscribe((event) => { ... })` > `agent.subscribe(async (event, signal) => { ... })` | CHANGELOG.md |
| G-PI-CHANGELOG-034 | Breaking Changes | `agent_end` is now the final emitted event for a run, but not the idle boundary | CHANGELOG.md |
| G-PI-CHANGELOG-035 | Breaking Changes | `agent.waitForIdle()`, `agent.prompt(...)`, and `agent.continue()` now settle only after awaited `agent_end` listeners finish | CHANGELOG.md |
| G-PI-CHANGELOG-036 | Breaking Changes | `agent.state.isStreaming` remains `true` until that settlement completes | CHANGELOG.md |
| G-PI-CHANGELOG-037 | Added | Added `AgentTool.prepareArguments` hook to prepare raw tool call arguments before schema validation, enabling compatibility shims for resumed sessions with outdated tool schemas | CHANGELOG.md |
| G-PI-CHANGELOG-038 | Added | Added `Agent.signal` to expose the active abort signal for the current turn, allowing callers to forward cancellation into nested async work ([#2660](https://github.com/badlogic/pimono/issues/2660)) | CHANGELOG.md |
| G-PI-CHANGELOG-039 | Fixed | Fixed steering messages to wait until the current assistant message's toolcall batch fully finishes instead of skipping pending tool calls. | CHANGELOG.md |
| G-PI-CHANGELOG-040 | Added | Added `beforeToolCall` and `afterToolCall` hooks to `AgentOptions` and `AgentLoopConfig` for preflight blocking and postexecution tool result mutation. | CHANGELOG.md |
| G-PI-CHANGELOG-041 | Changed | Added configurable tool execution mode to `Agent` and `agentLoop` via `toolExecution: "parallel" | "sequential"`, with `parallel` as the default. Parallel mode preflights tool calls sequentially, executes allowed tools concurrently, and emits final tool results in assistant source order. | CHANGELOG.md |
| G-PI-CHANGELOG-042 | Added | Added `transport` to `AgentOptions` and `AgentLoopConfig` forwarding, allowing stream transport preference (`"sse"`, `"websocket"`, `"auto"`) to flow into provider calls. | CHANGELOG.md |
| G-PI-CHANGELOG-043 | Fixed | Fixed `continue()` to resume queued steering/followup messages when context currently ends in an assistant message, and preserved oneatatime steering ordering during assistanttail resumes ([#1312](https://github.com/badlogic/pimono/pull/1312) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-044 | Added | Added `maxRetryDelayMs` option to `AgentOptions` to cap serverrequested retry delays. Passed through to the underlying stream function. ([#1123](https://github.com/badlogic/pimono/issues/1123)) | CHANGELOG.md |
| G-PI-CHANGELOG-045 | Added | `thinkingBudgets` option on `Agent` and `AgentOptions` to customize token budgets per thinking level ([#529](https://github.com/badlogic/pimono/pull/529) by [@melihmucuk](https://github.com/melihmucuk)) | CHANGELOG.md |
| G-PI-CHANGELOG-046 | Added | `sessionId` option on `Agent` to forward session identifiers to LLM providers for sessionbased caching. | CHANGELOG.md |
| G-PI-CHANGELOG-047 | Fixed | `minimal` thinking level now maps to `minimal` reasoning effort instead of being treated as `low`. | CHANGELOG.md |
| G-PI-CHANGELOG-048 | Breaking Changes | Queue API replaced with steer/followUp: The `queueMessage()` method has been split into two methods with different delivery semantics ([#403](https://github.com/badlogic/pimono/issues/403)): | CHANGELOG.md |
| G-PI-CHANGELOG-049 | Breaking Changes | `steer(msg)`: Interrupts the agent midrun. Delivered after current tool execution, skips remaining tools. | CHANGELOG.md |
| G-PI-CHANGELOG-050 | Breaking Changes | `followUp(msg)`: Waits until the agent finishes. Delivered only when there are no more tool calls or steering messages. | CHANGELOG.md |
| G-PI-CHANGELOG-051 | Breaking Changes | Queue mode renamed: `queueMode` option renamed to `steeringMode`. Added new `followUpMode` option. Both control whether messages are delivered oneatatime or all at once. | CHANGELOG.md |
| G-PI-CHANGELOG-052 | Breaking Changes | AgentLoopConfig callbacks renamed: `getQueuedMessages` split into `getSteeringMessages` and `getFollowUpMessages`. | CHANGELOG.md |
| G-PI-CHANGELOG-053 | Breaking Changes | Agent methods renamed: | CHANGELOG.md |
| G-PI-CHANGELOG-054 | Breaking Changes | `queueMessage()` → `steer()` and `followUp()` | CHANGELOG.md |
| G-PI-CHANGELOG-055 | Breaking Changes | `clearMessageQueue()` → `clearSteeringQueue()`, `clearFollowUpQueue()`, `clearAllQueues()` | CHANGELOG.md |
| G-PI-CHANGELOG-056 | Breaking Changes | `setQueueMode()`/`getQueueMode()` → `setSteeringMode()`/`getSteeringMode()` and `setFollowUpMode()`/`getFollowUpMode()` | CHANGELOG.md |
| G-PI-CHANGELOG-057 | Fixed | `prompt()` and `continue()` now throw if called while the agent is already streaming, preventing race conditions and corrupted state. Use `steer()` or `followUp()` to queue messages during streaming, or `await` the previous call. | CHANGELOG.md |
| G-PI-CHANGELOG-058 | Breaking Changes | Transport abstraction removed: `ProviderTransport`, `AppTransport`, and `AgentTransport` interface have been removed. Use the `streamFn` option directly for custom streaming implementations. | CHANGELOG.md |
| G-PI-CHANGELOG-059 | Breaking Changes | Agent options renamed: | CHANGELOG.md |
| G-PI-CHANGELOG-060 | Breaking Changes | `transport` → removed (use `streamFn` instead) | CHANGELOG.md |
| G-PI-CHANGELOG-061 | Breaking Changes | `messageTransformer` → `convertToLlm` | CHANGELOG.md |
| G-PI-CHANGELOG-062 | Breaking Changes | `preprocessor` → `transformContext` | CHANGELOG.md |
| G-PI-CHANGELOG-063 | Breaking Changes | `AppMessage` renamed to `AgentMessage`: All references to `AppMessage` have been renamed to `AgentMessage` for consistency. | CHANGELOG.md |
| G-PI-CHANGELOG-064 | Breaking Changes | `CustomMessages` renamed to `CustomAgentMessages`: The declaration merging interface has been renamed. | CHANGELOG.md |
| G-PI-CHANGELOG-065 | Breaking Changes | `UserMessageWithAttachments` and `Attachment` types removed: Attachment handling is now the responsibility of the `convertToLlm` function. | CHANGELOG.md |
| G-PI-CHANGELOG-066 | Breaking Changes | Agent loop moved from `@mariozechner/piai`: The `agentLoop`, `agentLoopContinue`, and related types have moved to this package. Import from `@mariozechner/piagentcore` instead. | CHANGELOG.md |
| G-PI-CHANGELOG-067 | Added | `streamFn` option on `Agent` for custom stream implementations. Default uses `streamSimple` from piai. | CHANGELOG.md |
| G-PI-CHANGELOG-068 | Added | `streamProxy()` utility function for browser apps that need to proxy LLM calls through a backend server. Replaces the removed `AppTransport`. | CHANGELOG.md |
| G-PI-CHANGELOG-069 | Added | `getApiKey` option for dynamic API key resolution (useful for expiring OAuth tokens like GitHub Copilot). | CHANGELOG.md |
| G-PI-CHANGELOG-070 | Added | `agentLoop()` and `agentLoopContinue()` lowlevel functions for running the agent loop without the `Agent` class wrapper. | CHANGELOG.md |
| G-PI-CHANGELOG-071 | Added | New exported types: `AgentLoopConfig`, `AgentContext`, `AgentTool`, `AgentToolResult`, `AgentToolUpdateCallback`, `StreamFn`. | CHANGELOG.md |
| G-PI-CHANGELOG-072 | Changed | `Agent` constructor now has all options optional (empty options use defaults). | CHANGELOG.md |
| G-PI-CHANGELOG-073 | Changed | `queueMessage()` is now synchronous (no longer returns a Promise). | CHANGELOG.md |
| G-PI-README-001 | AgentMessage vs LLM Message | Standard LLM messages (`user`, `assistant`, `toolResult`) | README.md |
| G-PI-README-002 | AgentMessage vs LLM Message | Custom appspecific message types via declaration merging | README.md |
| G-PI-README-003 | With Tool Calls | `parallel` (default): preflight tool calls sequentially, execute allowed tools concurrently, emit `tool_execution_end` as soon as each tool is finalized, then emit toolResult messages and `turn_end.toolResults` in assistant source order | README.md |
| G-PI-README-004 | With Tool Calls | `sequential`: execute tool calls one by one, matching the historical behavior | README.md |
| G-PI-README-005 | Error Handling | Throw an error when a tool fails. Do not return error messages as content. | README.md |
| G-PI-CHANGELOG-001 | Breaking Changes | Replaced `OpenAICompletionsCompat.reasoningEffortMap` with toplevel `Model.thinkingLevelMap` for modelspecific thinking controls ([#3208](https://github.com/badlogic/pimono/issues/3208)). Migration: move mappings from `model.compat.reasoningEffortMap` to `model.thinkingLevelMap`. See `packages/ai/README.md#custommodels` and `packages/codingagent/docs/models.md#thinkinglevelmap`. Map values keep the same providerspecific string semantics, and `null` marks a pi thinking level unsupported. Example: | CHANGELOG.md |
| G-PI-CHANGELOG-002 | Breaking Changes | Removed `supportsXhigh()`. Migration: use `getSupportedThinkingLevels(model).includes("xhigh")` or `clampThinkingLevel(model, requestedLevel)` instead ([#3208](https://github.com/badlogic/pimono/issues/3208)). | CHANGELOG.md |
| G-PI-CHANGELOG-003 | Added | Added Xiaomi MiMo Token Plan provider (Anthropiccompatible) with `XIAOMI_API_KEY` authentication ([#4005](https://github.com/badlogic/pimono/pull/4005) by [@Phoen1xCode](https://github.com/Phoen1xCode)). | CHANGELOG.md |
| G-PI-CHANGELOG-004 | Added | Added `Model.thinkingLevelMap`, `getSupportedThinkingLevels()`, and `clampThinkingLevel()` so model metadata can describe supported thinking levels and providerspecific level values ([#3208](https://github.com/badlogic/pimono/issues/3208)). | CHANGELOG.md |
| G-PI-CHANGELOG-005 | Fixed | Fixed Xiaomi MiMo model catalog to use the Token Plan Anthropic endpoint instead of the direct API ([#3912](https://github.com/badlogic/pimono/issues/3912)). | CHANGELOG.md |
| G-PI-CHANGELOG-006 | Added | Added `websocketcached` transport support for OpenAI Codex Responses used with ChatGPT subscription auth. This keeps the same WebSocket open for a session and, after the first request, sends only new conversation items instead of resending the full chat history when possible. | CHANGELOG.md |
| G-PI-CHANGELOG-007 | Breaking Changes | Removed builtin Google Gemini CLI and Google Antigravity support, including provider registration, model metadata, OAuth, and package exports. Existing callers must switch to another supported provider. | CHANGELOG.md |
| G-PI-CHANGELOG-008 | Added | Added Cloudflare AI Gateway as a builtin provider with OpenAI, Anthropic, and Workers AI gateway routing plus `CLOUDFLARE_API_KEY`/`CLOUDFLARE_ACCOUNT_ID`/`CLOUDFLARE_GATEWAY_ID` authentication ([#3856](https://github.com/badlogic/pimono/pull/3856) by [@mchenco](https://github.com/mchenco)). | CHANGELOG.md |
| G-PI-CHANGELOG-009 | Added | Added Moonshot AI as a builtin OpenAIcompatible provider with model catalog generation and `MOONSHOT_API_KEY` authentication. | CHANGELOG.md |
| G-PI-CHANGELOG-010 | Added | Added Mistral Medium 3.5 model metadata and reasoningmode handling ([#4009](https://github.com/badlogic/pimono/pull/4009) by [@technocidal](https://github.com/technocidal)). | CHANGELOG.md |
| G-PI-CHANGELOG-011 | Added | Added `AssistantMessage.responseModel` on the openaicompletions path: surfaces the concrete `chunk.model` when it differs from the requested id (e.g. OpenRouter `auto` > `anthropic/...`) ([#3968](https://github.com/badlogic/pimono/pull/3968) by [@purrgrammer](https://github.com/purrgrammer)). | CHANGELOG.md |
| G-PI-CHANGELOG-012 | Fixed | Fixed Google Vertex Gemini 3 tool call replay by no longer sending the nonVertex `skip_thought_signature_validator` sentinel for unsigned tool calls ([#4032](https://github.com/badlogic/pimono/issues/4032)). | CHANGELOG.md |
| G-PI-CHANGELOG-013 | Fixed | Updated `@anthropicai/sdk` to `^0.91.1` to clear GHSAp7fg763fg4gf audit findings ([#3992](https://github.com/badlogic/pimono/issues/3992)). | CHANGELOG.md |
| G-PI-CHANGELOG-014 | Fixed | Fixed DeepSeek V4 Flash `xhigh` thinking support so requests preserve `xhigh` and map it to DeepSeek's `max` reasoning effort ([#3944](https://github.com/badlogic/pimono/issues/3944)). | CHANGELOG.md |
| G-PI-CHANGELOG-015 | Fixed | Fixed Anthropic streams that end before `message_stop` to be treated as errors instead of successful partial responses ([#3936](https://github.com/badlogic/pimono/issues/3936)). | CHANGELOG.md |
| G-PI-CHANGELOG-016 | Fixed | Fixed generated OpenAIcompatible DeepSeek V4 models to carry the providerspecific reasoning effort mapping outside the direct DeepSeek provider ([#3940](https://github.com/badlogic/pimono/issues/3940)). | CHANGELOG.md |
| G-PI-CHANGELOG-017 | Fixed | Fixed DeepSeek V4 Flash and V4 Pro pricing metadata to match current official rates ([#3910](https://github.com/badlogic/pimono/issues/3910)). | CHANGELOG.md |
| G-PI-CHANGELOG-018 | Fixed | Fixed DeepSeek prompt cache hits to be tracked from `prompt_cache_hit_tokens` in OpenAIcompatible usage responses ([#3880](https://github.com/badlogic/pimono/issues/3880)). | CHANGELOG.md |
| G-PI-CHANGELOG-019 | Removed | Removed builtin Google Gemini CLI and Google Antigravity provider, model, OAuth, and export support. | CHANGELOG.md |
| G-PI-CHANGELOG-020 | Added | Added Cloudflare Workers AI as a builtin provider with model catalog generation, `CLOUDFLARE_API_KEY`/`CLOUDFLARE_ACCOUNT_ID` authentication, and OpenAIcompatible streaming support ([#3851](https://github.com/badlogic/pimono/pull/3851) by [@mchenco](https://github.com/mchenco)). | CHANGELOG.md |
| G-PI-CHANGELOG-021 | Fixed | Removed generated Cloudflare Workers AI `UserAgent` model headers so attribution can be controlled by callers. | CHANGELOG.md |
| G-PI-CHANGELOG-022 | Fixed | Fixed Bedrock inference profile capability checks by normalizing profile ARNs to the underlying model name. | CHANGELOG.md |
| G-PI-CHANGELOG-023 | Added | Added Azure Cognitive Services endpoint support for Azure OpenAI Responses base URLs ([#3799](https://github.com/badlogic/pimono/pull/3799) by [@marcbloech](https://github.com/marcbloech)). | CHANGELOG.md |
| G-PI-CHANGELOG-024 | Changed | Changed OpenAI Codex Responses default text verbosity to `low` when no verbosity is specified. | CHANGELOG.md |
| G-PI-CHANGELOG-025 | Fixed | Fixed APIkey environment discovery to fall back to `/proc/self/environ` when Bun's sandbox leaves `process.env` empty ([#3801](https://github.com/badlogic/pimono/pull/3801) by [@mdsjip](https://github.com/mdsjip)). | CHANGELOG.md |
| G-PI-CHANGELOG-026 | Fixed | Fixed Bedrock promptcaching and adaptivethinking capability checks to use the model name when the model id is an inference profile ARN ([#3527](https://github.com/badlogic/pimono/pull/3527) by [@anirudhmarc](https://github.com/anirudhmarc)). | CHANGELOG.md |
| G-PI-CHANGELOG-027 | Fixed | Fixed Anthropic SSE parsing to ignore unknown proxy events such as OpenAIstyle `done` terminators ([#3708](https://github.com/badlogic/pimono/issues/3708)). | CHANGELOG.md |
| G-PI-CHANGELOG-028 | Fixed | Fixed OpenAIcompatible prompt cache tests to cover proxies that explicitly disable long cache retention. | CHANGELOG.md |
| G-PI-CHANGELOG-029 | Fixed | Stopped sending `tools: []` on OpenAIcompatible, Anthropic, OpenAI Responses, OpenAI Codex Responses, and Azure OpenAI Responses requests when no tools are active (e.g. `pi notools`). DashScope/Aliyun Qwen (OpenAIcompatible) rejects empty tools arrays with `"[] is too short  'tools'"` (HTTP 400); the field is now omitted unless the conversation has tool history (the existing LiteLLM/Anthropicproxy workaround) ([#3650](https://github.com/badlogic/pimono/pull/3650) by [@HQidea](https://github.com/HQidea)). | CHANGELOG.md |
| G-PI-CHANGELOG-030 | Fixed | Fixed `supportsXhigh()` to recognize DeepSeek V4 Pro, preserving `xhigh` reasoning requests so they map to DeepSeek's `max` effort ([#3662](https://github.com/badlogic/pimono/issues/3662)) | CHANGELOG.md |
| G-PI-CHANGELOG-031 | Fixed | Fixed OpenAIcompatible DeepSeek V4 model replay to include empty `reasoning_content` on assistant messages when needed, preventing OpenRouter DeepSeek V4 sessions from failing after responses without reasoning deltas ([#3668](https://github.com/badlogic/pimono/issues/3668)) | CHANGELOG.md |
| G-PI-CHANGELOG-032 | Fixed | Fixed OpenAI/Azure/Anthropic provider request option forwarding to omit undefined `timeout`/`maxRetries`, avoiding SDK validation errors such as `timeout must be an integer` when provider controls are not set ([#3627](https://github.com/badlogic/pimono/issues/3627)) | CHANGELOG.md |
| G-PI-CHANGELOG-033 | Added | Added DeepSeek as a builtin OpenAIcompatible provider with V4 Flash and V4 Pro models and `DEEPSEEK_API_KEY` authentication. | CHANGELOG.md |
| G-PI-CHANGELOG-034 | Fixed | Fixed DeepSeek V4 session replay 400 errors by adding `thinkingFormat: "deepseek"` (sends `thinking: { type }` + `reasoning_effort`), a `reasoningEffortMap`, and `requiresReasoningContentOnAssistantMessages` compat that injects empty `reasoning_content` on all replayed assistant messages when reasoning is enabled ([#3636](https://github.com/badlogic/pimono/issues/3636)) | CHANGELOG.md |
| G-PI-CHANGELOG-035 | Fixed | Fixed GPT5.5 generated context window metadata to use the observed 272k limit. | CHANGELOG.md |
| G-PI-CHANGELOG-036 | Fixed | Fixed provider request controls to expose `timeoutMs` and `maxRetries` in stream options and forward them through OpenAI/Azure/Anthropic request options, preventing unconfigurable SDK timeout/retry defaults on longrunning local inference requests ([#3627](https://github.com/badlogic/pimono/issues/3627)) | CHANGELOG.md |
| G-PI-CHANGELOG-037 | Added | Added GPT5.5 to OpenAI Codex model generation. | CHANGELOG.md |
| G-PI-CHANGELOG-038 | Added | Added `findEnvKeys()` so callers can identify configured provider APIkey environment variables without exposing credential values while preserving `getEnvApiKey()` as the credentialvalue API. | CHANGELOG.md |
| G-PI-CHANGELOG-039 | Fixed | Fixed `googlevertex` to forward custom `model.baseUrl` values to `@google/genai`, enabling Vertex proxy and gateway endpoints ([#3619](https://github.com/badlogic/pimono/issues/3619)) | CHANGELOG.md |
| G-PI-CHANGELOG-040 | Fixed | Fixed OpenAIcompatible completion usage parsing to stop doublecounting reasoning tokens already included in `completion_tokens` ([#3581](https://github.com/badlogic/pimono/issues/3581)) | CHANGELOG.md |
| G-PI-CHANGELOG-041 | Fixed | Fixed long cache retention compatibility by adding `compat.supportsLongCacheRetention`, allowing Anthropic Messages and OpenAIcompatible proxies to explicitly disable longretention fields while enabling long retention by default when requested ([#3543](https://github.com/badlogic/pimono/issues/3543)) | CHANGELOG.md |
| G-PI-CHANGELOG-042 | Fixed | Fixed `openairesponses` compatibility by adding `compat.sendSessionIdHeader: false`, allowing strict OpenAIcompatible proxies to omit the underscorecontaining `session_id` header while still sending other sessionaffinity headers ([#3579](https://github.com/badlogic/pimono/issues/3579)) | CHANGELOG.md |
| G-PI-CHANGELOG-043 | Fixed | Fixed `anthropicmessages` tool streaming compatibility by adding `compat.supportsEagerToolInputStreaming`, allowing Anthropiccompatible providers to omit pertool `eager_input_streaming` and use the legacy finegrained tool streaming beta header instead ([#3575](https://github.com/badlogic/pimono/issues/3575)) | CHANGELOG.md |
| G-PI-CHANGELOG-044 | Fixed | Fixed `supportsXhigh()` to recognize `openaicodex` `gpt5.5`, preserving `xhigh` reasoning requests instead of clamping them to `high`. | CHANGELOG.md |
| G-PI-CHANGELOG-045 | Fixed | Fixed `openaicompletions` streamed toolcall assembly to coalesce deltas by stable tool index when OpenAIcompatible gateways mutate tool call IDs midstream, preventing malformed Kimi K2.6/OpenCode tool streams from splitting one call into multiple bogus tool calls ([#3576](https://github.com/badlogic/pimono/issues/3576)) | CHANGELOG.md |
| G-PI-CHANGELOG-046 | Fixed | Fixed `packages/ai` E2E coverage to use currently supported OpenAI Responses and OpenAI Codex models, and updated the Bedrock adaptivethinking payload expectation to match the current `display: "summarized"` shape. | CHANGELOG.md |
| G-PI-CHANGELOG-047 | Fixed | Fixed builtin `kimicoding` model generation to attach `UserAgent: KimiCLI/1.5` to all generated Kimi models, overriding the Anthropic SDK default UA so direct Kimi Coding requests use the provider's expected client identity ([#3586](https://github.com/badlogic/pimono/issues/3586)) | CHANGELOG.md |
| G-PI-CHANGELOG-048 | Fixed | Fixed GPT5.5 Codex capability handling to clamp unsupported minimal reasoning to `low` and apply the model's 2.5x priority servicetier pricing multiplier ([#3618](https://github.com/badlogic/pimono/pull/3618) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-049 | Breaking Changes | Migrated TypeBox support from `@sinclair/typebox` 0.34.x plus AJV to `typebox` 1.x plus TypeBox's builtin validator and valueconversion APIs. Tool argument validation now runs in evalrestricted JavaScript runtimes such as Cloudflare Workers and other environments that disallow `eval` / `new Function`, instead of being silently skipped. Migration: install and import from `typebox` instead of `@sinclair/typebox`, and retest any coercionsensitive tool paths that serialize schemas to plain JSON because those now go through the new TypeBoxbased validation and coercion path rather than AJV ([#3112](https://github.com/badlogic/pimono/issues/3112)) | CHANGELOG.md |
| G-PI-CHANGELOG-050 | Fixed | Fixed `googlegeminicli` builtin model discovery to include `gemini3.1flashlitepreview`, so Cloud Code Assist model lists expose it without requiring manual `model` fallback selection ([#3545](https://github.com/badlogic/pimono/issues/3545)) | CHANGELOG.md |
| G-PI-CHANGELOG-051 | Fixed | Fixed `transformMessages()` to synthesize missing trailing tool results for transcripts that end with unresolved assistant tool calls during direct lowlevel history replay ([#3555](https://github.com/badlogic/pimono/issues/3555)) | CHANGELOG.md |
| G-PI-CHANGELOG-052 | Added | Added Fireworks provider support via Fireworks' Anthropiccompatible Messages API, including builtin models sourced from models.dev and `FIREWORKS_API_KEY` auth ([#3519](https://github.com/badlogic/pimono/issues/3519)) | CHANGELOG.md |
| G-PI-CHANGELOG-053 | Fixed | Hardened Anthropic streaming against malformed toolcall JSON by owning SSE parsing with defensive JSON repair, replacing the deprecated `finegrainedtoolstreaming` beta header with pertool `eager_input_streaming`, and updating stale test model references ([#3175](https://github.com/badlogic/pimono/issues/3175)) | CHANGELOG.md |
| G-PI-CHANGELOG-054 | Fixed | Fixed Bedrock runtime endpoint resolution to stop pinning builtin regional endpoints over `AWS_REGION` / `AWS_PROFILE`, restoring `us.` and `eu.` inference profile support after v0.68.0 while preserving custom VPC/proxy endpoint overrides ([#3481](https://github.com/badlogic/pimono/issues/3481), [#3485](https://github.com/badlogic/pimono/issues/3485), [#3486](https://github.com/badlogic/pimono/issues/3486), [#3487](https://github.com/badlogic/pimono/issues/3487), [#3488](https://github.com/badlogic/pimono/issues/3488)) | CHANGELOG.md |
| G-PI-CHANGELOG-055 | Added | Added `PI_OAUTH_CALLBACK_HOST` support for builtin Anthropic, Gemini CLI, Google Antigravity, and OpenAI Codex OAuth flows, allowing local callback servers to bind to a custom interface instead of hardcoded `127.0.0.1` ([#3409](https://github.com/badlogic/pimono/pull/3409) by [@Michaelliv](https://github.com/Michaelliv)) | CHANGELOG.md |
| G-PI-CHANGELOG-056 | Changed | Changed Bedrock Converse requests to omit `inferenceConfig.maxTokens` when model token limits are unknown and to omit `temperature` when unset, letting Bedrock use model defaults and avoid unnecessary TPM quota reservation ([#3400](https://github.com/badlogic/pimono/pull/3400) by [@wirjo](https://github.com/wirjo)) | CHANGELOG.md |
| G-PI-CHANGELOG-057 | Fixed | Fixed `openaicompletions` `compat.requiresThinkingAsText` assistant replay to preserve textpart serialization and avoid samemodel crashes when prior assistant messages contain both thinking and text ([#3387](https://github.com/badlogic/pimono/issues/3387)) | CHANGELOG.md |
| G-PI-CHANGELOG-058 | Fixed | Fixed Cloud Code Assist tool schemas to strip JSON Schema metadeclaration keys such as `$schema`, `$defs`, and `definitions` before sending OpenAPI `parameters`, avoiding provider validation failures for toolenabled requests ([#3412](https://github.com/badlogic/pimono/pull/3412) by [@vladlearns](https://github.com/vladlearns)) | CHANGELOG.md |
| G-PI-CHANGELOG-059 | Fixed | Fixed nonvision model requests to replace user and toolresult image blocks with explicit text placeholders instead of silently dropping them during provider payload conversion ([#3429](https://github.com/badlogic/pimono/issues/3429)) | CHANGELOG.md |
| G-PI-CHANGELOG-060 | Fixed | Fixed direct OpenAI Chat Completions requests to map `sessionId` and `cacheRetention` to OpenAI prompt caching fields, sending `prompt_cache_key` when caching is enabled and `prompt_cache_retention: "24h"` for direct `api.openai.com` requests with long retention ([#3426](https://github.com/badlogic/pimono/issues/3426)) | CHANGELOG.md |
| G-PI-CHANGELOG-061 | Fixed | Fixed OpenAIcompatible Chat Completions requests to optionally send aligned `session_id`, `xclientrequestid`, and `xsessionaffinity` sessionaffinity headers from `sessionId` via `compat.sendSessionAffinityHeaders`, enabling cacheaffinity routing for backends such as Fireworks ([#3430](https://github.com/badlogic/pimono/issues/3430)) | CHANGELOG.md |
| G-PI-CHANGELOG-062 | Fixed | Fixed direct Bedrock runtime client construction to pass `model.baseUrl` through as the SDK `endpoint`, restoring support for custom Bedrock endpoints such as VPC or proxy routes ([#3402](https://github.com/badlogic/pimono/pull/3402) by [@wirjo](https://github.com/wirjo)) | CHANGELOG.md |
| G-PI-CHANGELOG-063 | Fixed | Fixed OpenAIcompatible Chat Completions Anthropicstyle prompt caching to apply `cache_control` markers to the system prompt, last tool definition, and last user/assistant text content via `compat.cacheControlFormat`, and enabled that compat for OpenCode/OpenCode Go Qwen 3.5/3.6 Plus models so prompt caching works there too ([#3392](https://github.com/badlogic/pimono/issues/3392)) | CHANGELOG.md |
| G-PI-CHANGELOG-064 | Fixed | Fixed Bedrock bearertoken authentication to use the SDK's native token auth path and omit Claude `thinking.display` for GovCloud targets, avoiding duplicate `Authorization` headers and GovCloud Converse validation errors ([#3359](https://github.com/badlogic/pimono/issues/3359)) | CHANGELOG.md |
| G-PI-CHANGELOG-065 | Fixed | Fixed direct Mistral tool definitions to strip TypeBox symbol metadata before passing schemas to the SDK, restoring tool calls after the SDK's stricter outbound validation ([#3361](https://github.com/badlogic/pimono/issues/3361)) | CHANGELOG.md |
| G-PI-CHANGELOG-066 | Added | Added Bedrock Converse bearertoken authentication via `AWS_BEARER_TOKEN_BEDROCK`, enabling APIkey style access without SigV4 credentials ([#3125](https://github.com/badlogic/pimono/pull/3125) by [@wirjo](https://github.com/wirjo)) | CHANGELOG.md |
| G-PI-CHANGELOG-067 | Fixed | Fixed Anthropic and Bedrock adaptivethinking payload tests to expect the default `display: "summarized"` field when reasoning is enabled. | CHANGELOG.md |
| G-PI-CHANGELOG-068 | Fixed | Fixed Mistral Small 4 reasoning requests to use `reasoning_effort` instead of `prompt_mode`, restoring default thinking support for `mistralsmall2603` and `mistralsmalllatest` ([#3338](https://github.com/badlogic/pimono/issues/3338)) | CHANGELOG.md |
| G-PI-CHANGELOG-069 | Fixed | Fixed `qwenchattemplate` OpenAIcompatible requests to set `chat_template_kwargs.preserve_thinking: true`, preserving prior Qwen thinking across turns so multiturn tool calls keep their arguments instead of degrading to empty `{}` payloads ([#3325](https://github.com/badlogic/pimono/issues/3325)) | CHANGELOG.md |
| G-PI-CHANGELOG-070 | Fixed | Fixed OpenAI Codex servicetier accounting to trust the explicitly requested tier when the API echoes the default tier in responses, keeping downstream usage costs aligned with the callerselected tier ([#3307](https://github.com/badlogic/pimono/pull/3307) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-071 | Added | Added `onResponse` to `StreamOptions` so callers can inspect provider HTTP status and headers after each response arrives and before the response stream is consumed ([#3128](https://github.com/badlogic/pimono/issues/3128)) | CHANGELOG.md |
| G-PI-CHANGELOG-072 | Added | Added `thinkingDisplay` (`"summarized" | "omitted"`) to `AnthropicOptions` and `BedrockOptions`, wiring it through to the Anthropic/Bedrock `thinking` config. Defaults to `"summarized"` so Claude Opus 4.7 and Mythos Preview keep returning thinking text; set it to `"omitted"` to skip thinking streaming for faster timetofirsttexttoken. | CHANGELOG.md |
| G-PI-CHANGELOG-073 | Fixed | Fixed OpenAI Responses prompt caching for non`api.openai.com` base URLs (OpenAIcompatible proxies such as litellm, theclawbay) by sending the `session_id` and `xclientrequestid` cacheaffinity headers unconditionally when a `sessionId` is provided, matching the official Codex CLI behavior ([#3264](https://github.com/badlogic/pimono/pull/3264) by [@vegarsti](https://github.com/vegarsti)) | CHANGELOG.md |
| G-PI-CHANGELOG-074 | Fixed | Fixed Opus 4.7 adaptive thinking configuration across Anthropic and Bedrock providers by recognizing Opus 4.7 adaptivethinking support and mapping `xhigh` reasoning to providersupported effort values ([#3286](https://github.com/badlogic/pimono/pull/3286) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-075 | Changed | Added `claudeopus47` model for Anthropic, OpenRouter. | CHANGELOG.md |
| G-PI-CHANGELOG-076 | Changed | Changed Anthropic prompt caching to add a `cache_control` breakpoint on the last tool definition, so tool schemas can be cached independently from transcript updates while preserving existing cache retention behavior ([#3260](https://github.com/badlogic/pimono/issues/3260)) | CHANGELOG.md |
| G-PI-CHANGELOG-077 | Changed | Changed Kimi Coding model generation to normalize deprecated `k2p5` to `kimiforcoding` from models.dev data and removed the old static fallback model list ([#3242](https://github.com/badlogic/pimono/issues/3242)) | CHANGELOG.md |
| G-PI-CHANGELOG-078 | Fixed | Fixed `googlevertex` API key resolution to treat `gcpvertexcredentials` as an Application Default Credentials marker instead of a literal API key, so markerbased setups correctly fall back to ADC ([#3221](https://github.com/badlogic/pimono/pull/3221) by [@deepkilo](https://github.com/deepkilo)) | CHANGELOG.md |
| G-PI-CHANGELOG-079 | Fixed | Fixed direct OpenAI Responses requests to send aligned `prompt_cache_key`, `session_id`, and `xclientrequestid` values when `sessionId` is provided, improving prompt cache affinity for appendonly sessions ([#3018](https://github.com/badlogic/pimono/pull/3018) by [@steipete](https://github.com/steipete)) | CHANGELOG.md |
| G-PI-CHANGELOG-080 | Fixed | Fixed streamingonly `partialJson` scratch buffers leaking into persisted OpenAI Responses tool calls, which could corrupt followup payloads on resumed conversations. | CHANGELOG.md |
| G-PI-CHANGELOG-081 | Added | Added full `OpenRouterRouting` field support, including fallbacks, parameter requirements, data collection, ZDR, ignore lists, quantizations, provider sorting, max price, and preferred throughput and latency constraints ([#2904](https://github.com/badlogic/pimono/pull/2904) by [@zmberber](https://github.com/zmberber)) | CHANGELOG.md |
| G-PI-CHANGELOG-082 | Fixed | Bumped default Antigravity UserAgent version to `1.21.9` ([#2901](https://github.com/badlogic/pimono/pull/2901) by [@aadishv](https://github.com/aadishv)) | CHANGELOG.md |
| G-PI-CHANGELOG-083 | Fixed | Fixed thinking levels for Gemma 4 models to use `thinkingLevel` and map Pi reasoning levels to the model's supported thinking levels ([#2903](https://github.com/badlogic/pimono/pull/2903) by [@aadishv](https://github.com/aadishv)) | CHANGELOG.md |
| G-PI-CHANGELOG-084 | Fixed | Fixed Gemini 2.5 Flash Lite minimal thinking budget to use the model's supported 512token minimum instead of the regular Flash 128token minimum, avoiding invalid thinking budget errors ([#2861](https://github.com/badlogic/pimono/pull/2861) by [@JasonOA888](https://github.com/JasonOA888)) | CHANGELOG.md |
| G-PI-CHANGELOG-085 | Fixed | Fixed OpenAI Codex Responses requests to forward configured `serviceTier` values, restoring servicetier selection for Codex sessions ([#2996](https://github.com/badlogic/pimono/pull/2996) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-086 | Fixed | Fixed bare `readline` import to use `node:readline` prefix for Deno compatibility ([#2885](https://github.com/badlogic/pimono/issues/2885) by [@milosvvtool](https://github.com/milosvvtool)) | CHANGELOG.md |
| G-PI-CHANGELOG-087 | Fixed | Fixed OpenAIcompatible completions streaming usage to preserve `prompt_tokens_details.cache_write_tokens` and normalize OpenRouter `cached_tokens` to previousrequest cache hits only, preventing cache read/write double counting in `usage` and cost calculation ([#2802](https://github.com/badlogic/pimono/issues/2802)) | CHANGELOG.md |
| G-PI-CHANGELOG-088 | Added | Added tool streaming support for newer Z.ai models ([#2732](https://github.com/badlogic/pimono/pull/2732) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-089 | Fixed | Fixed Anthropic context overflow detection to recognize HTTP 413 `request_too_large` errors, so callers can trigger compaction and retry instead of getting stuck on repeated oversizedimage requests ([#2734](https://github.com/badlogic/pimono/issues/2734)) | CHANGELOG.md |
| G-PI-CHANGELOG-090 | Fixed | Fixed OpenAI Responses toolcall streaming to emit a `toolcall_delta` when function call arguments arrive only in `response.function_call_arguments.done`, and to emit only the missing suffix when `.done` extends earlier streamed arguments ([#2745](https://github.com/badlogic/pimono/issues/2745)) | CHANGELOG.md |
| G-PI-CHANGELOG-091 | Fixed | Fixed Bedrock throttling errors being misidentified as context overflow, causing unnecessary compaction instead of retry ([#2699](https://github.com/badlogic/pimono/pull/2699) by [@xu0o0](https://github.com/xu0o0)) | CHANGELOG.md |
| G-PI-CHANGELOG-092 | Added | Added optin faux provider helpers for deterministic tests and scripted demos: `registerFauxProvider()`, `fauxAssistantMessage()`, `fauxText()`, `fauxThinking()`, and `fauxToolCall()`. | CHANGELOG.md |
| G-PI-CHANGELOG-093 | Added | Added `gemini3.1propreviewcustomtools` model support for the `googlevertex` provider ([#2610](https://github.com/badlogic/pimono/pull/2610) by [@gordonhwc](https://github.com/gordonhwc)) | CHANGELOG.md |
| G-PI-CHANGELOG-094 | Fixed | Fixed context overflow detection to recognize Ollama error responses like `prompt too long; exceeded max context length ...`, so callers can trigger compaction and retry instead of surfacing the raw overflow error ([#2626](https://github.com/badlogic/pimono/issues/2626)) | CHANGELOG.md |
| G-PI-CHANGELOG-095 | Breaking Changes | Removed deprecated direct `minimax` and `minimaxcn` model IDs, keeping only `MiniMaxM2.7` and `MiniMaxM2.7highspeed`. Update pinned model IDs to one of those supported direct MiniMax models, or use another provider route that still exposes the older IDs ([#2596](https://github.com/badlogic/pimono/pull/2596) by [@liyuan97](https://github.com/liyuan97)) | CHANGELOG.md |
| G-PI-CHANGELOG-096 | Fixed | Fixed GitHub Copilot OpenAI Responses requests to omit the `reasoning` field entirely when no reasoning effort is requested, avoiding `400` errors from Copilot `gpt5mini` rejecting `reasoning: { effort: "none" }` during internal summary calls ([#2567](https://github.com/badlogic/pimono/issues/2567)) | CHANGELOG.md |
| G-PI-CHANGELOG-097 | Fixed | Fixed Google and Vertex cost calculation to subtract cached prompt tokens from billable input tokens instead of doublecounting them when providers report `cachedContentTokenCount` ([#2588](https://github.com/badlogic/pimono/pull/2588) by [@sparkleMing](https://github.com/sparkleMing)) | CHANGELOG.md |
| G-PI-CHANGELOG-098 | Added | Added `requestMetadata` option to `BedrockOptions` for AWS cost allocation tagging; keyvalue pairs are forwarded to the Bedrock Converse API `requestMetadata` field and appear in AWS Cost Explorer split cost allocation data ([#2511](https://github.com/badlogic/pimono/pull/2511) by [@wjonaskr](https://github.com/wjonaskr)) | CHANGELOG.md |
| G-PI-CHANGELOG-099 | Added | Exported `BedrockOptions` type from the package root entry point, consistent with other provider option types. | CHANGELOG.md |
| G-PI-CHANGELOG-100 | Fixed | Fixed OpenAI Responses replay for foreign toolcall item IDs by hashing foreign `function_call.id` values into bounded `fc_<hash>` IDs instead of preserving backendspecific normalized shapes that OpenAI Codex rejects. | CHANGELOG.md |
| G-PI-CHANGELOG-101 | Fixed | Fixed Anthropic thinking disable handling to send `thinking: { type: "disabled" }` for reasoningcapable models when thinking is explicitly off, and added payload and envgated endtoend coverage for the Anthropic provider ([#2022](https://github.com/badlogic/pimono/issues/2022)) | CHANGELOG.md |
| G-PI-CHANGELOG-102 | Fixed | Fixed explicit thinking disable handling across Google, Google Vertex, Gemini CLI, OpenAI Responses, Azure OpenAI Responses, and OpenRouterbacked OpenAIcompatible completions. Gemini 3 models now fall back to the lowest supported thinking level when full disable is not supported, and OpenAI/OpenRouter reasoning models now send explicit `none` effort instead of relying on provider defaults ([#2490](https://github.com/badlogic/pimono/issues/2490)) | CHANGELOG.md |
| G-PI-CHANGELOG-103 | Fixed | Fixed OpenAIcompatible completions streams to ignore null chunks instead of crashing ([#2466](https://github.com/badlogic/pimono/pull/2466) by [@ChengZiQing](https://github.com/ChengZiQing)) | CHANGELOG.md |
| G-PI-CHANGELOG-104 | Changed | Changed MiniMax model metadata to add missing `MiniMaxM2.1highspeed` entries for the `minimax` and `minimaxcn` providers and normalize MiniMax Anthropiccompatible context limits to the provider's supported model set ([#2445](https://github.com/badlogic/pimono/pull/2445) by [@1500256797](https://github.com/1500256797)) | CHANGELOG.md |
| G-PI-CHANGELOG-105 | Added | Added `gpt5.4mini` model support for the `openaicodex` provider with Codex pricing metadata and unit coverage ([#2334](https://github.com/badlogic/pimono/pull/2334) by [@justram](https://github.com/justram)) | CHANGELOG.md |
| G-PI-CHANGELOG-106 | Fixed | Fixed `validateToolArguments()` to fall back gracefully when AJV schema compilation is blocked in restricted runtimes such as Cloudflare Workers, allowing tool execution to proceed without schema validation ([#2395](https://github.com/badlogic/pimono/issues/2395)) | CHANGELOG.md |
| G-PI-CHANGELOG-107 | Fixed | Fixed `googlevertex` API key resolution to ignore placeholder auth markers like `<authenticated>` and fall back to ADC instead of sending them as literal API keys ([#2335](https://github.com/badlogic/pimono/issues/2335)) | CHANGELOG.md |
| G-PI-CHANGELOG-108 | Fixed | Fixed OpenRouter reasoning requests to use the provider's nested `reasoning.effort` payload instead of OpenAI's `reasoning_effort`, restoring thinking level support for OpenRouter models ([#2298](https://github.com/badlogic/pimono/pull/2298) by [@PriNova](https://github.com/PriNova)) | CHANGELOG.md |
| G-PI-CHANGELOG-109 | Fixed | Fixed Bedrock prompt caching for application inference profiles by allowing cache points to be forced with `AWS_BEDROCK_FORCE_CACHE=1` when the profile ARN does not expose the underlying Claude model name ([#2346](https://github.com/badlogic/pimono/pull/2346) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-110 | Fixed | Fixed Gemini 3 and Antigravity image tool results to stay inline as multimodal tool responses instead of being rerouted through separate followup messages ([#2052](https://github.com/badlogic/pimono/issues/2052)) | CHANGELOG.md |
| G-PI-CHANGELOG-111 | Fixed | Fixed Bedrock Claude 4.6 model metadata to use the correct 200K context window instead of 1M ([#2305](https://github.com/badlogic/pimono/issues/2305)) | CHANGELOG.md |
| G-PI-CHANGELOG-112 | Fixed | Fixed lazy builtin provider registration so compiled Bun binaries can still load providers on first use without eagerly bundling provider SDKs ([#2314](https://github.com/badlogic/pimono/issues/2314)) | CHANGELOG.md |
| G-PI-CHANGELOG-113 | Fixed | Fixed builtin OAuth callback flows to share aligned callback handling across Anthropic, Gemini CLI, Antigravity, and OpenAI Codex, and fixed OpenAI Codex login to resolve immediately after callback completion ([#2316](https://github.com/badlogic/pimono/issues/2316)) | CHANGELOG.md |
| G-PI-CHANGELOG-114 | Fixed | Fixed OpenAIcompatible z.ai `network_error` responses to surface as errors so callers can retry them instead of treating them as successful assistant messages ([#2313](https://github.com/badlogic/pimono/issues/2313)) | CHANGELOG.md |
| G-PI-CHANGELOG-115 | Fixed | Fixed OpenAI Responses replay to normalize oversized resumed tool call IDs before sending them back to Codex and other Responsescompatible targets ([#2328](https://github.com/badlogic/pimono/issues/2328)) | CHANGELOG.md |
| G-PI-CHANGELOG-116 | Added | Added `client` injection support to `AnthropicOptions`, allowing callers to provide a prebuilt Anthropiccompatible client instead of constructing one internally. | CHANGELOG.md |
| G-PI-CHANGELOG-117 | Changed | Lazyload builtin provider modules and root provider wrappers so importing `@mariozechner/piai` no longer eagerly loads provider SDKs, significantly reducing base startup cost without changing dependency installation footprint ([#2297](https://github.com/badlogic/pimono/issues/2297)) | CHANGELOG.md |
| G-PI-CHANGELOG-118 | Fixed | Added providerspecific `responseId` support on `AssistantMessage` for providers that expose upstream response or message identifiers, including Anthropic, OpenAI, Google, Gemini CLI, and Mistral, and added endtoend coverage for supported OAuth and API key providers ([#2245](https://github.com/badlogic/pimono/issues/2245)) | CHANGELOG.md |
| G-PI-CHANGELOG-119 | Fixed | Fixed Claude 4.6 context window overrides in generated model metadata so buildtime catalogs reflect the intended values ([#2286](https://github.com/badlogic/pimono/issues/2286)) | CHANGELOG.md |
| G-PI-CHANGELOG-120 | Fixed | Fixed Anthropic OAuth manual login and token refresh by using the localhost callback URI for pasted redirect/code flows and omitting `scope` from refreshtoken requests ([#2169](https://github.com/badlogic/pimono/issues/2169)) | CHANGELOG.md |
| G-PI-CHANGELOG-121 | Fixed | Fixed OpenAI Codex websocket protocol to include required headers and properly terminate SSE streams on connection close ([#1961](https://github.com/badlogic/pimono/issues/1961)) | CHANGELOG.md |
| G-PI-CHANGELOG-122 | Fixed | Fixed Bedrock prompt caching being enabled for nonClaude models, causing API errors ([#2053](https://github.com/badlogic/pimono/issues/2053)) | CHANGELOG.md |
| G-PI-CHANGELOG-123 | Fixed | Fixed Qwen models via OpenAIcompatible providers by adding `qwenchattemplate` compat mode that uses Qwen's native chat template format ([#2020](https://github.com/badlogic/pimono/issues/2020)) | CHANGELOG.md |
| G-PI-CHANGELOG-124 | Fixed | Fixed Bedrock unsigned thinking replay to handle edge cases with empty or malformed thinking blocks ([#2063](https://github.com/badlogic/pimono/issues/2063)) | CHANGELOG.md |
| G-PI-CHANGELOG-125 | Fixed | Fixed xhigh reasoning effort detection for Claude Opus 4.6 to match by model ID instead of requiring explicit capability flag ([#2040](https://github.com/badlogic/pimono/issues/2040)) | CHANGELOG.md |
| G-PI-CHANGELOG-126 | Fixed | Handle `finish_reason: "end"` from Ollama/LM Studio by mapping it to `"stop"` instead of throwing ([#2142](https://github.com/badlogic/pimono/issues/2142)) | CHANGELOG.md |
| G-PI-CHANGELOG-127 | Added | Added `GOOGLE_CLOUD_API_KEY` environment variable support for the `googlevertex` provider as an alternative to Application Default Credentials ([#1976](https://github.com/badlogic/pimono/pull/1976) by [@gordonhwc](https://github.com/gordonhwc)) | CHANGELOG.md |
| G-PI-CHANGELOG-128 | Changed | Raised Claude Opus 4.6, Sonnet 4.6, and related Bedrock model context windows from 200K to 1M tokens ([#2135](https://github.com/badlogic/pimono/pull/2135) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-129 | Fixed | Fixed GitHub Copilot devicecode login polling to respect OAuth slowdown intervals, wait before the first token poll, and include a clearer clockdrift hint in WSL/VM environments when repeated slowdowns lead to timeout. | CHANGELOG.md |
| G-PI-CHANGELOG-130 | Fixed | Fixed usage statistics not being captured for OpenAIcompatible providers that return usage in `choice.usage` instead of the standard `chunk.usage` (e.g., Moonshot/Kimi) ([#2017](https://github.com/badlogic/pimono/issues/2017)) | CHANGELOG.md |
| G-PI-CHANGELOG-131 | Fixed | Fixed tool result images not being sent in `function_call_output` items for OpenAI Responses API providers, causing image data to be silently dropped in tool results ([#2104](https://github.com/badlogic/pimono/issues/2104)) | CHANGELOG.md |
| G-PI-CHANGELOG-132 | Fixed | Fixed assistant content being sent as structured content blocks instead of plain strings in the `openaicompletions` provider, causing errors with some OpenAIcompatible backends ([#2008](https://github.com/badlogic/pimono/pull/2008) by [@geraldoaax](https://github.com/geraldoaax)) | CHANGELOG.md |
| G-PI-CHANGELOG-133 | Fixed | Fixed error details in OpenAI Responses `response.failed` handler to include status code, error code, and message instead of a generic failure ([#1956](https://github.com/badlogic/pimono/pull/1956) by [@drewburr](https://github.com/drewburr)) | CHANGELOG.md |
| G-PI-CHANGELOG-134 | Fixed | Fixed context overflow detection to recognize z.ai `model_context_window_exceeded` errors surfaced through OpenAIcompatible stop reason handling ([#1937](https://github.com/badlogic/pimono/issues/1937)) | CHANGELOG.md |
| G-PI-CHANGELOG-135 | Added | Added perrequest payload inspection and replacement hook support via `beforeProviderRequest`, allowing callers to inspect or replace provider payloads before sending. | CHANGELOG.md |
| G-PI-CHANGELOG-136 | Added | Added `claudesonnet46` model for the `googleantigravity` provider ([#1859](https://github.com/badlogic/pimono/issues/1859)). | CHANGELOG.md |
| G-PI-CHANGELOG-137 | Added | Bumped default Antigravity UserAgent version to `1.18.4` ([#1859](https://github.com/badlogic/pimono/issues/1859)). | CHANGELOG.md |
| G-PI-CHANGELOG-138 | Fixed | Fixed Antigravity Claude thinking beta header detection to use provider and model capability instead of `thinking` suffix, so models like `claudesonnet46` receive the header correctly ([#1859](https://github.com/badlogic/pimono/issues/1859)). | CHANGELOG.md |
| G-PI-CHANGELOG-139 | Fixed | Fixed OpenAI Responses reasoning replay regression that dropped reasoning blocks on followup turns ([#1878](https://github.com/badlogic/pimono/issues/1878)) | CHANGELOG.md |
| G-PI-CHANGELOG-140 | Added | Added `gpt5.4` model support for `openai`, `openaicodex`, `azureopenairesponses`, and `opencode` providers, with GPT5.4 treated as xhighcapable and capped to a 272000 context window in builtin metadata. | CHANGELOG.md |
| G-PI-CHANGELOG-141 | Added | Added `gpt5.3codex` fallback model availability for `githubcopilot` until upstream model catalogs include it ([#1853](https://github.com/badlogic/pimono/issues/1853)). | CHANGELOG.md |
| G-PI-CHANGELOG-142 | Fixed | Preserved OpenAI Responses assistant `phase` metadata (`commentary`, `final_answer`) across turns by encoding `id` and `phase` in `textSignature` for session persistence and replay, with backward compatibility for legacy plain signatures ([#1819](https://github.com/badlogic/pimono/issues/1819)). | CHANGELOG.md |
| G-PI-CHANGELOG-143 | Fixed | Fixed OpenAI Responses replay to omit empty thinking blocks, avoiding invalid noop reasoning items in followup turns. | CHANGELOG.md |
| G-PI-CHANGELOG-144 | Fixed | Switched the Mistral provider from the OpenAIcompatible completions path to Mistral's native SDK and conversations API, preserving native thinking blocks and Mistralspecific message semantics across turns ([#1716](https://github.com/badlogic/pimono/issues/1716)). | CHANGELOG.md |
| G-PI-CHANGELOG-145 | Fixed | Fixed Antigravity endpoint fallback: 403/404 responses now cascade to the next endpoint instead of throwing immediately, added `autopushcloudcodepa.sandbox` endpoint to the fallback list, and removed extra fingerprint headers (`XGoogApiClient`, `ClientMetadata`) from Antigravity requests ([#1830](https://github.com/badlogic/pimono/issues/1830)). | CHANGELOG.md |
| G-PI-CHANGELOG-146 | Fixed | Fixed `@mariozechner/piai/oauth` package exports to point directly at built `dist` files, avoiding broken TypeScript resolution through unpublished wrapper targets ([#1856](https://github.com/badlogic/pimono/issues/1856)). | CHANGELOG.md |
| G-PI-CHANGELOG-147 | Fixed | Fixed Gemini 3 unsigned tool call replay: use `skip_thought_signature_validator` sentinel instead of converting function calls to text, preserving structured tool call context across multiturn conversations ([#1829](https://github.com/badlogic/pimono/issues/1829)). | CHANGELOG.md |
| G-PI-CHANGELOG-148 | Breaking Changes | Moved Node OAuth runtime exports off the toplevel package entry. Import OAuth login/refresh functions from `@mariozechner/piai/oauth` instead of `@mariozechner/piai` ([#1814](https://github.com/badlogic/pimono/issues/1814)) | CHANGELOG.md |
| G-PI-CHANGELOG-149 | Added | Added `gemini3.1flashlitepreview` fallback model entry for the `google` provider so it remains selectable until upstream model catalogs include it ([#1785](https://github.com/badlogic/pimono/issues/1785), thanks [@nWN](https://github.com/nWN)). | CHANGELOG.md |
| G-PI-CHANGELOG-150 | Added | Added OpenCode Go provider support with `opencodego` model catalog entries and `OPENCODE_API_KEY` environment variable support ([#1757](https://github.com/badlogic/pimono/issues/1757)). | CHANGELOG.md |
| G-PI-CHANGELOG-151 | Changed | Updated Antigravity Gemini 3.1 model metadata and request headers to match current upstream behavior. | CHANGELOG.md |
| G-PI-CHANGELOG-152 | Fixed | Fixed Gemini 3.1 thinkinglevel detection in `google` and `googlevertex` providers so `gemini3.1` models use Gemini 3 levelbased thinking config instead of budget fallback ([#1785](https://github.com/badlogic/pimono/issues/1785), thanks [@nWN](https://github.com/nWN)). | CHANGELOG.md |
| G-PI-CHANGELOG-153 | Fixed | Fixed browser bundling failures by lazyloading the Bedrock provider and removing Nodeonly side effects from the default browser import graph ([#1814](https://github.com/badlogic/pimono/issues/1814)). | CHANGELOG.md |
| G-PI-CHANGELOG-154 | Fixed | Fixed `ERR_VM_DYNAMIC_IMPORT_CALLBACK_MISSING` failures by replacing `Function`based dynamic imports with module dynamic imports in browsersafe provider loading paths ([#1814](https://github.com/badlogic/pimono/issues/1814)). | CHANGELOG.md |
| G-PI-CHANGELOG-155 | Fixed | Fixed Bedrock region resolution for `AWS_PROFILE` by honoring `region` from the selected profile when present ([#1800](https://github.com/badlogic/pimono/issues/1800)). | CHANGELOG.md |
| G-PI-CHANGELOG-156 | Fixed | Fixed Groq Qwen3 reasoning effort mapping by translating unsupported effort values to providersupported values ([#1745](https://github.com/badlogic/pimono/issues/1745)). | CHANGELOG.md |
| G-PI-CHANGELOG-157 | Fixed | Restored builtin OAuth providers when unregistering dynamically registered provider IDs and added `resetOAuthProviders()` for registry reset flows. | CHANGELOG.md |
| G-PI-CHANGELOG-158 | Fixed | Fixed Z.ai thinking control using wrong parameter name (`thinking` instead of `enable_thinking`), causing thinking to always be enabled and wasting tokens/latency ([#1674](https://github.com/badlogic/pimono/pull/1674) by [@okuyam2y](https://github.com/okuyam2y)) | CHANGELOG.md |
| G-PI-CHANGELOG-159 | Fixed | Fixed `redacted_thinking` blocks being silently dropped during Anthropic streaming. They are now captured as `ThinkingContent` with `redacted: true`, passed back to the API in multiturn conversations, and handled in crossmodel message transformation ([#1665](https://github.com/badlogic/pimono/pull/1665) by [@tctev](https://github.com/tctev)) | CHANGELOG.md |
| G-PI-CHANGELOG-160 | Fixed | Fixed `interleavedthinking20250514` beta header being sent for adaptive thinking models (Opus 4.6, Sonnet 4.6) where the header is deprecated or redundant ([#1665](https://github.com/badlogic/pimono/pull/1665) by [@tctev](https://github.com/tctev)) | CHANGELOG.md |
| G-PI-CHANGELOG-161 | Fixed | Fixed temperature being sent alongside extended thinking, which is incompatible with both adaptive and budgetbased thinking modes ([#1665](https://github.com/badlogic/pimono/pull/1665) by [@tctev](https://github.com/tctev)) | CHANGELOG.md |
| G-PI-CHANGELOG-162 | Fixed | Fixed `(external, cli)` useragent flag causing 401 errors on Anthropic setuptoken endpoint ([#1677](https://github.com/badlogic/pimono/pull/1677) by [@LazerLance777](https://github.com/LazerLance777)) | CHANGELOG.md |
| G-PI-CHANGELOG-163 | Fixed | Fixed crash when OpenAIcompatible provider returns a chunk with no `choices` array by adding optional chaining ([#1671](https://github.com/badlogic/pimono/issues/1671)) | CHANGELOG.md |
| G-PI-CHANGELOG-164 | Added | Added `gemini3.1propreview` model support to the `googlegeminicli` provider ([#1599](https://github.com/badlogic/pimono/pull/1599) by [@audichuang](https://github.com/audichuang)) | CHANGELOG.md |
| G-PI-CHANGELOG-165 | Fixed | Fixed adaptive thinking for Claude Sonnet 4.6 in Anthropic and Bedrock providers, and clamped unsupported `xhigh` effort values to supported levels ([#1548](https://github.com/badlogic/pimono/pull/1548) by [@tctev](https://github.com/tctev)) | CHANGELOG.md |
| G-PI-CHANGELOG-166 | Fixed | Fixed Vertex ADC credential detection race by avoiding caching a false negative during async import initialization ([#1550](https://github.com/badlogic/pimono/pull/1550) by [@jeremiahgaylordweb](https://github.com/jeremiahgaylordweb)) | CHANGELOG.md |
| G-PI-CHANGELOG-167 | Added | Added Anthropic `claudesonnet46` fallback model entry to generated model definitions. | CHANGELOG.md |
| G-PI-CHANGELOG-168 | Added | Added `transport` to `StreamOptions` with values `"sse"`, `"websocket"`, and `"auto"` (currently supported by `openaicodexresponses`). | CHANGELOG.md |
| G-PI-CHANGELOG-169 | Added | Added WebSocket transport support for OpenAI Codex Responses (`openaicodexresponses`). | CHANGELOG.md |
| G-PI-CHANGELOG-170 | Changed | OpenAI Codex Responses now defaults to SSE transport unless `transport` is explicitly set. | CHANGELOG.md |
| G-PI-CHANGELOG-171 | Changed | OpenAI Codex Responses WebSocket connections are cached per `sessionId` and expire after 5 minutes of inactivity. | CHANGELOG.md |
| G-PI-CHANGELOG-172 | Added | Added MiniMax M2.5 model entries for `minimax`, `minimaxcn`, `openrouter`, and `vercelaigateway` providers, plus `minimaxm2.5free` for `opencode`. | CHANGELOG.md |
| G-PI-CHANGELOG-173 | Added | Added optional `metadata` field to `StreamOptions` for passing providerspecific metadata (e.g. Anthropic `user_id` for abuse tracking/rate limiting) ([#1384](https://github.com/badlogic/pimono/pull/1384) by [@7Sageer](https://github.com/7Sageer)) | CHANGELOG.md |
| G-PI-CHANGELOG-174 | Added | Added `gpt5.3codexspark` model definition for OpenAI and OpenAI Codex providers (128k context, textonly, research preview). Not yet functional, may become available in the next few hours or days. | CHANGELOG.md |
| G-PI-CHANGELOG-175 | Changed | Routed GitHub Copilot Claude 4.x models through Anthropic Messages API, centralized Copilot dynamic header handling, and added Copilot Claude Anthropic stream coverage ([#1353](https://github.com/badlogic/pimono/pull/1353) by [@NateSmyth](https://github.com/NateSmyth)) | CHANGELOG.md |
| G-PI-CHANGELOG-176 | Fixed | Fixed OpenAI completions and responses streams to tolerate malformed trailing toolcall JSON without failing parsing ([#1424](https://github.com/badlogic/pimono/issues/1424)) | CHANGELOG.md |
| G-PI-CHANGELOG-177 | Changed | Updated the Antigravity system instruction to a more compact version for Google Gemini CLI compatibility | CHANGELOG.md |
| G-PI-CHANGELOG-178 | Fixed | Use `parametersJsonSchema` for Google provider tool declarations to support full JSON Schema (anyOf, oneOf, const, etc.) ([#1398](https://github.com/badlogic/pimono/issues/1398) by [@jarib](https://github.com/jarib)) | CHANGELOG.md |
| G-PI-CHANGELOG-179 | Fixed | Reverted incorrect Antigravity model change: `claudeopus46thinking` back to `claudeopus45thinking` (model doesn't exist on Antigravity endpoint) | CHANGELOG.md |
| G-PI-CHANGELOG-180 | Fixed | Corrected opencode context windows for Claude Sonnet 4 and 4.5 ([#1383](https://github.com/badlogic/pimono/issues/1383)) | CHANGELOG.md |
| G-PI-CHANGELOG-181 | Added | Added OpenRouter `auto` model alias for automatic model routing ([#1361](https://github.com/badlogic/pimono/pull/1361) by [@yogasanas](https://github.com/yogasanas)) | CHANGELOG.md |
| G-PI-CHANGELOG-182 | Changed | Replaced Claude Opus 4.5 with Opus 4.6 in model definitions ([#1345](https://github.com/badlogic/pimono/pull/1345) by [@calvinhpnet](https://github.com/calvinhpnet)) | CHANGELOG.md |
| G-PI-CHANGELOG-183 | Added | Added `AWS_BEDROCK_SKIP_AUTH` and `AWS_BEDROCK_FORCE_HTTP1` environment variables for connecting to unauthenticated Bedrock proxies ([#1320](https://github.com/badlogic/pimono/pull/1320) by [@virtuald](https://github.com/virtuald)) | CHANGELOG.md |
| G-PI-CHANGELOG-184 | Fixed | Set OpenAI Responses API requests to `store: false` by default to avoid serverside history logging ([#1308](https://github.com/badlogic/pimono/issues/1308)) | CHANGELOG.md |
| G-PI-CHANGELOG-185 | Fixed | Reexported TypeBox `Type`, `Static`, and `TSchema` from `@mariozechner/piai` to match documentation and avoid duplicate TypeBox type identity issues in pnpm setups ([#1338](https://github.com/badlogic/pimono/issues/1338)) | CHANGELOG.md |
| G-PI-CHANGELOG-186 | Fixed | Fixed Bedrock adaptive thinking handling for Claude Opus 4.6 with interleaved thinking beta responses ([#1323](https://github.com/badlogic/pimono/pull/1323) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-187 | Fixed | Fixed `AWS_BEDROCK_SKIP_AUTH` environment detection to avoid `process` access in nonNode.js environments | CHANGELOG.md |
| G-PI-CHANGELOG-188 | Fixed | Fixed `supportsXhigh()` to treat Anthropic Messages Opus 4.6 models as xhighcapable so `streamSimple` can map `xhigh` to adaptive effort `max` | CHANGELOG.md |
| G-PI-CHANGELOG-189 | Fixed | Fixed Bedrock Opus 4.6 model IDs (removed `:0` suffix) and cache pricing for `us.` and `eu.` variants | CHANGELOG.md |
| G-PI-CHANGELOG-190 | Fixed | Added missing `eu.anthropic.claudeopus46v1` inference profile to model catalog | CHANGELOG.md |
| G-PI-CHANGELOG-191 | Fixed | Fixed Claude Opus 4.6 context window metadata to 200000 for Anthropic and OpenCode providers | CHANGELOG.md |
| G-PI-CHANGELOG-192 | Added | Added adaptive thinking support for Claude Opus 4.6 with effort levels (`low`, `medium`, `high`, `max`) | CHANGELOG.md |
| G-PI-CHANGELOG-193 | Added | Added `effort` option to `AnthropicOptions` for controlling adaptive thinking depth | CHANGELOG.md |
| G-PI-CHANGELOG-194 | Added | `thinkingEnabled` now automatically uses adaptive thinking for Opus 4.6+ models and budgetbased thinking for older models | CHANGELOG.md |
| G-PI-CHANGELOG-195 | Added | `streamSimple`/`completeSimple` automatically map `ThinkingLevel` to effort levels for Opus 4.6 | CHANGELOG.md |
| G-PI-CHANGELOG-196 | Changed | Updated `@anthropicai/sdk` to 0.73.0 | CHANGELOG.md |
| G-PI-CHANGELOG-197 | Changed | Updated `@awssdk/clientbedrockruntime` to 3.983.0 | CHANGELOG.md |
| G-PI-CHANGELOG-198 | Changed | Updated `@google/genai` to 1.40.0 | CHANGELOG.md |
| G-PI-CHANGELOG-199 | Changed | Removed `fastxmlparser` override (no longer needed) | CHANGELOG.md |
| G-PI-CHANGELOG-200 | Added | Added Claude Opus 4.6 model to the generated model catalog | CHANGELOG.md |
| G-PI-CHANGELOG-201 | Added | Added GPT5.3 Codex model to the generated model catalog (OpenAI Codex provider only) | CHANGELOG.md |
| G-PI-CHANGELOG-202 | Fixed | Fixed OpenAI Codex Responses provider to respect configured baseUrl ([#1244](https://github.com/badlogic/pimono/issues/1244)) | CHANGELOG.md |
| G-PI-CHANGELOG-203 | Changed | Changed Bedrock model generation to drop legacy workarounds now handled upstream ([#1239](https://github.com/badlogic/pimono/pull/1239) by [@unexge](https://github.com/unexge)) | CHANGELOG.md |
| G-PI-CHANGELOG-204 | Fixed | Fixed xhigh thinking level support check to accept gpt5.2 model IDs ([#1209](https://github.com/badlogic/pimono/issues/1209)) | CHANGELOG.md |
| G-PI-CHANGELOG-205 | Fixed | Fixed `cache_control` not being applied to stringformat user messages in Anthropic provider | CHANGELOG.md |
| G-PI-CHANGELOG-206 | Fixed | Fixed `cacheRetention` option not being passed through in `buildBaseOptions` ([#1154](https://github.com/badlogic/pimono/issues/1154)) | CHANGELOG.md |
| G-PI-CHANGELOG-207 | Fixed | Fixed OAuth login/refresh not using HTTP proxy settings (`HTTP_PROXY`, `HTTPS_PROXY` env vars) ([#1132](https://github.com/badlogic/pimono/issues/1132)) | CHANGELOG.md |
| G-PI-CHANGELOG-208 | Fixed | Fixed OpenAIcompatible completions to omit unsupported `strict` tool fields for providers that reject them ([#1172](https://github.com/badlogic/pimono/issues/1172)) | CHANGELOG.md |
| G-PI-CHANGELOG-209 | Added | Added `PI_AI_ANTIGRAVITY_VERSION` environment variable to override the Antigravity UserAgent version when Google updates their version requirements ([#1129](https://github.com/badlogic/pimono/issues/1129)) | CHANGELOG.md |
| G-PI-CHANGELOG-210 | Added | Added `cacheRetention` stream option with providerspecific mappings for prompt cache controls, defaulting to short retention ([#1134](https://github.com/badlogic/pimono/issues/1134)) | CHANGELOG.md |
| G-PI-CHANGELOG-211 | Added | Added `maxRetryDelayMs` option to `StreamOptions` to cap serverrequested retry delays. When a provider (e.g., Google Gemini CLI) requests a delay longer than this value, the request fails immediately with an informative error instead of waiting silently. Default: 60000ms (60 seconds). Set to 0 to disable the cap. ([#1123](https://github.com/badlogic/pimono/issues/1123)) | CHANGELOG.md |
| G-PI-CHANGELOG-212 | Added | Added Qwen thinking format support for OpenAIcompatible completions via `enable_thinking`. ([#940](https://github.com/badlogic/pimono/pull/940) by [@4h9fbZ](https://github.com/4h9fbZ)) | CHANGELOG.md |
| G-PI-CHANGELOG-213 | Added | Added Vercel AI Gateway routing support via `vercelGatewayRouting` option in model config ([#1051](https://github.com/badlogic/pimono/pull/1051) by [@benvargas](https://github.com/benvargas)) | CHANGELOG.md |
| G-PI-CHANGELOG-214 | Fixed | Updated Antigravity UserAgent from 1.11.5 to 1.15.8 to fix rejected requests ([#1079](https://github.com/badlogic/pimono/issues/1079)) | CHANGELOG.md |
| G-PI-CHANGELOG-215 | Fixed | Fixed tool call argument defaults for Anthropic and Google history conversion when providers omit inputs ([#1065](https://github.com/badlogic/pimono/issues/1065)) | CHANGELOG.md |
| G-PI-CHANGELOG-216 | Added | Added Kimi For Coding provider support (Moonshot AI's Anthropiccompatible coding API) | CHANGELOG.md |
| G-PI-CHANGELOG-217 | Added | Added Hugging Face provider support via OpenAIcompatible Inference Router ([#994](https://github.com/badlogic/pimono/issues/994)) | CHANGELOG.md |
| G-PI-CHANGELOG-218 | Added | Added `PI_CACHE_RETENTION` environment variable to control cache TTL for Anthropic (5m vs 1h) and OpenAI (inmemory vs 24h). Set to `long` for extended retention. Only applies to direct API calls (api.anthropic.com, api.openai.com). ([#967](https://github.com/badlogic/pimono/issues/967)) | CHANGELOG.md |
| G-PI-CHANGELOG-219 | Fixed | Fixed OpenAI completions `toolChoice` handling to correctly set `type: "function"` wrapper ([#998](https://github.com/badlogic/pimono/pull/998) by [@williamtwomey](https://github.com/williamtwomey)) | CHANGELOG.md |
| G-PI-CHANGELOG-220 | Fixed | Fixed crossprovider handoff failing when switching from OpenAI Responses API providers (githubcopilot, openaicodex) to other providers due to pipeseparated tool call IDs not being normalized, and trailing underscores in truncated IDs being rejected by OpenAI Codex ([#1022](https://github.com/badlogic/pimono/issues/1022)) | CHANGELOG.md |
| G-PI-CHANGELOG-221 | Fixed | Fixed 429 rate limit errors incorrectly triggering autocompaction instead of retry with backoff ([#1038](https://github.com/badlogic/pimono/issues/1038)) | CHANGELOG.md |
| G-PI-CHANGELOG-222 | Fixed | Fixed Anthropic provider to handle `sensitive` stop_reason returned by API ([#978](https://github.com/badlogic/pimono/issues/978)) | CHANGELOG.md |
| G-PI-CHANGELOG-223 | Fixed | Fixed DeepSeek API compatibility by detecting `deepseek.com` URLs and disabling unsupported `developer` role ([#1048](https://github.com/badlogic/pimono/issues/1048)) | CHANGELOG.md |
| G-PI-CHANGELOG-224 | Fixed | Fixed Anthropic provider to preserve input token counts when proxies omit them in `message_delta` events ([#1045](https://github.com/badlogic/pimono/issues/1045)) | CHANGELOG.md |
| G-PI-CHANGELOG-225 | Fixed | Fixed OpenCode Zen model generation to exclude deprecated models ([#970](https://github.com/badlogic/pimono/pull/970) by [@DanielTatarkin](https://github.com/DanielTatarkin)) | CHANGELOG.md |
| G-PI-CHANGELOG-226 | Added | Added OpenRouter provider routing support for custom models via `openRouterRouting` compat field ([#859](https://github.com/badlogic/pimono/pull/859) by [@v01dpr1mr0s3](https://github.com/v01dpr1mr0s3)) | CHANGELOG.md |
| G-PI-CHANGELOG-227 | Added | Added `azureopenairesponses` provider support for Azure OpenAI Responses API. ([#890](https://github.com/badlogic/pimono/pull/890) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-228 | Added | Added HTTP proxy environment variable support for API requests ([#942](https://github.com/badlogic/pimono/pull/942) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-229 | Added | Added `createAssistantMessageEventStream()` factory function for use in extensions. | CHANGELOG.md |
| G-PI-CHANGELOG-230 | Added | Added `resetApiProviders()` to clear and reregister builtin API providers. | CHANGELOG.md |
| G-PI-CHANGELOG-231 | Changed | Refactored API streaming dispatch to use an API registry with providerowned `streamSimple` mapping. | CHANGELOG.md |
| G-PI-CHANGELOG-232 | Changed | Moved environment API key resolution to `envapikeys.ts` and reexported it from the package entrypoint. | CHANGELOG.md |
| G-PI-CHANGELOG-233 | Changed | Azure OpenAI Responses provider now uses base URL configuration with deploymentaware model mapping and no longer includes service tier handling. | CHANGELOG.md |
| G-PI-CHANGELOG-234 | Fixed | Fixed Bun runtime detection for dynamic imports in browsercompatible modules (stream.ts, openaicodexresponses.ts, openaicodex.ts) ([#922](https://github.com/badlogic/pimono/pull/922) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-235 | Fixed | Fixed streaming functions to use `model.api` instead of hardcoded API types | CHANGELOG.md |
| G-PI-CHANGELOG-236 | Fixed | Fixed Google providers to default tool call arguments to an empty object when omitted | CHANGELOG.md |
| G-PI-CHANGELOG-237 | Fixed | Fixed OpenAI Responses streaming to handle `arguments.done` events on OpenAIcompatible endpoints ([#917](https://github.com/badlogic/pimono/pull/917) by [@williballenthin](https://github.com/williballenthin)) | CHANGELOG.md |
| G-PI-CHANGELOG-238 | Fixed | Fixed OpenAI Codex Responses tool strictness handling after the shared responses refactor | CHANGELOG.md |
| G-PI-CHANGELOG-239 | Fixed | Fixed Azure OpenAI Responses streaming to guard deltas before content parts and correct metadata and handoff gating | CHANGELOG.md |
| G-PI-CHANGELOG-240 | Fixed | Fixed OpenAI completions toolresult image batching after consecutive tool results ([#902](https://github.com/badlogic/pimono/pull/902) by [@terrorobe](https://github.com/terrorobe)) | CHANGELOG.md |
| G-PI-CHANGELOG-241 | Added | Added `headers` option to `StreamOptions` for custom HTTP headers in API requests. Supported by all providers except Amazon Bedrock (which uses AWS SDK auth). Headers are merged with provider defaults and `model.headers`, with `options.headers` taking precedence. | CHANGELOG.md |
| G-PI-CHANGELOG-242 | Added | Added `originator` option to `loginOpenAICodex()` for custom OAuth client identification | CHANGELOG.md |
| G-PI-CHANGELOG-243 | Added | Browser compatibility for piai: replaced toplevel Node.js imports with dynamic imports for browser environments ([#873](https://github.com/badlogic/pimono/issues/873)) | CHANGELOG.md |
| G-PI-CHANGELOG-244 | Fixed | Fixed OpenAI Responses API 400 error "function_call without required reasoning item" when switching between models (same provider, different model). The fix omits the `id` field for function_calls from different models to avoid triggering OpenAI's reasoning/function_call pairing validation ([#886](https://github.com/badlogic/pimono/issues/886)) | CHANGELOG.md |
| G-PI-CHANGELOG-245 | Added | Added AWS credential detection for ECS/Kubernetes environments: `AWS_CONTAINER_CREDENTIALS_RELATIVE_URI`, `AWS_CONTAINER_CREDENTIALS_FULL_URI`, `AWS_WEB_IDENTITY_TOKEN_FILE` ([#848](https://github.com/badlogic/pimono/issues/848)) | CHANGELOG.md |
| G-PI-CHANGELOG-246 | Fixed | Fixed OpenAI Responses 400 error "reasoning without following item" by skipping errored/aborted assistant messages entirely in transformmessages.ts ([#838](https://github.com/badlogic/pimono/pull/838)) | CHANGELOG.md |
| G-PI-CHANGELOG-247 | Removed | Removed `strictResponsesPairing` compat option (no longer needed after the transformmessages fix) | CHANGELOG.md |
| G-PI-CHANGELOG-248 | Added | Added `OpenAIResponsesCompat` interface with `strictResponsesPairing` option for Azure OpenAI Responses API, which requires strict reasoning/message pairing in history replay ([#768](https://github.com/badlogic/pimono/pull/768) by [@prateekmedia](https://github.com/prateekmedia)) | CHANGELOG.md |
| G-PI-CHANGELOG-249 | Changed | Split `OpenAICompat` into `OpenAICompletionsCompat` and `OpenAIResponsesCompat` for typesafe APIspecific compat settings | CHANGELOG.md |
| G-PI-CHANGELOG-250 | Fixed | Fixed tool call ID normalization for crossprovider handoffs (e.g., Codex to Antigravity Claude) ([#821](https://github.com/badlogic/pimono/issues/821)) | CHANGELOG.md |
| G-PI-CHANGELOG-251 | Changed | OpenAI Codex responses now use the context system prompt directly in the instructions field. | CHANGELOG.md |
| G-PI-CHANGELOG-252 | Fixed | Fixed orphaned tool results after errored assistant messages causing Codex API errors. When an assistant message has `stopReason: "error"`, its tool calls are now excluded from pending tool tracking, preventing synthetic tool results from being generated for calls that will be dropped by providerspecific converters. ([#812](https://github.com/badlogic/pimono/issues/812)) | CHANGELOG.md |
| G-PI-CHANGELOG-253 | Fixed | Fixed Bedrock Claude max_tokens handling to always exceed thinking budget tokens, preventing compaction failures. ([#797](https://github.com/badlogic/pimono/pull/797) by [@pjtf93](https://github.com/pjtf93)) | CHANGELOG.md |
| G-PI-CHANGELOG-254 | Fixed | Fixed Claude Code tool name normalization to match the Claude Code tool list caseinsensitively and remove invalid mappings. | CHANGELOG.md |
| G-PI-CHANGELOG-255 | Fixed | Fixed OpenAIcompatible provider feature detection to use `model.provider` in addition to URL, allowing custom base URLs (e.g., proxies) to work correctly with providerspecific settings ([#774](https://github.com/badlogic/pimono/issues/774)) | CHANGELOG.md |
| G-PI-CHANGELOG-256 | Fixed | Fixed Gemini 3 context loss when switching from providers without thought signatures: unsigned tool calls are now converted to text with antimimicry notes instead of being skipped | CHANGELOG.md |
| G-PI-CHANGELOG-257 | Fixed | Fixed string numbers in tool arguments not being coerced to numbers during validation ([#786](https://github.com/badlogic/pimono/pull/786) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-258 | Fixed | Fixed Bedrock tool call IDs to use only alphanumeric characters, avoiding API errors from invalid characters ([#781](https://github.com/badlogic/pimono/pull/781) by [@pjtf93](https://github.com/pjtf93)) | CHANGELOG.md |
| G-PI-CHANGELOG-259 | Fixed | Fixed empty error assistant messages (from 429/500 errors) breaking the tool_use to tool_result chain by filtering them in `transformMessages` | CHANGELOG.md |
| G-PI-CHANGELOG-260 | Fixed | Fixed OpenCode provider's `/v1` endpoint to use `system` role instead of `developer` role, fixing `400 Incorrect role information` error for models using `openaicompletions` API ([#755](https://github.com/badlogic/pimono/pull/755) by [@melihmucuk](https://github.com/melihmucuk)) | CHANGELOG.md |
| G-PI-CHANGELOG-261 | Fixed | Added retry logic to OpenAI Codex provider for transient errors (429, 5xx, connection failures). Uses exponential backoff with up to 3 retries. ([#733](https://github.com/badlogic/pimono/issues/733)) | CHANGELOG.md |
| G-PI-CHANGELOG-262 | Added | Added MiniMax China (`minimaxcn`) provider support ([#725](https://github.com/badlogic/pimono/pull/725) by [@tallshort](https://github.com/tallshort)) | CHANGELOG.md |
| G-PI-CHANGELOG-263 | Added | Added `gpt5.2codex` models for GitHub Copilot and OpenCode Zen providers ([#734](https://github.com/badlogic/pimono/pull/734) by [@aadishv](https://github.com/aadishv)) | CHANGELOG.md |
| G-PI-CHANGELOG-264 | Fixed | Avoid unsigned Gemini 3 tool calls ([#741](https://github.com/badlogic/pimono/pull/741) by [@roshanasingh4](https://github.com/roshanasingh4)) | CHANGELOG.md |
| G-PI-CHANGELOG-265 | Fixed | Fixed signature support for nonAnthropic models in Amazon Bedrock provider ([#727](https://github.com/badlogic/pimono/pull/727) by [@unexge](https://github.com/unexge)) | CHANGELOG.md |
| G-PI-CHANGELOG-266 | Fixed | Fixed OpenAI Responses timeout option handling ([#706](https://github.com/badlogic/pimono/pull/706) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-267 | Fixed | Fixed Bedrock tool call conversion to apply message transforms ([#707](https://github.com/badlogic/pimono/pull/707) by [@pjtf93](https://github.com/pjtf93)) | CHANGELOG.md |
| G-PI-CHANGELOG-268 | Fixed | Export `parseStreamingJson` from main package for tsx dev mode compatibility | CHANGELOG.md |
| G-PI-CHANGELOG-269 | Added | Added Vercel AI Gateway provider with model discovery and `AI_GATEWAY_API_KEY` env support ([#689](https://github.com/badlogic/pimono/pull/689) by [@timolins](https://github.com/timolins)) | CHANGELOG.md |
| G-PI-CHANGELOG-270 | Fixed | Fixed z.ai thinking/reasoning: z.ai uses `thinking: { type: "enabled" }` instead of OpenAI's `reasoning_effort`. Added `thinkingFormat` compat flag to handle this. ([#688](https://github.com/badlogic/pimono/issues/688)) | CHANGELOG.md |
| G-PI-CHANGELOG-271 | Added | MiniMax provider support with M2 and M2.1 models via Anthropiccompatible API ([#656](https://github.com/badlogic/pimono/pull/656) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-272 | Added | Add Amazon Bedrock provider with prompt caching for Claude models (experimental, tested with Anthropic Claude models only) ([#494](https://github.com/badlogic/pimono/pull/494) by [@unexge](https://github.com/unexge)) | CHANGELOG.md |
| G-PI-CHANGELOG-273 | Added | Added `serviceTier` option for OpenAI Responses requests ([#672](https://github.com/badlogic/pimono/pull/672) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-274 | Added | Anthropic caching on OpenRouter: Interactions with Anthropic models via OpenRouter now set a 5minute cache point using Anthropicstyle `cache_control` breakpoints on the last assistant or user message. ([#584](https://github.com/badlogic/pimono/pull/584) by [@nathyong](https://github.com/nathyong)) | CHANGELOG.md |
| G-PI-CHANGELOG-275 | Added | Google Gemini CLI provider improvements: Added Antigravity endpoint fallback (tries daily sandbox then prod when `baseUrl` is unset), headerbased retry delay parsing (`RetryAfter`, `xratelimitreset`, `xratelimitresetafter`), stable `sessionId` derivation from first user message for cache affinity, empty SSE stream retry with backoff, and `anthropicbeta` header for Claude thinking models ([#670](https://github.com/badlogic/pimono/pull/670) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-276 | Fixed | Fixed Google provider thinking detection: `isThinkingPart()` now only checks `thought === true`, not `thoughtSignature`. Per Google docs, `thoughtSignature` is for context replay and can appear on any part type. Also removed `id` field from `functionCall`/`functionResponse` (rejected by Vertex AI and Cloud Code Assist), and added `textSignature` roundtrip for multiturn reasoning context. ([#631](https://github.com/badlogic/pimono/pull/631) by [@theBucky](https://github.com/theBucky)) | CHANGELOG.md |
| G-PI-CHANGELOG-277 | Changed | OpenAI Codex: switched to bundled system prompt matching opencode, changed originator to "pi", simplified prompt handling | CHANGELOG.md |
| G-PI-CHANGELOG-278 | Added | Added `GOOGLE_APPLICATION_CREDENTIALS` env var support for Vertex AI credential detection (standard for CI/production). | CHANGELOG.md |
| G-PI-CHANGELOG-279 | Added | Added `supportsUsageInStreaming` compatibility flag for OpenAIcompatible providers that reject `stream_options: { include_usage: true }`. Defaults to `true`. Set to `false` in model config for providers like gatewayz.ai. ([#596](https://github.com/badlogic/pimono/pull/596) by [@XesGaDeus](https://github.com/XesGaDeus)) | CHANGELOG.md |
| G-PI-CHANGELOG-280 | Added | Improved Google model pricing info ([#588](https://github.com/badlogic/pimono/pull/588) by [@aadishv](https://github.com/aadishv)) | CHANGELOG.md |
| G-PI-CHANGELOG-281 | Fixed | Fixed `os.homedir()` calls at module load time; now resolved lazily when needed. | CHANGELOG.md |
| G-PI-CHANGELOG-282 | Fixed | Fixed OpenAI Responses tool strict flag to use a boolean for LM Studio compatibility ([#598](https://github.com/badlogic/pimono/pull/598) by [@gnattu](https://github.com/gnattu)) | CHANGELOG.md |
| G-PI-CHANGELOG-283 | Fixed | Fixed Google Cloud Code Assist OAuth for paid subscriptions: properly handles longrunning operations for project provisioning, supports `GOOGLE_CLOUD_PROJECT` / `GOOGLE_CLOUD_PROJECT_ID` env vars for paid tiers, and handles VPCSC affected users ([#582](https://github.com/badlogic/pimono/pull/582) by [@cmf](https://github.com/cmf)) | CHANGELOG.md |
| G-PI-CHANGELOG-284 | Added | Added OpenCode Zen provider support with 26 models (Claude, GPT, Gemini, Grok, Kimi, GLM, Qwen, etc.). Set `OPENCODE_API_KEY` env var to use. | CHANGELOG.md |
| G-PI-CHANGELOG-285 | Fixed | Fixed Gemini CLI abort handling: detect native `AbortError` in retry catch block, cancel SSE reader when abort signal fires ([#568](https://github.com/badlogic/pimono/pull/568) by [@tmustier](https://github.com/tmustier)) | CHANGELOG.md |
| G-PI-CHANGELOG-286 | Fixed | Fixed Antigravity provider 429 errors by aligning request payload with CLIProxyAPI v6.6.89: inject Antigravity system instruction with `role: "user"`, set `requestType: "agent"`, and use `antigravity` userAgent. Added bridge prompt to override Antigravity behavior (identity, paths, web dev guidelines) with Pi defaults. ([#571](https://github.com/badlogic/pimono/pull/571) by [@benvargas](https://github.com/benvargas)) | CHANGELOG.md |
| G-PI-CHANGELOG-287 | Fixed | Fixed thinking block handling for crossmodel conversations: thinking blocks are now converted to plain text (no `<thinking>` tags) when switching models. Previously, `<thinking>` tags caused models to mimic the pattern and output literal tags. Also fixed empty thinking blocks causing API errors. ([#561](https://github.com/badlogic/pimono/issues/561)) | CHANGELOG.md |
| G-PI-CHANGELOG-288 | Added | `thinkingBudgets` option in `SimpleStreamOptions` for customizing token budgets per thinking level on tokenbased providers ([#529](https://github.com/badlogic/pimono/pull/529) by [@melihmucuk](https://github.com/melihmucuk)) | CHANGELOG.md |
| G-PI-CHANGELOG-289 | Breaking Changes | Removed OpenAI Codex model aliases (`gpt5`, `gpt5mini`, `gpt5nano`, `codexminilatest`, `gpt5codex`, `gpt5.1codex`, `gpt5.1chatlatest`). Use canonical model IDs: `gpt5.1`, `gpt5.1codexmax`, `gpt5.1codexmini`, `gpt5.2`, `gpt5.2codex`. ([#536](https://github.com/badlogic/pimono/pull/536) by [@ghoulr](https://github.com/ghoulr)) | CHANGELOG.md |
| G-PI-CHANGELOG-290 | Fixed | Fixed OpenAI Codex context window from 400,000 to 272,000 tokens to match Codex CLI defaults and prevent 400 errors. ([#536](https://github.com/badlogic/pimono/pull/536) by [@ghoulr](https://github.com/ghoulr)) | CHANGELOG.md |
| G-PI-CHANGELOG-291 | Fixed | Fixed Codex SSE error events to surface message, code, and status. ([#551](https://github.com/badlogic/pimono/pull/551) by [@tmustier](https://github.com/tmustier)) | CHANGELOG.md |
| G-PI-CHANGELOG-292 | Fixed | Fixed context overflow detection for `context_length_exceeded` error codes. | CHANGELOG.md |
| G-PI-CHANGELOG-293 | Added | Exported OpenAI Codex utilities: `CacheMetadata`, `getCodexInstructions`, `getModelFamily`, `ModelFamily`, `buildCodexPiBridge`, `buildCodexSystemPrompt`, `CodexSystemPrompt` ([#510](https://github.com/badlogic/pimono/pull/510) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-294 | Added | `sessionId` option in `StreamOptions` for providers that support sessionbased caching. OpenAI Codex provider uses this to set `prompt_cache_key` and routing headers. | CHANGELOG.md |
| G-PI-CHANGELOG-295 | Fixed | Codex provider now always includes `reasoning.encrypted_content` even when custom `include` options are passed ([#484](https://github.com/badlogic/pimono/pull/484) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-296 | Breaking Changes | OpenAI Codex models no longer have perthinkinglevel variants (e.g., `gpt5.2codexhigh`). Use the base model ID and set thinking level separately. The Codex provider clamps reasoning effort to what each model supports internally. (initial implementation by [@benvargas](https://github.com/benvargas) in [#472](https://github.com/badlogic/pimono/pull/472)) | CHANGELOG.md |
| G-PI-CHANGELOG-297 | Added | Headless OAuth support for all callbackserver providers (Google Gemini CLI, Antigravity, OpenAI Codex): paste redirect URL when browser callback is unreachable ([#428](https://github.com/badlogic/pimono/pull/428) by [@benvargas](https://github.com/benvargas), [#468](https://github.com/badlogic/pimono/pull/468) by [@crcatala](https://github.com/crcatala)) | CHANGELOG.md |
| G-PI-CHANGELOG-298 | Added | Cancellable GitHub Copilot device code polling via AbortSignal | CHANGELOG.md |
| G-PI-CHANGELOG-299 | Fixed | Codex requests now omit the `reasoning` field entirely when thinking is off, letting the backend use its default instead of forcing a value. ([#472](https://github.com/badlogic/pimono/pull/472)) | CHANGELOG.md |
| G-PI-CHANGELOG-300 | Added | OpenAI Codex OAuth provider with Responses API streaming support: `openaicodexresponses` streaming provider with SSE parsing, toolcall handling, usage/cost tracking, and PKCE OAuth flow ([#451](https://github.com/badlogic/pimono/pull/451) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-301 | Fixed | Vertex AI dummy value for `getEnvApiKey()`: Returns `"<authenticated>"` when Application Default Credentials are configured (`~/.config/gcloud/application_default_credentials.json` exists) and both `GOOGLE_CLOUD_PROJECT` (or `GCLOUD_PROJECT`) and `GOOGLE_CLOUD_LOCATION` are set. This allows `streamSimple()` to work with Vertex AI without explicit `apiKey` option. The ADC credentials file existence check is cached perprocess to avoid repeated filesystem access. | CHANGELOG.md |
| G-PI-CHANGELOG-302 | Fixed | Google Vertex AI models no longer appear in available models list without explicit authentication. Previously, `getEnvApiKey()` returned a dummy value for `googlevertex`, causing models to show up even when Google Cloud ADC was not configured. | CHANGELOG.md |
| G-PI-CHANGELOG-303 | Added | Vertex AI provider with ADC (Application Default Credentials) support. Authenticate with `gcloud auth applicationdefault login`, set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`, and access Gemini models via Vertex AI. ([#300](https://github.com/badlogic/pimono/pull/300) by [@defaultanton](https://github.com/defaultanton)) | CHANGELOG.md |
| G-PI-CHANGELOG-304 | Fixed | Gemini CLI rate limit handling: Added automatic retry with serverprovided delay for 429 errors. Parses delay from error messages like "Your quota will reset after 39s" and waits accordingly. Falls back to exponential backoff for other transient errors. ([#370](https://github.com/badlogic/pimono/issues/370)) | CHANGELOG.md |
| G-PI-CHANGELOG-305 | Breaking Changes | Agent API moved: All agent functionality (`agentLoop`, `agentLoopContinue`, `AgentContext`, `AgentEvent`, `AgentTool`, `AgentToolResult`, etc.) has moved to `@mariozechner/piagentcore`. Import from that package instead of `@mariozechner/piai`. | CHANGELOG.md |
| G-PI-CHANGELOG-306 | Added | `GoogleThinkingLevel` type: Exported type that mirrors Google's `ThinkingLevel` enum values (`"THINKING_LEVEL_UNSPECIFIED" | "MINIMAL" | "LOW" | "MEDIUM" | "HIGH"`). Allows configuring Gemini thinking levels without importing from `@google/genai`. | CHANGELOG.md |
| G-PI-CHANGELOG-307 | Added | `ANTHROPIC_OAUTH_TOKEN` env var: Now checked before `ANTHROPIC_API_KEY` in `getEnvApiKey()`, allowing OAuth tokens to take precedence. | CHANGELOG.md |
| G-PI-CHANGELOG-308 | Added | `eventstream.js` export: `AssistantMessageEventStream` utility now exported from package index. | CHANGELOG.md |
| G-PI-CHANGELOG-309 | Changed | OAuth uses Web Crypto API: PKCE generation and OAuth flows now use Web Crypto API (`crypto.subtle`) instead of Node.js `crypto` module. This improves browser compatibility while still working in Node.js 20+. | CHANGELOG.md |
| G-PI-CHANGELOG-310 | Changed | Deterministic model generation: `generatemodels.ts` now sorts providers and models alphabetically for consistent output across runs. ([#332](https://github.com/badlogic/pimono/pull/332) by [@mrexodia](https://github.com/mrexodia)) | CHANGELOG.md |
| G-PI-CHANGELOG-311 | Fixed | OpenAI completions empty content blocks: Empty text or thinking blocks in assistant messages are now filtered out before sending to the OpenAI completions API, preventing validation errors. ([#344](https://github.com/badlogic/pimono/pull/344) by [@defaultanton](https://github.com/defaultanton)) | CHANGELOG.md |
| G-PI-CHANGELOG-312 | Fixed | Thinking token duplication: Fixed thinking content duplication with chutes.ai provider. The provider was returning thinking content in both `reasoning_content` and `reasoning` fields, causing each chunk to be processed twice. Now only the first nonempty reasoning field is used. | CHANGELOG.md |
| G-PI-CHANGELOG-313 | Fixed | zAi provider API mapping: Fixed zAi models to use `openaicompletions` API with correct base URL (`https://api.z.ai/api/coding/paas/v4`) instead of incorrect Anthropic API mapping. ([#344](https://github.com/badlogic/pimono/pull/344), [#358](https://github.com/badlogic/pimono/pull/358) by [@defaultanton](https://github.com/defaultanton)) | CHANGELOG.md |
| G-PI-CHANGELOG-314 | Breaking Changes | OAuth storage removed ([#296](https://github.com/badlogic/pimono/issues/296)): All storage functions (`loadOAuthCredentials`, `saveOAuthCredentials`, `setOAuthStorage`, etc.) removed. Callers are responsible for storing credentials. | CHANGELOG.md |
| G-PI-CHANGELOG-315 | Breaking Changes | OAuth login functions: `loginAnthropic`, `loginGitHubCopilot`, `loginGeminiCli`, `loginAntigravity` now return `OAuthCredentials` instead of saving to disk. | CHANGELOG.md |
| G-PI-CHANGELOG-316 | Breaking Changes | refreshOAuthToken: Now takes `(provider, credentials)` and returns new `OAuthCredentials` instead of saving. | CHANGELOG.md |
| G-PI-CHANGELOG-317 | Breaking Changes | getOAuthApiKey: Now takes `(provider, credentials)` and returns `{ newCredentials, apiKey }` or null. | CHANGELOG.md |
| G-PI-CHANGELOG-318 | Breaking Changes | OAuthCredentials type: No longer includes `type: "oauth"` discriminator. Callers add discriminator when storing. | CHANGELOG.md |
| G-PI-CHANGELOG-319 | Breaking Changes | setApiKey, resolveApiKey: Removed. Callers must manage their own API key storage/resolution. | CHANGELOG.md |
| G-PI-CHANGELOG-320 | Breaking Changes | getApiKey: Renamed to `getEnvApiKey`. Only checks environment variables for known providers. | CHANGELOG.md |
| G-PI-CHANGELOG-321 | Fixed | Thinking tag leakage: Fixed Claude mimicking literal `</thinking>` tags in responses. Unsigned thinking blocks (from aborted streams) are now converted to plain text without `<thinking>` tags. The TUI still displays them as thinking blocks. ([#302](https://github.com/badlogic/pimono/pull/302) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-322 | Added | xhigh thinking level support: Added `supportsXhigh()` function to check if a model supports xhigh reasoning level. Also clamps xhigh to high for OpenAI models that don't support it. ([#236](https://github.com/badlogic/pimono/pull/236) by [@theBucky](https://github.com/theBucky)) | CHANGELOG.md |
| G-PI-CHANGELOG-323 | Fixed | Gemini multimodal tool results: Fixed images in tool results causing flaky/broken responses with Gemini models. For Gemini 3, images are now nested inside `functionResponse.parts` per the [docs](https://ai.google.dev/geminiapi/docs/functioncalling#multimodal). For older models (which don't support multimodal function responses), images are sent in a separate user message. | CHANGELOG.md |
| G-PI-CHANGELOG-324 | Fixed | Queued message steering: When `getQueuedMessages` is provided, the agent loop now checks for queued user messages after each tool call and skips remaining tool calls in the current assistant message when a queued message arrives (emitting error tool results). | CHANGELOG.md |
| G-PI-CHANGELOG-325 | Fixed | Double API version path in Google provider URL: Fixed Gemini API calls returning 404 after baseUrl support was added. The SDK was appending its default apiVersion to baseUrl which already included the version path. ([#251](https://github.com/badlogic/pimono/pull/251) by [@shellfyred](https://github.com/shellfyred)) | CHANGELOG.md |
| G-PI-CHANGELOG-326 | Fixed | Anthropic SDK retries disabled: Reenabled SDKlevel retries (default 2) for transient HTTP failures. ([#252](https://github.com/badlogic/pimono/issues/252)) | CHANGELOG.md |
| G-PI-CHANGELOG-327 | Added | Gemini 3 Flash thinking support: Extended thinking level support for Gemini 3 Flash models (MINIMAL, LOW, MEDIUM, HIGH) to match Pro models' capabilities. ([#212](https://github.com/badlogic/pimono/pull/212) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-328 | Added | GitHub Copilot thinking models: Added thinking support for additional Copilot models (o3mini, o1mini, o1preview). ([#234](https://github.com/badlogic/pimono/pull/234) by [@aadishv](https://github.com/aadishv)) | CHANGELOG.md |
| G-PI-CHANGELOG-329 | Fixed | Gemini tool result format: Fixed tool result format for Gemini 3 Flash Preview which strictly requires `{ output: value }` for success and `{ error: value }` for errors. Previous format using `{ result, isError }` was rejected by newer Gemini models. Also improved type safety by removing `as any` casts. ([#213](https://github.com/badlogic/pimono/issues/213), [#220](https://github.com/badlogic/pimono/pull/220)) | CHANGELOG.md |
| G-PI-CHANGELOG-330 | Fixed | Google baseUrl configuration: Google provider now respects `baseUrl` configuration for custom endpoints or API proxies. ([#216](https://github.com/badlogic/pimono/issues/216), [#221](https://github.com/badlogic/pimono/pull/221) by [@theBucky](https://github.com/theBucky)) | CHANGELOG.md |
| G-PI-CHANGELOG-331 | Fixed | GitHub Copilot vision requests: Added `CopilotVisionRequest` header when sending images to GitHub Copilot models. ([#222](https://github.com/badlogic/pimono/issues/222)) | CHANGELOG.md |
| G-PI-CHANGELOG-332 | Fixed | GitHub Copilot XInitiator header: Fixed XInitiator logic to check last message role instead of any message in history. This ensures proper billing when users send followup messages. ([#209](https://github.com/badlogic/pimono/issues/209)) | CHANGELOG.md |
| G-PI-CHANGELOG-333 | Added | Image limits test suite: Added comprehensive tests for providerspecific image limitations (max images, max size, max dimensions). Discovered actual limits: Anthropic (100 images, 5MB, 8000px), OpenAI (500 images, ≥25MB), Gemini (~2500 images, ≥40MB), Mistral (8 images, ~15MB), OpenRouter (~40 images contextlimited, ~15MB). ([#120](https://github.com/badlogic/pimono/pull/120)) | CHANGELOG.md |
| G-PI-CHANGELOG-334 | Added | Tool result streaming: Added `tool_execution_update` event and optional `onUpdate` callback to `AgentTool.execute()` for streaming tool output during execution. Tools can now emit partial results (e.g., bash stdout) that are forwarded to subscribers. ([#44](https://github.com/badlogic/pimono/issues/44)) | CHANGELOG.md |
| G-PI-CHANGELOG-335 | Added | XInitiator header for GitHub Copilot: Added XInitiator header handling for GitHub Copilot provider to ensure correct call accounting (agent calls are not deducted from quota). Sets initiator based on last message role. ([#200](https://github.com/badlogic/pimono/pull/200) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-336 | Changed | Normalized tool_execution_end result: `tool_execution_end` event now always contains `AgentToolResult` (no longer `AgentToolResult | string`). Errors are wrapped in the standard result format. | CHANGELOG.md |
| G-PI-CHANGELOG-337 | Fixed | Reasoning disabled by default: When `reasoning` option is not specified, thinking is now explicitly disabled for all providers. Previously, some providers like Gemini with "dynamic thinking" would use their default (thinking ON), causing unexpected token usage. This was the original intended behavior. ([#180](https://github.com/badlogic/pimono/pull/180) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-338 | Added | Interleaved thinking for Anthropic: Added `interleavedThinking` option to `AnthropicOptions`. When enabled, Claude 4 models can think between tool calls and reason after receiving tool results. Enabled by default (no extra token cost, just unlocks the capability). Set `interleavedThinking: false` to disable. | CHANGELOG.md |
| G-PI-CHANGELOG-339 | Added | Interleaved thinking for Anthropic: Enabled interleaved thinking in the Anthropic provider, allowing Claude models to output thinking blocks interspersed with text responses. | CHANGELOG.md |
| G-PI-CHANGELOG-340 | Added | GitHub Copilot provider: Added `githubcopilot` as a known provider with models sourced from models.dev. Includes Claude, GPT, Gemini, Grok, and other models available through GitHub Copilot. ([#191](https://github.com/badlogic/pimono/pull/191) by [@cau1k](https://github.com/cau1k)) | CHANGELOG.md |
| G-PI-CHANGELOG-341 | Fixed | GitHub Copilot gpt5 models: Fixed API selection for gpt5 models to use `openairesponses` instead of `openaicompletions` (gpt5 models are not accessible via completions endpoint) | CHANGELOG.md |
| G-PI-CHANGELOG-342 | Fixed | GitHub Copilot crossmodel context handoff: Fixed context handoff failing when switching between GitHub Copilot models using different APIs (e.g., gpt5 to claudesonnet4). Tool call IDs from OpenAI Responses API were incompatible with other models. ([#198](https://github.com/badlogic/pimono/issues/198)) | CHANGELOG.md |
| G-PI-CHANGELOG-343 | Fixed | Gemini 3 Pro thinking levels: Thinking level configuration now works correctly for Gemini 3 Pro models. Previously all levels mapped to 1 (minimal thinking). Now LOW/MEDIUM/HIGH properly control testtime computation. ([#176](https://github.com/badlogic/pimono/pull/176) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-344 | Changed | Anthropic SDK retries disabled: Set `maxRetries: 0` on Anthropic client to allow applicationlevel retry handling. The SDK's builtin retries were interfering with codingagent's retry logic. ([#157](https://github.com/badlogic/pimono/issues/157)) | CHANGELOG.md |
| G-PI-CHANGELOG-345 | Added | Mistral provider: Added support for Mistral AI models via the OpenAIcompatible API. Includes automatic handling of Mistralspecific requirements (tool call ID format). Set `MISTRAL_API_KEY` environment variable to use. | CHANGELOG.md |
| G-PI-CHANGELOG-346 | Fixed | Fixed Mistral 400 errors after aborted assistant messages by skipping empty assistant messages (no content, no tool calls) ([#165](https://github.com/badlogic/pimono/issues/165)) | CHANGELOG.md |
| G-PI-CHANGELOG-347 | Fixed | Removed synthetic assistant bridge message after tool results for Mistral (no longer required as of Dec 2025) ([#165](https://github.com/badlogic/pimono/issues/165)) | CHANGELOG.md |
| G-PI-CHANGELOG-348 | Fixed | Fixed bug where `ANTHROPIC_API_KEY` environment variable was deleted globally after first OAuth token usage, causing subsequent prompts to fail ([#164](https://github.com/badlogic/pimono/pull/164)) | CHANGELOG.md |
| G-PI-CHANGELOG-349 | Added | `agentLoopContinue` function: Continue an agent loop from existing context without adding a new user message. Validates that the last message is `user` or `toolResult`. Useful for retry after context overflow or resuming from manuallyadded tool results. | CHANGELOG.md |
| G-PI-CHANGELOG-350 | Breaking Changes | Removed providerlevel tool argument validation. Validation now happens in `agentLoop` via `executeToolCalls`, allowing models to retry on validation errors. For manual tool execution, use `validateToolCall(tools, toolCall)` or `validateToolArguments(tool, toolCall)`. | CHANGELOG.md |
| G-PI-CHANGELOG-351 | Added | Added `validateToolCall(tools, toolCall)` helper that finds the tool by name and validates arguments. | CHANGELOG.md |
| G-PI-CHANGELOG-352 | Added | OpenAI compatibility overrides: Added `compat` field to `Model` for `openaicompletions` API, allowing explicit configuration of provider quirks (`supportsStore`, `supportsDeveloperRole`, `supportsReasoningEffort`, `maxTokensField`). Falls back to URLbased detection if not set. Useful for LiteLLM, custom proxies, and other nonstandard endpoints. ([#133](https://github.com/badlogic/pimono/issues/133), thanks @finkandreas for the initial idea and PR) | CHANGELOG.md |
| G-PI-CHANGELOG-353 | Added | xhigh reasoning level: Added `xhigh` to `ReasoningEffort` type for OpenAI codexmax models. For nonOpenAI providers (Anthropic, Google), `xhigh` is automatically mapped to `high`. ([#143](https://github.com/badlogic/pimono/issues/143)) | CHANGELOG.md |
| G-PI-CHANGELOG-354 | Changed | Updated SDK versions: OpenAI SDK 5.21.0 → 6.10.0, Anthropic SDK 0.61.0 → 0.71.2, Google GenAI SDK 1.30.0 → 1.31.0 | CHANGELOG.md |
| G-PI-CHANGELOG-355 | Breaking Changes | Added `totalTokens` field to `Usage` type: All code that constructs `Usage` objects must now include the `totalTokens` field. This field represents the total tokens processed by the LLM (input + output + cache). For OpenAI and Google, this uses native API values (`total_tokens`, `totalTokenCount`). For Anthropic, it's computed as `input + output + cacheRead + cacheWrite`. | CHANGELOG.md |
| G-PI-CHANGELOG-356 | Added | Added `gpt5.1codexmax` model support | CHANGELOG.md |
| G-PI-CHANGELOG-357 | Fixed | OpenAI Token Counting: Fixed `usage.input` to exclude cached tokens for OpenAI providers. Previously, `input` included cached tokens, causing doublecounting when calculating total context size via `input + cacheRead`. Now `input` represents noncached input tokens across all providers, making `input + output + cacheRead + cacheWrite` the correct formula for total context size. | CHANGELOG.md |
| G-PI-CHANGELOG-358 | Fixed | Fixed Claude Opus 4.5 cache pricing (was 3x too expensive) | CHANGELOG.md |
| G-PI-CHANGELOG-359 | Fixed | Corrected cache_read: $1.50 → $0.50 per MTok | CHANGELOG.md |
| G-PI-CHANGELOG-360 | Fixed | Corrected cache_write: $18.75 → $6.25 per MTok | CHANGELOG.md |
| G-PI-CHANGELOG-361 | Fixed | Added manual override in `scripts/generatemodels.ts` until upstream fix is merged | CHANGELOG.md |
| G-PI-CHANGELOG-362 | Fixed | Submitted PR to models.dev: https://github.com/sst/models.dev/pull/439 | CHANGELOG.md |
| G-PI-README-001 | @mariozechner/pi-ai | Note: This library only includes models that support tool calling (function calling), as this is essential for agentic workflows. | README.md |
| G-PI-README-002 | Table of Contents | [Supported Providers](#supportedproviders) | README.md |
| G-PI-README-003 | Table of Contents | [Installation](#installation) | README.md |
| G-PI-README-004 | Table of Contents | [Quick Start](#quickstart) | README.md |
| G-PI-README-005 | Table of Contents | [Tools](#tools) | README.md |
| G-PI-README-006 | Table of Contents | [Defining Tools](#definingtools) | README.md |
| G-PI-README-007 | Table of Contents | [Handling Tool Calls](#handlingtoolcalls) | README.md |
| G-PI-README-008 | Table of Contents | [Streaming Tool Calls with Partial JSON](#streamingtoolcallswithpartialjson) | README.md |
| G-PI-README-009 | Table of Contents | [Validating Tool Arguments](#validatingtoolarguments) | README.md |
| G-PI-README-010 | Table of Contents | [Complete Event Reference](#completeeventreference) | README.md |
| G-PI-README-011 | Table of Contents | [Image Input](#imageinput) | README.md |
| G-PI-README-012 | Table of Contents | [Thinking/Reasoning](#thinkingreasoning) | README.md |
| G-PI-README-013 | Table of Contents | [Unified Interface](#unifiedinterfacestreamsimplecompletesimple) | README.md |
| G-PI-README-014 | Table of Contents | [ProviderSpecific Options](#providerspecificoptionsstreamcomplete) | README.md |
| G-PI-README-015 | Table of Contents | [Streaming Thinking Content](#streamingthinkingcontent) | README.md |
| G-PI-README-016 | Table of Contents | [Stop Reasons](#stopreasons) | README.md |
| G-PI-README-017 | Table of Contents | [Error Handling](#errorhandling) | README.md |
| G-PI-README-018 | Table of Contents | [Aborting Requests](#abortingrequests) | README.md |
| G-PI-README-019 | Table of Contents | [Continuing After Abort](#continuingafterabort) | README.md |
| G-PI-README-020 | Table of Contents | [APIs, Models, and Providers](#apismodelsandproviders) | README.md |
| G-PI-README-021 | Table of Contents | [Providers and Models](#providersandmodels) | README.md |
| G-PI-README-022 | Table of Contents | [Querying Providers and Models](#queryingprovidersandmodels) | README.md |
| G-PI-README-023 | Table of Contents | [Custom Models](#custommodels) | README.md |
| G-PI-README-024 | Table of Contents | [OpenAI Compatibility Settings](#openaicompatibilitysettings) | README.md |
| G-PI-README-025 | Table of Contents | [Type Safety](#typesafety) | README.md |
| G-PI-README-026 | Table of Contents | [CrossProvider Handoffs](#crossproviderhandoffs) | README.md |
| G-PI-README-027 | Table of Contents | [Context Serialization](#contextserialization) | README.md |
| G-PI-README-028 | Table of Contents | [Browser Usage](#browserusage) | README.md |
| G-PI-README-029 | Table of Contents | [Browser Compatibility Notes](#browsercompatibilitynotes) | README.md |
| G-PI-README-030 | Table of Contents | [Environment Variables](#environmentvariablesnodejsonly) | README.md |
| G-PI-README-031 | Table of Contents | [Checking Environment Variables](#checkingenvironmentvariables) | README.md |
| G-PI-README-032 | Table of Contents | [OAuth Providers](#oauthproviders) | README.md |
| G-PI-README-033 | Table of Contents | [Vertex AI](#vertexai) | README.md |
| G-PI-README-034 | Table of Contents | [CLI Login](#clilogin) | README.md |
| G-PI-README-035 | Table of Contents | [Programmatic OAuth](#programmaticoauth) | README.md |
| G-PI-README-036 | Table of Contents | [Login Flow Example](#loginflowexample) | README.md |
| G-PI-README-037 | Table of Contents | [Using OAuth Tokens](#usingoauthtokens) | README.md |
| G-PI-README-038 | Table of Contents | [Provider Notes](#providernotes) | README.md |
| G-PI-README-039 | Table of Contents | [License](#license) | README.md |
| G-PI-README-040 | Supported Providers | OpenAI | README.md |
| G-PI-README-041 | Supported Providers | Azure OpenAI (Responses) | README.md |
| G-PI-README-042 | Supported Providers | OpenAI Codex (ChatGPT Plus/Pro subscription, requires OAuth, see below) | README.md |
| G-PI-README-043 | Supported Providers | DeepSeek | README.md |
| G-PI-README-044 | Supported Providers | Anthropic | README.md |
| G-PI-README-045 | Supported Providers | Google | README.md |
| G-PI-README-046 | Supported Providers | Vertex AI (Gemini via Vertex AI) | README.md |
| G-PI-README-047 | Supported Providers | Mistral | README.md |
| G-PI-README-048 | Supported Providers | Cerebras | README.md |
| G-PI-README-049 | Supported Providers | Cloudflare AI Gateway | README.md |
| G-PI-README-050 | Supported Providers | Cloudflare Workers AI | README.md |
| G-PI-README-051 | Supported Providers | OpenRouter | README.md |
| G-PI-README-052 | Supported Providers | Vercel AI Gateway | README.md |
| G-PI-README-053 | Supported Providers | MiniMax | README.md |
| G-PI-README-054 | Supported Providers | GitHub Copilot (requires OAuth, see below) | README.md |
| G-PI-README-055 | Supported Providers | Amazon Bedrock | README.md |
| G-PI-README-056 | Supported Providers | OpenCode Zen | README.md |
| G-PI-README-057 | Supported Providers | OpenCode Go | README.md |
| G-PI-README-058 | Supported Providers | Fireworks (uses Anthropiccompatible API) | README.md |
| G-PI-README-059 | Supported Providers | Kimi For Coding (Moonshot AI, uses Anthropiccompatible API) | README.md |
| G-PI-README-060 | Supported Providers | Xiaomi MiMo Token Plan (uses Anthropiccompatible API) | README.md |
| G-PI-README-061 | Supported Providers | Any OpenAIcompatible API: Ollama, vLLM, LM Studio, etc. | README.md |
| G-PI-README-062 | Streaming Tool Calls with Partial JSON | Important notes about partial tool arguments: | README.md |
| G-PI-README-063 | Streaming Tool Calls with Partial JSON | During `toolcall_delta` events, `arguments` contains the besteffort parse of partial JSON | README.md |
| G-PI-README-064 | Streaming Tool Calls with Partial JSON | Fields may be missing or incomplete  always check for existence before use | README.md |
| G-PI-README-065 | Streaming Tool Calls with Partial JSON | String values may be truncated midword | README.md |
| G-PI-README-066 | Streaming Tool Calls with Partial JSON | Arrays may be incomplete | README.md |
| G-PI-README-067 | Streaming Tool Calls with Partial JSON | Nested objects may be partially populated | README.md |
| G-PI-README-068 | Streaming Tool Calls with Partial JSON | At minimum, `arguments` will be an empty object `{}`, never `undefined` | README.md |
| G-PI-README-069 | Streaming Tool Calls with Partial JSON | The Google provider does not support function call streaming. Instead, you will receive a single `toolcall_delta` event with the full arguments. | README.md |
| G-PI-README-070 | Stop Reasons | `"stop"`  Normal completion, the model finished its response | README.md |
| G-PI-README-071 | Stop Reasons | `"length"`  Output hit the maximum token limit | README.md |
| G-PI-README-072 | Stop Reasons | `"toolUse"`  Model is calling tools and expects tool results | README.md |
| G-PI-README-073 | Stop Reasons | `"error"`  An error occurred during generation | README.md |
| G-PI-README-074 | Stop Reasons | `"aborted"`  Request was cancelled via abort signal | README.md |
| G-PI-README-075 | APIs, Models, and Providers | `anthropicmessages`: Anthropic Messages API (`streamAnthropic`, `AnthropicOptions`) | README.md |
| G-PI-README-076 | APIs, Models, and Providers | `googlegenerativeai`: Google Generative AI API (`streamGoogle`, `GoogleOptions`) | README.md |
| G-PI-README-077 | APIs, Models, and Providers | `googlevertex`: Google Vertex AI API (`streamGoogleVertex`, `GoogleVertexOptions`) | README.md |
| G-PI-README-078 | APIs, Models, and Providers | `mistralconversations`: Mistral Conversations API (`streamMistral`, `MistralOptions`) | README.md |
| G-PI-README-079 | APIs, Models, and Providers | `openaicompletions`: OpenAI Chat Completions API (`streamOpenAICompletions`, `OpenAICompletionsOptions`) | README.md |
| G-PI-README-080 | APIs, Models, and Providers | `openairesponses`: OpenAI Responses API (`streamOpenAIResponses`, `OpenAIResponsesOptions`) | README.md |
| G-PI-README-081 | APIs, Models, and Providers | `openaicodexresponses`: OpenAI Codex Responses API (`streamOpenAICodexResponses`, `OpenAICodexResponsesOptions`) | README.md |
| G-PI-README-082 | APIs, Models, and Providers | `azureopenairesponses`: Azure OpenAI Responses API (`streamAzureOpenAIResponses`, `AzureOpenAIResponsesOptions`) | README.md |
| G-PI-README-083 | APIs, Models, and Providers | `bedrockconversestream`: Amazon Bedrock Converse API (`streamBedrock`, `BedrockOptions`) | README.md |
| G-PI-README-084 | Faux provider for tests | Responses are consumed from a queue in request start order. | README.md |
| G-PI-README-085 | Faux provider for tests | If the queue is empty, the faux provider returns an assistant error message with `errorMessage: "No more faux responses queued"`. | README.md |
| G-PI-README-086 | Faux provider for tests | Use `registration.setResponses([...])` to replace the remaining queue and `registration.appendResponses([...])` to add more responses. | README.md |
| G-PI-README-087 | Faux provider for tests | `registration.models` exposes all registered faux models. `registration.getModel()` returns the first one, and `registration.getModel(id)` returns a specific one. | README.md |
| G-PI-README-088 | Faux provider for tests | Use `fauxAssistantMessage(...)` for scripted assistant replies. Use `fauxText(...)`, `fauxThinking(...)`, and `fauxToolCall(...)` to build content blocks without filling in lowlevel fields manually. | README.md |
| G-PI-README-089 | Faux provider for tests | `registration.unregister()` removes the temporary provider from the global API registry. | README.md |
| G-PI-README-090 | Faux provider for tests | Usage is estimated at roughly 1 token per 4 characters. When `sessionId` is present and `cacheRetention` is not `"none"`, prompt cache reads and writes are simulated automatically. | README.md |
| G-PI-README-091 | Faux provider for tests | Tool call arguments stream incrementally via `toolcall_delta` chunks. | README.md |
| G-PI-README-092 | Faux provider for tests | By default, each streamed chunk is emitted on its own microtask. Set `tokensPerSecond` to pace chunk delivery in real time. | README.md |
| G-PI-README-093 | Faux provider for tests | The intended use is one deterministic scripted flow per registration. If you need independent concurrent flows, register separate faux providers. | README.md |
| G-PI-README-094 | Providers and Models | Anthropic models use the `anthropicmessages` API | README.md |
| G-PI-README-095 | Providers and Models | Google models use the `googlegenerativeai` API | README.md |
| G-PI-README-096 | Providers and Models | OpenAI models use the `openairesponses` API | README.md |
| G-PI-README-097 | Providers and Models | Mistral models use the `mistralconversations` API | README.md |
| G-PI-README-098 | Providers and Models | xAI, Cerebras, Groq, etc. models use the `openaicompletions` API (OpenAIcompatible) | README.md |
| G-PI-README-099 | OpenAI Compatibility Settings | LiteLLM proxies: May not support `store` field | README.md |
| G-PI-README-100 | OpenAI Compatibility Settings | Custom inference servers: May use nonstandard field names | README.md |
| G-PI-README-101 | OpenAI Compatibility Settings | Selfhosted endpoints: May have different feature support | README.md |
| G-PI-README-102 | How It Works | User and tool result messages are passed through unchanged | README.md |
| G-PI-README-103 | How It Works | Assistant messages from the same provider/API are preserved asis | README.md |
| G-PI-README-104 | How It Works | Assistant messages from different providers have their thinking blocks converted to text with `<thinking>` tags | README.md |
| G-PI-README-105 | How It Works | Tool calls and regular text are preserved unchanged | README.md |
| G-PI-README-106 | Provider Compatibility | Text content | README.md |
| G-PI-README-107 | Provider Compatibility | Tool calls and tool results (including images in tool results) | README.md |
| G-PI-README-108 | Provider Compatibility | Thinking/reasoning blocks (transformed to tagged text for crossprovider compatibility) | README.md |
| G-PI-README-109 | Provider Compatibility | Aborted messages with partial content | README.md |
| G-PI-README-110 | Provider Compatibility | Start with a fast model for initial responses | README.md |
| G-PI-README-111 | Provider Compatibility | Switch to a more capable model for complex reasoning | README.md |
| G-PI-README-112 | Provider Compatibility | Use specialized models for specific tasks | README.md |
| G-PI-README-113 | Provider Compatibility | Maintain conversation continuity across provider outages | README.md |
| G-PI-README-114 | Browser Compatibility Notes | Amazon Bedrock (`bedrockconversestream`) is not supported in browser environments. | README.md |
| G-PI-README-115 | Browser Compatibility Notes | OAuth login flows are not supported in browser environments. Use the `@mariozechner/piai/oauth` entry point in Node.js. | README.md |
| G-PI-README-116 | Browser Compatibility Notes | In browser builds, Bedrock can still appear in model lists. Calls to Bedrock models fail at runtime. | README.md |
| G-PI-README-117 | Browser Compatibility Notes | Use a serverside proxy or backend service if you need Bedrock or OAuthbased auth from a web app. | README.md |
| G-PI-README-118 | OAuth Providers | Anthropic (Claude Pro/Max subscription) | README.md |
| G-PI-README-119 | OAuth Providers | OpenAI Codex (ChatGPT Plus/Pro subscription, access to GPT5.x Codex models) | README.md |
| G-PI-README-120 | OAuth Providers | GitHub Copilot (Copilot subscription) | README.md |
| G-PI-README-121 | Vertex AI | API key: Set `GOOGLE_CLOUD_API_KEY` or pass `apiKey` in the call options. | README.md |
| G-PI-README-122 | Vertex AI | Local development (ADC): Run `gcloud auth applicationdefault login` | README.md |
| G-PI-README-123 | Vertex AI | CI/Production (ADC): Set `GOOGLE_APPLICATION_CREDENTIALS` to point to a service account JSON key file | README.md |
| G-PI-README-124 | Provider Notes | OpenAI Codex: Requires a ChatGPT Plus or Pro subscription. Provides access to GPT5.x Codex models with extended context windows and reasoning capabilities. The library automatically handles sessionbased prompt caching when `sessionId` is provided in stream options. You can set `transport` in stream options to `"sse"`, `"websocket"`, or `"auto"` for Codex Responses transport selection. When using WebSocket with a `sessionId`, connections are reused per session and expire after 5 minutes of inactivity. | README.md |
| G-PI-README-125 | Provider Notes | Azure OpenAI (Responses): Uses the Responses API only. Set `AZURE_OPENAI_API_KEY` and either `AZURE_OPENAI_BASE_URL` or `AZURE_OPENAI_RESOURCE_NAME`. `AZURE_OPENAI_BASE_URL` supports both `https://<resource>.openai.azure.com` and `https://<resource>.cognitiveservices.azure.com`; root endpoints are normalized to `.../openai/v1` automatically. Use `AZURE_OPENAI_API_VERSION` (defaults to `v1`) to override the API version if needed. Deployment names are treated as model IDs by default, override with `azureDeploymentName` or `AZURE_OPENAI_DEPLOYMENT_NAME_MAP` using commaseparated `modelid=deployment` pairs (for example `gpt4omini=mydeployment,gpt4o=prod`). Legacy deploymentbased URLs are intentionally unsupported. | README.md |
| G-PI-README-126 | Provider Notes | GitHub Copilot: If you get "The requested model is not supported" error, enable the model manually in VS Code: open Copilot Chat, click the model selector, select the model (warning icon), and click "Enable". | README.md |
| G-PI-README-127 | 1. Core Types (`src/types.ts`) | Add the API identifier to `KnownApi` (for example `"bedrockconversestream"`) | README.md |
| G-PI-README-128 | 1. Core Types (`src/types.ts`) | Create an options interface extending `StreamOptions` (for example `BedrockOptions`) | README.md |
| G-PI-README-129 | 1. Core Types (`src/types.ts`) | Add the provider name to `KnownProvider` (for example `"amazonbedrock"`) | README.md |
| G-PI-README-130 | 2. Provider Implementation (`src/providers/`) | `stream<Provider>()` function returning `AssistantMessageEventStream` | README.md |
| G-PI-README-131 | 2. Provider Implementation (`src/providers/`) | `streamSimple<Provider>()` for `SimpleStreamOptions` mapping | README.md |
| G-PI-README-132 | 2. Provider Implementation (`src/providers/`) | Providerspecific options interface | README.md |
| G-PI-README-133 | 2. Provider Implementation (`src/providers/`) | Message conversion functions to transform `Context` to provider format | README.md |
| G-PI-README-134 | 2. Provider Implementation (`src/providers/`) | Tool conversion if the provider supports tools | README.md |
| G-PI-README-135 | 2. Provider Implementation (`src/providers/`) | Response parsing to emit standardized events (`text`, `tool_call`, `thinking`, `usage`, `stop`) | README.md |
| G-PI-README-136 | 3. API Registry Integration (`src/providers/register-builtins.ts`) | Register the API with `registerApiProvider()` | README.md |
| G-PI-README-137 | 3. API Registry Integration (`src/providers/register-builtins.ts`) | Add a package subpath export in `package.json` for the provider module (`./dist/providers/<provider>.js`) | README.md |
| G-PI-README-138 | 3. API Registry Integration (`src/providers/register-builtins.ts`) | Add lazy loader wrappers in `src/providers/registerbuiltins.ts`, do not statically import provider implementation modules there | README.md |
| G-PI-README-139 | 3. API Registry Integration (`src/providers/register-builtins.ts`) | Add any rootlevel `export type` reexports in `src/index.ts` that should remain available from `@mariozechner/piai` | README.md |
| G-PI-README-140 | 3. API Registry Integration (`src/providers/register-builtins.ts`) | Add credential detection in `envapikeys.ts` for the new provider | README.md |
| G-PI-README-141 | 3. API Registry Integration (`src/providers/register-builtins.ts`) | Ensure `streamSimple` handles auth lookup via `getEnvApiKey()` or providerspecific auth | README.md |
| G-PI-README-142 | 4. Model Generation (`scripts/generate-models.ts`) | Add logic to fetch and parse models from the provider's source (e.g., models.dev API) | README.md |
| G-PI-README-143 | 4. Model Generation (`scripts/generate-models.ts`) | Map provider model data to the standardized `Model` interface | README.md |
| G-PI-README-144 | 4. Model Generation (`scripts/generate-models.ts`) | Handle providerspecific quirks (pricing format, capability flags, model ID transformations) | README.md |
| G-PI-README-145 | 5. Tests (`test/`) | `stream.test.ts`  Basic streaming and tool use | README.md |
| G-PI-README-146 | 5. Tests (`test/`) | `tokens.test.ts`  Token usage reporting | README.md |
| G-PI-README-147 | 5. Tests (`test/`) | `abort.test.ts`  Request cancellation | README.md |
| G-PI-README-148 | 5. Tests (`test/`) | `empty.test.ts`  Empty message handling | README.md |
| G-PI-README-149 | 5. Tests (`test/`) | `contextoverflow.test.ts`  Context limit errors | README.md |
| G-PI-README-150 | 5. Tests (`test/`) | `imagelimits.test.ts`  Image support (if applicable) | README.md |
| G-PI-README-151 | 5. Tests (`test/`) | `unicodesurrogate.test.ts`  Unicode handling | README.md |
| G-PI-README-152 | 5. Tests (`test/`) | `toolcallwithoutresult.test.ts`  Orphaned tool calls | README.md |
| G-PI-README-153 | 5. Tests (`test/`) | `imagetoolresult.test.ts`  Images in tool results | README.md |
| G-PI-README-154 | 5. Tests (`test/`) | `totaltokens.test.ts`  Token counting accuracy | README.md |
| G-PI-README-155 | 5. Tests (`test/`) | `crossproviderhandoff.test.ts`  Crossprovider context replay | README.md |
| G-PI-README-156 | 6. Coding Agent Integration (`../coding-agent/`) | Add a default model ID for the provider in `DEFAULT_MODELS` | README.md |
| G-PI-README-157 | 6. Coding Agent Integration (`../coding-agent/`) | Add environment variable documentation in the help text | README.md |
| G-PI-README-158 | 6. Coding Agent Integration (`../coding-agent/`) | Add the provider to the providers section with setup instructions | README.md |
| G-PI-README-159 | 7. Documentation | Add to the Supported Providers table | README.md |
| G-PI-README-160 | 7. Documentation | Document any providerspecific options or authentication requirements | README.md |
| G-PI-README-161 | 7. Documentation | Add environment variable to the Environment Variables section | README.md |
| G-PI-README-162 | Added | Added support for [Provider Name] provider ([#PR](link) by [@author](link)) | README.md |
| G-PI-CHANGELOG-001 | New Features | Xiaomi MiMo Token Plan provider  New Anthropiccompatible provider with `XIAOMI_API_KEY` auth, default model (`mimov2.5pro`), and `/login` display. See [docs/providers.md](docs/providers.md). ([#4005](https://github.com/badlogic/pimono/pull/4005) by [@Phoen1xCode](https://github.com/Phoen1xCode)). | CHANGELOG.md |
| G-PI-CHANGELOG-002 | New Features | Model thinking level metadata  Models can now declare which thinking levels they support via `thinkingLevelMap`, replacing the old `reasoningEffortMap`. See [docs/models.md#thinkinglevelmap](docs/models.md#thinkinglevelmap) and [docs/customprovider.md](docs/customprovider.md). ([#3208](https://github.com/badlogic/pimono/issues/3208)). | CHANGELOG.md |
| G-PI-CHANGELOG-003 | New Features | Custom provider base URL overrides  `pi.registerProvider()` now respects permodel `baseUrl` settings. See [docs/customprovider.md](docs/customprovider.md). ([#4063](https://github.com/badlogic/pimono/issues/4063)). | CHANGELOG.md |
| G-PI-CHANGELOG-004 | New Features | Postturn stop callback  Agent loop can now exit gracefully after a completed turn via `shouldStopAfterTurn`. See [`packages/agent/README.md`](https://github.com/badlogic/pimono/blob/main/packages/agent/README.md). | CHANGELOG.md |
| G-PI-CHANGELOG-005 | New Features | Selfupdate detection fix  `pi` now correctly identifies and applies available updates. ([#3942](https://github.com/badlogic/pimono/issues/3942), [#3980](https://github.com/badlogic/pimono/issues/3980), [#3922](https://github.com/badlogic/pimono/issues/3922)). | CHANGELOG.md |
| G-PI-CHANGELOG-006 | Breaking Changes | Replaced `compat.reasoningEffortMap` in `models.json` and `pi.registerProvider()` model definitions with modellevel `thinkingLevelMap` ([#3208](https://github.com/badlogic/pimono/issues/3208)). Migration: move old mappings from `compat.reasoningEffortMap` to `thinkingLevelMap`. Use string values for providerspecific thinking values and `null` for unsupported pi levels that should be hidden and skipped by cycling. See `docs/models.md#thinkinglevelmap` and `docs/customprovider.md`. | CHANGELOG.md |
| G-PI-CHANGELOG-007 | Added | Added Xiaomi MiMo Token Plan provider support with `XIAOMI_API_KEY`, default model resolution, `/login` display support, and provider documentation ([#4005](https://github.com/badlogic/pimono/pull/4005) by [@Phoen1xCode](https://github.com/Phoen1xCode)). | CHANGELOG.md |
| G-PI-CHANGELOG-008 | Added | Added modellevel `thinkingLevelMap` support in `models.json` and `pi.registerProvider()`, allowing models to expose only the thinking levels they actually support ([#3208](https://github.com/badlogic/pimono/issues/3208)). | CHANGELOG.md |
| G-PI-CHANGELOG-009 | Added | Added `shouldStopAfterTurn` agent loop callback for postturn stop control, inherited from `@mariozechner/piagentcore`. See [`packages/agent/README.md`](https://github.com/badlogic/pimono/blob/main/packages/agent/README.md). | CHANGELOG.md |
| G-PI-CHANGELOG-010 | Fixed | Fixed `pi.registerProvider()` to honor permodel `baseUrl` overrides ([#4063](https://github.com/badlogic/pimono/issues/4063)). | CHANGELOG.md |
| G-PI-CHANGELOG-011 | Fixed | Fixed selfupdate detection so `pi` correctly identifies when a newer version is available and applies updates ([#3942](https://github.com/badlogic/pimono/issues/3942), [#3980](https://github.com/badlogic/pimono/issues/3980), [#3922](https://github.com/badlogic/pimono/issues/3922)). | CHANGELOG.md |
| G-PI-CHANGELOG-012 | Added | Added `websocketcached` to the transport setting options for the OpenAI Codex provider used with ChatGPT subscription auth. This keeps the same WebSocket open for a session and, after the first request, sends only the new conversation items instead of resending the full chat history when possible. | CHANGELOG.md |
| G-PI-CHANGELOG-013 | Breaking Changes | Removed builtin Google Gemini CLI and Google Antigravity support. Existing configurations using those providers must switch to another supported provider. | CHANGELOG.md |
| G-PI-CHANGELOG-014 | New Features | Cloudflare AI Gateway provider support with `CLOUDFLARE_API_KEY`/`CLOUDFLARE_ACCOUNT_ID`/`CLOUDFLARE_GATEWAY_ID`, default model resolution, and `/login` display. See [docs/providers.md#cloudflareaigateway](docs/providers.md#cloudflareaigateway). ([#3856](https://github.com/badlogic/pimono/pull/3856) by [@mchenco](https://github.com/mchenco)). | CHANGELOG.md |
| G-PI-CHANGELOG-015 | New Features | Moonshot AI provider support with `MOONSHOT_API_KEY`, default model resolution, and `/login` display. | CHANGELOG.md |
| G-PI-CHANGELOG-016 | New Features | Mistral Medium 3.5 builtin model support. See [docs/providers.md#apikeys](docs/providers.md#apikeys). ([#4009](https://github.com/badlogic/pimono/pull/4009) by [@technocidal](https://github.com/technocidal)). | CHANGELOG.md |
| G-PI-CHANGELOG-017 | New Features | Extension APIs can replace finalized `message_end` messages, wrap custom editor factories via `ctx.ui.getEditorComponent()`, and observe thinking level changes. See [docs/extensions.md#message_startmessage_updatemessage_end](docs/extensions.md#message_startmessage_updatemessage_end), [docs/extensions.md#widgetsstatusandfooter](docs/extensions.md#widgetsstatusandfooter), and [docs/extensions.md#thinking_level_select](docs/extensions.md#thinking_level_select). | CHANGELOG.md |
| G-PI-CHANGELOG-018 | New Features | `PI_CODING_AGENT_SESSION_DIR` configures session storage from the environment. See [docs/usage.md#environmentvariables](docs/usage.md#environmentvariables). | CHANGELOG.md |
| G-PI-CHANGELOG-019 | Added | Added Cloudflare AI Gateway as a builtin provider with `CLOUDFLARE_API_KEY`/`CLOUDFLARE_ACCOUNT_ID`/`CLOUDFLARE_GATEWAY_ID` setup, default model resolution, `/login` display support, and provider documentation ([#3856](https://github.com/badlogic/pimono/pull/3856) by [@mchenco](https://github.com/mchenco)). | CHANGELOG.md |
| G-PI-CHANGELOG-020 | Added | Added Moonshot AI as a builtin provider with `MOONSHOT_API_KEY` setup, default model resolution, and `/login` display support. | CHANGELOG.md |
| G-PI-CHANGELOG-021 | Added | Added Mistral Medium 3.5 builtin model support via `@mariozechner/piai` ([#4009](https://github.com/badlogic/pimono/pull/4009) by [@technocidal](https://github.com/technocidal)). | CHANGELOG.md |
| G-PI-CHANGELOG-022 | Added | Added routed OpenAIcompatible response model metadata in assistant messages, so providers such as OpenRouter can expose the concrete model used ([#3968](https://github.com/badlogic/pimono/pull/3968) by [@purrgrammer](https://github.com/purrgrammer)). | CHANGELOG.md |
| G-PI-CHANGELOG-023 | Added | Added `PI_CODING_AGENT_SESSION_DIR` as an environment equivalent to `sessiondir` ([#4027](https://github.com/badlogic/pimono/issues/4027)). | CHANGELOG.md |
| G-PI-CHANGELOG-024 | Added | Added `message_end` extension result support for replacing finalized messages, enabling extensions to override assistant usage cost ([#3982](https://github.com/badlogic/pimono/issues/3982)). | CHANGELOG.md |
| G-PI-CHANGELOG-025 | Added | Added toplevel `name` support to `pi.registerProvider()` so extensionregistered providers can show a friendly name in `/login` ([#3956](https://github.com/badlogic/pimono/issues/3956)). | CHANGELOG.md |
| G-PI-CHANGELOG-026 | Added | Added `ctx.ui.getEditorComponent()` so extensions can wrap the currently configured custom editor factory ([#3935](https://github.com/badlogic/pimono/issues/3935)). | CHANGELOG.md |
| G-PI-CHANGELOG-027 | Added | Added a `thinking_level_select` extension event for observing thinking level changes ([#3888](https://github.com/badlogic/pimono/issues/3888)). | CHANGELOG.md |
| G-PI-CHANGELOG-028 | Fixed | Fixed WSL clipboard image paste by passing the PowerShell save path directly instead of through a custom environment variable ([#2469](https://github.com/badlogic/pimono/issues/2469)). | CHANGELOG.md |
| G-PI-CHANGELOG-029 | Fixed | Fixed Google Vertex Gemini 3 tool call replay for unsigned tool calls ([#4032](https://github.com/badlogic/pimono/issues/4032)). | CHANGELOG.md |
| G-PI-CHANGELOG-030 | Fixed | Fixed blocked `edit` tool results rendering the rejection reason twice after interactive extension confirmation ([#3830](https://github.com/badlogic/pimono/issues/3830)). | CHANGELOG.md |
| G-PI-CHANGELOG-031 | Fixed | Fixed extensiontriggered thinking level changes refreshing the interactive editor border immediately ([#3888](https://github.com/badlogic/pimono/issues/3888)). | CHANGELOG.md |
| G-PI-CHANGELOG-032 | Fixed | Fixed the codingagent README See Also link to point at `@mariozechner/piagentcore` ([#4023](https://github.com/badlogic/pimono/issues/4023)). | CHANGELOG.md |
| G-PI-CHANGELOG-033 | Fixed | Fixed `grep` and `find` tool argument injection for flaglike search patterns ([#4018](https://github.com/badlogic/pimono/issues/4018)). | CHANGELOG.md |
| G-PI-CHANGELOG-034 | Fixed | Fixed PowerShell shell command output on Windows by only spawning detached processes on Unix ([#4013](https://github.com/badlogic/pimono/pull/4013) by [@picasso250](https://github.com/picasso250)). | CHANGELOG.md |
| G-PI-CHANGELOG-035 | Fixed | Fixed Bun package manager `node_modules` discovery when `npmCommand` is configured to use Bun ([#3998](https://github.com/badlogic/pimono/pull/3998) by [@thirtythreeforty](https://github.com/thirtythreeforty)). | CHANGELOG.md |
| G-PI-CHANGELOG-036 | Fixed | Fixed edit and editpreview access failures to report filesystem errors correctly ([#3955](https://github.com/badlogic/pimono/pull/3955) by [@rwachtler](https://github.com/rwachtler)). | CHANGELOG.md |
| G-PI-CHANGELOG-037 | Fixed | Fixed `ProcessTerminal` sizing to use `COLUMNS` and `LINES` before falling back to 80x24 ([#4004](https://github.com/badlogic/pimono/issues/4004)). | CHANGELOG.md |
| G-PI-CHANGELOG-038 | Fixed | Updated `@anthropicai/sdk` to clear GHSAp7fg763fg4gf audit findings ([#3992](https://github.com/badlogic/pimono/issues/3992)). | CHANGELOG.md |
| G-PI-CHANGELOG-039 | Fixed | Updated `@mariozechner/clipboard` to an attested release so package managers with trust policies do not reject installs ([#3946](https://github.com/badlogic/pimono/issues/3946)). | CHANGELOG.md |
| G-PI-CHANGELOG-040 | Fixed | Fixed project context discovery to load `AGENTS.MD` files in addition to `AGENTS.md` ([#3949](https://github.com/badlogic/pimono/issues/3949)). | CHANGELOG.md |
| G-PI-CHANGELOG-041 | Fixed | Fixed `/handoff` to use compacted session context instead of precompaction raw messages ([#3945](https://github.com/badlogic/pimono/issues/3945)). | CHANGELOG.md |
| G-PI-CHANGELOG-042 | Fixed | Fixed DeepSeek V4 Flash `xhigh` thinking support so requests map to DeepSeek's `max` reasoning effort ([#3944](https://github.com/badlogic/pimono/issues/3944)). | CHANGELOG.md |
| G-PI-CHANGELOG-043 | Fixed | Fixed Anthropic streams that end before `message_stop` to be treated as errors instead of successful partial responses ([#3936](https://github.com/badlogic/pimono/issues/3936)). | CHANGELOG.md |
| G-PI-CHANGELOG-044 | Fixed | Fixed generated OpenAIcompatible DeepSeek V4 reasoning compatibility outside the direct DeepSeek provider ([#3940](https://github.com/badlogic/pimono/issues/3940)). | CHANGELOG.md |
| G-PI-CHANGELOG-045 | Fixed | Fixed idle followup submission to clear the editor like normal message submission ([#3926](https://github.com/badlogic/pimono/issues/3926)). | CHANGELOG.md |
| G-PI-CHANGELOG-046 | Fixed | Fixed editor rendering artifacts for Thai Sara Am and Lao AM vowel characters ([#3904](https://github.com/badlogic/pimono/issues/3904)). | CHANGELOG.md |
| G-PI-CHANGELOG-047 | Fixed | Fixed DeepSeek V4 Flash and V4 Pro pricing metadata to match current official rates ([#3910](https://github.com/badlogic/pimono/issues/3910)). | CHANGELOG.md |
| G-PI-CHANGELOG-048 | Fixed | Updated the sandbox extension example lockfile to resolve the vulnerable `lodashes` transitive dependency ([#3901](https://github.com/badlogic/pimono/issues/3901)). | CHANGELOG.md |
| G-PI-CHANGELOG-049 | Fixed | Fixed DeepSeek prompt cache hits to be tracked from OpenAIcompatible usage responses ([#3880](https://github.com/badlogic/pimono/issues/3880)). | CHANGELOG.md |
| G-PI-CHANGELOG-050 | Removed | Removed the discontinued Qwen CLI OAuth custom provider extension example ([#3832](https://github.com/badlogic/pimono/pull/3832) by [@4h9fbZ](https://github.com/4h9fbZ)). | CHANGELOG.md |
| G-PI-CHANGELOG-051 | Removed | Removed Google Gemini CLI and Google Antigravity builtin login, default model, documentation, and example extension support. | CHANGELOG.md |
| G-PI-CHANGELOG-052 | New Features | Cloudflare Workers AI provider support with `CLOUDFLARE_API_KEY`/`CLOUDFLARE_ACCOUNT_ID` setup. See [docs/providers.md#apikeys](docs/providers.md#apikeys). ([#3851](https://github.com/badlogic/pimono/pull/3851) by [@mchenco](https://github.com/mchenco)) | CHANGELOG.md |
| G-PI-CHANGELOG-053 | New Features | Pi update checks now use `pi.dev` and identify Pi with a `pi/<version>` user agent. See [docs/packages.md](docs/packages.md). ([#3877](https://github.com/badlogic/pimono/pull/3877) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-054 | Added | Added Cloudflare Workers AI as a builtin provider with `CLOUDFLARE_API_KEY`/`CLOUDFLARE_ACCOUNT_ID` setup, default model resolution, `/login` support, and provider documentation ([#3851](https://github.com/badlogic/pimono/pull/3851) by [@mchenco](https://github.com/mchenco)). | CHANGELOG.md |
| G-PI-CHANGELOG-055 | Changed | Changed Pi version checks to identify Pi with a `pi/<version>` user agent ([#3877](https://github.com/badlogic/pimono/pull/3877) by [@mitsuhiko](https://github.com/mitsuhiko)). | CHANGELOG.md |
| G-PI-CHANGELOG-056 | Fixed | Fixed config selector scroll indicators to show item counts instead of line counts ([#3820](https://github.com/badlogic/pimono/pull/3820) by [@aliou](https://github.com/aliou)). | CHANGELOG.md |
| G-PI-CHANGELOG-057 | Fixed | Fixed exported HTML to escape embedded image data and session metadata, preventing crafted session content from injecting markup ([#3819](https://github.com/badlogic/pimono/pull/3819) by [@justinpbarnett](https://github.com/justinpbarnett), [#3883](https://github.com/badlogic/pimono/pull/3883) by [@justinpbarnett](https://github.com/justinpbarnett)). | CHANGELOG.md |
| G-PI-CHANGELOG-058 | Fixed | Fixed Bunbased package manager startup by locating global `node_modules` relative to Bun's install layout ([#3861](https://github.com/badlogic/pimono/pull/3861) by [@thirtythreeforty](https://github.com/thirtythreeforty)). | CHANGELOG.md |
| G-PI-CHANGELOG-059 | Fixed | Fixed Bedrock inference profile capability checks by normalizing profile ARNs to the underlying model name. | CHANGELOG.md |
| G-PI-CHANGELOG-060 | Fixed | Fixed file discovery to fall back to `fdfind` when `fd` is unavailable. | CHANGELOG.md |
| G-PI-CHANGELOG-061 | Fixed | Fixed `pi update` to skip selfupdate reinstalls when the installed version is already current ([#3853](https://github.com/badlogic/pimono/issues/3853)). | CHANGELOG.md |
| G-PI-CHANGELOG-062 | Fixed | Fixed Cloudflare Workers AI attribution headers to honor the install telemetry setting. | CHANGELOG.md |
| G-PI-CHANGELOG-063 | Fixed | Fixed `pi update self` detection and execution for Windows packagemanager shim installs, including symlinked global package roots, and print the manual fallback command when selfupdate fails ([#3857](https://github.com/badlogic/pimono/issues/3857)). | CHANGELOG.md |
| G-PI-CHANGELOG-064 | Fixed | Fixed HTML export preserving ANSIrenderer trailing padding as extra blank wrapped lines. | CHANGELOG.md |
| G-PI-CHANGELOG-065 | Fixed | Fixed packaged `pi` startup failing because the session selector imported a sourceonly utility path. | CHANGELOG.md |
| G-PI-CHANGELOG-066 | New Features | `pi update` can now update pi itself in addition to installed pi packages. See [docs/packages.md](docs/packages.md). ([#3680](https://github.com/badlogic/pimono/pull/3680) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-067 | New Features | Azure Cognitive Services endpoint support for Azure OpenAI Responses deployments. See [docs/providers.md#apikeys](docs/providers.md#apikeys). ([#3799](https://github.com/badlogic/pimono/pull/3799) by [@marcbloech](https://github.com/marcbloech)) | CHANGELOG.md |
| G-PI-CHANGELOG-068 | New Features | Suppressible Anthropic extrausage billing warning via `warnings.anthropicExtraUsage` in `/settings`. See [docs/settings.md](docs/settings.md). ([#3808](https://github.com/badlogic/pimono/issues/3808)) | CHANGELOG.md |
| G-PI-CHANGELOG-069 | New Features | Extensioncontrolled working row visibility via `ctx.ui.setWorkingVisible()`, allowing extensions to hide the builtin loader row and render custom working state. See [docs/extensions.md](docs/extensions.md) and [examples/extensions/borderstatuseditor.ts](examples/extensions/borderstatuseditor.ts). ([#3674](https://github.com/badlogic/pimono/issues/3674)) | CHANGELOG.md |
| G-PI-CHANGELOG-070 | Added | Added `pi update` support for updating pi itself in addition to installed pi packages ([#3680](https://github.com/badlogic/pimono/pull/3680) by [@mitsuhiko](https://github.com/mitsuhiko)). | CHANGELOG.md |
| G-PI-CHANGELOG-071 | Added | Added Azure Cognitive Services endpoint support for Azure OpenAI Responses base URLs ([#3799](https://github.com/badlogic/pimono/pull/3799) by [@marcbloech](https://github.com/marcbloech)). | CHANGELOG.md |
| G-PI-CHANGELOG-072 | Added | Added `warnings.anthropicExtraUsage` and a `/settings` warnings submenu to suppress the Anthropic extra usage billing warning ([#3808](https://github.com/badlogic/pimono/issues/3808)) | CHANGELOG.md |
| G-PI-CHANGELOG-073 | Added | Added `ctx.ui.setWorkingVisible()` so extensions can hide the builtin interactive working loader row without reserving layout space, plus a borderstatus editor example that moves working state into a custom editor border ([#3674](https://github.com/badlogic/pimono/issues/3674)) | CHANGELOG.md |
| G-PI-CHANGELOG-074 | Fixed | Fixed duplicate printable characters from Kitty keyboard protocol CSIu plus raw character input on layouts such as Italian ([#3780](https://github.com/badlogic/pimono/issues/3780)). | CHANGELOG.md |
| G-PI-CHANGELOG-075 | Fixed | Fixed APIkey environment discovery and Bun startup to fall back to `/proc/self/environ` when Bun's sandbox leaves `process.env` empty ([#3801](https://github.com/badlogic/pimono/pull/3801) by [@mdsjip](https://github.com/mdsjip)). | CHANGELOG.md |
| G-PI-CHANGELOG-076 | Fixed | Fixed Bun sandboxed packagemanager commands when `process.env` is empty ([#3807](https://github.com/badlogic/pimono/pull/3807) by [@mdsjip](https://github.com/mdsjip)). | CHANGELOG.md |
| G-PI-CHANGELOG-077 | Fixed | Fixed symlinked packages, resources, skills, and sessions being duplicated in selectors and loaders ([#3818](https://github.com/badlogic/pimono/pull/3818) by [@aliou](https://github.com/aliou)). | CHANGELOG.md |
| G-PI-CHANGELOG-078 | Fixed | Fixed Bedrock promptcaching and adaptivethinking capability checks for inference profile ARNs ([#3527](https://github.com/badlogic/pimono/pull/3527) by [@anirudhmarc](https://github.com/anirudhmarc)). | CHANGELOG.md |
| G-PI-CHANGELOG-079 | Fixed | Fixed OpenAI Codex Responses default verbosity to `low` when no verbosity is specified. | CHANGELOG.md |
| G-PI-CHANGELOG-080 | Fixed | Stopped sending empty `tools` arrays to providers that reject them when tools are disabled ([#3650](https://github.com/badlogic/pimono/pull/3650) by [@HQidea](https://github.com/HQidea)). | CHANGELOG.md |
| G-PI-CHANGELOG-081 | Fixed | Fixed Anthropic SSE parsing to ignore unknown proxy events such as OpenAIstyle `done` terminators ([#3708](https://github.com/badlogic/pimono/issues/3708)). | CHANGELOG.md |
| G-PI-CHANGELOG-082 | Fixed | Fixed provider registration with overrideonly `models.json` entries to preserve builtin model lists ([#3651](https://github.com/badlogic/pimono/issues/3651)). | CHANGELOG.md |
| G-PI-CHANGELOG-083 | Fixed | Fixed `/login` to show auth supplied by `models.json` provider definitions. | CHANGELOG.md |
| G-PI-CHANGELOG-084 | Fixed | Fixed HTML export whitespace around extensionrendered tool output and expandable output hints. | CHANGELOG.md |
| G-PI-CHANGELOG-085 | Fixed | Fixed bash executor temp output streams leaking file descriptors when output was truncated by line count ([#3786](https://github.com/badlogic/pimono/issues/3786)) | CHANGELOG.md |
| G-PI-CHANGELOG-086 | Fixed | Fixed extension `pi.setSessionName()` updates to refresh the interactive terminal title immediately ([#3686](https://github.com/badlogic/pimono/issues/3686)) | CHANGELOG.md |
| G-PI-CHANGELOG-087 | Fixed | Fixed `/tree` cancellation via `session_before_tree` leaving the session stuck in compaction state ([#3688](https://github.com/badlogic/pimono/issues/3688)) | CHANGELOG.md |
| G-PI-CHANGELOG-088 | Fixed | Fixed Escape interrupt handling when extensions hide the builtin working loader row ([#3674](https://github.com/badlogic/pimono/issues/3674)) | CHANGELOG.md |
| G-PI-CHANGELOG-089 | Fixed | Fixed codingagent test expectations for current default models and missingauth guidance. | CHANGELOG.md |
| G-PI-CHANGELOG-090 | Fixed | Fixed long localLLM SSE streams aborting at 5 minutes with `UND_ERR_BODY_TIMEOUT` by disabling undici `bodyTimeout`/`headersTimeout` on the global dispatcher; provider SDKs continue to enforce their own deadlines via `retry.provider.timeoutMs` ([#3715](https://github.com/badlogic/pimono/issues/3715)) | CHANGELOG.md |
| G-PI-CHANGELOG-091 | Fixed | Fixed provider retry/timeout forwarding to omit undefined provider request controls, avoiding downstream SDK validation errors such as `timeout must be an integer` when `retry.provider.timeoutMs` is not configured ([#3627](https://github.com/badlogic/pimono/issues/3627)) | CHANGELOG.md |
| G-PI-CHANGELOG-092 | New Features | DeepSeek provider support with V4 Flash/Pro models and `DEEPSEEK_API_KEY` authentication. See [README.md#providersmodels](README.md#providersmodels) and [docs/providers.md#apikeys](docs/providers.md#apikeys). | CHANGELOG.md |
| G-PI-CHANGELOG-093 | New Features | Provider request timeout/retry controls via `retry.provider.{timeoutMs,maxRetries,maxRetryDelayMs}`, useful for longrunning local inference and provider SDK retry behavior. See [docs/settings.md#retry](docs/settings.md#retry). ([#3627](https://github.com/badlogic/pimono/issues/3627)) | CHANGELOG.md |
| G-PI-CHANGELOG-094 | Added | Added DeepSeek to builtin provider setup, default model resolution, and provider documentation. | CHANGELOG.md |
| G-PI-CHANGELOG-095 | Fixed | Fixed `/copy` to avoid unbounded OSC 52 writes and clipboard races that could break terminal rendering or panic the native clipboard addon ([#3639](https://github.com/badlogic/pimono/issues/3639)) | CHANGELOG.md |
| G-PI-CHANGELOG-096 | Fixed | Fixed extension flag docs to show `pi.getFlag()` using registered flag names without the CLI `` prefix ([#3614](https://github.com/badlogic/pimono/issues/3614)) | CHANGELOG.md |
| G-PI-CHANGELOG-097 | Fixed | Fixed provider retry/timeout settings wiring by adding `retry.provider.{timeoutMs,maxRetries,maxRetryDelayMs}`, migrating legacy `retry.maxDelayMs`, and forwarding provider controls into `streamSimple` request options ([#3627](https://github.com/badlogic/pimono/issues/3627)) | CHANGELOG.md |
| G-PI-CHANGELOG-098 | Fixed | Fixed Windows git package installs to bypass `cmd.exe` for native git commands, so install paths containing spaces no longer break `pi install git:...` with `fatal: Too many arguments` ([#3642](https://github.com/badlogic/pimono/issues/3642)) | CHANGELOG.md |
| G-PI-CHANGELOG-099 | Fixed | Fixed DeepSeek V4 session replay 400 errors by sending DeepSeekcompatible thinking controls and replayed assistant `reasoning_content` fields ([#3636](https://github.com/badlogic/pimono/issues/3636)) | CHANGELOG.md |
| G-PI-CHANGELOG-100 | Fixed | Fixed GPT5.5 generated context window metadata to use the observed 272k limit. | CHANGELOG.md |
| G-PI-CHANGELOG-101 | Fixed | Fixed CSIu Ctrl+letter decoding inside bracketed paste, so pasted modifiedkey escape sequences no longer become literal editor text ([#3623](https://github.com/badlogic/pimono/pull/3623) by [@Exrun94](https://github.com/Exrun94)) | CHANGELOG.md |
| G-PI-CHANGELOG-102 | New Features | Searchable auth provider login flow: the `/login` provider selector now supports fuzzy search/filtering, making it faster to find providers when many are configured. See [docs/providers.md](docs/providers.md). ([#3572](https://github.com/badlogic/pimono/pull/3572) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-103 | New Features | GPT5.5 Codex support: `openaicodex/gpt5.5` is available as a model option, including `xhigh` reasoning support and corrected prioritytier pricing. | CHANGELOG.md |
| G-PI-CHANGELOG-104 | New Features | Terminal progress indicators are now optin: OSC 9;4 progress reporting during streaming/compaction is off by default and can be toggled via `terminal.showTerminalProgress` in `/settings` ([#3588](https://github.com/badlogic/pimono/issues/3588)) | CHANGELOG.md |
| G-PI-CHANGELOG-105 | New Features | `nobuiltintools` / `createAgentSession({ noTools: "builtin" })` now correctly disables only builtin tools while keeping extension tools active. See [docs/extensions.md](docs/extensions.md) and [README.md](README.md) ([#3592](https://github.com/badlogic/pimono/issues/3592)) | CHANGELOG.md |
| G-PI-CHANGELOG-106 | Breaking Changes | Disabled OSC 9;4 terminal progress indicators by default. Set `terminal.showTerminalProgress` to `true` in `/settings` to reenable ([#3588](https://github.com/badlogic/pimono/issues/3588)) | CHANGELOG.md |
| G-PI-CHANGELOG-107 | Added | Added searchable auth provider login flow with fuzzy filtering in the provider selector ([#3572](https://github.com/badlogic/pimono/pull/3572) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-108 | Added | Added GPT5.5 Codex model | CHANGELOG.md |
| G-PI-CHANGELOG-109 | Added | Added auth source labels in `/login` so provider entries can show when auth comes from `apikey`, an environment variable, or custom provider fallback without exposing secrets. | CHANGELOG.md |
| G-PI-CHANGELOG-110 | Changed | Updated default model selection across providers to current recommended models. | CHANGELOG.md |
| G-PI-CHANGELOG-111 | Changed | Improved stale extension context errors after session replacement or reload to tell extension authors to avoid captured `pi`/command `ctx` and use `withSession` for postreplacement work. | CHANGELOG.md |
| G-PI-CHANGELOG-112 | Fixed | Fixed `/model` selector cancellation to request render instead of incorrectly triggering login selector. | CHANGELOG.md |
| G-PI-CHANGELOG-113 | Fixed | Changed login, OAuth, and extension selectors for more consistent styling. | CHANGELOG.md |
| G-PI-CHANGELOG-114 | Fixed | Added Amazon Bedrock setup guidance to `/login` and updated `/model` copy to refer to configured providers instead of only API keys. | CHANGELOG.md |
| G-PI-CHANGELOG-115 | Fixed | Improved nomodel and missingauth warnings to point users to `/login` for OAuth or API key setup. | CHANGELOG.md |
| G-PI-CHANGELOG-116 | Fixed | Fixed `/quit` shutdown ordering to stop the TUI before extension UI teardown can repaint, preserving the final rendered frame while still emitting `session_shutdown` before process exit. | CHANGELOG.md |
| G-PI-CHANGELOG-117 | Fixed | Fixed `SettingsManager.inMemory()` initial settings being lost after reloads triggered by SDK resource loading ([#3616](https://github.com/badlogic/pimono/issues/3616)) | CHANGELOG.md |
| G-PI-CHANGELOG-118 | Fixed | Fixed `models.json` provider compatibility to accept `compat.supportsLongCacheRetention`, allowing proxies to opt out of longretention cache fields when needed while long retention is enabled by default when requested ([#3543](https://github.com/badlogic/pimono/issues/3543)) | CHANGELOG.md |
| G-PI-CHANGELOG-119 | Fixed | Fixed `thinking xhigh` for `openaicodex` `gpt5.5` so it is no longer downgraded to `high`. | CHANGELOG.md |
| G-PI-CHANGELOG-120 | Fixed | Fixed git package installs with custom `npmCommand` values such as `pnpm` by avoiding npmspecific production flags in that compatibility path ([#3604](https://github.com/badlogic/pimono/issues/3604)) | CHANGELOG.md |
| G-PI-CHANGELOG-121 | Fixed | Fixed first user messages rendering without spacing after existing notices such as compaction summaries or status messages ([#3613](https://github.com/badlogic/pimono/issues/3613)) | CHANGELOG.md |
| G-PI-CHANGELOG-122 | Fixed | Fixed the handoff extension example to use the replacementsession context after creating a new session, avoiding stale `ctx` errors when it installs the generated prompt ([#3606](https://github.com/badlogic/pimono/issues/3606)) | CHANGELOG.md |
| G-PI-CHANGELOG-123 | Fixed | Fixed session replacement and `/quit` teardown ordering to run hostowned extension UI cleanup synchronously after `session_shutdown` handlers complete but before invalidating the old extension context, preventing stale extension UI from rendering against a disposed session ([#3597](https://github.com/badlogic/pimono/pull/3597) by [@vegarsti](https://github.com/vegarsti)) | CHANGELOG.md |
| G-PI-CHANGELOG-124 | Fixed | Fixed crash on `/quit` when an extension registers a custom footer whose `render()` accesses `ctx`, by tearing down extensionprovided UI before invalidating the extension runner during shutdown ([#3595](https://github.com/badlogic/pimono/issues/3595)) | CHANGELOG.md |
| G-PI-CHANGELOG-125 | Fixed | Fixed autoretry to treat Bedrock/Smithy HTTP/2 transport failures like `http2 request did not get a response` as transient errors, so the agent retries automatically instead of waiting for a manual nudge ([#3594](https://github.com/badlogic/pimono/issues/3594)) | CHANGELOG.md |
| G-PI-CHANGELOG-126 | Fixed | Fixed the CLI/SDK toolselection split so `nobuiltintools` and `createAgentSession({ noTools: "builtin" })` disable only builtin default tools while keeping extension/custom tools enabled, instead of falling through to the same "disable everything" path as `notools` ([#3592](https://github.com/badlogic/pimono/issues/3592)) | CHANGELOG.md |
| G-PI-CHANGELOG-127 | Fixed | Fixed remaining hardcoded `pi` / `.pi` branding to route through `APP_NAME` and `CONFIG_DIR_NAME` extension points, so SDK rebrands get consistent naming in `/quit` description, `process.title`, and the projectlocal extensions directory ([#3583](https://github.com/badlogic/pimono/pull/3583) by [@jlaneve](https://github.com/jlaneve)) | CHANGELOG.md |
| G-PI-CHANGELOG-128 | Fixed | Fixed `picodingagent` shipping `uuid@11`, which triggered `npm audit` moderate vulnerability reports for downstream installs; the package now depends on `uuid@14` ([#3577](https://github.com/badlogic/pimono/issues/3577)) | CHANGELOG.md |
| G-PI-CHANGELOG-129 | Fixed | Fixed `openaicompletions` streamed toolcall assembly to coalesce deltas by stable tool index when OpenAIcompatible gateways mutate tool call IDs midstream, preventing malformed Kimi K2.6/OpenCode tool streams from splitting one call into multiple bogus tool calls ([#3576](https://github.com/badlogic/pimono/issues/3576)) | CHANGELOG.md |
| G-PI-CHANGELOG-130 | Fixed | Fixed `ctx.ui.setWorkingMessage()` to persist across loader recreation, matching the behavior of `ctx.ui.setWorkingIndicator()` ([#3566](https://github.com/badlogic/pimono/issues/3566)) | CHANGELOG.md |
| G-PI-CHANGELOG-131 | Fixed | Fixed codingagent `fs.watch` error handling for theme and gitfooter watchers to retry after transient watcher failures such as `EMFILE`, avoiding startup crashes in large repos ([#3564](https://github.com/badlogic/pimono/issues/3564)) | CHANGELOG.md |
| G-PI-CHANGELOG-132 | Fixed | Fixed builtin `kimicoding` model generation to attach the expected `UserAgent` header so direct Kimi Coding requests use the provider's expected client identity ([#3586](https://github.com/badlogic/pimono/issues/3586)) | CHANGELOG.md |
| G-PI-CHANGELOG-133 | Fixed | Fixed extension shortcut conflict diagnostics to display at startup instead of only on reload, so extension authors discover reserved keybinding conflicts immediately rather than discovering them later through user feedback ([#3617](https://github.com/badlogic/pimono/issues/3617)) | CHANGELOG.md |
| G-PI-CHANGELOG-134 | Fixed | Fixed `models.json` Anthropiccompatible provider configuration to accept `compat.supportsEagerToolInputStreaming`, allowing proxies that reject pertool `eager_input_streaming` to use the legacy finegrained tool streaming beta header instead ([#3575](https://github.com/badlogic/pimono/issues/3575)) | CHANGELOG.md |
| G-PI-CHANGELOG-135 | Fixed | Fixed startup banner extension labels to strip trailing `index.js`/`index.ts` suffixes ([#3596](https://github.com/badlogic/pimono/pull/3596) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-136 | Fixed | Fixed OSC 9;4 terminal progress updates to stay alive in terminals such as Ghostty during longrunning agent work ([#3610](https://github.com/badlogic/pimono/issues/3610)) | CHANGELOG.md |
| G-PI-CHANGELOG-137 | Fixed | Fixed OpenAIcompatible completion usage parsing to avoid doublecounting reasoning tokens already included in `completion_tokens` ([#3581](https://github.com/badlogic/pimono/issues/3581)) | CHANGELOG.md |
| G-PI-CHANGELOG-138 | Fixed | Fixed `openairesponses` compatibility for strict OpenAIcompatible proxies by allowing `models.json` to disable the underscorecontaining `session_id` header with `compat.sendSessionIdHeader: false` ([#3579](https://github.com/badlogic/pimono/issues/3579)) | CHANGELOG.md |
| G-PI-CHANGELOG-139 | Fixed | Fixed GPT5.5 Codex capability handling to clamp unsupported minimal reasoning to `low` and apply the model's 2.5x priority servicetier pricing multiplier ([#3618](https://github.com/badlogic/pimono/pull/3618) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-140 | New Features | TypeBox 1.x migration for extensions and SDK integrations, including TypeBoxnative tool argument validation that now works in evalrestricted runtimes such as Cloudflare Workers. See [docs/extensions.md](docs/extensions.md) and [docs/sdk.md](docs/sdk.md). | CHANGELOG.md |
| G-PI-CHANGELOG-141 | New Features | Stacked extension autocomplete providers via `ctx.ui.addAutocompleteProvider(...)`, allowing extensions to layer custom completion logic on top of builtin slash and path completion. See [docs/extensions.md#autocompleteproviders](docs/extensions.md#autocompleteproviders) and [examples/extensions/githubissueautocomplete.ts](examples/extensions/githubissueautocomplete.ts). | CHANGELOG.md |
| G-PI-CHANGELOG-142 | New Features | Terminating tool results via `terminate: true`, allowing custom tools to end on a final tool call without paying for an automatic followup LLM turn. See [docs/extensions.md](docs/extensions.md) and [examples/extensions/structuredoutput.ts](examples/extensions/structuredoutput.ts). | CHANGELOG.md |
| G-PI-CHANGELOG-143 | New Features | OSC 9;4 terminal progress indicators during agent streaming and compaction for supporting terminals. | CHANGELOG.md |
| G-PI-CHANGELOG-144 | Breaking Changes | Migrated firstparty codingagent code, SDK/examples/docs, and package metadata from `@sinclair/typebox` 0.34.x to `typebox` 1.x. New extensions, SDK integrations, and pi packages should depend on and import from `typebox`. Legacy extension loading still aliases the root `@sinclair/typebox` package, but `@sinclair/typebox/compiler` is no longer shimmed. This migration also picks up the new `@mariozechner/piai` TypeBoxnative validator path, so tool argument validation now works in evalrestricted runtimes such as Cloudflare Workers instead of being skipped ([#3112](https://github.com/badlogic/pimono/issues/3112)) | CHANGELOG.md |
| G-PI-CHANGELOG-145 | Breaking Changes | Sessionreplacement commands now invalidate captured prereplacement sessionbound extension objects after `ctx.newSession()`, `ctx.fork()`, and `ctx.switchSession()`. Old `pi` and command `ctx` references now throw instead of silently targeting the replaced session. Migration: if code needs to keep working in the replacement session after one of those calls, pass `withSession` to that same method and do the postswitch work there. In practice, move postswitch `pi.sendUserMessage()`, `pi.sendMessage()`, and commandctx/sessionmanager access into `withSession`, and use only the `ReplacedSessionContext` passed to that callback for sessionbound operations. Footguns: `withSession` runs after the old extension instance has already received `session_shutdown`, old cleanup may already have invalidated captured state, captured old `pi` / old command `ctx` are stale, and previously extracted raw objects such as `const sm = ctx.sessionManager` remain the caller's responsibility and must not be reused after the switch. | CHANGELOG.md |
| G-PI-CHANGELOG-146 | Added | Added support for terminating tool results via `terminate: true`, allowing custom tools to end the current tool batch without an automatic followup LLM call, plus a `structuredoutput.ts` extension example and extension docs showing the pattern ([#3525](https://github.com/badlogic/pimono/issues/3525)) | CHANGELOG.md |
| G-PI-CHANGELOG-147 | Added | Added OSC 9;4 terminal progress indicators during agent streaming and compaction, so terminals like iTerm2, WezTerm, Windows Terminal, and Kitty show activity in their tab bar | CHANGELOG.md |
| G-PI-CHANGELOG-148 | Added | Added `ctx.ui.addAutocompleteProvider(...)` for stacking extension autocomplete providers on top of the builtin slash/path provider, plus a `githubissueautocomplete.ts` example and extension docs ([#2983](https://github.com/badlogic/pimono/issues/2983)) | CHANGELOG.md |
| G-PI-CHANGELOG-149 | Fixed | Fixed exported session HTML to sanitize markdown link URLs before rendering them into anchor tags, blocking `javascript:`style payloads while preserving safe links in shared/exported sessions ([#3532](https://github.com/badlogic/pimono/issues/3532)) | CHANGELOG.md |
| G-PI-CHANGELOG-150 | Fixed | Fixed `ctx.getSystemPrompt()` inside `before_agent_start` to reflect chained systemprompt changes made by earlier `before_agent_start` handlers, and clarified the extension docs around providerpayload rewrites and what `ctx.getSystemPrompt()` does and does not report ([#3539](https://github.com/badlogic/pimono/issues/3539)) | CHANGELOG.md |
| G-PI-CHANGELOG-151 | Fixed | Fixed builtin `googlegeminicli` model lists and selector entries to include `gemini3.1flashlitepreview`, so Cloud Code Assist users no longer need manual `model` fallback selection to use it ([#3545](https://github.com/badlogic/pimono/issues/3545)) | CHANGELOG.md |
| G-PI-CHANGELOG-152 | Fixed | Fixed extension sessionreplacement flows so `ctx.newSession()`, `ctx.fork()`, `ctx.switchSession()`, and importedsession replacements fully rebind before postswitch work runs, added `withSession` replacement callbacks with fresh `ReplacedSessionContext` helpers, and make stale prereplacement `pi` / `ctx` sessionbound accesses throw instead of silently targeting the wrong session ([#2860](https://github.com/badlogic/pimono/issues/2860)) | CHANGELOG.md |
| G-PI-CHANGELOG-153 | Fixed | Fixed `models.json` builtin provider overrides to accept `headers` without requiring `baseUrl`, so requestheaderonly overrides now load and apply correctly ([#3538](https://github.com/badlogic/pimono/issues/3538)) | CHANGELOG.md |
| G-PI-CHANGELOG-154 | New Features | Fireworks provider support with builtin models and `FIREWORKS_API_KEY` auth. See [README.md#providersmodels](README.md#providersmodels) and [docs/providers.md](docs/providers.md). | CHANGELOG.md |
| G-PI-CHANGELOG-155 | New Features | Configurable inline tool image width via `terminal.imageWidthCells` in `/settings`. See [docs/settings.md#terminalimages](docs/settings.md#terminalimages). | CHANGELOG.md |
| G-PI-CHANGELOG-156 | Added | Added builtin Fireworks provider support, including `FIREWORKS_API_KEY` setup/docs and the default Fireworks model `accounts/fireworks/models/kimik2p6` ([#3519](https://github.com/badlogic/pimono/issues/3519)) | CHANGELOG.md |
| G-PI-CHANGELOG-157 | Fixed | Fixed interactive inline tool images to honor configurable `terminal.imageWidthCells` via `/settings`, so tooloutput images are no longer hardcapped to 60 terminal cells ([#3508](https://github.com/badlogic/pimono/issues/3508)) | CHANGELOG.md |
| G-PI-CHANGELOG-158 | Fixed | Fixed `sessionDir` in `settings.json` to expand `~`, so portable sessiondirectory settings no longer require a shell wrapper ([#3514](https://github.com/badlogic/pimono/issues/3514)) | CHANGELOG.md |
| G-PI-CHANGELOG-159 | Fixed | Fixed parallel toolcall rows to leave the pending state as soon as each tool is finalized, while still appending persisted tool results in assistant source order ([#3503](https://github.com/badlogic/pimono/issues/3503)) | CHANGELOG.md |
| G-PI-CHANGELOG-160 | Fixed | Fixed exported session markdown to render Markdown while showing HTMLlike message content such as `<file name="...">...</file>` verbatim, so shared sessions match the TUI instead of letting the browser interpret message text ([#3484](https://github.com/badlogic/pimono/issues/3484)) | CHANGELOG.md |
| G-PI-CHANGELOG-161 | Fixed | Fixed exported session HTML to render `grep` and `find` output through their existing TUI renderers and `ls` output through a native template renderer, avoiding missing formatting and spacing artifacts in shared sessions ([#3491](https://github.com/badlogic/pimono/pull/3491) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-162 | Fixed | Fixed `@` autocomplete fuzzy search to follow symlinked directories and include symlinked paths in results ([#3507](https://github.com/badlogic/pimono/issues/3507)) | CHANGELOG.md |
| G-PI-CHANGELOG-163 | Fixed | Fixed proxied agent streams to preserve the proxysafe serializable subset of stream options, including session, transport, retrydelay, metadata, header, cacheretention, and thinkingbudget settings ([#3512](https://github.com/badlogic/pimono/issues/3512)) | CHANGELOG.md |
| G-PI-CHANGELOG-164 | Fixed | Hardened Anthropic streaming against malformed toolcall JSON by owning SSE parsing with defensive JSON repair, replacing the deprecated `finegrainedtoolstreaming` beta header with pertool `eager_input_streaming`, and updating stale test model references ([#3175](https://github.com/badlogic/pimono/issues/3175)) | CHANGELOG.md |
| G-PI-CHANGELOG-165 | Fixed | Fixed Bedrock runtime endpoint resolution to stop pinning builtin regional endpoints over `AWS_REGION` / `AWS_PROFILE`, restoring `us.` and `eu.` inference profile support after v0.68.0 while preserving custom VPC/proxy endpoint overrides ([#3481](https://github.com/badlogic/pimono/issues/3481), [#3485](https://github.com/badlogic/pimono/issues/3485), [#3486](https://github.com/badlogic/pimono/issues/3486), [#3487](https://github.com/badlogic/pimono/issues/3487), [#3488](https://github.com/badlogic/pimono/issues/3488)) | CHANGELOG.md |
| G-PI-CHANGELOG-166 | New Features | Configurable streaming working indicator for extensions via `ctx.ui.setWorkingIndicator()`, including animated, static, and hidden indicators. See [docs/tui.md#workingindicator](docs/tui.md#workingindicator), [docs/extensions.md](docs/extensions.md), and [examples/extensions/workingindicator.ts](examples/extensions/workingindicator.ts). | CHANGELOG.md |
| G-PI-CHANGELOG-167 | New Features | `before_agent_start` now exposes `systemPromptOptions` (`BuildSystemPromptOptions`) so extensions can inspect the structured systemprompt inputs without rediscovering resources. See [docs/extensions.md#before_agent_start](docs/extensions.md#before_agent_start) and [examples/extensions/promptcustomizer.ts](examples/extensions/promptcustomizer.ts). | CHANGELOG.md |
| G-PI-CHANGELOG-168 | New Features | Configurable keybindings for scoped model selector actions and sessiontree filter actions. See [docs/keybindings.md](docs/keybindings.md). | CHANGELOG.md |
| G-PI-CHANGELOG-169 | New Features | `/clone` duplicates the current active branch into a new session, while extensions can choose whether to fork `before` or `at` an entry via `ctx.fork(..., { position })`. See [README.md](README.md), [docs/extensions.md](docs/extensions.md), and [docs/session.md](docs/session.md). | CHANGELOG.md |
| G-PI-CHANGELOG-170 | Breaking Changes | Changed SDK and CLI tool selection from cwdbound builtin tool instances to toolname allowlists. `createAgentSession({ tools })` now expects `string[]` names such as `"read"` and `"bash"` instead of `Tool[]`, `tools` now allowlists builtin, extension, and custom tools by name, and `notools` now disables all tools by default rather than only builtins. Migrate SDK code from `tools: [readTool, bashTool]` to `tools: ["read", "bash"]` ([#2835](https://github.com/badlogic/pimono/issues/2835), [#3452](https://github.com/badlogic/pimono/issues/3452)) | CHANGELOG.md |
| G-PI-CHANGELOG-171 | Breaking Changes | Removed prebuilt cwdbound tool and tooldefinition exports from `@mariozechner/picodingagent`, including `readTool`, `bashTool`, `editTool`, `writeTool`, `grepTool`, `findTool`, `lsTool`, `readOnlyTools`, `codingTools`, and the corresponding `ToolDefinition` values. Use the explicit factory exports instead, for example `createReadTool(cwd)`, `createBashTool(cwd)`, `createCodingTools(cwd)`, and `createReadToolDefinition(cwd)` ([#3452](https://github.com/badlogic/pimono/issues/3452)) | CHANGELOG.md |
| G-PI-CHANGELOG-172 | Breaking Changes | Removed ambient `process.cwd()` / default agentdir fallback behavior from public resource helpers. `DefaultResourceLoader`, `loadProjectContextFiles()`, and `loadSkills()` now require explicit cwd/agentdir style inputs, and exported systemprompt option types now require an explicit `cwd`. Pass the session or project cwd explicitly instead of relying on processglobal defaults ([#3452](https://github.com/badlogic/pimono/issues/3452)) | CHANGELOG.md |
| G-PI-CHANGELOG-173 | Added | Added extension support for customizing the interactive streaming working indicator via `ctx.ui.setWorkingIndicator()`, including custom animated frames, static indicators, hidden indicators, a new `workingindicator.ts` example extension, and updated extension/TUI/RPC docs ([#3413](https://github.com/badlogic/pimono/issues/3413)) | CHANGELOG.md |
| G-PI-CHANGELOG-174 | Added | Added `systemPromptOptions` (`BuildSystemPromptOptions`) to `before_agent_start` extension events, so extensions can inspect the structured inputs used to build the current system prompt ([#3473](https://github.com/badlogic/pimono/pull/3473) by [@dljsjr](https://github.com/dljsjr)) | CHANGELOG.md |
| G-PI-CHANGELOG-175 | Added | Added `/clone` to duplicate the current active branch into a new session, while keeping `/fork` focused on forking from a previous user message ([#2962](https://github.com/badlogic/pimono/issues/2962)) | CHANGELOG.md |
| G-PI-CHANGELOG-176 | Added | Added `ctx.fork()` support for `position: "before" | "at"` so extensions and integrations can branch before a user message or duplicate the current point in the conversation; the interactive clone/fork UX builds on that runtime support ([#3431](https://github.com/badlogic/pimono/pull/3431) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-177 | Added | Added configurable keybinding ids for scoped model selector actions and tree filter actions, so those interactive shortcuts can be remapped in `keybindings.json` ([#3343](https://github.com/badlogic/pimono/pull/3343) by [@mpazik](https://github.com/mpazik)) | CHANGELOG.md |
| G-PI-CHANGELOG-178 | Added | Added `PI_OAUTH_CALLBACK_HOST` support for builtin OAuth login flows, allowing local callback servers used by `pi auth` to bind to a custom interface instead of hardcoded `127.0.0.1` ([#3409](https://github.com/badlogic/pimono/pull/3409) by [@Michaelliv](https://github.com/Michaelliv)) | CHANGELOG.md |
| G-PI-CHANGELOG-179 | Added | Added `reason` and `targetSessionFile` metadata to `session_shutdown` extension events, so extensions can distinguish quit, reload, newsession, resume, and fork teardown paths ([#2863](https://github.com/badlogic/pimono/issues/2863)) | CHANGELOG.md |
| G-PI-CHANGELOG-180 | Changed | Changed `pi update` to batch npm package updates per scope and run git package updates with bounded parallelism, reducing multipackage update time while preserving skip behavior for pinned and alreadycurrent packages ([#2980](https://github.com/badlogic/pimono/issues/2980)) | CHANGELOG.md |
| G-PI-CHANGELOG-181 | Changed | Changed Bedrock session requests to omit `maxTokens` when model token limits are unknown and to omit `temperature` when unset, letting Bedrock use provider defaults and avoid unnecessary TPM quota reservation ([#3400](https://github.com/badlogic/pimono/pull/3400) by [@wirjo](https://github.com/wirjo)) | CHANGELOG.md |
| G-PI-CHANGELOG-182 | Fixed | Fixed `AgentSession` systemprompt option initialization to avoid constructing an invalid empty `BuildSystemPromptOptions`, so `npm run check` passes after `cwd` became mandatory. | CHANGELOG.md |
| G-PI-CHANGELOG-183 | Fixed | Fixed shellpath resolution to stop consulting ambient `process.cwd()` state during bash execution, so session/projectspecific `shellPath` settings now follow the active codingagent session cwd instead of the launcher cwd ([#3452](https://github.com/badlogic/pimono/issues/3452)) | CHANGELOG.md |
| G-PI-CHANGELOG-184 | Fixed | Fixed `ctx.ui.setWorkingIndicator()` custom frames to render verbatim instead of forcing the theme accent color, so extensions now own workingindicator coloring when they customize it ([#3467](https://github.com/badlogic/pimono/issues/3467)) | CHANGELOG.md |
| G-PI-CHANGELOG-185 | Fixed | Fixed `pi update` reinstalling npm packages that are already at the latest published version by checking the installed package version before running `npm install <pkg>@latest` ([#3000](https://github.com/badlogic/pimono/issues/3000)) | CHANGELOG.md |
| G-PI-CHANGELOG-186 | Fixed | Fixed `@` autocomplete plain queries to stop matching against the full cwd/base path, so path fragments in worktree names no longer crowd out intended results such as `@plan` ([#2778](https://github.com/badlogic/pimono/issues/2778)) | CHANGELOG.md |
| G-PI-CHANGELOG-187 | Fixed | Fixed builtin tool wrapping to use the same extensionrunner context path as extension tools, so builtin tools receive execution context and `read` can warn when the current model does not support images ([#3429](https://github.com/badlogic/pimono/issues/3429)) | CHANGELOG.md |
| G-PI-CHANGELOG-188 | Fixed | Fixed `openaicompletions` assistant replay to preserve `compat.requiresThinkingAsText` textpart serialization, avoiding samemodel followup crashes when previous assistant messages mix thinking and text ([#3387](https://github.com/badlogic/pimono/issues/3387)) | CHANGELOG.md |
| G-PI-CHANGELOG-189 | Fixed | Fixed direct OpenAI Chat Completions sessions to map `sessionId` and `cacheRetention` to prompt caching fields, sending `prompt_cache_key` when caching is enabled and `prompt_cache_retention: "24h"` for direct `api.openai.com` requests with long retention ([#3426](https://github.com/badlogic/pimono/issues/3426)) | CHANGELOG.md |
| G-PI-CHANGELOG-190 | Fixed | Fixed OpenAIcompatible Chat Completions sessions to optionally send aligned `session_id`, `xclientrequestid`, and `xsessionaffinity` headers from `sessionId` via `compat.sendSessionAffinityHeaders`, improving cacheaffinity routing for backends such as Fireworks ([#3430](https://github.com/badlogic/pimono/issues/3430)) | CHANGELOG.md |
| G-PI-CHANGELOG-191 | Fixed | Fixed threaded `/resume` session relationships and currentsession detection to canonicalize symlinked session paths during selector comparisons, so shared session directories no longer break parentchild matching or activesession delete protection ([#3364](https://github.com/badlogic/pimono/issues/3364)) | CHANGELOG.md |
| G-PI-CHANGELOG-192 | Fixed | Fixed `/session`, Sessions docs, and CLI help to consistently document that session reuse supports both file paths and session IDs, and that `/session` shows the current session ID ([#3390](https://github.com/badlogic/pimono/issues/3390)) | CHANGELOG.md |
| G-PI-CHANGELOG-193 | Fixed | Fixed Windows pnpm global install detection to recognize `\\.pnpm\\` store paths, so update notices now suggest `pnpm install g @mariozechner/picodingagent` instead of falling back to npm ([#3378](https://github.com/badlogic/pimono/issues/3378)) | CHANGELOG.md |
| G-PI-CHANGELOG-194 | Fixed | Fixed missing `@sinclair/typebox` runtime dependency in `@mariozechner/picodingagent`, so strict pnpm installs no longer fail with `ERR_MODULE_NOT_FOUND` when starting `pi` ([#3434](https://github.com/badlogic/pimono/issues/3434)) | CHANGELOG.md |
| G-PI-CHANGELOG-195 | Fixed | Fixed xterm uppercase typing in the interactive editor by decoding printable `modifyOtherKeys` input and normalizing shifted letter matching, so `Shift+letter` no longer disappears in `pi` ([#3436](https://github.com/badlogic/pimono/issues/3436)) | CHANGELOG.md |
| G-PI-CHANGELOG-196 | Fixed | Fixed `/compact` to reuse the session thinking level for compaction summaries instead of forcing `high`, avoiding invalid reasoningeffort errors on `githubcopilot/claudeopus4.7` sessions configured for `medium` thinking ([#3438](https://github.com/badlogic/pimono/issues/3438)) | CHANGELOG.md |
| G-PI-CHANGELOG-197 | Fixed | Fixed shared/exported plaintext tool output to preserve indentation instead of collapsing leading whitespace in the web share page ([#3440](https://github.com/badlogic/pimono/issues/3440)) | CHANGELOG.md |
| G-PI-CHANGELOG-198 | Fixed | Fixed exported share pages to use browsersafe `T` and `O` shortcuts with clickable header toggles for thinking and tool visibility instead of browserreserved `Ctrl+T` / `Ctrl+O` bindings ([#3374](https://github.com/badlogic/pimono/pull/3374) by [@vekexasia](https://github.com/vekexasia)) | CHANGELOG.md |
| G-PI-CHANGELOG-199 | Fixed | Fixed skill resolution to dedupe symlinked aliases by canonical path, so `pi config` no longer shows duplicate skill entries when `~/.pi/agent/skills` points to `~/.agents/skills` ([#3417](https://github.com/badlogic/pimono/pull/3417) by [@rwachtler](https://github.com/rwachtler)) | CHANGELOG.md |
| G-PI-CHANGELOG-200 | Fixed | Fixed OpenRouter request attribution to include Pi app headers (`HTTPReferer: https://pi.dev`, `XOpenRouterTitle: pi`, `XOpenRouterCategories: cliagent`) when sessions are created through the codingagent SDK and install telemetry is enabled ([#3414](https://github.com/badlogic/pimono/issues/3414)) | CHANGELOG.md |
| G-PI-CHANGELOG-201 | Fixed | Fixed custommodel `compat` schema/docs to support `cacheControlFormat: "anthropic"` for OpenAIcompatible providers that expose Anthropicstyle prompt caching via `cache_control` markers ([#3392](https://github.com/badlogic/pimono/issues/3392)) | CHANGELOG.md |
| G-PI-CHANGELOG-202 | Fixed | Fixed Cloud Code Assist tool schemas to strip JSON Schema metadeclaration keys before provider translation, avoiding validation failures for toolenabled sessions that use `$schema`, `$defs`, and related metadata ([#3412](https://github.com/badlogic/pimono/pull/3412) by [@vladlearns](https://github.com/vladlearns)) | CHANGELOG.md |
| G-PI-CHANGELOG-203 | Fixed | Fixed direct Bedrock sessions to honor `model.baseUrl` as the runtime client endpoint, restoring support for custom Bedrock VPC or proxy routes ([#3402](https://github.com/badlogic/pimono/pull/3402) by [@wirjo](https://github.com/wirjo)) | CHANGELOG.md |
| G-PI-CHANGELOG-204 | Fixed | Fixed the `edit` tool to coerce stringified `edits` JSON before validation, so models that send the array payload as a JSON string no longer fall back to adhoc shell edits ([#3370](https://github.com/badlogic/pimono/pull/3370) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-205 | Fixed | Fixed package manifest positive glob entries to expand before loading packaged resources, restoring manifest patterns such as `skills//.md` ([#3350](https://github.com/badlogic/pimono/pull/3350) by [@neonspectra](https://github.com/neonspectra)) | CHANGELOG.md |
| G-PI-CHANGELOG-206 | New Features | Bedrock sessions can now authenticate with `AWS_BEARER_TOKEN_BEDROCK`, enabling Converse API access without local SigV4 credentials. See [docs/providers.md#amazonbedrock](docs/providers.md#amazonbedrock). | CHANGELOG.md |
| G-PI-CHANGELOG-207 | Added | Added Bedrock bearertoken authentication support via `AWS_BEARER_TOKEN_BEDROCK`, enabling codingagent sessions to use Bedrock Converse without local SigV4 credentials ([#3125](https://github.com/badlogic/pimono/pull/3125) by [@wirjo](https://github.com/wirjo)) | CHANGELOG.md |
| G-PI-CHANGELOG-208 | Fixed | Fixed `/scopedmodels` Alt+Up/Down to stay a noop in the implicit `all enabled` state instead of materializing a full explicit enabledmodel list and marking the selector dirty ([#3331](https://github.com/badlogic/pimono/issues/3331)) | CHANGELOG.md |
| G-PI-CHANGELOG-209 | Fixed | Fixed Mistral Small 4 default thinking requests to use the model's supported reasoning control, avoiding `400` errors when starting sessions on `mistralsmall2603` and `mistralsmalllatest` ([#3338](https://github.com/badlogic/pimono/issues/3338)) | CHANGELOG.md |
| G-PI-CHANGELOG-210 | Fixed | Fixed Qwen chattemplate thinking replay to preserve prior thinking across turns, so affected OpenAIcompatible models keep multiturn toolcall arguments instead of degrading to empty `{}` payloads ([#3325](https://github.com/badlogic/pimono/issues/3325)) | CHANGELOG.md |
| G-PI-CHANGELOG-211 | Fixed | Fixed exported HTML transcripts so text selection no longer triggers clickbased expand/collapse toggles ([#3332](https://github.com/badlogic/pimono/pull/3332) by [@xu0o0](https://github.com/xu0o0)) | CHANGELOG.md |
| G-PI-CHANGELOG-212 | Fixed | Fixed flaky git package update notifications by waiting for captured git command stdio to fully drain before comparing local and remote commit SHAs ([#3027](https://github.com/badlogic/pimono/issues/3027)) | CHANGELOG.md |
| G-PI-CHANGELOG-213 | Fixed | Fixed system prompt dates to use a stable `YYYYMMDD` format instead of localedependent output, keeping prompts deterministic across runtimes and locales ([#2814](https://github.com/badlogic/pimono/issues/2814)) | CHANGELOG.md |
| G-PI-CHANGELOG-214 | Fixed | Fixed autoretry transient error detection to treat `Network connection lost.` as retryable, so dropped provider connections retry instead of terminating the agent ([#3317](https://github.com/badlogic/pimono/issues/3317)) | CHANGELOG.md |
| G-PI-CHANGELOG-215 | Fixed | Fixed compact interactive extension startup summaries to disambiguate package extensions and repeated local `index.ts` entries by using packageaware labels and the minimal parent path needed to make local entries unique ([#3308](https://github.com/badlogic/pimono/issues/3308)) | CHANGELOG.md |
| G-PI-CHANGELOG-216 | Fixed | Fixed git package dependency installation to use production installs (`npm install omit=dev`) during both install and update flows, so extension runtime dependencies must come from `dependencies` and not `devDependencies` ([#3009](https://github.com/badlogic/pimono/issues/3009)) | CHANGELOG.md |
| G-PI-CHANGELOG-217 | Fixed | Fixed `tool_result` / `afterToolCall` extension handling for error results by forwarding `details` and `isError` overrides through `AgentSession` instead of dropping them when `isError` was already true ([#3051](https://github.com/badlogic/pimono/issues/3051)) | CHANGELOG.md |
| G-PI-CHANGELOG-218 | Fixed | Fixed missing root exports for `RpcClient` and RPC protocol types from `@mariozechner/picodingagent`, so ESM consumers can import them from the main package entrypoint ([#3275](https://github.com/badlogic/pimono/issues/3275)) | CHANGELOG.md |
| G-PI-CHANGELOG-219 | Fixed | Fixed OpenAI Codex servicetier cost accounting to trust the explicitly requested tier when the API echoes the default tier in responses, keeping session cost displays aligned with the selected tier ([#3307](https://github.com/badlogic/pimono/pull/3307) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-220 | Fixed | Fixed parallel toolcall finalization to convert `afterToolCall` hook throws into error tool results instead of aborting the remaining tool batch ([#3084](https://github.com/badlogic/pimono/issues/3084)) | CHANGELOG.md |
| G-PI-CHANGELOG-221 | Fixed | Fixed Bun binary asset path resolution to honor `PI_PACKAGE_DIR` for builtin themes, HTML export templates, and interactive bundled assets ([#3074](https://github.com/badlogic/pimono/issues/3074)) | CHANGELOG.md |
| G-PI-CHANGELOG-222 | Fixed | Fixed usermessage turn spacing in interactive mode by restoring an intermessage spacer before user turns (except the first user message), preventing assistant and user blocks from rendering flush together. | CHANGELOG.md |
| G-PI-CHANGELOG-223 | Fixed | Fixed interactive `/import` handling to support quoted JSONL paths with spaces, route missing JSONL files through the nonfatal `SessionImportFileNotFoundError` path, and document the `importFromJsonl()` exceptions (`SessionImportFileNotFoundError`, `MissingSessionCwdError`). | CHANGELOG.md |
| G-PI-CHANGELOG-224 | New Features | Prompt templates support an `argumenthint` frontmatter field that renders before the description in the `/` autocomplete dropdown, using `<angle>` for required and `[square]` for optional arguments. See [docs/prompttemplates.md#argumenthints](docs/prompttemplates.md#argumenthints). | CHANGELOG.md |
| G-PI-CHANGELOG-225 | New Features | New `after_provider_response` extension hook lets extensions inspect provider HTTP status codes and headers immediately after each response is received and before stream consumption begins. See [docs/extensions.md](docs/extensions.md). | CHANGELOG.md |
| G-PI-CHANGELOG-226 | New Features | Compact interactive startup header with a commaseparated view of loaded AGENTS.md files, prompt templates, skills, and extensions. Press `Ctrl+O` to toggle the expanded listing. | CHANGELOG.md |
| G-PI-CHANGELOG-227 | New Features | Markdown links in assistant output now render as OSC 8 hyperlinks on terminals that advertise support; unknown terminals and tmux/screen default to plain text so URLs are never silently dropped. | CHANGELOG.md |
| G-PI-CHANGELOG-228 | Added | Added `argumenthint` frontmatter field for prompt templates, displayed before the description in the autocomplete dropdown ([#2780](https://github.com/badlogic/pimono/pull/2780) by [@andresvi94](https://github.com/andresvi94)) | CHANGELOG.md |
| G-PI-CHANGELOG-229 | Added | Added `after_provider_response` extension hook so extensions can inspect provider HTTP status codes and headers after each provider response is received and before stream consumption begins ([#3128](https://github.com/badlogic/pimono/issues/3128)) | CHANGELOG.md |
| G-PI-CHANGELOG-230 | Added | Added OSC 8 hyperlink rendering for markdown links when the terminal advertises support ([#3248](https://github.com/badlogic/pimono/pull/3248) by [@ofa1](https://github.com/ofa1)) | CHANGELOG.md |
| G-PI-CHANGELOG-231 | Changed | Changed interactive startup header to a compact, commaseparated view of loaded AGENTS.md files, prompt templates, skills, and extensions, with `Ctrl+O` to toggle the expanded listing ([#3267](https://github.com/badlogic/pimono/pull/3267)) | CHANGELOG.md |
| G-PI-CHANGELOG-232 | Changed | Tightened hyperlink capability detection to default `hyperlinks: false` for unknown terminals and force it off under tmux/screen (including nested sessions), preventing markdown link URLs from disappearing on terminals that silently swallow OSC 8 sequences ([#3248](https://github.com/badlogic/pimono/pull/3248)) | CHANGELOG.md |
| G-PI-CHANGELOG-233 | Fixed | Fixed interactive user message rendering to keep bottom padding visible in terminals affected by OSC 133 prompt markers without adding an extra blank line before the following assistant message ([#3090](https://github.com/badlogic/pimono/issues/3090)) | CHANGELOG.md |
| G-PI-CHANGELOG-234 | Fixed | Fixed `verbose` startup output to begin with expanded startup help and loaded resource listings after the compact startup header change ([#3147](https://github.com/badlogic/pimono/issues/3147)) | CHANGELOG.md |
| G-PI-CHANGELOG-235 | Fixed | Fixed `find` tool returning no results for pathbased glob patterns such as `src//.spec.ts` or `some/parent/child/` by switching fd into fullpath mode and normalizing the pattern when it contains a `/` ([#3302](https://github.com/badlogic/pimono/issues/3302)) | CHANGELOG.md |
| G-PI-CHANGELOG-236 | Fixed | Fixed `find` tool applying nested `.gitignore` rules across sibling directories (e.g. rules from `a/.gitignore` hiding matching files under `b/`) by dropping the manual `ignorefile` collection and delegating to fd's hierarchical `.gitignore` handling via `norequiregit` ([#3303](https://github.com/badlogic/pimono/issues/3303)) | CHANGELOG.md |
| G-PI-CHANGELOG-237 | Fixed | Fixed OpenAI Responses prompt caching for non`api.openai.com` base URLs (OpenAIcompatible proxies such as litellm, theclawbay) by sending the `session_id` and `xclientrequestid` cacheaffinity headers unconditionally when a `sessionId` is provided, matching the official Codex CLI behavior ([#3264](https://github.com/badlogic/pimono/pull/3264) by [@vegarsti](https://github.com/vegarsti)) | CHANGELOG.md |
| G-PI-CHANGELOG-238 | Fixed | Fixed the `preset` example extension to snapshot the active model, thinking level, and tool set on the first preset application and restore that state when cycling back to `(none)`, instead of falling back to a hardcoded default tool list ([#3272](https://github.com/badlogic/pimono/pull/3272) by [@stembi](https://github.com/stembi)) | CHANGELOG.md |
| G-PI-CHANGELOG-239 | Fixed | Fixed Opus 4.7 adaptive thinking configuration across Anthropic and Bedrock providers by recognizing Opus 4.7 adaptivethinking support and mapping `xhigh` reasoning to providersupported effort values ([#3286](https://github.com/badlogic/pimono/pull/3286) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-240 | Fixed | Fixed Zellij `Shift+Enter` regressions by reverting the Zellijspecific Kitty keyboard query bypass and restoring the previous keyboard negotiation behavior ([#3259](https://github.com/badlogic/pimono/issues/3259)) | CHANGELOG.md |
| G-PI-CHANGELOG-241 | New Features | `nocontextfiles` (`nc`) disables automatic `AGENTS.md` / `CLAUDE.md` discovery when you need a clean run without project context injection. See [README.md#contextfiles](README.md#contextfiles). | CHANGELOG.md |
| G-PI-CHANGELOG-242 | New Features | `loadProjectContextFiles()` is now exported as a standalone utility for extensions and SDKstyle integrations that need to inspect the same contextfile resolution order used by the CLI. See [README.md#contextfiles](README.md#contextfiles). | CHANGELOG.md |
| G-PI-CHANGELOG-243 | New Features | New `after_provider_response` extension hook lets extensions inspect provider HTTP status codes and headers immediately after response creation and before stream consumption. See [docs/extensions.md](docs/extensions.md). | CHANGELOG.md |
| G-PI-CHANGELOG-244 | Added | Added `nocontextfiles` (`nc`) to disable `AGENTS.md` and `CLAUDE.md` context file discovery and loading ([#3253](https://github.com/badlogic/pimono/issues/3253)) | CHANGELOG.md |
| G-PI-CHANGELOG-245 | Added | Exported `loadProjectContextFiles()` as a standalone utility so extensions can discover project context files without instantiating a full `DefaultResourceLoader` ([#3142](https://github.com/badlogic/pimono/issues/3142)) | CHANGELOG.md |
| G-PI-CHANGELOG-246 | Added | Added `after_provider_response` extension hook so extensions can inspect provider HTTP status codes and headers after each provider response is received and before stream consumption begins ([#3128](https://github.com/badlogic/pimono/issues/3128)) | CHANGELOG.md |
| G-PI-CHANGELOG-247 | Changed | Added `claudeopus47` model for Anthropic. | CHANGELOG.md |
| G-PI-CHANGELOG-248 | Changed | Changed Anthropic prompt caching to add a `cache_control` breakpoint on the last tool definition, so tool schemas can be cached independently from transcript updates while preserving existing cache retention behavior ([#3260](https://github.com/badlogic/pimono/issues/3260)) | CHANGELOG.md |
| G-PI-CHANGELOG-249 | Fixed | Fixed markdown strikethrough parsing in interactive rendering and HTML export to require strict doubletilde delimiters (`~~text~~`) with nonwhitespace boundaries. | CHANGELOG.md |
| G-PI-CHANGELOG-250 | Fixed | Fixed shutdown handling to kill tracked detached `bash` tool child processes on exit signals, preventing orphaned background processes. | CHANGELOG.md |
| G-PI-CHANGELOG-251 | Fixed | Fixed flaky `edittoolnofullredraw` TUI tests by waiting for asynchronous preview and preflight error rendering instead of relying on fixed render ticks. | CHANGELOG.md |
| G-PI-CHANGELOG-252 | Fixed | Fixed `kimicoding` default model selection to use `kimiforcoding` instead of `kimik2thinking` ([#3242](https://github.com/badlogic/pimono/issues/3242)) | CHANGELOG.md |
| G-PI-CHANGELOG-253 | Fixed | Fixed `ctrl+z` on native Windows to avoid crashing interactive mode, disable the default suspend binding there, and show a status message when suspend is invoked manually ([#3191](https://github.com/badlogic/pimono/issues/3191)) | CHANGELOG.md |
| G-PI-CHANGELOG-254 | Fixed | Fixed `find` tool cancellation and responsiveness on broad searches by making `.gitignore` discovery and `fd` execution fully abortaware and nonblocking ([#3148](https://github.com/badlogic/pimono/issues/3148)) | CHANGELOG.md |
| G-PI-CHANGELOG-255 | Fixed | Fixed `grep` broadsearch stalls when `context=0` by formatting match lines from ripgrep JSON output instead of doing synchronous permatch file reads ([#3205](https://github.com/badlogic/pimono/issues/3205)) | CHANGELOG.md |
| G-PI-CHANGELOG-256 | New Features | `renderShell: "self"` for custom and builtin tool renderers so tools can own their outer shell instead of the default boxed shell. Useful for stable large previews such as edit diffs. See [docs/extensions.md#customrendering](docs/extensions.md#customrendering). | CHANGELOG.md |
| G-PI-CHANGELOG-257 | New Features | Interactive autoretry status now shows a live countdown during backoff instead of a static retry delay message. | CHANGELOG.md |
| G-PI-CHANGELOG-258 | Added | Added `renderShell: "self"` for custom and builtin tool renderers so tools can own their outer shell instead of using the default boxed shell. This is useful for stable large previews such as edit diffs ([#3134](https://github.com/badlogic/pimono/issues/3134)) | CHANGELOG.md |
| G-PI-CHANGELOG-259 | Fixed | Fixed edit diff previews to stay visible during edit permission dialogs and session replay without reintroducing largeresult redraw flicker ([#3134](https://github.com/badlogic/pimono/issues/3134)) | CHANGELOG.md |
| G-PI-CHANGELOG-260 | Fixed | Fixed `/reload` to render a static reload status box instead of an animated spinner, avoiding redraw instability during interactive reloads. | CHANGELOG.md |
| G-PI-CHANGELOG-261 | Fixed | Fixed the `planmode` example extension to allow `eza` in the readonly bash allowlist instead of the deprecated `exa` command ([#3240](https://github.com/badlogic/pimono/pull/3240) by [@rwachtler](https://github.com/rwachtler)) | CHANGELOG.md |
| G-PI-CHANGELOG-262 | Fixed | Fixed `googlevertex` API key resolution to treat `gcpvertexcredentials` as an Application Default Credentials marker instead of a literal API key, so markerbased setups correctly fall back to ADC ([#3221](https://github.com/badlogic/pimono/pull/3221) by [@deepkilo](https://github.com/deepkilo)) | CHANGELOG.md |
| G-PI-CHANGELOG-263 | Fixed | Fixed RPC `prompt` to wait for prompt preflight success before emitting its single authoritative response, while still treating handled and queued prompts as success ([#3049](https://github.com/badlogic/pimono/issues/3049)) | CHANGELOG.md |
| G-PI-CHANGELOG-264 | Fixed | Fixed `/scopedmodels` reordering to propagate into the `/model` scoped tab, preserving the userdefined scoped model order instead of resorting it ([#3217](https://github.com/badlogic/pimono/issues/3217)) | CHANGELOG.md |
| G-PI-CHANGELOG-265 | Fixed | Fixed `session_shutdown` to fire on `SIGHUP` and `SIGTERM` in interactive, print, and RPC modes so extensions can run shutdown cleanup on those signaldriven exits ([#3212](https://github.com/badlogic/pimono/issues/3212)) | CHANGELOG.md |
| G-PI-CHANGELOG-266 | Fixed | Fixed screenshot path parsing to handle lower case am/pm in macOS screenshot filenames ([#3194](https://github.com/badlogic/pimono/pull/3194) by [@jayayeseekay](https://github.com/jayayeseekay)) | CHANGELOG.md |
| G-PI-CHANGELOG-267 | Fixed | Fixed interactive autoretry status updates to show a live countdown during backoff instead of a static retry delay message ([#3187](https://github.com/badlogic/pimono/issues/3187)) | CHANGELOG.md |
| G-PI-CHANGELOG-268 | New Features | Support for multiple `appendsystemprompt` flags, each value is appended to the system prompt separated by double newlines. See [README.md#otheroptions](README.md#otheroptions). | CHANGELOG.md |
| G-PI-CHANGELOG-269 | New Features | Support for passing inline extension factories to `main()` for embedded integrations and custom entrypoints. | CHANGELOG.md |
| G-PI-CHANGELOG-270 | New Features | Interactive keybinding support for Kitty `super`modified shortcuts such as `super+k`, `super+enter`, and `ctrl+super+k`. See [docs/keybindings.md](docs/keybindings.md). | CHANGELOG.md |
| G-PI-CHANGELOG-271 | Added | Added support for multiple `appendsystemprompt` flags, each value is appended to the system prompt separated by double newlines ([#3171](https://github.com/badlogic/pimono/pull/3171) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-272 | Added | Added interactive keybinding support for Kitty `super`modified shortcuts such as `super+k`, `super+enter`, and `ctrl+super+k` ([#3111](https://github.com/badlogic/pimono/pull/3111) by [@sudosubin](https://github.com/sudosubin)) | CHANGELOG.md |
| G-PI-CHANGELOG-273 | Added | Added support for passing inline extension factories to `main()` for embedded integrations and custom entrypoints ([#3099](https://github.com/badlogic/pimono/pull/3099) by [@pmateusz](https://github.com/pmateusz)) | CHANGELOG.md |
| G-PI-CHANGELOG-274 | Fixed | Fixed direct OpenAI Responses and Codex SSE requests to align `prompt_cache_key`, `session_id`, and `xclientrequestid` values with the same sessionderived identifier, improving prompt cache affinity for appendonly sessions ([#3018](https://github.com/badlogic/pimono/pull/3018) by [@steipete](https://github.com/steipete)) | CHANGELOG.md |
| G-PI-CHANGELOG-275 | Fixed | Fixed streamingonly `partialJson` scratch buffers leaking into persisted OpenAI Responses tool calls, which could corrupt followup payloads on resumed conversations. | CHANGELOG.md |
| G-PI-CHANGELOG-276 | Fixed | Fixed Ctrl+Alt letter key matching in tmux by falling through from legacy ESCprefixed handling to CSIu and xterm `modifyOtherKeys` parsing when the legacy form does not match ([#2989](https://github.com/badlogic/pimono/pull/2989) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-277 | Fixed | Fixed the shipped `subagent` example to avoid leaking Bun virtual filesystem script paths into subagent prompts ([#3002](https://github.com/badlogic/pimono/pull/3002) by [@nathyong](https://github.com/nathyong)) | CHANGELOG.md |
| G-PI-CHANGELOG-278 | Fixed | Fixed bordered loaders to stop their animation timer when disposed, preventing stale loader updates after teardown. | CHANGELOG.md |
| G-PI-CHANGELOG-279 | Telemetry | Pi needs a reliable perversion usage signal to understand whether releases are being adopted and to help justify funding continued development. | CHANGELOG.md |
| G-PI-CHANGELOG-280 | Telemetry | npm download counts are not a reliable proxy for actual Pi usage. | CHANGELOG.md |
| G-PI-CHANGELOG-281 | Telemetry | It only runs in interactive mode. | CHANGELOG.md |
| G-PI-CHANGELOG-282 | Telemetry | It does not run in RPC mode, print mode, JSON mode, or SDK mode. | CHANGELOG.md |
| G-PI-CHANGELOG-283 | Telemetry | On a fresh interactive install, Pi writes `lastChangelogVersion`, then sends the ping. | CHANGELOG.md |
| G-PI-CHANGELOG-284 | Telemetry | On later interactive startups, if the local changelog contains entries newer than the previously stored `lastChangelogVersion`, Pi writes the new `lastChangelogVersion`, then sends the ping. | CHANGELOG.md |
| G-PI-CHANGELOG-285 | Telemetry | The request is fireandforget. Startup does not wait for it, and any errors are ignored. | CHANGELOG.md |
| G-PI-CHANGELOG-286 | Telemetry | Only the Pi version in the request path, for example `https://pi.dev/install?version=0.67.1`. | CHANGELOG.md |
| G-PI-CHANGELOG-287 | Telemetry | The server stores only aggregate perversion counters such as `{ "0.67.1": 3 }`. | CHANGELOG.md |
| G-PI-CHANGELOG-288 | Telemetry | It does not store IP addresses, client identifiers, prompts, paths, models, auth state, or any other peruser data. It literally only increments a counter for that version. | CHANGELOG.md |
| G-PI-CHANGELOG-289 | Telemetry | `/settings` → disable `Install telemetry` | CHANGELOG.md |
| G-PI-CHANGELOG-290 | Telemetry | `settings.json` → set `enableInstallTelemetry` to `false` | CHANGELOG.md |
| G-PI-CHANGELOG-291 | Telemetry | `PI_OFFLINE=1` | CHANGELOG.md |
| G-PI-CHANGELOG-292 | Telemetry | `PI_TELEMETRY=0` | CHANGELOG.md |
| G-PI-CHANGELOG-293 | New Features | Full `openRouterRouting` support in `models.json`, including fallbacks, parameter requirements, data collection, ZDR, ignore lists, quantizations, provider sorting, max price, and preferred throughput and latency constraints. See [docs/models.md](docs/models.md). | CHANGELOG.md |
| G-PI-CHANGELOG-294 | New Features | `PI_CODING_AGENT=true` environment variable set at startup so subprocesses can detect they are running inside the coding agent. | CHANGELOG.md |
| G-PI-CHANGELOG-295 | New Features | Updated `antigravityimagegen.ts` example extension to use UserAgent version `1.21.9` ([#2901](https://github.com/badlogic/pimono/pull/2901) by [@aadishv](https://github.com/aadishv)) | CHANGELOG.md |
| G-PI-CHANGELOG-296 | New Features | Fixed `listmodels` silently swallowing `models.json` load errors; errors are now printed to stderr ([#3072](https://github.com/badlogic/pimono/issues/3072)) | CHANGELOG.md |
| G-PI-CHANGELOG-297 | New Features | Fixed custom models for builtin providers (e.g. `openrouter`) being silently dropped from `listmodels` by inheriting `api`/`baseUrl` from builtin model definitions and no longer requiring `apiKey` for providers with existing auth ([#2921](https://github.com/badlogic/pimono/issues/2921) and [#3072](https://github.com/badlogic/pimono/issues/3072)) | CHANGELOG.md |
| G-PI-CHANGELOG-298 | Added | Added full `openRouterRouting` field support in `models.json`, including fallbacks, parameter requirements, data collection, ZDR, ignore lists, quantizations, provider sorting, max price, and preferred throughput and latency constraints ([#2904](https://github.com/badlogic/pimono/pull/2904) by [@zmberber](https://github.com/zmberber)) | CHANGELOG.md |
| G-PI-CHANGELOG-299 | Added | Set `PI_CODING_AGENT=true` environment variable at startup so subprocesses can detect they are running inside the coding agent ([#2868](https://github.com/badlogic/pimono/issues/2868)) | CHANGELOG.md |
| G-PI-CHANGELOG-300 | Fixed | Fixed interactive changelog rendering for the telemetry notes by moving the section under a `### Telemetry` heading, so startup shows the full release notes instead of only the version header. | CHANGELOG.md |
| G-PI-CHANGELOG-301 | Fixed | Updated `antigravityimagegen.ts` example extension to use UserAgent version `1.21.9` ([#2901](https://github.com/badlogic/pimono/pull/2901) by [@aadishv](https://github.com/aadishv)) | CHANGELOG.md |
| G-PI-CHANGELOG-302 | Fixed | Bumped default Antigravity UserAgent version to `1.21.9` ([#2901](https://github.com/badlogic/pimono/pull/2901) by [@aadishv](https://github.com/aadishv)) | CHANGELOG.md |
| G-PI-CHANGELOG-303 | Fixed | Fixed Gemma 4 thinking level mapping to route between `MINIMAL` and `HIGH`, and map Pi reasoning levels to the model's supported thinking levels ([#2903](https://github.com/badlogic/pimono/pull/2903) by [@aadishv](https://github.com/aadishv)) | CHANGELOG.md |
| G-PI-CHANGELOG-304 | Fixed | Fixed Gemini 2.5 Flash Lite minimal thinking budget to use the model's supported 512token minimum instead of the regular Flash 128token minimum, avoiding invalid thinking budget errors ([#2861](https://github.com/badlogic/pimono/pull/2861) by [@JasonOA888](https://github.com/JasonOA888)) | CHANGELOG.md |
| G-PI-CHANGELOG-305 | Fixed | Fixed OpenAI Codex Responses requests to forward configured `serviceTier` values, restoring servicetier selection for Codex sessions ([#2996](https://github.com/badlogic/pimono/pull/2996) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-306 | Fixed | Fixed newly generated session IDs to use UUIDv7, improving time locality for sessionbased request routing ([#3018](https://github.com/badlogic/pimono/pull/3018) by [@steipete](https://github.com/steipete)) | CHANGELOG.md |
| G-PI-CHANGELOG-307 | Fixed | Fixed `Container.render()` stack overflow on long sessions by replacing `Array.push(...spread)` with a loopbased push, preventing `RangeError: Maximum call stack size exceeded` when child output exceeds the V8 call stack argument limit ([#2651](https://github.com/badlogic/pimono/issues/2651)) | CHANGELOG.md |
| G-PI-CHANGELOG-308 | Fixed | Fixed editor stickycolumn tracking around paste markers so vertical cursor navigation restores the column from before the cursor entered a paste marker instead of jumping inside or past pasted content ([#3092](https://github.com/badlogic/pimono/pull/3092) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-309 | Fixed | Fixed queued messages typed during `/tree` branch summarization to flush automatically after navigation completes, so they no longer remain stuck in the steering queue ([#3091](https://github.com/badlogic/pimono/pull/3091) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-310 | Fixed | Fixed npm package update check to work with packages on nondefault registries by using `npm view` instead of hardcoded `registry.npmjs.org` fetch ([#3164](https://github.com/badlogic/pimono/pull/3164) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-311 | Changed | Changed the Earendil announcement from an automatic startup notice to the hidden `/dementedelves` slash command. | CHANGELOG.md |
| G-PI-CHANGELOG-312 | New Features | Earendil startup announcement with bundled inline image rendering and a linked blog post for April 8 and 9, 2026. | CHANGELOG.md |
| G-PI-CHANGELOG-313 | New Features | Interactive Anthropic subscription auth warning when Anthropic subscription auth is active, clarifying that Anthropic thirdparty usage draws from extra usage and is billed per token. | CHANGELOG.md |
| G-PI-CHANGELOG-314 | Fixed | Fixed bare `readline` import to use `node:readline` prefix for Deno compatibility ([#2885](https://github.com/badlogic/pimono/issues/2885) by [@milosvvtool](https://github.com/milosvvtool)) | CHANGELOG.md |
| G-PI-CHANGELOG-315 | Fixed | Fixed autoretry to treat stream failures like `request ended without sending any chunks` as transient errors ([#2892](https://github.com/badlogic/pimono/issues/2892)) | CHANGELOG.md |
| G-PI-CHANGELOG-316 | Fixed | Fixed interactive startup notices to render after the initial resource listing, and added a bundled Earendil startup announcement with inline image rendering for April 8 and 9, 2026. Moved the blog link above the image to avoid overlap with terminal image rendering. | CHANGELOG.md |
| G-PI-CHANGELOG-317 | Fixed | Fixed interactive mode to warn when Anthropic subscription auth is active, so users know Anthropic thirdparty usage draws from extra usage and is billed per token. | CHANGELOG.md |
| G-PI-CHANGELOG-318 | Fixed | Fixed bash output truncation by line count to always persist full output to a temp file, preventing data loss when output exceeds 2000 lines but stays under the byte threshold ([#2852](https://github.com/badlogic/pimono/issues/2852)) | CHANGELOG.md |
| G-PI-CHANGELOG-319 | Fixed | RpcClient now forwards subprocess stderr to parent process in realtime ([#2805](https://github.com/badlogic/pimono/issues/2805)) | CHANGELOG.md |
| G-PI-CHANGELOG-320 | Fixed | Theme file watcher now handles async `fs.watch` error events instead of crashing the process ([#2791](https://github.com/badlogic/pimono/issues/2791)) | CHANGELOG.md |
| G-PI-CHANGELOG-321 | Fixed | Fixed stored session cwd handling so resuming or importing a session whose original working directory no longer exists now prompts interactive users to continue in the current cwd, while noninteractive modes fail with a clear error. | CHANGELOG.md |
| G-PI-CHANGELOG-322 | Fixed | Fixed resource collision precedence so project and user skills, prompt templates, and themes override package resources consistently, and CLIprovided paths take precedence over discovered resources ([#2781](https://github.com/badlogic/pimono/issues/2781)) | CHANGELOG.md |
| G-PI-CHANGELOG-323 | Fixed | Fixed OpenAIcompatible completions streaming usage accounting to preserve `prompt_tokens_details.cache_write_tokens` and normalize OpenRouter `cached_tokens`, preventing incorrect cache read/write token and cost reporting in pi ([#2802](https://github.com/badlogic/pimono/issues/2802)) | CHANGELOG.md |
| G-PI-CHANGELOG-324 | Fixed | Fixed CLI extension paths like `git:gist.github.com/...` being incorrectly resolved against cwd instead of being passed through to the package manager ([#2845](https://github.com/badlogic/pimono/pull/2845) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-325 | Fixed | Fixed piped stdin runs with `mode json` to preserve JSONL output instead of falling back to plain text ([#2848](https://github.com/badlogic/pimono/pull/2848) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-326 | Fixed | Fixed interactive command docs to stop listing removed `/exit` as a supported quit command ([#2850](https://github.com/badlogic/pimono/issues/2850)) | CHANGELOG.md |
| G-PI-CHANGELOG-327 | New Features | Session runtime API: `createAgentSessionRuntime()` and `AgentSessionRuntime` provide a closurebased runtime that recreates cwdbound services and session config on every session switch. Startup, `/new`, `/resume`, `/fork`, and import all use the same creation path. See [docs/sdk.md](docs/sdk.md) and [examples/sdk/13sessionruntime.ts](examples/sdk/13sessionruntime.ts). | CHANGELOG.md |
| G-PI-CHANGELOG-328 | New Features | Label timestamps in `/tree`: Toggle timestamps on tree entries with `Shift+T`, with smart date formatting and timestamp preservation through branching ([#2691](https://github.com/badlogic/pimono/pull/2691) by [@wwinter](https://github.com/wwinter)) | CHANGELOG.md |
| G-PI-CHANGELOG-329 | New Features | `defineTool()` helper: Create standalone custom tool definitions with full TypeScript parameter type inference, no manual casts needed ([#2746](https://github.com/badlogic/pimono/issues/2746)). See [docs/extensions.md](docs/extensions.md). | CHANGELOG.md |
| G-PI-CHANGELOG-330 | New Features | Unified diagnostics: Arg parsing, service creation, session option resolution, and resource loading all return structured diagnostics (`info`/`warning`/`error`) instead of logging or exiting. The app layer decides presentation and exit behavior. | CHANGELOG.md |
| G-PI-CHANGELOG-331 | Breaking Changes | Removed extension posttransition events `session_switch` and `session_fork`. Use `session_start` with `event.reason` (`"startup" | "reload" | "new" | "resume" | "fork"`). For `"new"`, `"resume"`, and `"fork"`, `session_start` includes `previousSessionFile`. | CHANGELOG.md |
| G-PI-CHANGELOG-332 | Breaking Changes | Removed sessionreplacement methods from `AgentSession`. Use `AgentSessionRuntime` for `newSession()`, `switchSession()`, `fork()`, and `importFromJsonl()`. Crosscwd session replacement rebuilds all cwdbound runtime state and replaces the live `AgentSession` instance. | CHANGELOG.md |
| G-PI-CHANGELOG-333 | Breaking Changes | Removed `session_directory` from extension and settings APIs. | CHANGELOG.md |
| G-PI-CHANGELOG-334 | Breaking Changes | Unknown singledash CLI flags (e.g. `s`) now produce an error instead of being silently ignored. | CHANGELOG.md |
| G-PI-CHANGELOG-335 | Added | Added `createAgentSessionRuntime()` and `AgentSessionRuntime` for runtimebacked session replacement. The runtime takes a `CreateAgentSessionRuntimeFactory` closure that closes over processglobal fixed inputs and recreates cwdbound services and session config for each effective cwd. Startup and later `/new`, `/resume`, `/fork`, import all use the same factory. | CHANGELOG.md |
| G-PI-CHANGELOG-336 | Added | Added unified diagnostics model (`info`/`warning`/`error`) for arg parsing, service creation, session option resolution, and resource loading. Creation logic no longer logs or exits. The app layer decides presentation and exit behavior. | CHANGELOG.md |
| G-PI-CHANGELOG-337 | Added | Added error diagnostics for missing explicit CLI resource paths (`e`, `skill`, `prompttemplate`, `theme`) | CHANGELOG.md |
| G-PI-CHANGELOG-338 | Added | Added `defineTool()` so standalone and arraybased custom tool definitions keep inferred parameter types without manual casts ([#2746](https://github.com/badlogic/pimono/issues/2746)) | CHANGELOG.md |
| G-PI-CHANGELOG-339 | Added | Added label timestamps to the session tree with a `Shift+T` toggle in `/tree`, smart date formatting, and timestamp preservation through branching ([#2691](https://github.com/badlogic/pimono/pull/2691) by [@wwinter](https://github.com/wwinter)) | CHANGELOG.md |
| G-PI-CHANGELOG-340 | Fixed | Fixed startup resource loading to reuse the initial `ResourceLoader` for the first runtime, so extensions are not loaded twice before session startup and `session_start` handlers still fire for singletonstyle extensions ([#2766](https://github.com/badlogic/pimono/issues/2766)) | CHANGELOG.md |
| G-PI-CHANGELOG-341 | Fixed | Fixed retry settlement so retried agent runs wait for the full retry cycle to complete before declaring idle, preventing stale state after transient errors | CHANGELOG.md |
| G-PI-CHANGELOG-342 | Fixed | Fixed theme `export` colors to resolve theme variables the same way as `colors`, so `/export` HTML backgrounds now honor entries like `pageBg: "base"` instead of requiring inline hex values ([#2707](https://github.com/badlogic/pimono/issues/2707)) | CHANGELOG.md |
| G-PI-CHANGELOG-343 | Fixed | Fixed Bedrock throttling errors being misidentified as context overflow, causing unnecessary compaction instead of retry ([#2699](https://github.com/badlogic/pimono/pull/2699) by [@xu0o0](https://github.com/xu0o0)) | CHANGELOG.md |
| G-PI-CHANGELOG-344 | Fixed | Added tool streaming support for newer Z.ai models ([#2732](https://github.com/badlogic/pimono/pull/2732) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-345 | New Features | Extensions and SDK callers can attach a `prepareArguments` hook to any tool definition, letting them normalize or migrate raw model arguments before schema validation. The builtin `edit` tool uses this to transparently support sessions created with the old singleedit schema. See [docs/extensions.md](docs/extensions.md) | CHANGELOG.md |
| G-PI-CHANGELOG-346 | New Features | Extensions can customize the collapsed thinking block label via `ctx.ui.setHiddenThinkingLabel()`. See [examples/extensions/hiddenthinkinglabel.ts](examples/extensions/hiddenthinkinglabel.ts) ([#2673](https://github.com/badlogic/pimono/issues/2673)) | CHANGELOG.md |
| G-PI-CHANGELOG-347 | Breaking Changes | `ModelRegistry` no longer has a public constructor. SDK callers and tests must use `ModelRegistry.create(authStorage, modelsJsonPath?)` for filebacked registries or `ModelRegistry.inMemory(authStorage)` for builtinonly registries. Direct `new ModelRegistry(...)` calls no longer compile. | CHANGELOG.md |
| G-PI-CHANGELOG-348 | Added | Added `ToolDefinition.prepareArguments` hook to prepare raw tool call arguments before schema validation, enabling compatibility shims for resumed sessions with outdated tool schemas | CHANGELOG.md |
| G-PI-CHANGELOG-349 | Added | Builtin `edit` tool now uses `prepareArguments` to silently fold legacy toplevel `oldText`/`newText` into `edits[]` when resuming old sessions | CHANGELOG.md |
| G-PI-CHANGELOG-350 | Added | Added `ctx.ui.setHiddenThinkingLabel()` so extensions can customize the collapsed thinking label in interactive mode, with a noop in RPC mode and a runnable example extension in `examples/extensions/hiddenthinkinglabel.ts` ([#2673](https://github.com/badlogic/pimono/issues/2673)) | CHANGELOG.md |
| G-PI-CHANGELOG-351 | Fixed | Fixed extensionqueued user messages to refresh the interactive pendingmessage list so messages submitted while a turn is active are no longer silently dropped ([#2674](https://github.com/badlogic/pimono/pull/2674) by [@mrexodia](https://github.com/mrexodia)) | CHANGELOG.md |
| G-PI-CHANGELOG-352 | Fixed | Fixed monorepo `tsconfig.json` path mappings to resolve `@mariozechner/piai` subpath exports to source files in development checkouts ([#2625](https://github.com/badlogic/pimono/pull/2625) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-353 | Fixed | Fixed TUI cell size response handling to consume only exact `CSI 6 ; height ; width t` replies, so bare `Escape` is no longer swallowed while waiting for terminal image metadata ([#2661](https://github.com/badlogic/pimono/issues/2661)) | CHANGELOG.md |
| G-PI-CHANGELOG-354 | Fixed | Fixed Kitty keyboard protocol keypad functional keys to normalize to logical digits, symbols, and navigation keys, so numpad input in terminals such as iTerm2 no longer inserts Private Use Area gibberish or gets ignored ([#2650](https://github.com/badlogic/pimono/issues/2650)) | CHANGELOG.md |
| G-PI-CHANGELOG-355 | New Features | Extension handlers can now use `ctx.signal` to forward cancellation into nested model calls, `fetch()`, and other abortaware work. See [docs/extensions.md#ctxsignal](docs/extensions.md#ctxsignal) ([#2660](https://github.com/badlogic/pimono/issues/2660)) | CHANGELOG.md |
| G-PI-CHANGELOG-356 | New Features | Builtin `edit` tool input now uses `edits[]` as the only replacement shape, reducing invalid tool calls caused by mixed singleedit and multiedit schemas ([#2639](https://github.com/badlogic/pimono/issues/2639)) | CHANGELOG.md |
| G-PI-CHANGELOG-357 | New Features | Large multiedit results no longer trigger fullscreen redraws in the interactive TUI when the final diff is rendered ([#2664](https://github.com/badlogic/pimono/issues/2664)) | CHANGELOG.md |
| G-PI-CHANGELOG-358 | Added | Added `ctx.signal` to `ExtensionContext` and wired it to the active agent turn so extension handlers can forward cancellation into nested model calls, `fetch()`, and other abortaware work ([#2660](https://github.com/badlogic/pimono/issues/2660)) | CHANGELOG.md |
| G-PI-CHANGELOG-359 | Fixed | Fixed builtin `edit` tool input to use `edits[]` as the only replacement shape, eliminating the mixed singleedit and multiedit modes that caused repeated invalid tool calls and retries ([#2639](https://github.com/badlogic/pimono/issues/2639)) | CHANGELOG.md |
| G-PI-CHANGELOG-360 | Fixed | Fixed edit tool TUI rendering to defer large multiedit diffs to the settled result, avoiding fullscreen redraws when the tool completes ([#2664](https://github.com/badlogic/pimono/issues/2664)) | CHANGELOG.md |
| G-PI-CHANGELOG-361 | Added | Added `gemini3.1propreviewcustomtools` model availability for the `googlevertex` provider ([#2610](https://github.com/badlogic/pimono/pull/2610) by [@gordonhwc](https://github.com/gordonhwc)) | CHANGELOG.md |
| G-PI-CHANGELOG-362 | Fixed | Documented `tool_call` input mutation as supported extension API behavior, clarified that postmutation inputs are not revalidated, and added regression coverage for executing mutated tool arguments ([#2611](https://github.com/badlogic/pimono/issues/2611)) | CHANGELOG.md |
| G-PI-CHANGELOG-363 | Fixed | Fixed repeated compactions dropping messages that were kept by an earlier compaction by resummarizing from the previous kept boundary and recalculating `tokensBefore` from the rebuilt session context ([#2608](https://github.com/badlogic/pimono/issues/2608)) | CHANGELOG.md |
| G-PI-CHANGELOG-364 | Fixed | Fixed interactive compaction UI updates so `ctx.compact()` rebuilds the chat through unified compaction events, manual compaction no longer duplicates the summary block, and the `triggercompact` example only fires when context usage crosses its threshold ([#2617](https://github.com/badlogic/pimono/issues/2617)) | CHANGELOG.md |
| G-PI-CHANGELOG-365 | Fixed | Fixed interactive compaction completion to append a synthetic compaction summary after rebuilding the chat so the latest compaction remains visible at the bottom | CHANGELOG.md |
| G-PI-CHANGELOG-366 | Fixed | Fixed skill discovery to stop recursing once a directory contains `SKILL.md`, and to ignore root `.md` files in `.agents/skills` while keeping root markdown skill files supported in `~/.pi/agent/skills`, `.pi/skills`, and package `skills/` directories ([#2603](https://github.com/badlogic/pimono/issues/2603)) | CHANGELOG.md |
| G-PI-CHANGELOG-367 | Fixed | Fixed edit tool diff rendering for multiedit operations with large unchanged gaps so distant edits collapse intermediate context instead of dumping the full unchanged middle block | CHANGELOG.md |
| G-PI-CHANGELOG-368 | Fixed | Fixed edit tool error rendering to avoid repeating the same exactmatch failure in both the preview and result blocks | CHANGELOG.md |
| G-PI-CHANGELOG-369 | Fixed | Fixed autocompaction overflow recovery for Ollama models when the backend returns explicit `prompt too long; exceeded max context length ...` errors instead of silently truncating input ([#2626](https://github.com/badlogic/pimono/issues/2626)) | CHANGELOG.md |
| G-PI-CHANGELOG-370 | Fixed | Fixed builtin tool overrides that reuse builtin parameter schemas to still honor custom `renderCall` and `renderResult` renderers in the interactive TUI, restoring the `minimalmode` example ([#2595](https://github.com/badlogic/pimono/issues/2595)) | CHANGELOG.md |
| G-PI-CHANGELOG-371 | Breaking Changes | `ModelRegistry.getApiKey(model)` has been replaced by `getApiKeyAndHeaders(model)` because `models.json` auth and header values can now resolve dynamically on every request. Extensions and SDK integrations that previously fetched only an API key must now fetch request auth per call and forward both `apiKey` and `headers`. Use `getApiKeyForProvider(provider)` only when you explicitly want providerlevel API key lookup without model headers or `authHeader` handling ([#1835](https://github.com/badlogic/pimono/issues/1835)) | CHANGELOG.md |
| G-PI-CHANGELOG-372 | Breaking Changes | Removed deprecated direct `minimax` and `minimaxcn` model IDs, keeping only `MiniMaxM2.7` and `MiniMaxM2.7highspeed`. Update pinned model IDs to one of those supported direct MiniMax models, or use another provider route that still exposes the older IDs ([#2596](https://github.com/badlogic/pimono/pull/2596) by [@liyuan97](https://github.com/liyuan97)) | CHANGELOG.md |
| G-PI-CHANGELOG-373 | Added | Added `sessionDir` setting support in global and project `settings.json` so session storage can be configured without passing `sessiondir` on every invocation ([#2598](https://github.com/badlogic/pimono/pull/2598) by [@smcllns](https://github.com/smcllns)) | CHANGELOG.md |
| G-PI-CHANGELOG-374 | Added | Added a startup onboarding hint in the interactive header telling users pi can explain its own features and documentation ([#2620](https://github.com/badlogic/pimono/pull/2620) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-375 | Added | Added `edit` tool multiedit support so one call can update multiple separate, disjoint regions in the same file while matching all replacements against the original file content | CHANGELOG.md |
| G-PI-CHANGELOG-376 | Added | Added support for `PI_TUI_WRITE_LOG` directory paths, creating a unique log file (`tui<timestamp><pid>.log`) per instance for easier debugging of multiple pi sessions ([#2508](https://github.com/badlogic/pimono/pull/2508) by [@mrexodia](https://github.com/mrexodia)) | CHANGELOG.md |
| G-PI-CHANGELOG-377 | Fixed | Fixed file mutation queue ordering so concurrent `edit` and `write` operations targeting the same file stay serialized in request order instead of being reordered during queuekey resolution | CHANGELOG.md |
| G-PI-CHANGELOG-378 | Fixed | Fixed `models.json` shellcommand auth and headers to resolve at request time instead of being cached into longlived model state. pi now leaves TTL, caching, and recovery policy to userprovided wrapper commands because arbitrary shell commands need providerspecific strategies ([#1835](https://github.com/badlogic/pimono/issues/1835)) | CHANGELOG.md |
| G-PI-CHANGELOG-379 | Fixed | Fixed Google and Vertex cost calculation to subtract cached prompt tokens from billable input tokens instead of doublecounting them when providers report `cachedContentTokenCount` ([#2588](https://github.com/badlogic/pimono/pull/2588) by [@sparkleMing](https://github.com/sparkleMing)) | CHANGELOG.md |
| G-PI-CHANGELOG-380 | Fixed | Added missing `ajv` direct dependency; previously relied on transitive install via `@mariozechner/piai` which broke standalone installs ([#2252](https://github.com/badlogic/pimono/issues/2252)) | CHANGELOG.md |
| G-PI-CHANGELOG-381 | Fixed | Fixed `/export` HTML backgrounds to honor `theme.export.pageBg`, `cardBg`, and `infoBg` instead of always deriving them from `userMessageBg` ([#2565](https://github.com/badlogic/pimono/issues/2565)) | CHANGELOG.md |
| G-PI-CHANGELOG-382 | Fixed | Fixed interactive bash execution collapsed previews to recompute visual line wrapping at render time, so previews respect the current terminal width after resizes and splitpane width changes ([#2569](https://github.com/badlogic/pimono/issues/2569)) | CHANGELOG.md |
| G-PI-CHANGELOG-383 | Fixed | Fixed RPC `get_session_stats` to expose `contextUsage`, so headless clients can read actual current contextwindow usage instead of deriving it from token totals ([#2550](https://github.com/badlogic/pimono/issues/2550)) | CHANGELOG.md |
| G-PI-CHANGELOG-384 | Fixed | Fixed `pi update` for git packages to fetch only the tracked target branch with `notags`, reducing unrelated branch and tag noise while preserving forcepushsafe updates ([#2548](https://github.com/badlogic/pimono/issues/2548)) | CHANGELOG.md |
| G-PI-CHANGELOG-385 | Fixed | Fixed print and JSON modes to emit `session_shutdown` before exit, so extensions can release longlived resources and noninteractive runs terminate cleanly ([#2576](https://github.com/badlogic/pimono/issues/2576)) | CHANGELOG.md |
| G-PI-CHANGELOG-386 | Fixed | Fixed GitHub Copilot OpenAI Responses requests to omit the `reasoning` field entirely when no reasoning effort is requested, avoiding `400` errors from Copilot `gpt5mini` rejecting `reasoning: { effort: "none" }` during internal summary calls ([#2567](https://github.com/badlogic/pimono/issues/2567)) | CHANGELOG.md |
| G-PI-CHANGELOG-387 | Fixed | Fixed blockquote text color breaking after inline links (and other inline elements) due to missing style restoration prefix | CHANGELOG.md |
| G-PI-CHANGELOG-388 | Fixed | Fixed slashcommand Tab completion from immediately chaining into argument autocomplete after completing the command name, restoring flows like `/model` that submit into a selector dialog ([#2577](https://github.com/badlogic/pimono/issues/2577)) | CHANGELOG.md |
| G-PI-CHANGELOG-389 | Fixed | Fixed stale content and incorrect viewport tracking after TUI content shrinks or transient components inflate the working area ([#2126](https://github.com/badlogic/pimono/pull/2126) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-390 | Fixed | Fixed `@` autocomplete to debounce editortriggered searches, cancel inflight `fd` lookups cleanly, and keep suggestions visible while results refresh ([#1278](https://github.com/badlogic/pimono/issues/1278)) | CHANGELOG.md |
| G-PI-CHANGELOG-391 | New Features | Builtin tools as extensible ToolDefinitions. Extension authors can now override rendering of builtin read/write/edit/bash/grep/find/ls tools with custom `renderCall`/`renderResult` components. See [docs/extensions.md](docs/extensions.md). | CHANGELOG.md |
| G-PI-CHANGELOG-392 | New Features | Unified source provenance via `sourceInfo`. All resources, commands, tools, skills, and prompt templates now carry structured `sourceInfo` with path, scope, and source metadata. Visible in autocomplete, RPC discovery, and SDK introspection. See [docs/extensions.md](docs/extensions.md). | CHANGELOG.md |
| G-PI-CHANGELOG-393 | New Features | AWS Bedrock cost allocation tagging. New `requestMetadata` option on `BedrockOptions` forwards keyvalue pairs to the Bedrock Converse API for AWS Cost Explorer split cost allocation. | CHANGELOG.md |
| G-PI-CHANGELOG-394 | Breaking Changes | Changed `ToolDefinition.renderCall` and `renderResult` semantics. Fallback rendering now happens only when a renderer is not defined for that slot. If `renderCall` or `renderResult` is defined, it must return a `Component`. | CHANGELOG.md |
| G-PI-CHANGELOG-395 | Breaking Changes | Changed slash command provenance to use `sourceInfo` consistently. RPC `get_commands`, `RpcSlashCommand`, and SDK `SlashCommandInfo` no longer expose `location` or `path`. Use `sourceInfo` instead ([#1734](https://github.com/badlogic/pimono/issues/1734)) | CHANGELOG.md |
| G-PI-CHANGELOG-396 | Breaking Changes | Removed legacy `source` fields from `Skill` and `PromptTemplate`. Use `sourceInfo.source` for provenance instead ([#1734](https://github.com/badlogic/pimono/issues/1734)) | CHANGELOG.md |
| G-PI-CHANGELOG-397 | Breaking Changes | Removed `ResourceLoader.getPathMetadata()`. Resource provenance is now attached directly to loaded resources via `sourceInfo` ([#1734](https://github.com/badlogic/pimono/issues/1734)) | CHANGELOG.md |
| G-PI-CHANGELOG-398 | Breaking Changes | Removed `extensionPath` from `RegisteredCommand` and `RegisteredTool`. Use `sourceInfo.path` for provenance instead ([#1734](https://github.com/badlogic/pimono/issues/1734)) | CHANGELOG.md |
| G-PI-CHANGELOG-399 | Migration Notes | RPC `get_commands`: replace `path` and `location` with `sourceInfo.path`, `sourceInfo.scope`, and `sourceInfo.source` | CHANGELOG.md |
| G-PI-CHANGELOG-400 | Migration Notes | `SlashCommandInfo`: replace `command.path` and `command.location` with `command.sourceInfo` | CHANGELOG.md |
| G-PI-CHANGELOG-401 | Migration Notes | `Skill` and `PromptTemplate`: replace `.source` with `.sourceInfo.source` | CHANGELOG.md |
| G-PI-CHANGELOG-402 | Migration Notes | `RegisteredCommand` and `RegisteredTool`: replace `.extensionPath` with `.sourceInfo.path` | CHANGELOG.md |
| G-PI-CHANGELOG-403 | Migration Notes | Custom `ResourceLoader` implementations: remove `getPathMetadata()` and read provenance from loaded resources directly | CHANGELOG.md |
| G-PI-CHANGELOG-404 | Migration Notes | `command.path` > `command.sourceInfo.path` | CHANGELOG.md |
| G-PI-CHANGELOG-405 | Migration Notes | `command.location === "user"` > `command.sourceInfo.scope === "user"` | CHANGELOG.md |
| G-PI-CHANGELOG-406 | Migration Notes | `skill.source` > `skill.sourceInfo.source` | CHANGELOG.md |
| G-PI-CHANGELOG-407 | Migration Notes | `tool.extensionPath` > `tool.sourceInfo.path` | CHANGELOG.md |
| G-PI-CHANGELOG-408 | Changed | Builtin tools now work like custom tools in extensions. To get builtin tool definitions, import `readToolDefinition` / `createReadToolDefinition()` and the equivalent `bash`, `edit`, `write`, `grep`, `find`, and `ls` exports from `@mariozechner/picodingagent`. | CHANGELOG.md |
| G-PI-CHANGELOG-409 | Changed | Cleaned up `buildSystemPrompt()` so builtin tool snippets and toollocal guidelines come from builtin `ToolDefinition` metadata, while crosstool and global prompt rules stay in system prompt construction. | CHANGELOG.md |
| G-PI-CHANGELOG-410 | Changed | Added structured `sourceInfo` to `pi.getAllTools()` results for builtin, SDK, and extension tools ([#1734](https://github.com/badlogic/pimono/issues/1734)) | CHANGELOG.md |
| G-PI-CHANGELOG-411 | Fixed | Fixed extension command name conflicts so extensions with duplicate command names can load together. Conflicting extension commands now get numeric invocation suffixes in load order, for example `/review:1` and `/review:2` ([#1061](https://github.com/badlogic/pimono/issues/1061)) | CHANGELOG.md |
| G-PI-CHANGELOG-412 | Fixed | Fixed slash command source attribution for extension commands, prompt templates, and skills in autocomplete and command discovery ([#1734](https://github.com/badlogic/pimono/issues/1734)) | CHANGELOG.md |
| G-PI-CHANGELOG-413 | Fixed | Fixed autoresized image handling to enforce the inline image size limit on the final base64 payload, return textonly fallbacks when resizing cannot produce a safe image, and avoid falling back to the original image in `read` and `@file` autoresize paths ([#2055](https://github.com/badlogic/pimono/issues/2055)) | CHANGELOG.md |
| G-PI-CHANGELOG-414 | Fixed | Fixed `pi update` for git packages to skip destructive reset, clean, and reinstall steps when the fetched target already matches the local checkout ([#2503](https://github.com/badlogic/pimono/issues/2503)) | CHANGELOG.md |
| G-PI-CHANGELOG-415 | Fixed | Fixed print and JSON mode to take over stdout during noninteractive startup, keeping packagemanager and other incidental chatter off protocol/output stdout ([#2482](https://github.com/badlogic/pimono/issues/2482)) | CHANGELOG.md |
| G-PI-CHANGELOG-416 | Fixed | Fixed clihighlight autodetection for languageless code blocks that misidentified prose as programming languages and colored random English words as keywords | CHANGELOG.md |
| G-PI-CHANGELOG-417 | Fixed | Fixed Anthropic thinking disable handling to send `thinking: { type: "disabled" }` for reasoningcapable models when thinking is explicitly off ([#2022](https://github.com/badlogic/pimono/issues/2022)) | CHANGELOG.md |
| G-PI-CHANGELOG-418 | Fixed | Fixed explicit thinking disable handling across Google, Google Vertex, Gemini CLI, OpenAI Responses, Azure OpenAI Responses, and OpenRouterbacked OpenAIcompatible completions ([#2490](https://github.com/badlogic/pimono/issues/2490)) | CHANGELOG.md |
| G-PI-CHANGELOG-419 | Fixed | Fixed OpenAI Responses replay for foreign toolcall item IDs by hashing foreign IDs into bounded `fc_<hash>` IDs | CHANGELOG.md |
| G-PI-CHANGELOG-420 | Fixed | Fixed OpenAIcompatible completions streams to ignore null chunks instead of crashing ([#2466](https://github.com/badlogic/pimono/pull/2466) by [@ChengZiQing](https://github.com/ChengZiQing)) | CHANGELOG.md |
| G-PI-CHANGELOG-421 | Fixed | Fixed `truncateToWidth()` performance for very large strings by streaming truncation ([#2447](https://github.com/badlogic/pimono/issues/2447)) | CHANGELOG.md |
| G-PI-CHANGELOG-422 | Fixed | Fixed markdown heading styling being lost after inline code spans within headings | CHANGELOG.md |
| G-PI-CHANGELOG-423 | New Features | Typed `tool_call` handler return values via `ToolCallEventResult` exports from the toplevel package and core extension entry. See [docs/extensions.md](docs/extensions.md). | CHANGELOG.md |
| G-PI-CHANGELOG-424 | New Features | Updated default models for `zai`, `cerebras`, `minimax`, and `minimaxcn`, and aligned MiniMax catalog coverage and limits with the current provider lineup. See [docs/models.md](docs/models.md) and [docs/providers.md](docs/providers.md). | CHANGELOG.md |
| G-PI-CHANGELOG-425 | Added | Added `ToolCallEventResult` to the `@mariozechner/picodingagent` toplevel and core extension exports so extension authors can type explicit `tool_call` handler return values ([#2458](https://github.com/badlogic/pimono/issues/2458)) | CHANGELOG.md |
| G-PI-CHANGELOG-426 | Changed | Changed the default models for `zai`, `cerebras`, `minimax`, and `minimaxcn` to match the current provider lineup, and added missing `MiniMaxM2.1highspeed` model entries with normalized MiniMax context limits ([#2445](https://github.com/badlogic/pimono/pull/2445) by [@1500256797](https://github.com/1500256797)) | CHANGELOG.md |
| G-PI-CHANGELOG-427 | Fixed | Fixed `ctrl+z` suspend and `fg` resume reliability by keeping the process alive until the `SIGCONT` handler restores the TUI, avoiding immediate process exit in environments with no other live eventloop handles ([#2454](https://github.com/badlogic/pimono/issues/2454)) | CHANGELOG.md |
| G-PI-CHANGELOG-428 | Fixed | Fixed `createAgentSession({ agentDir })` to derive the default persisted session path from the provided `agentDir`, keeping session storage aligned with settings, auth, models, and resource loading ([#2457](https://github.com/badlogic/pimono/issues/2457)) | CHANGELOG.md |
| G-PI-CHANGELOG-429 | Fixed | Fixed shared keybinding resolution to stop user overrides from evicting unrelated default shortcuts such as selector confirm and editor cursor keys ([#2455](https://github.com/badlogic/pimono/issues/2455)) | CHANGELOG.md |
| G-PI-CHANGELOG-430 | Fixed | Fixed Termux software keyboard height changes from forcing fullscreen redraws and replaying TUI history on every toggle ([#2467](https://github.com/badlogic/pimono/issues/2467)) | CHANGELOG.md |
| G-PI-CHANGELOG-431 | Fixed | Fixed projectlocal npm package updates to install npm `latest` instead of reusing stale saved dependency ranges, and added `Did you mean ...?` suggestions when `pi update <source>` omits the configured npm or git source prefix ([#2459](https://github.com/badlogic/pimono/issues/2459)) | CHANGELOG.md |
| G-PI-CHANGELOG-432 | New Features | Namespaced keybinding ids and a unified keybinding manager across the app and TUI. See [docs/keybindings.md](docs/keybindings.md) and [docs/extensions.md](docs/extensions.md). | CHANGELOG.md |
| G-PI-CHANGELOG-433 | New Features | JSONL session export and import via `/export <path.jsonl>` and `/import <path.jsonl>`. See [README.md](README.md) and [docs/session.md](docs/session.md). | CHANGELOG.md |
| G-PI-CHANGELOG-434 | New Features | Resizable sidebar in HTML share and export views. See [README.md](README.md). | CHANGELOG.md |
| G-PI-CHANGELOG-435 | Breaking Changes | Interactive keybinding ids are now namespaced, and `keybindings.json` now uses those same canonical namespaced ids. Older config files are migrated automatically on startup. Custom editors and extension UI components still receive an injected `keybindings: KeybindingsManager`. They do not call `getKeybindings()` or `setKeybindings()` themselves. Declaration merging applies to that injected type ([#2391](https://github.com/badlogic/pimono/issues/2391)) | CHANGELOG.md |
| G-PI-CHANGELOG-436 | Breaking Changes | Extension author migration: update `keyHint()`, `keyText()`, and injected `keybindings.matches(...)` calls from old builtin names like `"expandTools"`, `"selectConfirm"`, and `"interrupt"` to namespaced ids like `"app.tools.expand"`, `"tui.select.confirm"`, and `"app.interrupt"`. See [docs/keybindings.md](docs/keybindings.md) for the full list. `pi.registerShortcut("ctrl+shift+p", ...)` is unchanged because extension shortcuts still use raw key combos, not keybinding ids. | CHANGELOG.md |
| G-PI-CHANGELOG-437 | Added | Added `gpt5.4mini` to the `openaicodex` model catalog ([#2334](https://github.com/badlogic/pimono/pull/2334) by [@justram](https://github.com/justram)) | CHANGELOG.md |
| G-PI-CHANGELOG-438 | Added | Added JSONL session export and import via `/export <path.jsonl>` and `/import <path.jsonl>` ([#2356](https://github.com/badlogic/pimono/pull/2356) by [@hjanuschka](https://github.com/hjanuschka)) | CHANGELOG.md |
| G-PI-CHANGELOG-439 | Added | Added a resizable sidebar to HTML share and export views ([#2435](https://github.com/badlogic/pimono/pull/2435) by [@dmmulroy](https://github.com/dmmulroy)) | CHANGELOG.md |
| G-PI-CHANGELOG-440 | Fixed | Tests for sessionselectorrename and treeselector are now keybindingagnostic, resetting editor keybindings to defaults before each test so user `keybindings.json` cannot cause failures ([#2360](https://github.com/badlogic/pimono/issues/2360)) | CHANGELOG.md |
| G-PI-CHANGELOG-441 | Fixed | Fixed custom `keybindings.json` overrides to shadow conflicting default shortcuts globally, so bindings such as `cursorUp: ["up", "ctrl+p"]` no longer leave default actions like model cycling active ([#2391](https://github.com/badlogic/pimono/issues/2391)) | CHANGELOG.md |
| G-PI-CHANGELOG-442 | Fixed | Fixed concurrent `edit` and `write` mutations targeting the same file to run serially, preventing interleaved file writes from overwriting each other ([#2327](https://github.com/badlogic/pimono/issues/2327)) | CHANGELOG.md |
| G-PI-CHANGELOG-443 | Fixed | Fixed RPC mode to redirect unexpected stdout writes to stderr so JSONL responses remain parseable ([#2388](https://github.com/badlogic/pimono/issues/2388)) | CHANGELOG.md |
| G-PI-CHANGELOG-444 | Fixed | Fixed autoretry with toolusing retry responses so `session.prompt()` waits for the full retry loop, including tool execution, before returning ([#2440](https://github.com/badlogic/pimono/pull/2440) by [@pasky](https://github.com/pasky)) | CHANGELOG.md |
| G-PI-CHANGELOG-445 | Fixed | Fixed `/model` to refresh scoped model lists after `models.json` changes, avoiding stale selector contents ([#2408](https://github.com/badlogic/pimono/pull/2408) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-446 | Fixed | Fixed `validateToolArguments()` to fall back gracefully when AJV schema compilation is blocked in restricted runtimes such as Cloudflare Workers, allowing tool execution to proceed without schema validation ([#2395](https://github.com/badlogic/pimono/issues/2395)) | CHANGELOG.md |
| G-PI-CHANGELOG-447 | Fixed | Fixed CLI startup to suppress process warnings from leaking into terminal, print, and RPC output ([#2404](https://github.com/badlogic/pimono/issues/2404)) | CHANGELOG.md |
| G-PI-CHANGELOG-448 | Fixed | Fixed bash tool rendering to show elapsed time at the bottom of the tool block ([#2406](https://github.com/badlogic/pimono/issues/2406)) | CHANGELOG.md |
| G-PI-CHANGELOG-449 | Fixed | Fixed custom theme file watching to reload updated theme contents from disk instead of keeping stale cached theme data ([#2417](https://github.com/badlogic/pimono/issues/2417), [#2003](https://github.com/badlogic/pimono/issues/2003)) | CHANGELOG.md |
| G-PI-CHANGELOG-450 | Fixed | Fixed footer Git branch refreshes to run asynchronously so branch watcher updates do not block the UI ([#2418](https://github.com/badlogic/pimono/issues/2418)) | CHANGELOG.md |
| G-PI-CHANGELOG-451 | Fixed | Fixed invalid extension provider registrations to surface an extension error without preventing other providers from loading ([#2431](https://github.com/badlogic/pimono/issues/2431)) | CHANGELOG.md |
| G-PI-CHANGELOG-452 | Fixed | Fixed Windows bash execution hanging for commands that spawn detached descendants inheriting stdout/stderr handles, which caused `agentbrowser` and similar commands to spin forever ([#2389](https://github.com/badlogic/pimono/pull/2389) by [@mrexodia](https://github.com/mrexodia)) | CHANGELOG.md |
| G-PI-CHANGELOG-453 | Fixed | Fixed `googlevertex` API key resolution to ignore placeholder auth markers like `<authenticated>` and fall back to ADC instead of sending them as literal API keys ([#2335](https://github.com/badlogic/pimono/issues/2335)) | CHANGELOG.md |
| G-PI-CHANGELOG-454 | Fixed | Fixed desktop clipboard text copy to prefer native OS clipboard integration before shell fallbacks, improving reliability on macOS and Windows ([#2347](https://github.com/badlogic/pimono/issues/2347)) | CHANGELOG.md |
| G-PI-CHANGELOG-455 | Fixed | Fixed Bun Bedrock provider registration to survive provider resets and session reloads in compiled binaries ([#2350](https://github.com/badlogic/pimono/pull/2350) by [@unexge](https://github.com/unexge)) | CHANGELOG.md |
| G-PI-CHANGELOG-456 | Fixed | Fixed OpenRouter reasoning requests to use the provider's nested reasoning payload, restoring thinking level support for OpenRouter models and custom compat settings ([#2298](https://github.com/badlogic/pimono/pull/2298) by [@PriNova](https://github.com/PriNova)) | CHANGELOG.md |
| G-PI-CHANGELOG-457 | Fixed | Fixed Bedrock application inference profiles to support prompt caching when `AWS_BEDROCK_FORCE_CACHE=1` is set, covering profile ARNs that do not expose the underlying Claude model name ([#2346](https://github.com/badlogic/pimono/pull/2346) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-458 | New Features | Fork existing sessions directly from the CLI with `fork <path|id>`, which copies a source session into a new session in the current project. See [README.md](README.md). | CHANGELOG.md |
| G-PI-CHANGELOG-459 | New Features | Extensions and SDK callers can reuse pi's builtin local bash backend via `createLocalBashOperations()` for `user_bash` interception and custom bash integrations. See [docs/extensions.md#user_bash](docs/extensions.md#user_bash). | CHANGELOG.md |
| G-PI-CHANGELOG-460 | New Features | Startup no longer updates unpinned npm and git packages automatically. Use `pi update` explicitly, while interactive mode checks for updates in the background and notifies you when newer packages are available. See [README.md](README.md). | CHANGELOG.md |
| G-PI-CHANGELOG-461 | Breaking Changes | Changed package startup behavior so installed unpinned packages are no longer checked or updated during startup. Use `pi update` to apply npm/git package updates, while interactive mode now checks for available package updates in the background and notifies you when updates are available ([#1963](https://github.com/badlogic/pimono/issues/1963)) | CHANGELOG.md |
| G-PI-CHANGELOG-462 | Added | Added `fork <path|id>` CLI flag to fork an existing session file or partial session UUID directly into a new session ([#2290](https://github.com/badlogic/pimono/issues/2290)) | CHANGELOG.md |
| G-PI-CHANGELOG-463 | Added | Added `createLocalBashOperations()` export so extensions and SDK callers can wrap pi's builtin local bash backend for `user_bash` handling and other custom bash integrations ([#2299](https://github.com/badlogic/pimono/issues/2299)) | CHANGELOG.md |
| G-PI-CHANGELOG-464 | Fixed | Fixed active model selection to refresh immediately after dynamic provider registrations or updates change the available model set ([#2291](https://github.com/badlogic/pimono/issues/2291)) | CHANGELOG.md |
| G-PI-CHANGELOG-465 | Fixed | Fixed tmux xterm `modifyOtherKeys` matching for `Backspace`, `Escape`, and `Space`, and resolved raw `\x08` backspace ambiguity by treating Windows Terminal sessions differently from legacy terminals ([#2293](https://github.com/badlogic/pimono/issues/2293)) | CHANGELOG.md |
| G-PI-CHANGELOG-466 | Fixed | Fixed Gemini 3 and Antigravity image tool results to stay inline as multimodal tool responses instead of being rerouted through separate followup messages ([#2052](https://github.com/badlogic/pimono/issues/2052)) | CHANGELOG.md |
| G-PI-CHANGELOG-467 | Fixed | Fixed bundled Bedrock Claude 4.6 model metadata to use the correct 200K context window instead of 1M ([#2305](https://github.com/badlogic/pimono/issues/2305)) | CHANGELOG.md |
| G-PI-CHANGELOG-468 | Fixed | Fixed `/reload` to reload keybindings from disk so changes in `keybindings.json` apply immediately ([#2309](https://github.com/badlogic/pimono/issues/2309)) | CHANGELOG.md |
| G-PI-CHANGELOG-469 | Fixed | Fixed lazy builtin provider registration so compiled Bun binaries can still load providers on first use without eagerly bundling provider SDKs ([#2314](https://github.com/badlogic/pimono/issues/2314)) | CHANGELOG.md |
| G-PI-CHANGELOG-470 | Fixed | Fixed builtin OAuth login flows to use aligned callback handling across Anthropic, Gemini CLI, Antigravity, and OpenAI Codex, and fixed OpenAI Codex login to complete immediately once the browser callback succeeds ([#2316](https://github.com/badlogic/pimono/issues/2316)) | CHANGELOG.md |
| G-PI-CHANGELOG-471 | Fixed | Fixed OpenAIcompatible z.ai `network_error` responses to trigger error handling and retries instead of being treated as successful assistant output ([#2313](https://github.com/badlogic/pimono/issues/2313)) | CHANGELOG.md |
| G-PI-CHANGELOG-472 | Fixed | Fixed print mode to merge piped stdin into the initial prompt when both stdin and an explicit prompt are provided ([#2315](https://github.com/badlogic/pimono/issues/2315)) | CHANGELOG.md |
| G-PI-CHANGELOG-473 | Fixed | Fixed OpenAI Responses replay in codingagent to normalize oversized resumed tool call IDs before sending them back to OpenAI Codex and other Responsescompatible targets ([#2328](https://github.com/badlogic/pimono/issues/2328)) | CHANGELOG.md |
| G-PI-CHANGELOG-474 | Fixed | Fixed tmux extendedkeys warning to stay hidden when the tmux server is unreachable, avoiding false startup warnings in sandboxed environments ([#2311](https://github.com/badlogic/pimono/pull/2311) by [@kaffarell](https://github.com/kaffarell)) | CHANGELOG.md |
| G-PI-CHANGELOG-475 | New Features | Faster startup by lazyloading `@mariozechner/piai` provider SDKs on first use instead of import time ([#2297](https://github.com/badlogic/pimono/issues/2297)) | CHANGELOG.md |
| G-PI-CHANGELOG-476 | New Features | Better provider retry behavior when providers return error messages as responses ([#2264](https://github.com/badlogic/pimono/issues/2264)) | CHANGELOG.md |
| G-PI-CHANGELOG-477 | New Features | Better terminal integration via OSC 133 commandexecuted markers ([#2242](https://github.com/badlogic/pimono/issues/2242)) | CHANGELOG.md |
| G-PI-CHANGELOG-478 | New Features | Better Git footer branch detection for repositories using reftable storage ([#2300](https://github.com/badlogic/pimono/issues/2300)) | CHANGELOG.md |
| G-PI-CHANGELOG-479 | Breaking Changes | Changed custom tool system prompt behavior so extension and SDK tools are included in the default `Available tools` section only when they provide `promptSnippet`. Omitting `promptSnippet` now leaves the tool out of that section instead of falling back to `description` ([#2285](https://github.com/badlogic/pimono/issues/2285)) | CHANGELOG.md |
| G-PI-CHANGELOG-480 | Changed | Lazyload builtin `@mariozechner/piai` provider modules and root provider wrappers so codingagent startup no longer eagerly loads provider SDKs before first use ([#2297](https://github.com/badlogic/pimono/issues/2297)) | CHANGELOG.md |
| G-PI-CHANGELOG-481 | Fixed | Fixed session title handling in `/tree`, compaction, and branch summarization so empty title clears render correctly and `session_info` entries stay out of summaries ([#2304](https://github.com/badlogic/pimono/pull/2304) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-482 | Fixed | Fixed footer branch detection for Git repositories using reftable storage so branch names still appear correctly in the footer ([#2300](https://github.com/badlogic/pimono/issues/2300)) | CHANGELOG.md |
| G-PI-CHANGELOG-483 | Fixed | Fixed rendered user messages to emit an OSC 133 commandexecuted marker after command output, improving terminal prompt integration ([#2242](https://github.com/badlogic/pimono/issues/2242)) | CHANGELOG.md |
| G-PI-CHANGELOG-484 | Fixed | Fixed provider retry handling to treat providerreturned error messages as retryable failures instead of successful responses ([#2264](https://github.com/badlogic/pimono/issues/2264)) | CHANGELOG.md |
| G-PI-CHANGELOG-485 | Fixed | Fixed Claude 4.6 context window overrides in bundled model metadata so codingagent sees the intended model limits after generated catalogs are rebuilt ([#2286](https://github.com/badlogic/pimono/issues/2286)) | CHANGELOG.md |
| G-PI-CHANGELOG-486 | Fixed | Fixed steering messages to wait until the current assistant message's toolcall batch fully finishes instead of skipping pending tool calls. | CHANGELOG.md |
| G-PI-CHANGELOG-487 | Added | Improved settings, theme, thinking, and showimages selector layouts by using configurable selectlist primary column sizing ([#2154](https://github.com/badlogic/pimono/pull/2154) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-488 | Fixed | Fixed fuzzy `edit` matching to normalize Unicode compatibility variants before comparison, reducing false "oldText not found" failures for text such as CJK and fullwidth characters ([#2044](https://github.com/badlogic/pimono/issues/2044)) | CHANGELOG.md |
| G-PI-CHANGELOG-489 | Fixed | Fixed `/model <ref>` exact matching and picker search to recognize canonical `provider/model` references when model IDs themselves contain `/`, such as LM Studio models like `unsloth/qwen3.535ba3b` ([#2174](https://github.com/badlogic/pimono/issues/2174)) | CHANGELOG.md |
| G-PI-CHANGELOG-490 | Fixed | Fixed Anthropic OAuth manual login and token refresh by using the localhost callback URI for pasted redirect/code flows and omitting `scope` from refreshtoken requests ([#2169](https://github.com/badlogic/pimono/issues/2169)) | CHANGELOG.md |
| G-PI-CHANGELOG-491 | Fixed | Fixed stale scrollback remaining after session switches by clearing the screen before wiping scrollback ([#2155](https://github.com/badlogic/pimono/pull/2155) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-492 | Fixed | Fixed extra blank lines after markdown block elements in rendered output ([#2152](https://github.com/badlogic/pimono/pull/2152) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-493 | Added | Added `pi uninstall` alias for `pi install uninstall` convenience | CHANGELOG.md |
| G-PI-CHANGELOG-494 | Fixed | Fixed OpenAI Codex websocket protocol to include required headers and properly terminate SSE streams on connection close ([#1961](https://github.com/badlogic/pimono/issues/1961)) | CHANGELOG.md |
| G-PI-CHANGELOG-495 | Fixed | Fixed WSL clipboard image fallback to properly handle missing clipboard utilities and permission errors ([#1722](https://github.com/badlogic/pimono/issues/1722)) | CHANGELOG.md |
| G-PI-CHANGELOG-496 | Fixed | Fixed extension `session_start` hook firing before TUI was ready, causing UI operations in `session_start` handlers to fail ([#2035](https://github.com/badlogic/pimono/issues/2035)) | CHANGELOG.md |
| G-PI-CHANGELOG-497 | Fixed | Fixed Windows shell and path handling for package manager operations and autocomplete to properly handle drive letters and mixed path separators | CHANGELOG.md |
| G-PI-CHANGELOG-498 | Fixed | Fixed Bedrock prompt caching being enabled for nonClaude models, causing API errors ([#2053](https://github.com/badlogic/pimono/issues/2053)) | CHANGELOG.md |
| G-PI-CHANGELOG-499 | Fixed | Fixed Qwen models via OpenAIcompatible providers by adding `qwenchattemplate` compat mode that uses Qwen's native chat template format ([#2020](https://github.com/badlogic/pimono/issues/2020)) | CHANGELOG.md |
| G-PI-CHANGELOG-500 | Fixed | Fixed Bedrock unsigned thinking replay to handle edge cases with empty or malformed thinking blocks ([#2063](https://github.com/badlogic/pimono/issues/2063)) | CHANGELOG.md |
| G-PI-CHANGELOG-501 | Fixed | Fixed headless clipboard fallback logging spurious errors in noninteractive environments ([#2056](https://github.com/badlogic/pimono/issues/2056)) | CHANGELOG.md |
| G-PI-CHANGELOG-502 | Fixed | Fixed `models.json` provider compat flags not being honored when loading custom model definitions ([#2062](https://github.com/badlogic/pimono/issues/2062)) | CHANGELOG.md |
| G-PI-CHANGELOG-503 | Fixed | Fixed xhigh reasoning effort detection for Claude Opus 4.6 to match by model ID instead of requiring explicit capability flag ([#2040](https://github.com/badlogic/pimono/issues/2040)) | CHANGELOG.md |
| G-PI-CHANGELOG-504 | Fixed | Fixed prompt cwd containing Windows backslashes breaking bash tool execution by normalizing to forward slashes ([#2080](https://github.com/badlogic/pimono/issues/2080)) | CHANGELOG.md |
| G-PI-CHANGELOG-505 | Fixed | Fixed editor paste to preserve literal content instead of normalizing newlines, preventing content corruption for text with embedded escape sequences ([#2064](https://github.com/badlogic/pimono/issues/2064)) | CHANGELOG.md |
| G-PI-CHANGELOG-506 | Fixed | Fixed skill discovery recursing past skill root directories when nested SKILL.md files exist ([#2075](https://github.com/badlogic/pimono/issues/2075)) | CHANGELOG.md |
| G-PI-CHANGELOG-507 | Fixed | Fixed tab completion to preserve `./` prefix when completing relative paths ([#2087](https://github.com/badlogic/pimono/issues/2087)) | CHANGELOG.md |
| G-PI-CHANGELOG-508 | Fixed | Fixed npm package installs and lookups being tied to the active repository Node version by adding `npmCommand` as an argvstyle settings override for package manager operations ([#2072](https://github.com/badlogic/pimono/issues/2072)) | CHANGELOG.md |
| G-PI-CHANGELOG-509 | Fixed | Fixed `ctx.ui.getEditorText()` in the extension API returning paste markers (e.g., `[paste #1 +24 lines]`) instead of the actual pasted content ([#2084](https://github.com/badlogic/pimono/issues/2084)) | CHANGELOG.md |
| G-PI-CHANGELOG-510 | Fixed | Fixed startup crash when downloading `fd`/`ripgrep` on first run by using `pipeline()` instead of `finished(readable.pipe(writable))` so stream errors from timeouts are caught properly, and increased the download timeout from 10s to 120s ([#2066](https://github.com/badlogic/pimono/issues/2066)) | CHANGELOG.md |
| G-PI-CHANGELOG-511 | New Features | Claude Opus 4.6, Sonnet 4.6, and related Bedrock models now use a 1M token context window (up from 200K) ([#2135](https://github.com/badlogic/pimono/pull/2135) by [@mitsuhiko](https://github.com/mitsuhiko)). | CHANGELOG.md |
| G-PI-CHANGELOG-512 | New Features | Extension tool calls now execute in parallel by default, with sequential `tool_call` preflight preserved for extension interception. | CHANGELOG.md |
| G-PI-CHANGELOG-513 | New Features | `GOOGLE_CLOUD_API_KEY` environment variable support for the `googlevertex` provider as an alternative to Application Default Credentials ([#1976](https://github.com/badlogic/pimono/pull/1976) by [@gordonhwc](https://github.com/gordonhwc)). | CHANGELOG.md |
| G-PI-CHANGELOG-514 | New Features | Extensions can supply deterministic session IDs via `newSession()` ([#2130](https://github.com/badlogic/pimono/pull/2130) by [@zhahaoyu](https://github.com/zhahaoyu)). | CHANGELOG.md |
| G-PI-CHANGELOG-515 | Added | Added `GOOGLE_CLOUD_API_KEY` environment variable support for the `googlevertex` provider as an alternative to Application Default Credentials ([#1976](https://github.com/badlogic/pimono/pull/1976) by [@gordonhwc](https://github.com/gordonhwc)) | CHANGELOG.md |
| G-PI-CHANGELOG-516 | Added | Added custom session ID support in `newSession()` for extensions that need deterministic session paths ([#2130](https://github.com/badlogic/pimono/pull/2130) by [@zhahaoyu](https://github.com/zhahaoyu)) | CHANGELOG.md |
| G-PI-CHANGELOG-517 | Changed | Changed extension tool interception to use agentcore `beforeToolCall` and `afterToolCall` hooks instead of wrapperbased interception. Tool calls now execute in parallel by default, extension `tool_call` preflight still runs sequentially, and final tool results are emitted in assistant source order. | CHANGELOG.md |
| G-PI-CHANGELOG-518 | Changed | Raised Claude Opus 4.6, Sonnet 4.6, and related Bedrock model context windows from 200K to 1M tokens ([#2135](https://github.com/badlogic/pimono/pull/2135) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-519 | Fixed | Fixed `tool_call` extension handlers observing stale `sessionManager` state during multitool turns by draining queued agent events before each `tool_call` preflight. In parallel tool mode this guarantees state through the current assistant toolcalling message, but not sibling tool results from the same assistant message. | CHANGELOG.md |
| G-PI-CHANGELOG-520 | Fixed | Fixed interactive input fields backed by the TUI `Input` component to scroll by visual column width for wide Unicode text (CJK, fullwidth characters), preventing rendered line overflow and TUI crashes in places like search and filter inputs ([#1982](https://github.com/badlogic/pimono/issues/1982)) | CHANGELOG.md |
| G-PI-CHANGELOG-521 | Fixed | Fixed `shift+tab` and other modified Tab bindings in tmux when `extendedkeysformat` is left at the default `xterm` | CHANGELOG.md |
| G-PI-CHANGELOG-522 | Fixed | Fixed EXIF orientation not being applied during image convert and resize, causing JPEG and WebP images from phone cameras to display rotated or mirrored ([#2105](https://github.com/badlogic/pimono/pull/2105) by [@melihmucuk](https://github.com/melihmucuk)) | CHANGELOG.md |
| G-PI-CHANGELOG-523 | Fixed | Fixed the default codingagent system prompt to include only the current date in ISO format, not the current time, so prompt prefixes stay cacheable across reloads and resumed sessions ([#2131](https://github.com/badlogic/pimono/issues/2131)) | CHANGELOG.md |
| G-PI-CHANGELOG-524 | Fixed | Fixed retry regex to match `server_error` and `internal_error` error types from providers, improving automatic retry coverage ([#2117](https://github.com/badlogic/pimono/pull/2117) by [@MadKangYu](https://github.com/MadKangYu)) | CHANGELOG.md |
| G-PI-CHANGELOG-525 | Fixed | Fixed example extensions to support `PI_CODING_AGENT_DIR` environment variable for custom agent directory paths ([#2009](https://github.com/badlogic/pimono/pull/2009) by [@smithbm2316](https://github.com/smithbm2316)) | CHANGELOG.md |
| G-PI-CHANGELOG-526 | Fixed | Fixed tool result images not being sent in `function_call_output` items for OpenAI Responses API providers, causing image data to be silently dropped in tool results ([#2104](https://github.com/badlogic/pimono/issues/2104)) | CHANGELOG.md |
| G-PI-CHANGELOG-527 | Fixed | Fixed assistant content being sent as structured content blocks instead of plain strings in the `openaicompletions` provider, causing errors with some OpenAIcompatible backends ([#2008](https://github.com/badlogic/pimono/pull/2008) by [@geraldoaax](https://github.com/geraldoaax)) | CHANGELOG.md |
| G-PI-CHANGELOG-528 | Fixed | Fixed error details in OpenAI Responses `response.failed` handler to include status code, error code, and message instead of a generic failure ([#1956](https://github.com/badlogic/pimono/pull/1956) by [@drewburr](https://github.com/drewburr)) | CHANGELOG.md |
| G-PI-CHANGELOG-529 | Fixed | Fixed GitHub Copilot devicecode login polling to respect OAuth slowdown intervals, wait before the first token poll, and include a clearer clockdrift hint in WSL/VM environments when repeated slowdowns lead to timeout | CHANGELOG.md |
| G-PI-CHANGELOG-530 | Fixed | Fixed usage statistics not being captured for OpenAIcompatible providers that return usage in `choice.usage` instead of the standard `chunk.usage` (e.g., Moonshot/Kimi) ([#2017](https://github.com/badlogic/pimono/issues/2017)) | CHANGELOG.md |
| G-PI-CHANGELOG-531 | Fixed | Fixed editor scroll indicator rendering crash in narrow terminal widths ([#2103](https://github.com/badlogic/pimono/pull/2103) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-532 | Fixed | Fixed tab characters in editor and input paste not being normalized to spaces ([#2027](https://github.com/badlogic/pimono/pull/2027), [#1975](https://github.com/badlogic/pimono/pull/1975) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-533 | Fixed | Fixed `wordWrapLine` overflow when wide characters (CJK, fullwidth) fall exactly at the wrap boundary ([#2082](https://github.com/badlogic/pimono/pull/2082) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-534 | Fixed | Fixed paste markers not being treated as atomic segments in editor word wrapping and cursor navigation ([#2111](https://github.com/badlogic/pimono/pull/2111) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-535 | New Features | Tree branch folding and segmentjump navigation in `/tree`, with `Ctrl+←`/`Ctrl+→` and `Alt+←`/`Alt+→` shortcuts while `←`/`→` and `Page Up`/`Page Down` remain available for paging. See [docs/tree.md](docs/tree.md) and [docs/keybindings.md](docs/keybindings.md). | CHANGELOG.md |
| G-PI-CHANGELOG-536 | New Features | `session_directory` extension event for customizing session directory paths before session manager creation. See [docs/extensions.md](docs/extensions.md). | CHANGELOG.md |
| G-PI-CHANGELOG-537 | New Features | Digit keybindings (`09`) in the TUI keybinding system, including modified combos like `ctrl+1`. See [docs/keybindings.md](docs/keybindings.md). | CHANGELOG.md |
| G-PI-CHANGELOG-538 | Added | Added `/tree` branch folding and segmentjump navigation with `Ctrl+←`/`Ctrl+→` and `Alt+←`/`Alt+→`, while keeping `←`/`→` and `Page Up`/`Page Down` for paging ([#1724](https://github.com/badlogic/pimono/pull/1724) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-539 | Added | Added `session_directory` extension event that fires before session manager creation, allowing extensions to customize the session directory path based on cwd and other factors. CLI `sessiondir` flag takes precedence over extensionprovided paths ([#1730](https://github.com/badlogic/pimono/pull/1730) by [@hjanuschka](https://github.com/hjanuschka)). | CHANGELOG.md |
| G-PI-CHANGELOG-540 | Added | Added digit keys (`09`) to the keybinding system, including Kitty CSIu and xterm `modifyOtherKeys` support for bindings like `ctrl+1` ([#1905](https://github.com/badlogic/pimono/issues/1905)) | CHANGELOG.md |
| G-PI-CHANGELOG-541 | Fixed | Fixed custom tool collapsed/expanded rendering in HTML exports. Custom tools that define different collapsed vs expanded displays now render correctly in exported HTML, with expandable sections when both states differ and direct display when only expanded exists ([#1934](https://github.com/badlogic/pimono/pull/1934) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-542 | Fixed | Fixed tmux startup guidance and keyboard setup warnings for modified key handling, including Ghostty `shift+enter=text:\n` remap guidance and tmux `extendedkeysformat` detection ([#1872](https://github.com/badlogic/pimono/issues/1872)) | CHANGELOG.md |
| G-PI-CHANGELOG-543 | Fixed | Fixed z.ai context overflow recovery so `model_context_window_exceeded` errors trigger autocompaction instead of surfacing as unhandled stop reason failures ([#1937](https://github.com/badlogic/pimono/issues/1937)) | CHANGELOG.md |
| G-PI-CHANGELOG-544 | Fixed | Fixed autocomplete selection ignoring typed text: highlight now follows the first prefix match as the user types, and exact matches are always selected on Enter ([#1931](https://github.com/badlogic/pimono/pull/1931) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-545 | Fixed | Fixed slashcommand Tab completion to immediately open argument completions when available ([#1481](https://github.com/badlogic/pimono/pull/1481) by [@barapa](https://github.com/barapa)) | CHANGELOG.md |
| G-PI-CHANGELOG-546 | Fixed | Fixed explicit `pi e <path>` extensions losing command and tool conflicts to discovered extensions by giving CLIloaded extensions higher precedence ([#1896](https://github.com/badlogic/pimono/issues/1896)) | CHANGELOG.md |
| G-PI-CHANGELOG-547 | Fixed | Fixed Windows external editor launch for `Ctrl+G` and `ctx.ui.editor()` so shellbased commands like `EDITOR="code wait"` work correctly ([#1925](https://github.com/badlogic/pimono/issues/1925)) | CHANGELOG.md |
| G-PI-CHANGELOG-548 | New Features | Extensions can intercept and modify provider request payloads via `before_provider_request`. See [docs/extensions.md#before_provider_request](docs/extensions.md#before_provider_request). | CHANGELOG.md |
| G-PI-CHANGELOG-549 | New Features | Extension UIs can use noncapturing overlays with explicit focus control via `OverlayOptions.nonCapturing` and `OverlayHandle.focus()` / `unfocus()` / `isFocused()`. See [docs/extensions.md](docs/extensions.md) and [../tui/README.md](../tui/README.md). | CHANGELOG.md |
| G-PI-CHANGELOG-550 | New Features | RPC mode now uses strict LFonly JSONL framing for robust payload handling. See [docs/rpc.md](docs/rpc.md). | CHANGELOG.md |
| G-PI-CHANGELOG-551 | Breaking Changes | RPC mode now uses strict LFdelimited JSONL framing. Clients must split records on `\n` only instead of using generic line readers such as Node `readline`, which also split on Unicode separators inside JSON payloads ([#1911](https://github.com/badlogic/pimono/issues/1911)) | CHANGELOG.md |
| G-PI-CHANGELOG-552 | Added | Added `before_provider_request` extension hook so extensions can inspect or replace provider payloads before requests are sent, with an example in `examples/extensions/providerpayload.ts` | CHANGELOG.md |
| G-PI-CHANGELOG-553 | Added | Added noncapturing overlay focus control for extension UIs via `OverlayOptions.nonCapturing` and `OverlayHandle.focus()` / `unfocus()` / `isFocused()` ([#1916](https://github.com/badlogic/pimono/pull/1916) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-554 | Changed | Overlay compositing in extension UIs now uses focus order so focused overlays render on top while preserving stack semantics for show/hide behavior ([#1916](https://github.com/badlogic/pimono/pull/1916) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-555 | Fixed | Fixed RPC mode stdin/stdout framing to use strict LFdelimited JSONL instead of `readline`, so payloads containing `U+2028` or `U+2029` no longer corrupt command or event streams ([#1911](https://github.com/badlogic/pimono/issues/1911)) | CHANGELOG.md |
| G-PI-CHANGELOG-556 | Fixed | Fixed automatic overlay focus restoration in extension UIs to skip noncapturing overlays, and fixed overlay hide behavior to only reassign focus when the hidden overlay had focus ([#1916](https://github.com/badlogic/pimono/pull/1916) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-557 | Fixed | Fixed `pi config` misclassifying `~/.agents/skills` as projectscoped in nongit directories under `$HOME`, so toggling those skills no longer writes project overrides to `.pi/settings.json` ([#1915](https://github.com/badlogic/pimono/issues/1915)) | CHANGELOG.md |
| G-PI-CHANGELOG-558 | New Features | `claudesonnet46` model available via the `googleantigravity` provider ([#1859](https://github.com/badlogic/pimono/issues/1859)) | CHANGELOG.md |
| G-PI-CHANGELOG-559 | New Features | Custom editors can now define their own `onEscape`/`onCtrlD` handlers without being overwritten by app defaults, enabling vimmode extensions ([#1838](https://github.com/badlogic/pimono/issues/1838)) | CHANGELOG.md |
| G-PI-CHANGELOG-560 | New Features | Shift+Enter and Ctrl+Enter now work inside tmux via xterm modifyOtherKeys fallback ([docs/tmux.md](docs/tmux.md), [#1872](https://github.com/badlogic/pimono/issues/1872)) | CHANGELOG.md |
| G-PI-CHANGELOG-561 | New Features | Autocompaction is now resilient to persistent API errors (e.g. 529 overloaded) and no longer retriggers spuriously after compaction ([#1834](https://github.com/badlogic/pimono/issues/1834), [#1860](https://github.com/badlogic/pimono/issues/1860)) | CHANGELOG.md |
| G-PI-CHANGELOG-562 | Added | Added `claudesonnet46` model for the `googleantigravity` provider ([#1859](https://github.com/badlogic/pimono/issues/1859)). | CHANGELOG.md |
| G-PI-CHANGELOG-563 | Added | Added [tmux setup documentation](docs/tmux.md) for modified enter key support ([#1872](https://github.com/badlogic/pimono/issues/1872)) | CHANGELOG.md |
| G-PI-CHANGELOG-564 | Fixed | Fixed custom editors having their `onEscape`/`onCtrlD` handlers unconditionally overwritten by applevel defaults, making vimstyle escape handling impossible ([#1838](https://github.com/badlogic/pimono/issues/1838)) | CHANGELOG.md |
| G-PI-CHANGELOG-565 | Fixed | Fixed autocompaction retriggering on the first prompt after compaction due to stale precompaction assistant usage ([#1860](https://github.com/badlogic/pimono/issues/1860) by [@joelhooks](https://github.com/joelhooks)) | CHANGELOG.md |
| G-PI-CHANGELOG-566 | Fixed | Fixed sessions never autocompacting when hitting persistent API errors (e.g. 529 overloaded) by estimating context size from the last successful response ([#1834](https://github.com/badlogic/pimono/issues/1834)) | CHANGELOG.md |
| G-PI-CHANGELOG-567 | Fixed | Fixed compaction summarization requests exceeding context limits by truncating tool results to 2k chars ([#1796](https://github.com/badlogic/pimono/issues/1796)) | CHANGELOG.md |
| G-PI-CHANGELOG-568 | Fixed | Fixed `/new` leaving startup header content, including the changelog, visible after starting a fresh session ([#1880](https://github.com/badlogic/pimono/issues/1880)) | CHANGELOG.md |
| G-PI-CHANGELOG-569 | Fixed | Fixed misleading docs and example implying that returning `{ isError: true }` from a tool's `execute` function marks the execution as failed; errors must be signaled by throwing ([#1881](https://github.com/badlogic/pimono/issues/1881)) | CHANGELOG.md |
| G-PI-CHANGELOG-570 | Fixed | Fixed model switches through nonreasoning models to preserve the saved default thinking level instead of persisting a capabilityforced `off` clamp ([#1864](https://github.com/badlogic/pimono/issues/1864)) | CHANGELOG.md |
| G-PI-CHANGELOG-571 | Fixed | Fixed parallel pi processes failing with false "No API key found" errors due to immediate lockfile contention on `auth.json` and `settings.json` ([#1871](https://github.com/badlogic/pimono/issues/1871)) | CHANGELOG.md |
| G-PI-CHANGELOG-572 | Fixed | Fixed OpenAI Responses reasoning replay regression that broke multiturn reasoning continuity ([#1878](https://github.com/badlogic/pimono/issues/1878)) | CHANGELOG.md |
| G-PI-CHANGELOG-573 | New Features | GPT5.4 support across `openai`, `openaicodex`, `azureopenairesponses`, and `opencode`, with `gpt5.4` now the default for `openai` and `openaicodex` ([README.md](README.md), [docs/providers.md](docs/providers.md)). | CHANGELOG.md |
| G-PI-CHANGELOG-574 | New Features | `treeFilterMode` setting to choose the default `/tree` filter mode (`default`, `notools`, `useronly`, `labeledonly`, `all`) ([docs/settings.md](docs/settings.md), [#1852](https://github.com/badlogic/pimono/pull/1852) by [@lajarre](https://github.com/lajarre)). | CHANGELOG.md |
| G-PI-CHANGELOG-575 | New Features | Mistral native conversations integration with SDKbacked provider behavior, preserving Mistralspecific thinking and replay semantics ([README.md](README.md), [docs/providers.md](docs/providers.md), [#1716](https://github.com/badlogic/pimono/issues/1716)). | CHANGELOG.md |
| G-PI-CHANGELOG-576 | Added | Added `gpt5.4` model availability for `openai`, `openaicodex`, `azureopenairesponses`, and `opencode` providers. | CHANGELOG.md |
| G-PI-CHANGELOG-577 | Added | Added `gpt5.3codex` fallback model availability for `githubcopilot` until upstream model catalogs include it ([#1853](https://github.com/badlogic/pimono/issues/1853)). | CHANGELOG.md |
| G-PI-CHANGELOG-578 | Added | Added `treeFilterMode` setting to choose the default `/tree` filter mode (`default`, `notools`, `useronly`, `labeledonly`, `all`) ([#1852](https://github.com/badlogic/pimono/pull/1852) by [@lajarre](https://github.com/lajarre)). | CHANGELOG.md |
| G-PI-CHANGELOG-579 | Changed | Updated the default models for the `openai` and `openaicodex` providers to `gpt5.4`. | CHANGELOG.md |
| G-PI-CHANGELOG-580 | Fixed | Fixed GPT5.3 Codex followup turns dropping OpenAI Responses assistant `phase` metadata by preserving replayable signatures in session history and forwarding `phase` back to the Responses API ([#1819](https://github.com/badlogic/pimono/issues/1819)). | CHANGELOG.md |
| G-PI-CHANGELOG-581 | Fixed | Fixed OpenAI Responses replay to omit empty thinking blocks, avoiding invalid noop reasoning items in followup turns. | CHANGELOG.md |
| G-PI-CHANGELOG-582 | Fixed | Updated Mistral integration to use the native SDKbacked provider and conversations API, including codingagent model/provider wiring and Mistral setup documentation ([#1716](https://github.com/badlogic/pimono/issues/1716)). | CHANGELOG.md |
| G-PI-CHANGELOG-583 | Fixed | Fixed Antigravity reliability: endpoint cascade on 403/404, added autopush sandbox fallback, removed extra fingerprint headers ([#1830](https://github.com/badlogic/pimono/issues/1830)). | CHANGELOG.md |
| G-PI-CHANGELOG-584 | Fixed | Fixed `@mariozechner/piai/oauth` extension imports in published installs by resolving the subpath directly from built `dist` files instead of packageroot wrapper shims ([#1856](https://github.com/badlogic/pimono/issues/1856)). | CHANGELOG.md |
| G-PI-CHANGELOG-585 | Fixed | Fixed Gemini 3 multiturn tool use losing structured context by using `skip_thought_signature_validator` sentinel for unsigned function calls instead of text fallback ([#1829](https://github.com/badlogic/pimono/issues/1829)). | CHANGELOG.md |
| G-PI-CHANGELOG-586 | Fixed | Fixed model selector filter not accepting typed characters in VS Code 1.110+ due to missing Kitty CSIu printable decoding in the `Input` component ([#1857](https://github.com/badlogic/pimono/issues/1857)) | CHANGELOG.md |
| G-PI-CHANGELOG-587 | Fixed | Fixed editor/footer visibility drift during terminal resize by forcing full redraws when terminal width or height changes ([#1844](https://github.com/badlogic/pimono/pull/1844) by [@ghoulr](https://github.com/ghoulr)). | CHANGELOG.md |
| G-PI-CHANGELOG-588 | Fixed | Fixed footer width truncation for wide Unicode text (session name, model, provider) to prevent TUI crashes from rendered lines exceeding terminal width ([#1833](https://github.com/badlogic/pimono/issues/1833)). | CHANGELOG.md |
| G-PI-CHANGELOG-589 | Fixed | Fixed Windows write preview background artifacts by normalizing CRLF content (`\r\n`) to LF for display rendering in tool output previews ([#1854](https://github.com/badlogic/pimono/issues/1854)). | CHANGELOG.md |
| G-PI-CHANGELOG-590 | Fixed | Fixed extension alias fallback resolution to use ESMaware resolution for `jiti` aliases in global installs ([#1821](https://github.com/badlogic/pimono/pull/1821) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-591 | Fixed | Fixed markdown blockquote rendering to isolate blockquote styling from default text style, preventing style leakage. | CHANGELOG.md |
| G-PI-CHANGELOG-592 | New Features | Added OpenCode Go provider support with `opencodego` model defaults and `OPENCODE_API_KEY` environment variable support ([docs/providers.md](docs/providers.md), [#1757](https://github.com/badlogic/pimono/issues/1757)). | CHANGELOG.md |
| G-PI-CHANGELOG-593 | New Features | Added `branchSummary.skipPrompt` setting to skip branch summarization prompts during tree navigation ([docs/settings.md](docs/settings.md), [#1792](https://github.com/badlogic/pimono/issues/1792)). | CHANGELOG.md |
| G-PI-CHANGELOG-594 | New Features | Added `gemini3.1flashlitepreview` fallback model availability for Google provider catalogs when upstream model metadata lags ([README.md](README.md), [#1785](https://github.com/badlogic/pimono/issues/1785)). | CHANGELOG.md |
| G-PI-CHANGELOG-595 | Breaking Changes | Changed scoped model thinking semantics. Scoped entries without an explicit `:<thinking>` suffix now inherit the current session thinking level when selected, instead of applying a startupcaptured default. | CHANGELOG.md |
| G-PI-CHANGELOG-596 | Breaking Changes | Moved Node OAuth runtime exports off the toplevel `@mariozechner/piai` entry. OAuth login and refresh must be imported from `@mariozechner/piai/oauth` ([#1814](https://github.com/badlogic/pimono/issues/1814)). | CHANGELOG.md |
| G-PI-CHANGELOG-597 | Added | Added `branchSummary.skipPrompt` setting to skip the summary prompt when navigating branches ([#1792](https://github.com/badlogic/pimono/issues/1792)). | CHANGELOG.md |
| G-PI-CHANGELOG-598 | Added | Added OpenCode Go provider support with `opencodego` model defaults and `OPENCODE_API_KEY` environment variable support ([#1757](https://github.com/badlogic/pimono/issues/1757)). | CHANGELOG.md |
| G-PI-CHANGELOG-599 | Added | Added `gemini3.1flashlitepreview` fallback model availability in provider catalogs when upstream catalogs lag ([#1785](https://github.com/badlogic/pimono/issues/1785)). | CHANGELOG.md |
| G-PI-CHANGELOG-600 | Changed | Updated Antigravity Gemini 3.1 model metadata and request headers to match upstream behavior. | CHANGELOG.md |
| G-PI-CHANGELOG-601 | Fixed | Fixed IME hardware cursor positioning in the custom extension editor (`ctx.ui.editor()` / extension editor dialog) by propagating focus to the internal `Editor`, preventing the terminal cursor from getting stuck at the bottomright during composition. | CHANGELOG.md |
| G-PI-CHANGELOG-602 | Fixed | Added OSC 133 semantic zone markers around rendered user messages to support terminal navigation between prompts in iTerm2, WezTerm, Kitty, Ghostty, and other compatible terminals ([#1805](https://github.com/badlogic/pimono/issues/1805)). | CHANGELOG.md |
| G-PI-CHANGELOG-603 | Fixed | Fixed markdown blockquotes dropping nested list content in the TUI renderer ([#1787](https://github.com/badlogic/pimono/issues/1787)). | CHANGELOG.md |
| G-PI-CHANGELOG-604 | Fixed | Fixed TUI width handling for regional indicator symbols to prevent wrap drift and stale characters during streaming ([#1783](https://github.com/badlogic/pimono/issues/1783)). | CHANGELOG.md |
| G-PI-CHANGELOG-605 | Fixed | Fixed Kitty CSIu handling to ignore unsupported modifiers so modifieronly events do not insert printable characters ([#1807](https://github.com/badlogic/pimono/issues/1807)). | CHANGELOG.md |
| G-PI-CHANGELOG-606 | Fixed | Fixed singleline paste handling to insert text atomically and avoid repeated `@` autocomplete scans on large pastes ([#1812](https://github.com/badlogic/pimono/issues/1812)). | CHANGELOG.md |
| G-PI-CHANGELOG-607 | Fixed | Fixed extension loading with the new `@mariozechner/piai/oauth` export path by aliasing the oauth subpath in the extension loader and development path mapping ([#1814](https://github.com/badlogic/pimono/issues/1814)). | CHANGELOG.md |
| G-PI-CHANGELOG-608 | Fixed | Fixed browsersafe provider loading regressions by preloading the Bedrock provider module in compiled Bun binaries and rebuilding binaries against fresh workspace dependencies ([#1814](https://github.com/badlogic/pimono/issues/1814)). | CHANGELOG.md |
| G-PI-CHANGELOG-609 | Fixed | Fixed GNU screen terminal detection by downgrading theme output to 256color mode for `screen` TERM values ([#1809](https://github.com/badlogic/pimono/issues/1809)). | CHANGELOG.md |
| G-PI-CHANGELOG-610 | Fixed | Fixed branch summarization queue handling so messages typed while summaries are generated are processed correctly ([#1803](https://github.com/badlogic/pimono/issues/1803)). | CHANGELOG.md |
| G-PI-CHANGELOG-611 | Fixed | Fixed compaction summary requests to avoid reasoning output for nonreasoning models ([#1793](https://github.com/badlogic/pimono/issues/1793)). | CHANGELOG.md |
| G-PI-CHANGELOG-612 | Fixed | Fixed overflow autocompaction cascades so a single overflow does not trigger repeated compaction loops. | CHANGELOG.md |
| G-PI-CHANGELOG-613 | Fixed | Fixed `models.json` to allow providerscoped custom model ids and modellevel `baseUrl` overrides ([#1759](https://github.com/badlogic/pimono/issues/1759), [#1777](https://github.com/badlogic/pimono/issues/1777)). | CHANGELOG.md |
| G-PI-CHANGELOG-614 | Fixed | Fixed session selector display sanitization by stripping control characters from session display text ([#1747](https://github.com/badlogic/pimono/issues/1747)). | CHANGELOG.md |
| G-PI-CHANGELOG-615 | Fixed | Fixed Groq Qwen3 reasoning effort mapping for OpenAIcompatible models ([#1745](https://github.com/badlogic/pimono/issues/1745)). | CHANGELOG.md |
| G-PI-CHANGELOG-616 | Fixed | Fixed Bedrock `AWS_PROFILE` region resolution by honoring profile `region` values ([#1800](https://github.com/badlogic/pimono/issues/1800)). | CHANGELOG.md |
| G-PI-CHANGELOG-617 | Fixed | Fixed Gemini 3.1 thinkinglevel detection for `google` and `googlevertex` providers ([#1785](https://github.com/badlogic/pimono/issues/1785)). | CHANGELOG.md |
| G-PI-CHANGELOG-618 | Fixed | Fixed browser bundling compatibility for `@mariozechner/piai` by removing Nodeonly side effects from default browser import paths ([#1814](https://github.com/badlogic/pimono/issues/1814)). | CHANGELOG.md |
| G-PI-CHANGELOG-619 | New Features | Runtime tool registration now applies immediately in active sessions. Tools registered via `pi.registerTool()` after startup are available to `pi.getAllTools()` and the LLM without `/reload` ([docs/extensions.md](docs/extensions.md), [examples/extensions/dynamictools.ts](examples/extensions/dynamictools.ts), [#1720](https://github.com/badlogic/pimono/issues/1720)). | CHANGELOG.md |
| G-PI-CHANGELOG-620 | New Features | Tool definitions can customize the default system prompt with `promptSnippet` (`Available tools`) and `promptGuidelines` (`Guidelines`) while the tool is active ([docs/extensions.md](docs/extensions.md), [#1720](https://github.com/badlogic/pimono/issues/1720)). | CHANGELOG.md |
| G-PI-CHANGELOG-621 | New Features | Custom tool renderers can suppress transcript output without leaving extra spacing or empty transcript footprint in interactive rendering ([docs/extensions.md](docs/extensions.md), [#1719](https://github.com/badlogic/pimono/pull/1719)). | CHANGELOG.md |
| G-PI-CHANGELOG-622 | Added | Added optional `promptSnippet` to `ToolDefinition` for oneline entries in the default system prompt's `Available tools` section. Active extension tools appear there when registered and active ([#1237](https://github.com/badlogic/pimono/pull/1237) by [@semtexzv](https://github.com/semtexzv)). | CHANGELOG.md |
| G-PI-CHANGELOG-623 | Added | Added optional `promptGuidelines` to `ToolDefinition` so active tools can append toolspecific bullets to the default system prompt `Guidelines` section ([#1720](https://github.com/badlogic/pimono/issues/1720)). | CHANGELOG.md |
| G-PI-CHANGELOG-624 | Fixed | Fixed `pi.registerTool()` dynamic registration after session initialization. Tools registered in `session_start` and later handlers now refresh immediately, become active, and are visible to the LLM without `/reload` ([#1720](https://github.com/badlogic/pimono/issues/1720)) | CHANGELOG.md |
| G-PI-CHANGELOG-625 | Fixed | Fixed session message persistence ordering by serializing `AgentSession` event processing, preventing `toolResult` entries from being written before their corresponding assistant toolcall messages when extension handlers are asynchronous ([#1717](https://github.com/badlogic/pimono/issues/1717)) | CHANGELOG.md |
| G-PI-CHANGELOG-626 | Fixed | Fixed spacing artifacts when custom tool renderers intentionally suppress percall transcript output, including extra blank rows in interactive streaming and nonzero transcript footprint for empty custom renders ([#1719](https://github.com/badlogic/pimono/pull/1719) by [@alasano](https://github.com/alasano)) | CHANGELOG.md |
| G-PI-CHANGELOG-627 | Fixed | Fixed `session.prompt()` returning before retry completion by creating the retry promise synchronously at `agent_end` dispatch, which closes a race when earlier queued event handlers are async ([#1726](https://github.com/badlogic/pimono/pull/1726) by [@pasky](https://github.com/pasky)) | CHANGELOG.md |
| G-PI-CHANGELOG-628 | Fixed | Changed the default image paste keybinding on Windows to `alt+v` to avoid `ctrl+v` conflicts with terminal paste behavior ([#1682](https://github.com/badlogic/pimono/pull/1682) by [@mrexodia](https://github.com/mrexodia)). | CHANGELOG.md |
| G-PI-CHANGELOG-629 | New Features | Extensions can dynamically remove custom providers via `pi.unregisterProvider(name)`, restoring any builtin models that were overridden, without requiring `/reload` ([docs](https://github.com/badlogic/pimono/blob/main/packages/codingagent/docs/customprovider.md)). | CHANGELOG.md |
| G-PI-CHANGELOG-630 | New Features | `pi.registerProvider()` now takes effect immediately when called outside the initial extension load phase (e.g. from a command handler), removing the need for `/reload` after late registrations. | CHANGELOG.md |
| G-PI-CHANGELOG-631 | Added | `pi.unregisterProvider(name)` removes a dynamically registered provider and its models from the registry without requiring `/reload`. Builtin models that were overridden by the provider are restored ([#1669](https://github.com/badlogic/pimono/pull/1669) by [@aliou](https://github.com/aliou)). | CHANGELOG.md |
| G-PI-CHANGELOG-632 | Fixed | `pi.registerProvider()` now takes effect immediately when called after the initial extension load phase (e.g. from a command handler). Previously the registration sat in a pending queue that was never flushed until the next `/reload` ([#1669](https://github.com/badlogic/pimono/pull/1669) by [@aliou](https://github.com/aliou)). | CHANGELOG.md |
| G-PI-CHANGELOG-633 | Fixed | Fixed duplicate session headers when forking from a point before any assistant message. `createBranchedSession` now defers file creation to `_persist()` when the branched path has no assistant message, matching the `newSession()` contract ([#1672](https://github.com/badlogic/pimono/pull/1672) by [@wwinter](https://github.com/wwinter)). | CHANGELOG.md |
| G-PI-CHANGELOG-634 | Fixed | Fixed SIGINT being delivered to pi while the process is suspended (e.g. via `ctrl+z`), which could corrupt terminal state on resume ([#1668](https://github.com/badlogic/pimono/pull/1668) by [@aliou](https://github.com/aliou)). | CHANGELOG.md |
| G-PI-CHANGELOG-635 | Fixed | Fixed Z.ai thinking control using wrong parameter name, causing thinking to always be enabled and wasting tokens/latency ([#1674](https://github.com/badlogic/pimono/pull/1674) by [@okuyam2y](https://github.com/okuyam2y)) | CHANGELOG.md |
| G-PI-CHANGELOG-636 | Fixed | Fixed `redacted_thinking` blocks being silently dropped during Anthropic streaming, and related issues with interleavedthinking beta headers and temperature being sent alongside extended thinking ([#1665](https://github.com/badlogic/pimono/pull/1665) by [@tctev](https://github.com/tctev)) | CHANGELOG.md |
| G-PI-CHANGELOG-637 | Fixed | Fixed `(external, cli)` useragent flag causing 401 errors on Anthropic setuptoken endpoint ([#1677](https://github.com/badlogic/pimono/pull/1677) by [@LazerLance777](https://github.com/LazerLance777)) | CHANGELOG.md |
| G-PI-CHANGELOG-638 | Fixed | Fixed crash when OpenAIcompatible provider returns a chunk with no `choices` array ([#1671](https://github.com/badlogic/pimono/issues/1671)) | CHANGELOG.md |
| G-PI-CHANGELOG-639 | New Features | Added offline startup mode via `offline` (or `PI_OFFLINE`) to disable startup network operations, with startup network timeouts to avoid hangs in restricted or offline environments. | CHANGELOG.md |
| G-PI-CHANGELOG-640 | New Features | Added `gemini3.1propreview` model support to the `googlegeminicli` provider ([#1599](https://github.com/badlogic/pimono/pull/1599) by [@audichuang](https://github.com/audichuang)). | CHANGELOG.md |
| G-PI-CHANGELOG-641 | Fixed | Fixed offline startup hangs by adding offline startup behavior and network timeouts during managed tool setup ([#1631](https://github.com/badlogic/pimono/pull/1631) by [@mcollina](https://github.com/mcollina)) | CHANGELOG.md |
| G-PI-CHANGELOG-642 | Fixed | Fixed Windows VT input initialization in ESM by loading koffi via createRequire, avoiding runtime and bundling issues in enduser environments ([#1627](https://github.com/badlogic/pimono/pull/1627) by [@kaste](https://github.com/kaste)) | CHANGELOG.md |
| G-PI-CHANGELOG-643 | Fixed | Fixed managed `fd`/`rg` bootstrap on Windows in Git Bash by using `extractzip` for `.zip` archives, searching extracted layouts more robustly, and isolating extraction temp directories to avoid concurrent download races ([#1348](https://github.com/badlogic/pimono/issues/1348)) | CHANGELOG.md |
| G-PI-CHANGELOG-644 | Fixed | Fixed extension loading on Windows when resolving `@sinclair/typebox` aliases so subpath imports like `@sinclair/typebox/compiler` resolve correctly. | CHANGELOG.md |
| G-PI-CHANGELOG-645 | Fixed | Fixed adaptive thinking for Claude Sonnet 4.6 in Anthropic and Bedrock providers, and clamped unsupported `xhigh` effort values to supported levels ([#1548](https://github.com/badlogic/pimono/pull/1548) by [@tctev](https://github.com/tctev)) | CHANGELOG.md |
| G-PI-CHANGELOG-646 | Fixed | Fixed Vertex ADC credential detection race by avoiding caching a false negative during async import initialization ([#1550](https://github.com/badlogic/pimono/pull/1550) by [@jeremiahgaylordweb](https://github.com/jeremiahgaylordweb)) | CHANGELOG.md |
| G-PI-CHANGELOG-647 | Fixed | Fixed subagent extension example to resolve user agents from the configured agent directory instead of hardcoded paths ([#1559](https://github.com/badlogic/pimono/pull/1559) by [@tianshuwang](https://github.com/tianshuwang)) | CHANGELOG.md |
| G-PI-CHANGELOG-648 | Breaking Changes | Resource precedence for extensions, skills, prompts, themes, and slashcommand name collisions is now projectfirst (`cwd/.pi`) before userglobal (`~/.pi/agent`). If you relied on global resources overriding project resources with the same names, rename or reorder your resources. | CHANGELOG.md |
| G-PI-CHANGELOG-649 | Breaking Changes | Extension registration conflicts no longer unload the entire later extension. All extensions stay loaded, and conflicting command/tool/flag names are resolved by first registration in load order. | CHANGELOG.md |
| G-PI-CHANGELOG-650 | Fixed | Fixed `.pi` folder being created unnecessarily when only reading settings. The folder is now only created when writing projectspecific settings. | CHANGELOG.md |
| G-PI-CHANGELOG-651 | Fixed | Fixed extensiondriven runtime theme changes to persist in settings so `/settings` reflects the active `currentTheme` after `ctx.ui.setTheme(...)` ([#1483](https://github.com/badlogic/pimono/pull/1483) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-652 | Fixed | Fixed interactive mode freezes during large streaming `write` tool calls by using incremental syntax highlighting while partial arguments stream, with a final full rehighlight after toolcall arguments complete. | CHANGELOG.md |
| G-PI-CHANGELOG-653 | Fixed | Externalized koffi from bun binary builds, reducing archive sizes by ~15MB per platform (e.g. darwinarm64: 43MB > 28MB). Koffi's Windowsonly `.node` file is now shipped alongside the Windows binary only. | CHANGELOG.md |
| G-PI-CHANGELOG-654 | Added | Added default skill autodiscovery for `.agents/skills` locations. Pi now discovers project skills from `.agents/skills` in `cwd` and ancestor directories (up to git repo root, or filesystem root when not in a repo), and global skills from `~/.agents/skills`, in addition to existing `.pi` skill paths. | CHANGELOG.md |
| G-PI-CHANGELOG-655 | Changed | Added Gemini 3.1 model catalog entries for all builtin providers that currently expose it: `google`, `googlevertex`, `opencode`, `openrouter`, and `vercelaigateway`. | CHANGELOG.md |
| G-PI-CHANGELOG-656 | Changed | Added Claude Opus 4.6 Thinking to the `googleantigravity` model catalog. | CHANGELOG.md |
| G-PI-CHANGELOG-657 | Breaking Changes | `SettingsManager` persistence semantics changed for SDK consumers. Setters now update inmemory state immediately and queue disk writes. Code that requires durable ondisk settings must call `await settingsManager.flush()`. | CHANGELOG.md |
| G-PI-CHANGELOG-658 | Breaking Changes | `AuthStorage` constructor is no longer public. Use static factories (`AuthStorage.create(...)`, `AuthStorage.fromStorage(...)`, `AuthStorage.inMemory(...)`). This breaks code that used `new AuthStorage(...)` directly. | CHANGELOG.md |
| G-PI-CHANGELOG-659 | Added | Added `SettingsManager.drainErrors()` for callercontrolled settings I/O error handling without managerside console output. | CHANGELOG.md |
| G-PI-CHANGELOG-660 | Added | Added auth storage backends (`FileAuthStorageBackend`, `InMemoryAuthStorageBackend`) and `AuthStorage.fromStorage(...)` for storagefirst auth persistence wiring. | CHANGELOG.md |
| G-PI-CHANGELOG-661 | Added | Added Anthropic `claudesonnet46` model fallback entry to generated model definitions. | CHANGELOG.md |
| G-PI-CHANGELOG-662 | Changed | `SettingsManager` now uses scoped storage abstraction with perscope locked read/merge/write persistence for global and project settings. | CHANGELOG.md |
| G-PI-CHANGELOG-663 | Fixed | Fixed project settings persistence to preserve unrelated external edits via mergeonwrite, while still applying inmemory changes for modified keys. | CHANGELOG.md |
| G-PI-CHANGELOG-664 | Fixed | Fixed auth credential persistence to preserve unrelated external edits to `auth.json` via locked read/merge/write updates. | CHANGELOG.md |
| G-PI-CHANGELOG-665 | Fixed | Fixed auth load/persist error surfacing by buffering errors and exposing them via `AuthStorage.drainErrors()`. | CHANGELOG.md |
| G-PI-CHANGELOG-666 | Added | Added `transport` setting (`"sse"`, `"websocket"`, `"auto"`) to `/settings` and `settings.json` for providers that support multiple transports (currently `openaicodex` via OpenAI Codex Responses). | CHANGELOG.md |
| G-PI-CHANGELOG-667 | Changed | Interactive mode now applies transport changes immediately to the active agent session. | CHANGELOG.md |
| G-PI-CHANGELOG-668 | Changed | Settings migration now maps legacy `websockets: boolean` to the new `transport` setting. | CHANGELOG.md |
| G-PI-CHANGELOG-669 | Added | Added MiniMax M2.5 model entries for `minimax`, `minimaxcn`, `openrouter`, and `vercelaigateway` providers, plus `minimaxm2.5free` for `opencode`. | CHANGELOG.md |
| G-PI-CHANGELOG-670 | New Features | Extension terminal input interception via `terminal_input`, allowing extensions to consume or transform raw input before normal TUI handling. See [docs/extensions.md](docs/extensions.md). | CHANGELOG.md |
| G-PI-CHANGELOG-671 | New Features | Expanded CLI model selection: `model` now supports `provider/id`, fuzzy matching, and `:<thinking>` suffixes. See [README.md](README.md) and [docs/models.md](docs/models.md). | CHANGELOG.md |
| G-PI-CHANGELOG-672 | New Features | Safer package source handling with stricter git source parsing and improved local path normalization. See [docs/packages.md](docs/packages.md). | CHANGELOG.md |
| G-PI-CHANGELOG-673 | New Features | New builtin model definition `gpt5.3codexspark` for OpenAI and OpenAI Codex providers. | CHANGELOG.md |
| G-PI-CHANGELOG-674 | New Features | Improved OpenAI stream robustness for malformed trailing toolcall JSON in partial chunks. | CHANGELOG.md |
| G-PI-CHANGELOG-675 | New Features | Added builtin GLM5 model support via z.ai and OpenRouter provider catalogs. | CHANGELOG.md |
| G-PI-CHANGELOG-676 | Breaking Changes | `ContextUsage.tokens` and `ContextUsage.percent` are now `number | null`. After compaction, context token count is unknown until the next LLM response, so these fields return `null`. Extensions that read `ContextUsage` must handle the `null` case. Removed `usageTokens`, `trailingTokens`, and `lastUsageIndex` fields from `ContextUsage` (implementation details that should not have been public) ([#1382](https://github.com/badlogic/pimono/pull/1382) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-677 | Breaking Changes | Git source parsing is now strict without `git:` prefix: only protocol URLs are treated as git (`https://`, `http://`, `ssh://`, `git://`). Shorthand sources like `github.com/org/repo` and `git@github.com:org/repo` now require the `git:` prefix. ([#1426](https://github.com/badlogic/pimono/issues/1426)) | CHANGELOG.md |
| G-PI-CHANGELOG-678 | Added | Added extension event forwarding for message and tool execution lifecycles (`message_start`, `message_update`, `message_end`, `tool_execution_start`, `tool_execution_update`, `tool_execution_end`) ([#1375](https://github.com/badlogic/pimono/pull/1375) by [@sumeet](https://github.com/sumeet)) | CHANGELOG.md |
| G-PI-CHANGELOG-679 | Added | Added `terminal_input` extension event to intercept, consume, or transform raw terminal input before normal TUI handling. | CHANGELOG.md |
| G-PI-CHANGELOG-680 | Added | Added `gpt5.3codexspark` model definition for OpenAI and OpenAI Codex providers (research preview). | CHANGELOG.md |
| G-PI-CHANGELOG-681 | Changed | Routed GitHub Copilot Claude 4.x models through Anthropic Messages API, with updated Copilot header handling for Claude model requests. | CHANGELOG.md |
| G-PI-CHANGELOG-682 | Fixed | Fixed context usage percentage in footer showing stale precompaction values. After compaction the footer now shows `?/200k` until the next LLM response provides accurate usage ([#1382](https://github.com/badlogic/pimono/pull/1382) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-683 | Fixed | Fixed `_checkCompaction()` using the first compaction entry instead of the latest, which could cause incorrect overflow detection with multiple compactions ([#1382](https://github.com/badlogic/pimono/pull/1382) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-684 | Fixed | `model` now works without `provider`, supports `provider/id` syntax, fuzzy matching, and `:<thinking>` suffix (e.g., `model sonnet:high`, `model openai/gpt4o`) ([#1350](https://github.com/badlogic/pimono/pull/1350) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-685 | Fixed | Fixed local package path normalization for extension sources while tightening git source parsing rules ([#1426](https://github.com/badlogic/pimono/issues/1426)) | CHANGELOG.md |
| G-PI-CHANGELOG-686 | Fixed | Fixed extension terminal input listeners not being cleared during session resets, which could leave stale handlers active. | CHANGELOG.md |
| G-PI-CHANGELOG-687 | Fixed | Fixed Termux bootstrap package name for `fd` installation ([#1433](https://github.com/badlogic/pimono/pull/1433)) | CHANGELOG.md |
| G-PI-CHANGELOG-688 | Fixed | Fixed `@` file autocomplete fuzzy matching to prioritize pathprefix and segment matches for nested paths ([#1423](https://github.com/badlogic/pimono/issues/1423)) | CHANGELOG.md |
| G-PI-CHANGELOG-689 | Fixed | Fixed OpenAI streaming toolcall parsing to tolerate malformed trailing JSON in partial chunks ([#1424](https://github.com/badlogic/pimono/issues/1424)) | CHANGELOG.md |
| G-PI-CHANGELOG-690 | New Features | Extensions can trigger a full runtime reload via `ctx.reload()`, useful for hotreloading configuration or restarting the agent. See [docs/extensions.md](docs/extensions.md) and the [`reloadruntime` example](examples/extensions/reloadruntime.ts) ([#1371](https://github.com/badlogic/pimono/issues/1371)) | CHANGELOG.md |
| G-PI-CHANGELOG-691 | New Features | Short CLI disable aliases: `ne` (`noextensions`), `ns` (`noskills`), and `np` (`noprompttemplates`) for faster interactive usage and scripting. | CHANGELOG.md |
| G-PI-CHANGELOG-692 | New Features | `/export` HTML now includes collapsible tool input schemas (parameter names, types, and descriptions), improving session review and sharing workflows ([#1416](https://github.com/badlogic/pimono/pull/1416) by [@marchellodev](https://github.com/marchellodev)). | CHANGELOG.md |
| G-PI-CHANGELOG-693 | New Features | `pi.getAllTools()` now exposes tool parameters in addition to name and description, enabling richer extension integrations ([#1416](https://github.com/badlogic/pimono/pull/1416) by [@marchellodev](https://github.com/marchellodev)). | CHANGELOG.md |
| G-PI-CHANGELOG-694 | Added | Added `ctx.reload()` to the extension API for programmatic runtime reload ([#1371](https://github.com/badlogic/pimono/issues/1371)) | CHANGELOG.md |
| G-PI-CHANGELOG-695 | Added | Added short aliases for disable flags: `ne` for `noextensions`, `ns` for `noskills`, `np` for `noprompttemplates` | CHANGELOG.md |
| G-PI-CHANGELOG-696 | Added | `/export` HTML now includes tool input schema (parameter names, types, descriptions) in a collapsible section under each tool ([#1416](https://github.com/badlogic/pimono/pull/1416) by [@marchellodev](https://github.com/marchellodev)) | CHANGELOG.md |
| G-PI-CHANGELOG-697 | Added | `pi.getAllTools()` now returns tool parameters in addition to name and description ([#1416](https://github.com/badlogic/pimono/pull/1416) by [@marchellodev](https://github.com/marchellodev)) | CHANGELOG.md |
| G-PI-CHANGELOG-698 | Fixed | Fixed extension source parsing so dotprefixed local paths (for example `.pi/extensions/foo.ts`) are treated as local paths instead of git URLs | CHANGELOG.md |
| G-PI-CHANGELOG-699 | Fixed | Fixed fd/rg download failing on Windows due to `unzip` not being available; now uses `tar` for both `.tar.gz` and `.zip` extraction, with proper error reporting ([#1348](https://github.com/badlogic/pimono/issues/1348)) | CHANGELOG.md |
| G-PI-CHANGELOG-700 | Fixed | Fixed RPC mode documentation incorrectly stating `ctx.hasUI` is `false`; it is `true` because dialog and fireandforget UI methods work via the RPC subprotocol. Also documented missing unsupported/degraded methods (`pasteToEditor`, `getAllThemes`, `getTheme`, `setTheme`) ([#1411](https://github.com/badlogic/pimono/pull/1411) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-701 | Fixed | Fixed `rg` not available in bash tool by downloading it at startup alongside `fd` ([#1348](https://github.com/badlogic/pimono/issues/1348)) | CHANGELOG.md |
| G-PI-CHANGELOG-702 | Fixed | Fixed `customcompaction` example to use `ModelRegistry` ([#1387](https://github.com/badlogic/pimono/issues/1387)) | CHANGELOG.md |
| G-PI-CHANGELOG-703 | Fixed | Google providers now support full JSON Schema in tool declarations (anyOf, oneOf, const, etc.) ([#1398](https://github.com/badlogic/pimono/issues/1398) by [@jarib](https://github.com/jarib)) | CHANGELOG.md |
| G-PI-CHANGELOG-704 | Fixed | Reverted incorrect Antigravity model change: `claudeopus46thinking` back to `claudeopus45thinking` (model does not exist on Antigravity endpoint) | CHANGELOG.md |
| G-PI-CHANGELOG-705 | Fixed | Updated the Antigravity system instruction to a more compact version for Google Gemini CLI compatibility | CHANGELOG.md |
| G-PI-CHANGELOG-706 | Fixed | Corrected opencode context windows for Claude Sonnet 4 and 4.5 ([#1383](https://github.com/badlogic/pimono/issues/1383)) | CHANGELOG.md |
| G-PI-CHANGELOG-707 | Fixed | Fixed subagent example unknownagent errors to include available agent names ([#1414](https://github.com/badlogic/pimono/pull/1414) by [@dnouri](https://github.com/dnouri)) | CHANGELOG.md |
| G-PI-CHANGELOG-708 | New Features | Emacsstyle kill ring (`ctrl+k`/`ctrl+y`/`alt+y`) and undo (`ctrl+z`) in the editor input ([#1373](https://github.com/badlogic/pimono/pull/1373) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-709 | New Features | OpenRouter `auto` model alias (`openrouter:auto`) for automatic model routing ([#1361](https://github.com/badlogic/pimono/pull/1361) by [@yogasanas](https://github.com/yogasanas)) | CHANGELOG.md |
| G-PI-CHANGELOG-710 | New Features | Extensions can programmatically paste content into the editor via `pasteToEditor` in the extension UI context. See [docs/extensions.md](docs/extensions.md) ([#1351](https://github.com/badlogic/pimono/pull/1351) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-711 | New Features | `pi <package> help` and invalid subcommands now show helpful output instead of failing silently ([#1347](https://github.com/badlogic/pimono/pull/1347) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-712 | Added | Added `pasteToEditor` to extension UI context for programmatic editor paste ([#1351](https://github.com/badlogic/pimono/pull/1351) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-713 | Added | Added package subcommand help and friendly error messages for invalid commands ([#1347](https://github.com/badlogic/pimono/pull/1347) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-714 | Added | Added OpenRouter `auto` model alias for automatic model routing ([#1361](https://github.com/badlogic/pimono/pull/1361) by [@yogasanas](https://github.com/yogasanas)) | CHANGELOG.md |
| G-PI-CHANGELOG-715 | Added | Added kill ring (ctrl+k/ctrl+y/alt+y) and undo (ctrl+z) support to the editor input ([#1373](https://github.com/badlogic/pimono/pull/1373) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-716 | Changed | Replaced Claude Opus 4.5 with Opus 4.6 as default model ([#1345](https://github.com/badlogic/pimono/pull/1345) by [@calvinhpnet](https://github.com/calvinhpnet)) | CHANGELOG.md |
| G-PI-CHANGELOG-717 | Fixed | Fixed temporary git package caches (`e <giturl>`) to refresh on cache hits for unpinned sources, including detached/noupstream checkouts | CHANGELOG.md |
| G-PI-CHANGELOG-718 | Fixed | Fixed aborting retries when an extension customizes the editor ([#1364](https://github.com/badlogic/pimono/pull/1364) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-719 | Fixed | Fixed autocomplete not propagating to custom editors created by extensions ([#1372](https://github.com/badlogic/pimono/pull/1372) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-720 | Fixed | Fixed extension shutdown to use clean TUI shutdown path, preventing orphaned processes | CHANGELOG.md |
| G-PI-CHANGELOG-721 | New Features | Permodel overrides in `models.json` via `modelOverrides`, allowing customization of builtin provider models without replacing provider model lists. See [docs/models.md#permodeloverrides](docs/models.md#permodeloverrides). | CHANGELOG.md |
| G-PI-CHANGELOG-722 | New Features | `models.json` provider `models` now merge with builtin models by `id`, so custom models can be added or replace matching builtins without full provider replacement. See [docs/models.md#overridingbuiltinproviders](docs/models.md#overridingbuiltinproviders). | CHANGELOG.md |
| G-PI-CHANGELOG-723 | New Features | Bedrock proxy support for unauthenticated endpoints via `AWS_BEDROCK_SKIP_AUTH` and `AWS_BEDROCK_FORCE_HTTP1`. See [docs/providers.md](docs/providers.md). | CHANGELOG.md |
| G-PI-CHANGELOG-724 | Breaking Changes | Changed `models.json` provider `models` behavior from full replacement to mergebyid with builtin models. Builtin models are now kept by default, and custom models upsert by `id`. | CHANGELOG.md |
| G-PI-CHANGELOG-725 | Added | Added `modelOverrides` in `models.json` to customize individual builtin models per provider without full provider replacement ([#1332](https://github.com/badlogic/pimono/pull/1332) by [@charlescooper](https://github.com/charlescooper)) | CHANGELOG.md |
| G-PI-CHANGELOG-726 | Added | Added `AWS_BEDROCK_SKIP_AUTH` and `AWS_BEDROCK_FORCE_HTTP1` environment variables for connecting to unauthenticated Bedrock proxies ([#1320](https://github.com/badlogic/pimono/pull/1320) by [@virtuald](https://github.com/virtuald)) | CHANGELOG.md |
| G-PI-CHANGELOG-727 | Fixed | Fixed extra spacing between thinkingonly assistant content and subsequent tool execution blocks when assistant messages contain no text | CHANGELOG.md |
| G-PI-CHANGELOG-728 | Fixed | Fixed queued steering/followup/custom messages remaining stuck after threshold autocompaction by resuming the agent loop when Agentlevel queues still contain pending messages ([#1312](https://github.com/badlogic/pimono/pull/1312) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-729 | Fixed | Fixed `tool_result` extension handlers to chain result patches across handlers instead of lasthandlerwins behavior ([#1280](https://github.com/badlogic/pimono/issues/1280)) | CHANGELOG.md |
| G-PI-CHANGELOG-730 | Fixed | Fixed compromised auth lock files being handled gracefully instead of crashing auth storage initialization ([#1322](https://github.com/badlogic/pimono/issues/1322)) | CHANGELOG.md |
| G-PI-CHANGELOG-731 | Fixed | Fixed Bedrock adaptive thinking handling for Claude Opus 4.6 with interleaved thinking beta responses ([#1323](https://github.com/badlogic/pimono/pull/1323) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-732 | Fixed | Fixed OpenAI Responses API requests to use `store: false` by default to avoid serverside history logging ([#1308](https://github.com/badlogic/pimono/issues/1308)) | CHANGELOG.md |
| G-PI-CHANGELOG-733 | Fixed | Fixed interactive mode startup by initializing autocomplete after resources are loaded ([#1328](https://github.com/badlogic/pimono/issues/1328)) | CHANGELOG.md |
| G-PI-CHANGELOG-734 | Fixed | Fixed `modelOverrides` merge behavior for nested objects and documented usage details ([#1062](https://github.com/badlogic/pimono/issues/1062)) | CHANGELOG.md |
| G-PI-CHANGELOG-735 | Breaking Changes | Removed `/exit` command handling. Use `/quit` to exit ([#1303](https://github.com/badlogic/pimono/issues/1303)) | CHANGELOG.md |
| G-PI-CHANGELOG-736 | Fixed | Fixed `/quit` being shadowed by fuzzy slash command autocomplete matches from skills by adding `/quit` to builtin command autocomplete ([#1303](https://github.com/badlogic/pimono/issues/1303)) | CHANGELOG.md |
| G-PI-CHANGELOG-737 | Fixed | Fixed local package source parsing and settings normalization regression that misclassified relative paths as git URLs and prevented globally installed local packages from loading after restart ([#1304](https://github.com/badlogic/pimono/issues/1304)) | CHANGELOG.md |
| G-PI-CHANGELOG-738 | Fixed | Fixed thinking level capability detection so Anthropic Opus 4.6 models expose `xhigh` in selectors and cycling | CHANGELOG.md |
| G-PI-CHANGELOG-739 | Fixed | Fixed extensions setting not respecting `package.json` `pi.extensions` manifest when directory is specified directly ([#1302](https://github.com/badlogic/pimono/pull/1302) by [@hjanuschka](https://github.com/hjanuschka)) | CHANGELOG.md |
| G-PI-CHANGELOG-740 | Fixed | Fixed git package parsing fallback for unknown hosts so enterprise git sources like `git:github.tools.sap/org/repo` are treated as git packages instead of local paths | CHANGELOG.md |
| G-PI-CHANGELOG-741 | Fixed | Fixed git package `@ref` parsing for shorthand, HTTPS, and SSH source formats, including branch refs with slashes | CHANGELOG.md |
| G-PI-CHANGELOG-742 | Fixed | Fixed Bedrock default model ID from `us.anthropic.claudeopus46v1:0` to `us.anthropic.claudeopus46v1` | CHANGELOG.md |
| G-PI-CHANGELOG-743 | Fixed | Fixed Bedrock Opus 4.6 model metadata (IDs, cache pricing) and added missing EU profile | CHANGELOG.md |
| G-PI-CHANGELOG-744 | Fixed | Fixed Claude Opus 4.6 context window metadata to 200000 for Anthropic and OpenCode providers | CHANGELOG.md |
| G-PI-CHANGELOG-745 | Changed | Updated default model for `anthropic` provider to `claudeopus46` | CHANGELOG.md |
| G-PI-CHANGELOG-746 | Changed | Updated default model for `openaicodex` provider to `gpt5.3codex` | CHANGELOG.md |
| G-PI-CHANGELOG-747 | Changed | Updated default model for `amazonbedrock` provider to `us.anthropic.claudeopus46v1:0` | CHANGELOG.md |
| G-PI-CHANGELOG-748 | Changed | Updated default model for `vercelaigateway` provider to `anthropic/claudeopus46` | CHANGELOG.md |
| G-PI-CHANGELOG-749 | Changed | Updated default model for `opencode` provider to `claudeopus46` | CHANGELOG.md |
| G-PI-CHANGELOG-750 | New Features | Claude Opus 4.6 model support. | CHANGELOG.md |
| G-PI-CHANGELOG-751 | New Features | GPT5.3 Codex model support (OpenAI Codex provider only). | CHANGELOG.md |
| G-PI-CHANGELOG-752 | New Features | SSH URL support for git packages. See [docs/packages.md](docs/packages.md). | CHANGELOG.md |
| G-PI-CHANGELOG-753 | New Features | `auth.json` API keys now support shell command resolution (`!command`) and environment variable lookup. See [docs/providers.md](docs/providers.md). | CHANGELOG.md |
| G-PI-CHANGELOG-754 | New Features | Model selectors now display the selected model name. | CHANGELOG.md |
| G-PI-CHANGELOG-755 | Added | API keys in `auth.json` now support shell command resolution (`!command`) and environment variable lookup, matching the behavior in `models.json` | CHANGELOG.md |
| G-PI-CHANGELOG-756 | Added | Added `minimalmode.ts` example extension demonstrating how to override builtin tool rendering for a minimal display mode | CHANGELOG.md |
| G-PI-CHANGELOG-757 | Added | Added Claude Opus 4.6 model to the model catalog | CHANGELOG.md |
| G-PI-CHANGELOG-758 | Added | Added GPT5.3 Codex model to the model catalog (OpenAI Codex provider only) | CHANGELOG.md |
| G-PI-CHANGELOG-759 | Added | Added SSH URL support for git packages ([#1287](https://github.com/badlogic/pimono/pull/1287) by [@markusn](https://github.com/markusn)) | CHANGELOG.md |
| G-PI-CHANGELOG-760 | Added | Model selectors now display the selected model name ([#1275](https://github.com/badlogic/pimono/pull/1275) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-761 | Fixed | Fixed HTML export losing indentation in ANSIrendered tool output (e.g. JSON code blocks in custom tool results) ([#1269](https://github.com/badlogic/pimono/pull/1269) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-762 | Fixed | Fixed images being silently dropped when `prompt()` is called with both `images` and `streamingBehavior` during streaming. `steer()`, `followUp()`, and the corresponding RPC commands now accept optional images. ([#1271](https://github.com/badlogic/pimono/pull/1271) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-763 | Fixed | CLI `help`, `version`, `listmodels`, and `export` now exit even if extensions keep the event loop alive ([#1285](https://github.com/badlogic/pimono/pull/1285) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-764 | Fixed | Fixed crash when models send malformed tool arguments (objects instead of strings) ([#1259](https://github.com/badlogic/pimono/issues/1259)) | CHANGELOG.md |
| G-PI-CHANGELOG-765 | Fixed | Fixed custom message expand state not being respected ([#1258](https://github.com/badlogic/pimono/pull/1258) by [@Gurpartap](https://github.com/Gurpartap)) | CHANGELOG.md |
| G-PI-CHANGELOG-766 | Fixed | Fixed skill loader to respect .gitignore, .ignore, and .fdignore when scanning directories | CHANGELOG.md |
| G-PI-CHANGELOG-767 | New Features | Configurable resume keybinding action for opening the session resume selector. See [docs/keybindings.md](docs/keybindings.md). ([#1249](https://github.com/badlogic/pimono/pull/1249) by [@juanibiapina](https://github.com/juanibiapina)) | CHANGELOG.md |
| G-PI-CHANGELOG-768 | Added | Added `resume` as a configurable keybinding action, allowing users to bind a key to open the session resume selector (like `newSession`, `tree`, and `fork`) ([#1249](https://github.com/badlogic/pimono/pull/1249) by [@juanibiapina](https://github.com/juanibiapina)) | CHANGELOG.md |
| G-PI-CHANGELOG-769 | Changed | Slash command menu now triggers on the first line even when other lines have content, allowing commands to be prepended to existing text ([#1227](https://github.com/badlogic/pimono/pull/1227) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-770 | Fixed | Ignored unknown skill frontmatter fields when loading skills | CHANGELOG.md |
| G-PI-CHANGELOG-771 | Fixed | Fixed `/reload` not picking up changes in global settings.json ([#1241](https://github.com/badlogic/pimono/issues/1241)) | CHANGELOG.md |
| G-PI-CHANGELOG-772 | Fixed | Fixed forked sessions to persist the user message after forking | CHANGELOG.md |
| G-PI-CHANGELOG-773 | Fixed | Fixed forked sessions to write to new session files instead of the parent ([#1242](https://github.com/badlogic/pimono/issues/1242)) | CHANGELOG.md |
| G-PI-CHANGELOG-774 | Fixed | Fixed local package removal to normalize paths before comparison ([#1243](https://github.com/badlogic/pimono/issues/1243)) | CHANGELOG.md |
| G-PI-CHANGELOG-775 | Fixed | Fixed OpenAI Codex Responses provider to respect configured baseUrl ([#1244](https://github.com/badlogic/pimono/issues/1244)) | CHANGELOG.md |
| G-PI-CHANGELOG-776 | Fixed | Fixed `/settings` crashing in narrow terminals by handling small widths in the settings list ([#1246](https://github.com/badlogic/pimono/pull/1246) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-777 | Fixed | Fixed Unix bash detection to fall back to PATH lookup when `/bin/bash` is unavailable, including Termux setups ([#1230](https://github.com/badlogic/pimono/pull/1230) by [@VaclavSynacek](https://github.com/VaclavSynacek)) | CHANGELOG.md |
| G-PI-CHANGELOG-778 | Changed | Changed Bedrock model generation to drop legacy workarounds now handled upstream ([#1239](https://github.com/badlogic/pimono/pull/1239) by [@unexge](https://github.com/unexge)) | CHANGELOG.md |
| G-PI-CHANGELOG-779 | Fixed | Fixed Windows package installs regression by using shell execution instead of `.cmd` resolution ([#1220](https://github.com/badlogic/pimono/issues/1220)) | CHANGELOG.md |
| G-PI-CHANGELOG-780 | New Features | Share URLs now default to pi.dev, graciously donated by exe.dev. | CHANGELOG.md |
| G-PI-CHANGELOG-781 | Changed | Share URLs now use pi.dev by default while pi.dev and buildwithpi.ai continue to work. | CHANGELOG.md |
| G-PI-CHANGELOG-782 | Fixed | Fixed input scrolling to avoid splitting emoji sequences ([#1228](https://github.com/badlogic/pimono/pull/1228) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-783 | New Features | Command discovery for extensions via `ExtensionAPI.getCommands()`, with `commands.ts` example for invocation patterns. See [docs/extensions.md#pigetcommands](docs/extensions.md#pigetcommands) and [examples/extensions/commands.ts](examples/extensions/commands.ts). | CHANGELOG.md |
| G-PI-CHANGELOG-784 | New Features | Local path support for `pi install` and `pi remove`, with relative path resolution against the settings file. See [docs/packages.md#localpaths](docs/packages.md#localpaths). | CHANGELOG.md |
| G-PI-CHANGELOG-785 | Breaking Changes | RPC `get_commands` response and `SlashCommandSource` type: renamed `"template"` to `"prompt"` for consistency with the rest of the codebase | CHANGELOG.md |
| G-PI-CHANGELOG-786 | Added | Added `ExtensionAPI.getCommands()` to let extensions list available slash commands (extensions, prompt templates, skills) for invocation via `prompt` ([#1210](https://github.com/badlogic/pimono/pull/1210) by [@wwinter](https://github.com/wwinter)) | CHANGELOG.md |
| G-PI-CHANGELOG-787 | Added | Added `commands.ts` example extension and exported `SlashCommandInfo` types for command discovery integrations ([#1210](https://github.com/badlogic/pimono/pull/1210) by [@wwinter](https://github.com/wwinter)) | CHANGELOG.md |
| G-PI-CHANGELOG-788 | Added | Added local path support for `pi install` and `pi remove` with relative paths stored against the target settings file ([#1216](https://github.com/badlogic/pimono/issues/1216)) | CHANGELOG.md |
| G-PI-CHANGELOG-789 | Fixed | Fixed default thinking level persistence so settingsderived defaults are saved and restored correctly | CHANGELOG.md |
| G-PI-CHANGELOG-790 | Fixed | Fixed Windows package installs by resolving `npm.cmd` when `npm` is not directly executable ([#1220](https://github.com/badlogic/pimono/issues/1220)) | CHANGELOG.md |
| G-PI-CHANGELOG-791 | Fixed | Fixed xhigh thinking level support check to accept gpt5.2 model IDs ([#1209](https://github.com/badlogic/pimono/issues/1209)) | CHANGELOG.md |
| G-PI-CHANGELOG-792 | New Features | Extension tool output expansion controls via ExtensionUIContext getToolsExpanded and setToolsExpanded. See [docs/extensions.md](docs/extensions.md) and [docs/rpc.md](docs/rpc.md). | CHANGELOG.md |
| G-PI-CHANGELOG-793 | Added | Added ExtensionUIContext getToolsExpanded and setToolsExpanded for controlling tool output expansion ([#1199](https://github.com/badlogic/pimono/pull/1199) by [@academo](https://github.com/academo)) | CHANGELOG.md |
| G-PI-CHANGELOG-794 | Added | Added install method detection to show package manager specific update instructions ([#1203](https://github.com/badlogic/pimono/pull/1203) by [@Itsnotaka](https://github.com/Itsnotaka)) | CHANGELOG.md |
| G-PI-CHANGELOG-795 | Fixed | Fixed Kitty key release events leaking to parent shell over slow SSH connections by draining stdin for up to 1s on exit ([#1204](https://github.com/badlogic/pimono/issues/1204)) | CHANGELOG.md |
| G-PI-CHANGELOG-796 | Fixed | Fixed legacy newline handling in the editor to preserve previous newline behavior | CHANGELOG.md |
| G-PI-CHANGELOG-797 | Fixed | Fixed @ autocomplete to include hidden paths | CHANGELOG.md |
| G-PI-CHANGELOG-798 | Fixed | Fixed submit fallback to honor configured keybindings | CHANGELOG.md |
| G-PI-CHANGELOG-799 | Fixed | Fixed extension commands conflicting with builtin commands by skipping them ([#1196](https://github.com/badlogic/pimono/pull/1196) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-800 | Fixed | Fixed @prefixed tool paths failing to resolve by stripping the prefix ([#1206](https://github.com/badlogic/pimono/issues/1206)) | CHANGELOG.md |
| G-PI-CHANGELOG-801 | Fixed | Fixed install method detection to avoid stale cached results | CHANGELOG.md |
| G-PI-CHANGELOG-802 | New Features | Extension API switchSession: Extensions can now programmatically switch sessions via `ctx.switchSession(sessionPath)`. See [docs/extensions.md](docs/extensions.md). ([#1187](https://github.com/badlogic/pimono/issues/1187)) | CHANGELOG.md |
| G-PI-CHANGELOG-803 | New Features | Clear on shrink setting: New `terminal.clearOnShrink` setting keeps the editor and footer pinned to the bottom of the terminal when content shrinks. May cause some flicker due to redraws. Disabled by default. Enable via `/settings` or `PI_CLEAR_ON_SHRINK=1` env var. | CHANGELOG.md |
| G-PI-CHANGELOG-804 | Fixed | Fixed scoped models not finding valid credentials after logout ([#1194](https://github.com/badlogic/pimono/pull/1194) by [@terrorobe](https://github.com/terrorobe)) | CHANGELOG.md |
| G-PI-CHANGELOG-805 | Fixed | Fixed Ctrl+D exit closing the parent SSH session due to stdin buffer race condition ([#1185](https://github.com/badlogic/pimono/issues/1185)) | CHANGELOG.md |
| G-PI-CHANGELOG-806 | Fixed | Fixed emoji cursor positioning in editor input ([#1183](https://github.com/badlogic/pimono/pull/1183) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-807 | Breaking Changes | Extension tool signature change: `ToolDefinition.execute` now uses `(toolCallId, params, signal, onUpdate, ctx)` parameter order to match `AgentTool.execute`. Previously it was `(toolCallId, params, onUpdate, ctx, signal)`. This makes wrapping builtin tools trivial since the first four parameters now align. Update your extensions by swapping the `signal` and `onUpdate` parameters: | CHANGELOG.md |
| G-PI-CHANGELOG-808 | New Features | Android/Termux support: Pi now runs on Android via Termux. Install with: | CHANGELOG.md |
| G-PI-CHANGELOG-809 | New Features | Bash spawn hook: Extensions can now intercept and modify bash commands before execution via `pi.setBashSpawnHook()`. Adjust the command string, working directory, or environment variables. See [docs/extensions.md](docs/extensions.md). ([#1160](https://github.com/badlogic/pimono/pull/1160) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-810 | New Features | Linux ARM64 musl support: Pi now runs on Alpine Linux ARM64 (linuxarm64musl) via updated clipboard dependency. | CHANGELOG.md |
| G-PI-CHANGELOG-811 | New Features | Nix/Guix support: `PI_PACKAGE_DIR` environment variable overrides the package path for contentaddressed package managers where store paths tokenize poorly. See [README.md#environmentvariables](README.md#environmentvariables). ([#1153](https://github.com/badlogic/pimono/pull/1153) by [@odysseus0](https://github.com/odysseus0)) | CHANGELOG.md |
| G-PI-CHANGELOG-812 | New Features | Named session filter: `/resume` picker now supports filtering to show only named sessions via Ctrl+N. Configurable via `toggleSessionNamedFilter` keybinding. See [docs/keybindings.md](docs/keybindings.md). ([#1128](https://github.com/badlogic/pimono/pull/1128) by [@wwinter](https://github.com/wwinter)) | CHANGELOG.md |
| G-PI-CHANGELOG-813 | New Features | Typed tool call events: Extension developers can narrow `ToolCallEvent` types using `isToolCallEventType()` for better TypeScript support. See [docs/extensions.md#toolcallevents](docs/extensions.md#toolcallevents). ([#1147](https://github.com/badlogic/pimono/pull/1147) by [@giuseppeg](https://github.com/giuseppeg)) | CHANGELOG.md |
| G-PI-CHANGELOG-814 | New Features | Extension UI Protocol: Full RPC documentation and examples for extension dialogs and notifications, enabling headless clients to support interactive extensions. See [docs/rpc.md#extensionuiprotocol](docs/rpc.md#extensionuiprotocol). ([#1144](https://github.com/badlogic/pimono/pull/1144) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-815 | Added | Added Linux ARM64 musl (Alpine Linux) support via clipboard dependency update | CHANGELOG.md |
| G-PI-CHANGELOG-816 | Added | Added Android/Termux support with graceful clipboard fallback ([#1164](https://github.com/badlogic/pimono/issues/1164)) | CHANGELOG.md |
| G-PI-CHANGELOG-817 | Added | Added bash tool spawn hook support for adjusting command, cwd, and env before execution ([#1160](https://github.com/badlogic/pimono/pull/1160) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-818 | Added | Added typed `ToolCallEvent.input` per tool with `isToolCallEventType()` type guard for narrowing builtin tool events ([#1147](https://github.com/badlogic/pimono/pull/1147) by [@giuseppeg](https://github.com/giuseppeg)) | CHANGELOG.md |
| G-PI-CHANGELOG-819 | Added | Exported `discoverAndLoadExtensions` from package to enable extension testing without a local repo clone ([#1148](https://github.com/badlogic/pimono/issues/1148)) | CHANGELOG.md |
| G-PI-CHANGELOG-820 | Added | Added Extension UI Protocol documentation to RPC docs covering all request/response types for extension dialogs and notifications ([#1144](https://github.com/badlogic/pimono/pull/1144) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-821 | Added | Added `rpcdemo.ts` example extension exercising all RPCsupported extension UI methods ([#1144](https://github.com/badlogic/pimono/pull/1144) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-822 | Added | Added `rpcextensionui.ts` TUI example client demonstrating the extension UI protocol with interactive dialogs ([#1144](https://github.com/badlogic/pimono/pull/1144) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-823 | Added | Added `PI_PACKAGE_DIR` environment variable to override package path for contentaddressed package managers (Nix, Guix) where store paths tokenize poorly ([#1153](https://github.com/badlogic/pimono/pull/1153) by [@odysseus0](https://github.com/odysseus0)) | CHANGELOG.md |
| G-PI-CHANGELOG-824 | Added | `/resume` session picker now supports namedonly filter toggle (default Ctrl+N, configurable via `toggleSessionNamedFilter`) to show only named sessions ([#1128](https://github.com/badlogic/pimono/pull/1128) by [@wwinter](https://github.com/wwinter)) | CHANGELOG.md |
| G-PI-CHANGELOG-825 | Fixed | Fixed `pi update` not updating npm/git packages when called without arguments ([#1151](https://github.com/badlogic/pimono/issues/1151)) | CHANGELOG.md |
| G-PI-CHANGELOG-826 | Fixed | Fixed `models.json` validation requiring fields documented as optional. Model definitions now only require `id`; all other fields (`name`, `reasoning`, `input`, `cost`, `contextWindow`, `maxTokens`) have sensible defaults. ([#1146](https://github.com/badlogic/pimono/issues/1146)) | CHANGELOG.md |
| G-PI-CHANGELOG-827 | Fixed | Fixed models resolving relative paths in skill files from cwd instead of skill directory by adding explicit guidance to skills preamble ([#1136](https://github.com/badlogic/pimono/issues/1136)) | CHANGELOG.md |
| G-PI-CHANGELOG-828 | Fixed | Fixed tree selector losing focus state when navigating entries ([#1142](https://github.com/badlogic/pimono/pull/1142) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-829 | Fixed | Fixed `cacheRetention` option not being passed through in `buildBaseOptions` ([#1154](https://github.com/badlogic/pimono/issues/1154)) | CHANGELOG.md |
| G-PI-CHANGELOG-830 | Fixed | Fixed OAuth login/refresh not using HTTP proxy settings (`HTTP_PROXY`, `HTTPS_PROXY` env vars) ([#1132](https://github.com/badlogic/pimono/issues/1132)) | CHANGELOG.md |
| G-PI-CHANGELOG-831 | Fixed | Fixed `pi update <source>` installing packages locally when the source is only registered globally ([#1163](https://github.com/badlogic/pimono/pull/1163) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-832 | Fixed | Fixed tree navigation with summarization overwriting editor content typed during the summarization wait ([#1169](https://github.com/badlogic/pimono/pull/1169) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-833 | Added | Added `titlebarspinner.ts` example extension that shows a braille spinner animation in the terminal title while the agent is working. | CHANGELOG.md |
| G-PI-CHANGELOG-834 | Added | Added `PI_AI_ANTIGRAVITY_VERSION` environment variable documentation to help text ([#1129](https://github.com/badlogic/pimono/issues/1129)) | CHANGELOG.md |
| G-PI-CHANGELOG-835 | Added | Added `cacheRetention` stream option with providerspecific mappings for prompt cache controls, defaulting to short retention ([#1134](https://github.com/badlogic/pimono/issues/1134)) | CHANGELOG.md |
| G-PI-CHANGELOG-836 | Added | Added `newSession`, `tree`, and `fork` keybinding actions for `/new`, `/tree`, and `/fork` commands. All unbound by default. ([#1114](https://github.com/badlogic/pimono/pull/1114) by [@juanibiapina](https://github.com/juanibiapina)) | CHANGELOG.md |
| G-PI-CHANGELOG-837 | Added | Added `retry.maxDelayMs` setting to cap maximum serverrequested retry delay. When a provider requests a longer delay (e.g., Google's "quota will reset after 5h"), the request fails immediately with an informative error instead of waiting silently. Default: 60000ms (60 seconds). ([#1123](https://github.com/badlogic/pimono/issues/1123)) | CHANGELOG.md |
| G-PI-CHANGELOG-838 | Added | `/resume` session picker: new "Threaded" sort mode (now default) displays sessions in a tree structure based on fork relationships. Compact oneline format with message count and age on the right. ([#1124](https://github.com/badlogic/pimono/pull/1124) by [@pasky](https://github.com/pasky)) | CHANGELOG.md |
| G-PI-CHANGELOG-839 | Added | Added Qwen CLI OAuth provider extension example. ([#940](https://github.com/badlogic/pimono/pull/940) by [@4h9fbZ](https://github.com/4h9fbZ)) | CHANGELOG.md |
| G-PI-CHANGELOG-840 | Added | Added OAuth `modifyModels` hook support for extensionregistered providers at registration time. ([#940](https://github.com/badlogic/pimono/pull/940) by [@4h9fbZ](https://github.com/4h9fbZ)) | CHANGELOG.md |
| G-PI-CHANGELOG-841 | Added | Added Qwen thinking format support for OpenAIcompatible completions via `enable_thinking`. ([#940](https://github.com/badlogic/pimono/pull/940) by [@4h9fbZ](https://github.com/4h9fbZ)) | CHANGELOG.md |
| G-PI-CHANGELOG-842 | Added | Added sticky column tracking for vertical cursor navigation so the editor restores the preferred column when moving across short lines. ([#1120](https://github.com/badlogic/pimono/pull/1120) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-843 | Added | Added `resources_discover` extension hook to supply additional skills, prompts, and themes on startup and reload. | CHANGELOG.md |
| G-PI-CHANGELOG-844 | Fixed | Fixed `switchSession()` appending spurious `thinking_level_change` entry to session log on resume. `setThinkingLevel()` is now idempotent. ([#1118](https://github.com/badlogic/pimono/issues/1118)) | CHANGELOG.md |
| G-PI-CHANGELOG-845 | Fixed | Fixed clipboard image paste on WSL2/WSLg writing invalid PNG files when clipboard provides `image/bmp` format. BMP images are now converted to PNG before saving. ([#1112](https://github.com/badlogic/pimono/pull/1112) by [@lightningRalf](https://github.com/lightningRalf)) | CHANGELOG.md |
| G-PI-CHANGELOG-846 | Fixed | Fixed Kitty keyboard protocol base layout fallback so nonQWERTY layouts do not trigger wrong shortcuts ([#1096](https://github.com/badlogic/pimono/pull/1096) by [@rytswd](https://github.com/rytswd)) | CHANGELOG.md |
| G-PI-CHANGELOG-847 | Fixed | Multifile extensions in packages now work correctly. Package resolution now uses the same discovery logic as local extensions: only `index.ts` (or manifestdeclared entries) are loaded from subdirectories, not helper modules. ([#1102](https://github.com/badlogic/pimono/issues/1102)) | CHANGELOG.md |
| G-PI-CHANGELOG-848 | Added | Added `ctx.getSystemPrompt()` to extension context for accessing the current effective system prompt ([#1098](https://github.com/badlogic/pimono/pull/1098) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-849 | Fixed | Fixed empty rows appearing below footer when content shrinks (e.g., closing `/tree`, clearing multiline editor) ([#1095](https://github.com/badlogic/pimono/pull/1095) by [@marckrenn](https://github.com/marckrenn)) | CHANGELOG.md |
| G-PI-CHANGELOG-850 | Fixed | Fixed terminal cursor remaining hidden after exiting TUI via `stop()` when a render was pending ([#1099](https://github.com/badlogic/pimono/pull/1099) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-851 | New Features | OSC 52 clipboard support for SSH/mosh  The `/copy` command now works over remote connections using the OSC 52 terminal escape sequence. No more clipboard frustration when using pi over SSH. ([#1069](https://github.com/badlogic/pimono/issues/1069) by [@gturkoglu](https://github.com/gturkoglu)) | CHANGELOG.md |
| G-PI-CHANGELOG-852 | New Features | Vercel AI Gateway routing  Route requests through Vercel's AI Gateway with provider failover and load balancing. Configure via `vercelGatewayRouting` in models.json. ([#1051](https://github.com/badlogic/pimono/pull/1051) by [@benvargas](https://github.com/benvargas)) | CHANGELOG.md |
| G-PI-CHANGELOG-853 | New Features | Character jump navigation  Bash/Readlinestyle character search: Ctrl+] jumps forward to the next occurrence of a character, Ctrl+Alt+] jumps backward. ([#1074](https://github.com/badlogic/pimono/pull/1074) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-854 | New Features | Emacsstyle Ctrl+B/Ctrl+F navigation  Alternative keybindings for word navigation (cursor word left/right) in the editor. ([#1053](https://github.com/badlogic/pimono/pull/1053) by [@ninlds](https://github.com/ninlds)) | CHANGELOG.md |
| G-PI-CHANGELOG-855 | New Features | Line boundary navigation  Editor jumps to line start when pressing Up at first visual line, and line end when pressing Down at last visual line. ([#1050](https://github.com/badlogic/pimono/pull/1050) by [@4h9fbZ](https://github.com/4h9fbZ)) | CHANGELOG.md |
| G-PI-CHANGELOG-856 | New Features | Performance improvements  Optimized image line detection and box rendering cache in the TUI for better rendering performance. ([#1084](https://github.com/badlogic/pimono/pull/1084) by [@can1357](https://github.com/can1357)) | CHANGELOG.md |
| G-PI-CHANGELOG-857 | New Features | `set_session_name` RPC command  Headless clients can now set the session display name programmatically. ([#1075](https://github.com/badlogic/pimono/pull/1075) by [@dnouri](https://github.com/dnouri)) | CHANGELOG.md |
| G-PI-CHANGELOG-858 | New Features | Disable doubleescape behavior  New `"none"` option for `doubleEscapeAction` setting completely disables the doubleescape shortcut. ([#973](https://github.com/badlogic/pimono/issues/973) by [@juanibiapina](https://github.com/juanibiapina)) | CHANGELOG.md |
| G-PI-CHANGELOG-859 | Added | Added "none" option to `doubleEscapeAction` setting to disable doubleescape behavior entirely ([#973](https://github.com/badlogic/pimono/issues/973) by [@juanibiapina](https://github.com/juanibiapina)) | CHANGELOG.md |
| G-PI-CHANGELOG-860 | Added | Added OSC 52 clipboard support for SSH/mosh sessions. `/copy` now works over remote connections. ([#1069](https://github.com/badlogic/pimono/issues/1069) by [@gturkoglu](https://github.com/gturkoglu)) | CHANGELOG.md |
| G-PI-CHANGELOG-861 | Added | Added Vercel AI Gateway routing support via `vercelGatewayRouting` in models.json ([#1051](https://github.com/badlogic/pimono/pull/1051) by [@benvargas](https://github.com/benvargas)) | CHANGELOG.md |
| G-PI-CHANGELOG-862 | Added | Added Ctrl+B and Ctrl+F keybindings for cursor word left/right navigation in the editor ([#1053](https://github.com/badlogic/pimono/pull/1053) by [@ninlds](https://github.com/ninlds)) | CHANGELOG.md |
| G-PI-CHANGELOG-863 | Added | Added character jump navigation: Ctrl+] jumps forward to next character, Ctrl+Alt+] jumps backward ([#1074](https://github.com/badlogic/pimono/pull/1074) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-864 | Added | Editor now jumps to line start when pressing Up at first visual line, and line end when pressing Down at last visual line ([#1050](https://github.com/badlogic/pimono/pull/1050) by [@4h9fbZ](https://github.com/4h9fbZ)) | CHANGELOG.md |
| G-PI-CHANGELOG-865 | Added | Optimized image line detection and box rendering cache for better TUI performance ([#1084](https://github.com/badlogic/pimono/pull/1084) by [@can1357](https://github.com/can1357)) | CHANGELOG.md |
| G-PI-CHANGELOG-866 | Added | Added `set_session_name` RPC command for headless clients to set session display name ([#1075](https://github.com/badlogic/pimono/pull/1075) by [@dnouri](https://github.com/dnouri)) | CHANGELOG.md |
| G-PI-CHANGELOG-867 | Fixed | Read tool now handles macOS filenames with curly quotes (U+2019) and NFD Unicode normalization ([#1078](https://github.com/badlogic/pimono/issues/1078)) | CHANGELOG.md |
| G-PI-CHANGELOG-868 | Fixed | Respect .gitignore, .ignore, and .fdignore files when scanning package resources for skills, prompts, themes, and extensions ([#1072](https://github.com/badlogic/pimono/issues/1072)) | CHANGELOG.md |
| G-PI-CHANGELOG-869 | Fixed | Fixed tool call argument defaults when providers omit inputs ([#1065](https://github.com/badlogic/pimono/issues/1065)) | CHANGELOG.md |
| G-PI-CHANGELOG-870 | Fixed | Invalid JSON in settings.json no longer causes the file to be overwritten with empty settings ([#1054](https://github.com/badlogic/pimono/issues/1054)) | CHANGELOG.md |
| G-PI-CHANGELOG-871 | Fixed | Config selector now shows folder name for extensions with duplicate display names ([#1064](https://github.com/badlogic/pimono/pull/1064) by [@Graffioh](https://github.com/Graffioh)) | CHANGELOG.md |
| G-PI-CHANGELOG-872 | New Features | Kimi For Coding provider: Access Moonshot AI's Anthropiccompatible coding API. Set `KIMI_API_KEY` environment variable. See [README.md#kimiforcoding](README.md#kimiforcoding). | CHANGELOG.md |
| G-PI-CHANGELOG-873 | Added | Added Kimi For Coding provider support (Moonshot AI's Anthropiccompatible coding API). Set `KIMI_API_KEY` environment variable. See [README.md#kimiforcoding](README.md#kimiforcoding). | CHANGELOG.md |
| G-PI-CHANGELOG-874 | Fixed | Resources now appear before messages when resuming a session, preventing loaded context from appearing at the bottom of the chat. | CHANGELOG.md |
| G-PI-CHANGELOG-875 | New Features | Hugging Face provider: Access Hugging Face models via OpenAIcompatible Inference Router. Set `HF_TOKEN` environment variable. See [README.md#huggingface](README.md#huggingface). | CHANGELOG.md |
| G-PI-CHANGELOG-876 | New Features | Extended prompt caching: `PI_CACHE_RETENTION=long` enables 1hour caching for Anthropic (vs 5min default) and 24hour for OpenAI (vs inmemory default). Only applies to direct API calls. See [README.md#promptcaching](README.md#promptcaching). | CHANGELOG.md |
| G-PI-CHANGELOG-877 | New Features | Configurable autocomplete height: `autocompleteMaxVisible` setting (320 items, default 5) controls dropdown size. Adjust via `/settings` or `settings.json`. | CHANGELOG.md |
| G-PI-CHANGELOG-878 | New Features | Shellstyle keybindings: `alt+b`/`alt+f` for word navigation, `ctrl+d` for delete character forward. See [docs/keybindings.md](docs/keybindings.md). | CHANGELOG.md |
| G-PI-CHANGELOG-879 | New Features | RPC `get_commands`: Headless clients can now list available commands programmatically. See [docs/rpc.md](docs/rpc.md). | CHANGELOG.md |
| G-PI-CHANGELOG-880 | Added | Added Hugging Face provider support via OpenAIcompatible Inference Router ([#994](https://github.com/badlogic/pimono/issues/994)) | CHANGELOG.md |
| G-PI-CHANGELOG-881 | Added | Added `PI_CACHE_RETENTION` environment variable to control cache TTL for Anthropic (5m vs 1h) and OpenAI (inmemory vs 24h). Set to `long` for extended retention. ([#967](https://github.com/badlogic/pimono/issues/967)) | CHANGELOG.md |
| G-PI-CHANGELOG-882 | Added | Added `autocompleteMaxVisible` setting for configurable autocomplete dropdown height (320 items, default 5) ([#972](https://github.com/badlogic/pimono/pull/972) by [@masonc15](https://github.com/masonc15)) | CHANGELOG.md |
| G-PI-CHANGELOG-883 | Added | Added `/files` command to list all file operations (read, write, edit) in the current session | CHANGELOG.md |
| G-PI-CHANGELOG-884 | Added | Added shellstyle keybindings: `alt+b`/`alt+f` for word navigation, `ctrl+d` for delete character forward (when editor has text) ([#1043](https://github.com/badlogic/pimono/issues/1043) by [@jasonish](https://github.com/jasonish)) | CHANGELOG.md |
| G-PI-CHANGELOG-885 | Added | Added `get_commands` RPC method for headless clients to list available commands ([#995](https://github.com/badlogic/pimono/pull/995) by [@dnouri](https://github.com/dnouri)) | CHANGELOG.md |
| G-PI-CHANGELOG-886 | Changed | Improved `extractCursorPosition` performance in TUI: scans lines in reverse order, earlyouts when cursor is above viewport ([#1004](https://github.com/badlogic/pimono/pull/1004) by [@can1357](https://github.com/can1357)) | CHANGELOG.md |
| G-PI-CHANGELOG-887 | Changed | Autocomplete improvements: better handling of partial matches and edge cases ([#1024](https://github.com/badlogic/pimono/pull/1024) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-888 | Fixed | External edits to `settings.json` are now preserved when pi reloads or saves unrelated settings. Previously, editing settings.json directly (e.g., removing a package from `packages` array) would be silently reverted on next pi startup when automatic setters like `setLastChangelogVersion()` triggered a save. | CHANGELOG.md |
| G-PI-CHANGELOG-889 | Fixed | Fixed custom header not displaying correctly with `quietStartup` enabled ([#1039](https://github.com/badlogic/pimono/pull/1039) by [@tudoroancea](https://github.com/tudoroancea)) | CHANGELOG.md |
| G-PI-CHANGELOG-890 | Fixed | Empty array in package filter now disables all resources instead of falling back to manifest defaults ([#1044](https://github.com/badlogic/pimono/issues/1044)) | CHANGELOG.md |
| G-PI-CHANGELOG-891 | Fixed | Autoretry counter now resets after each successful LLM response instead of accumulating across tooluse turns ([#1019](https://github.com/badlogic/pimono/issues/1019)) | CHANGELOG.md |
| G-PI-CHANGELOG-892 | Fixed | Fixed incorrect `.md` file names in warning messages ([#1041](https://github.com/badlogic/pimono/issues/1041) by [@llimllib](https://github.com/llimllib)) | CHANGELOG.md |
| G-PI-CHANGELOG-893 | Fixed | Fixed provider name hidden in footer when terminal is narrow ([#981](https://github.com/badlogic/pimono/pull/981) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-894 | Fixed | Fixed backslash input buffering causing delayed character display in editor ([#1037](https://github.com/badlogic/pimono/pull/1037) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-895 | Fixed | Fixed markdown table rendering with proper row dividers and minimum column width ([#997](https://github.com/badlogic/pimono/pull/997) by [@tmustier](https://github.com/tmustier)) | CHANGELOG.md |
| G-PI-CHANGELOG-896 | Fixed | Fixed OpenAI completions `toolChoice` handling ([#998](https://github.com/badlogic/pimono/pull/998) by [@williamtwomey](https://github.com/williamtwomey)) | CHANGELOG.md |
| G-PI-CHANGELOG-897 | Fixed | Fixed crossprovider handoff failing when switching from OpenAI Responses API providers due to pipeseparated tool call IDs ([#1022](https://github.com/badlogic/pimono/issues/1022)) | CHANGELOG.md |
| G-PI-CHANGELOG-898 | Fixed | Fixed 429 rate limit errors incorrectly triggering autocompaction instead of retry with backoff ([#1038](https://github.com/badlogic/pimono/issues/1038)) | CHANGELOG.md |
| G-PI-CHANGELOG-899 | Fixed | Fixed Anthropic provider to handle `sensitive` stop_reason returned by API ([#978](https://github.com/badlogic/pimono/issues/978)) | CHANGELOG.md |
| G-PI-CHANGELOG-900 | Fixed | Fixed DeepSeek API compatibility by detecting `deepseek.com` URLs and disabling unsupported `developer` role ([#1048](https://github.com/badlogic/pimono/issues/1048)) | CHANGELOG.md |
| G-PI-CHANGELOG-901 | Fixed | Fixed Anthropic provider to preserve input token counts when proxies omit them in `message_delta` events ([#1045](https://github.com/badlogic/pimono/issues/1045)) | CHANGELOG.md |
| G-PI-CHANGELOG-902 | Fixed | Fixed `autocompleteMaxVisible` setting not persisting to `settings.json` | CHANGELOG.md |
| G-PI-CHANGELOG-903 | Fixed | Git extension updates now handle forcepushed remotes gracefully instead of failing ([#961](https://github.com/badlogic/pimono/pull/961) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-904 | Fixed | Extension `ctx.newSession({ setup })` now properly syncs agent state and renders messages after setup callback runs ([#968](https://github.com/badlogic/pimono/issues/968)) | CHANGELOG.md |
| G-PI-CHANGELOG-905 | Fixed | Fixed extension UI bindings not initializing when starting with no extensions, which broke UI methods after `/reload` | CHANGELOG.md |
| G-PI-CHANGELOG-906 | Fixed | Fixed `/hotkeys` output to titlecase extension hotkeys ([#969](https://github.com/badlogic/pimono/pull/969) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-907 | Fixed | Fixed model catalog generation to exclude deprecated OpenCode Zen models ([#970](https://github.com/badlogic/pimono/pull/970) by [@DanielTatarkin](https://github.com/DanielTatarkin)) | CHANGELOG.md |
| G-PI-CHANGELOG-908 | Fixed | Fixed git extension removal to prune empty directories | CHANGELOG.md |
| G-PI-CHANGELOG-909 | New Features | Pi packages for bundling and installing extensions, skills, prompts, and themes. See [docs/packages.md](docs/packages.md). | CHANGELOG.md |
| G-PI-CHANGELOG-910 | New Features | Hot reload (`/reload`) of resources including AGENTS.md, SYSTEM.md, APPEND_SYSTEM.md, prompt templates, skills, themes, and extensions. See [README.md#commands](README.md#commands) and [README.md#contextfiles](README.md#contextfiles). | CHANGELOG.md |
| G-PI-CHANGELOG-911 | New Features | Custom providers via `pi.registerProvider()` for proxies, custom endpoints, OAuth or SSO flows, and nonstandard streaming APIs. See [docs/customprovider.md](docs/customprovider.md). | CHANGELOG.md |
| G-PI-CHANGELOG-912 | New Features | Azure OpenAI Responses provider support with deploymentaware model mapping. See [docs/providers.md#azureopenai](docs/providers.md#azureopenai). | CHANGELOG.md |
| G-PI-CHANGELOG-913 | New Features | OpenRouter routing support for custom models via `openRouterRouting`. See [docs/providers.md#apikeys](docs/providers.md#apikeys) and [docs/models.md](docs/models.md). | CHANGELOG.md |
| G-PI-CHANGELOG-914 | New Features | Skill invocation messages are now collapsible and skills can opt out of model invocation via `disablemodelinvocation`. See [docs/skills.md#frontmatter](docs/skills.md#frontmatter). | CHANGELOG.md |
| G-PI-CHANGELOG-915 | New Features | Session selector renaming and configurable keybindings. See [README.md#commands](README.md#commands) and [docs/keybindings.md](docs/keybindings.md). | CHANGELOG.md |
| G-PI-CHANGELOG-916 | New Features | `models.json` headers can resolve environment variables and shell commands. See [docs/models.md#valueresolution](docs/models.md#valueresolution). | CHANGELOG.md |
| G-PI-CHANGELOG-917 | New Features | `verbose` CLI flag to override quiet startup. See [README.md#clireference](README.md#clireference). | CHANGELOG.md |
| G-PI-CHANGELOG-918 | Breaking Changes | Header values in `models.json` now resolve environment variables (if a header value matches an env var name, the env var value is used). This may change behavior if a literal header value accidentally matches an env var name. ([#909](https://github.com/badlogic/pimono/issues/909)) | CHANGELOG.md |
| G-PI-CHANGELOG-919 | Breaking Changes | External packages (npm/git) are now configured via `packages` array in settings.json instead of `extensions`. Existing npm:/git: entries in `extensions` are automigrated. ([#645](https://github.com/badlogic/pimono/issues/645)) | CHANGELOG.md |
| G-PI-CHANGELOG-920 | Breaking Changes | Resource loading now uses `ResourceLoader` only and settings.json uses arrays for extensions, skills, prompts, and themes ([#645](https://github.com/badlogic/pimono/issues/645)) | CHANGELOG.md |
| G-PI-CHANGELOG-921 | Breaking Changes | Removed `discoverAuthStorage` and `discoverModels` from the SDK. `AuthStorage` and `ModelRegistry` now default to `~/.pi/agent` paths unless you pass an `agentDir` ([#645](https://github.com/badlogic/pimono/issues/645)) | CHANGELOG.md |
| G-PI-CHANGELOG-922 | Added | Session renaming in `/resume` picker via `Ctrl+R` without opening the session ([#863](https://github.com/badlogic/pimono/pull/863) by [@svkozak](https://github.com/svkozak)) | CHANGELOG.md |
| G-PI-CHANGELOG-923 | Added | Session selector keybindings are now configurable ([#948](https://github.com/badlogic/pimono/pull/948) by [@aos](https://github.com/aos)) | CHANGELOG.md |
| G-PI-CHANGELOG-924 | Added | `disablemodelinvocation` frontmatter field for skills to prevent agentic invocation while still allowing explicit `/skill:name` commands ([#927](https://github.com/badlogic/pimono/issues/927)) | CHANGELOG.md |
| G-PI-CHANGELOG-925 | Added | Exposed `copyToClipboard` utility for extensions ([#926](https://github.com/badlogic/pimono/issues/926) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-926 | Added | Skill invocation messages are now collapsible in chat output, showing collapsed by default with skill name and expand hint ([#894](https://github.com/badlogic/pimono/issues/894)) | CHANGELOG.md |
| G-PI-CHANGELOG-927 | Added | Header values in `models.json` now support environment variables and shell commands, matching `apiKey` resolution ([#909](https://github.com/badlogic/pimono/issues/909)) | CHANGELOG.md |
| G-PI-CHANGELOG-928 | Added | Added HTTP proxy environment variable support for API requests ([#942](https://github.com/badlogic/pimono/pull/942) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-929 | Added | Added OpenRouter provider routing support for custom models via `openRouterRouting` compat field ([#859](https://github.com/badlogic/pimono/pull/859) by [@v01dpr1mr0s3](https://github.com/v01dpr1mr0s3)) | CHANGELOG.md |
| G-PI-CHANGELOG-930 | Added | Added `azureopenairesponses` provider support for Azure OpenAI Responses API. ([#890](https://github.com/badlogic/pimono/pull/890) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-931 | Added | Added changelog link to update notifications ([#925](https://github.com/badlogic/pimono/pull/925) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-932 | Added | Added `verbose` CLI flag to override quietStartup setting ([#906](https://github.com/badlogic/pimono/pull/906) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-933 | Added | `markdown.codeBlockIndent` setting to customize code block indentation in rendered output | CHANGELOG.md |
| G-PI-CHANGELOG-934 | Added | Extension package management with `pi install`, `pi remove`, `pi update`, and `pi list` commands ([#645](https://github.com/badlogic/pimono/issues/645)) | CHANGELOG.md |
| G-PI-CHANGELOG-935 | Added | Package filtering: selectively load resources from packages using object form in `packages` array ([#645](https://github.com/badlogic/pimono/issues/645)) | CHANGELOG.md |
| G-PI-CHANGELOG-936 | Added | Glob pattern support with minimatch in package filters, toplevel settings arrays, and pi manifest (e.g., `"!funky.json"`, `".ts"`) ([#645](https://github.com/badlogic/pimono/issues/645)) | CHANGELOG.md |
| G-PI-CHANGELOG-937 | Added | `/reload` command to reload extensions, skills, prompts, and themes ([#645](https://github.com/badlogic/pimono/issues/645)) | CHANGELOG.md |
| G-PI-CHANGELOG-938 | Added | `pi config` command with TUI to enable/disable package and toplevel resources via patterns ([#938](https://github.com/badlogic/pimono/issues/938)) | CHANGELOG.md |
| G-PI-CHANGELOG-939 | Added | CLI flags for `skill`, `prompttemplate`, `theme`, `noprompttemplates`, and `nothemes` ([#645](https://github.com/badlogic/pimono/issues/645)) | CHANGELOG.md |
| G-PI-CHANGELOG-940 | Added | Package deduplication: if same package appears in global and project settings, project wins ([#645](https://github.com/badlogic/pimono/issues/645)) | CHANGELOG.md |
| G-PI-CHANGELOG-941 | Added | Unified collision reporting with `ResourceDiagnostic` type for all resource types ([#645](https://github.com/badlogic/pimono/issues/645)) | CHANGELOG.md |
| G-PI-CHANGELOG-942 | Added | Show provider alongside the model in the footer if multiple providers are available | CHANGELOG.md |
| G-PI-CHANGELOG-943 | Added | Custom provider support via `pi.registerProvider()` with `streamSimple` for custom API implementations | CHANGELOG.md |
| G-PI-CHANGELOG-944 | Added | Added `customprovider.ts` example extension demonstrating custom Anthropic provider with OAuth | CHANGELOG.md |
| G-PI-CHANGELOG-945 | Changed | `/resume` picker sort toggle moved to `Ctrl+S` to free `Ctrl+R` for rename ([#863](https://github.com/badlogic/pimono/pull/863) by [@svkozak](https://github.com/svkozak)) | CHANGELOG.md |
| G-PI-CHANGELOG-946 | Changed | HTML export: clicking a sidebar message now navigates to its newest leaf and scrolls to it, instead of truncating the branch ([#853](https://github.com/badlogic/pimono/pull/853) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-947 | Changed | HTML export: active path is now visually highlighted with dimmed offpath nodes ([#929](https://github.com/badlogic/pimono/pull/929) by [@hewliyang](https://github.com/hewliyang)) | CHANGELOG.md |
| G-PI-CHANGELOG-948 | Changed | Azure OpenAI Responses provider now uses base URL configuration with deploymentaware model mapping and no longer includes service tier handling | CHANGELOG.md |
| G-PI-CHANGELOG-949 | Changed | `/reload` now rerenders the entire scrollback so updated extension components are visible immediately ([#928](https://github.com/badlogic/pimono/pull/928) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-950 | Changed | Skill, prompt template, and theme discovery now use settings and CLI path arrays instead of legacy filters ([#645](https://github.com/badlogic/pimono/issues/645)) | CHANGELOG.md |
| G-PI-CHANGELOG-951 | Fixed | Extension `setWorkingMessage()` calls in `agent_start` handlers now work correctly; previously the message was silently ignored because the loading animation didn't exist yet ([#935](https://github.com/badlogic/pimono/issues/935)) | CHANGELOG.md |
| G-PI-CHANGELOG-952 | Fixed | Fixed package autodiscovery to respect loader rules, config overrides, and forceexclude patterns | CHANGELOG.md |
| G-PI-CHANGELOG-953 | Fixed | Fixed /reload restoring the correct editor after reload ([#949](https://github.com/badlogic/pimono/pull/949) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-954 | Fixed | Fixed distributed themes breaking `/export` ([#946](https://github.com/badlogic/pimono/pull/946) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-955 | Fixed | Fixed startup hints to clarify thinking level selection and expanded thinking guidance | CHANGELOG.md |
| G-PI-CHANGELOG-956 | Fixed | Fixed SDK initial model resolution to use `findInitialModel` and default to Claude Opus 4.5 for Anthropic models | CHANGELOG.md |
| G-PI-CHANGELOG-957 | Fixed | Fixed nomodels warning to include the `/model` instruction | CHANGELOG.md |
| G-PI-CHANGELOG-958 | Fixed | Fixed authentication error messages to point to the authentication documentation | CHANGELOG.md |
| G-PI-CHANGELOG-959 | Fixed | Fixed bash output hint lines to truncate to terminal width | CHANGELOG.md |
| G-PI-CHANGELOG-960 | Fixed | Fixed custom editors to honor the `paddingX` setting ([#936](https://github.com/badlogic/pimono/pull/936) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-961 | Fixed | Fixed system prompt tool list to show only builtin tools | CHANGELOG.md |
| G-PI-CHANGELOG-962 | Fixed | Fixed package manager to check npm package versions before using cached copies | CHANGELOG.md |
| G-PI-CHANGELOG-963 | Fixed | Fixed package manager to run `npm install` after cloning git repositories with a package.json | CHANGELOG.md |
| G-PI-CHANGELOG-964 | Fixed | Fixed extension provider registrations to apply before model resolution | CHANGELOG.md |
| G-PI-CHANGELOG-965 | Fixed | Fixed editor multiline insertion handling and lastAction tracking ([#945](https://github.com/badlogic/pimono/pull/945) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-966 | Fixed | Fixed editor word wrapping to reserve a cursor column ([#934](https://github.com/badlogic/pimono/pull/934) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-967 | Fixed | Fixed editor word wrapping to use singlepass backtracking for whitespace handling ([#924](https://github.com/badlogic/pimono/pull/924) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-968 | Fixed | Fixed Kitty image ID allocation and cleanup to prevent image ID collisions | CHANGELOG.md |
| G-PI-CHANGELOG-969 | Fixed | Fixed overlays staying centered after terminal resizes ([#950](https://github.com/badlogic/pimono/pull/950) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-970 | Fixed | Fixed streaming dispatch to use the model api type instead of hardcoded API defaults | CHANGELOG.md |
| G-PI-CHANGELOG-971 | Fixed | Fixed Google providers to default tool call arguments to an empty object when omitted | CHANGELOG.md |
| G-PI-CHANGELOG-972 | Fixed | Fixed OpenAI Responses streaming to handle `arguments.done` events on OpenAIcompatible endpoints ([#917](https://github.com/badlogic/pimono/pull/917) by [@williballenthin](https://github.com/williballenthin)) | CHANGELOG.md |
| G-PI-CHANGELOG-973 | Fixed | Fixed OpenAI Codex Responses tool strictness handling after the shared responses refactor | CHANGELOG.md |
| G-PI-CHANGELOG-974 | Fixed | Fixed Azure OpenAI Responses streaming to guard deltas before content parts and correct metadata and handoff gating | CHANGELOG.md |
| G-PI-CHANGELOG-975 | Fixed | Fixed OpenAI completions toolresult image batching after consecutive tool results ([#902](https://github.com/badlogic/pimono/pull/902) by [@terrorobe](https://github.com/terrorobe)) | CHANGELOG.md |
| G-PI-CHANGELOG-976 | Fixed | Offbyone error in bash output "earlier lines" count caused by counting spacing newline as hidden content ([#921](https://github.com/badlogic/pimono/issues/921)) | CHANGELOG.md |
| G-PI-CHANGELOG-977 | Fixed | User package filters now layer on top of manifest filters instead of replacing them ([#645](https://github.com/badlogic/pimono/issues/645)) | CHANGELOG.md |
| G-PI-CHANGELOG-978 | Fixed | Autoretry now handles "terminated" errors from Codex API midstream failures | CHANGELOG.md |
| G-PI-CHANGELOG-979 | Fixed | Followup queue (Alt+Enter) now sends full paste content instead of `[paste #N ...]` markers ([#912](https://github.com/badlogic/pimono/issues/912)) | CHANGELOG.md |
| G-PI-CHANGELOG-980 | Fixed | Fixed AltUp not restoring messages queued during compaction ([#923](https://github.com/badlogic/pimono/pull/923) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-981 | Fixed | Fixed session corruption when loading empty or invalid session files via `session` flag ([#932](https://github.com/badlogic/pimono/issues/932) by [@armanddp](https://github.com/armanddp)) | CHANGELOG.md |
| G-PI-CHANGELOG-982 | Fixed | Fixed extension shortcuts not firing when extension also uses `setEditorComponent()` ([#947](https://github.com/badlogic/pimono/pull/947) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-983 | Fixed | Session "modified" time now uses last message timestamp instead of file mtime, so renaming doesn't reorder the recent list ([#863](https://github.com/badlogic/pimono/pull/863) by [@svkozak](https://github.com/svkozak)) | CHANGELOG.md |
| G-PI-CHANGELOG-984 | Added | `markdown.codeBlockIndent` setting to customize code block indentation in rendered output ([#855](https://github.com/badlogic/pimono/pull/855) by [@terrorobe](https://github.com/terrorobe)) | CHANGELOG.md |
| G-PI-CHANGELOG-985 | Added | Added `inlinebash.ts` example extension for expanding `!{command}` patterns in prompts ([#881](https://github.com/badlogic/pimono/pull/881) by [@scutifer](https://github.com/scutifer)) | CHANGELOG.md |
| G-PI-CHANGELOG-986 | Added | Added `antigravityimagegen.ts` example extension for AI image generation via Google Antigravity ([#893](https://github.com/badlogic/pimono/pull/893) by [@benvargas](https://github.com/benvargas)) | CHANGELOG.md |
| G-PI-CHANGELOG-987 | Added | Added `PI_SHARE_VIEWER_URL` environment variable for custom share viewer URLs ([#889](https://github.com/badlogic/pimono/pull/889) by [@andresaraujo](https://github.com/andresaraujo)) | CHANGELOG.md |
| G-PI-CHANGELOG-988 | Added | Added Alt+Delete as hotkey for delete word forwards ([#878](https://github.com/badlogic/pimono/pull/878) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-989 | Changed | Tree selector: changed label filter shortcut from `l` to `Shift+L` so users can search for entries containing "l" ([#861](https://github.com/badlogic/pimono/pull/861) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-990 | Changed | Fuzzy matching now scores consecutive matches higher for better search relevance ([#860](https://github.com/badlogic/pimono/pull/860) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-991 | Fixed | Fixed error messages showing hardcoded `~/.pi/agent/` paths instead of respecting `PI_CODING_AGENT_DIR` ([#887](https://github.com/badlogic/pimono/pull/887) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-992 | Fixed | Fixed `write` tool not displaying errors in the UI when execution fails ([#856](https://github.com/badlogic/pimono/issues/856)) | CHANGELOG.md |
| G-PI-CHANGELOG-993 | Fixed | Fixed HTML export using default theme instead of user's active theme ([#870](https://github.com/badlogic/pimono/pull/870) by [@scutifer](https://github.com/scutifer)) | CHANGELOG.md |
| G-PI-CHANGELOG-994 | Fixed | Show session name in the footer and terminal / tab title ([#876](https://github.com/badlogic/pimono/pull/876) by [@scutifer](https://github.com/scutifer)) | CHANGELOG.md |
| G-PI-CHANGELOG-995 | Fixed | Fixed 256color fallback in Terminal.app to prevent color rendering issues ([#869](https://github.com/badlogic/pimono/pull/869) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-996 | Fixed | Fixed viewport tracking and cursor positioning for overlays and content shrink scenarios | CHANGELOG.md |
| G-PI-CHANGELOG-997 | Fixed | Fixed autocomplete to allow searches with `/` characters (e.g., `folder1/folder2`) ([#882](https://github.com/badlogic/pimono/pull/882) by [@richardgill](https://github.com/richardgill)) | CHANGELOG.md |
| G-PI-CHANGELOG-998 | Fixed | Fixed autolinked emails displaying redundant `(mailto:...)` suffix ([#888](https://github.com/badlogic/pimono/pull/888) by [@terrorobe](https://github.com/terrorobe)) | CHANGELOG.md |
| G-PI-CHANGELOG-999 | Fixed | Fixed `@` file autocomplete adding space after directories, breaking continued autocomplete into subdirectories | CHANGELOG.md |
| G-PI-CHANGELOG-1000 | Added | Added widget placement option for extension widgets via `widgetPlacement` in `pi.addWidget()` ([#850](https://github.com/badlogic/pimono/pull/850) by [@marckrenn](https://github.com/marckrenn)) | CHANGELOG.md |
| G-PI-CHANGELOG-1001 | Added | Added AWS credential detection for ECS/Kubernetes environments: `AWS_CONTAINER_CREDENTIALS_RELATIVE_URI`, `AWS_CONTAINER_CREDENTIALS_FULL_URI`, `AWS_WEB_IDENTITY_TOKEN_FILE` ([#848](https://github.com/badlogic/pimono/issues/848)) | CHANGELOG.md |
| G-PI-CHANGELOG-1002 | Added | Add "quiet startup" setting to `/settings` ([#847](https://github.com/badlogic/pimono/pull/847) by [@unexge](https://github.com/unexge)) | CHANGELOG.md |
| G-PI-CHANGELOG-1003 | Changed | HTML export now includes JSONL download button, jumptolastmessage on click, and fixed missing labels ([#853](https://github.com/badlogic/pimono/pull/853) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1004 | Changed | Improved error message for OAuth authentication failures (expired credentials, offline) instead of generic 'No API key found' ([#849](https://github.com/badlogic/pimono/pull/849) by [@zedrdave](https://github.com/zedrdave)) | CHANGELOG.md |
| G-PI-CHANGELOG-1005 | Fixed | Fixed `/model` selector scope toggle so you can switch between all and scoped models when scoped models are saved ([#844](https://github.com/badlogic/pimono/issues/844)) | CHANGELOG.md |
| G-PI-CHANGELOG-1006 | Fixed | Fixed OpenAI Responses 400 error "reasoning without following item" when replaying aborted turns ([#838](https://github.com/badlogic/pimono/pull/838)) | CHANGELOG.md |
| G-PI-CHANGELOG-1007 | Fixed | Fixed pi exiting with code 0 when cancelling resume session selection | CHANGELOG.md |
| G-PI-CHANGELOG-1008 | Removed | Removed `strictResponsesPairing` compat option from models.json schema (no longer needed) | CHANGELOG.md |
| G-PI-CHANGELOG-1009 | Added | Added `strictResponsesPairing` compat option for custom OpenAI Responses models on Azure ([#768](https://github.com/badlogic/pimono/pull/768) by [@prateekmedia](https://github.com/prateekmedia)) | CHANGELOG.md |
| G-PI-CHANGELOG-1010 | Added | Session selector (`/resume`) now supports path display toggle (`Ctrl+P`) and session deletion (`Ctrl+D`) with inline confirmation ([#816](https://github.com/badlogic/pimono/pull/816) by [@wwinter](https://github.com/wwinter)) | CHANGELOG.md |
| G-PI-CHANGELOG-1011 | Added | Added undo support in interactive mode with Ctrl+ hotkey. ([#831](https://github.com/badlogic/pimono/pull/831) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-1012 | Changed | Share URLs now use hash fragments (`#`) instead of query strings (`?`) to prevent session IDs from being sent to buildwithpi.ai ([#829](https://github.com/badlogic/pimono/pull/829) by [@terrorobe](https://github.com/terrorobe)) | CHANGELOG.md |
| G-PI-CHANGELOG-1013 | Changed | API keys in `models.json` can now be retrieved via shell command using `!` prefix (e.g., `"apiKey": "!security findgenericpassword ws 'anthropic'"` for macOS Keychain) ([#762](https://github.com/badlogic/pimono/pull/762) by [@cv](https://github.com/cv)) | CHANGELOG.md |
| G-PI-CHANGELOG-1014 | Fixed | Fixed IME candidate window appearing in wrong position when filtering menus with Input Method Editor (e.g., Chinese IME). Components with search inputs now properly propagate focus state for cursor positioning. ([#827](https://github.com/badlogic/pimono/issues/827)) | CHANGELOG.md |
| G-PI-CHANGELOG-1015 | Fixed | Fixed extension shortcut conflicts to respect user keybindings when builtin actions are remapped. ([#826](https://github.com/badlogic/pimono/pull/826) by [@richardgill](https://github.com/richardgill)) | CHANGELOG.md |
| G-PI-CHANGELOG-1016 | Fixed | Fixed photon WASM loading in standalone compiled binaries. | CHANGELOG.md |
| G-PI-CHANGELOG-1017 | Fixed | Fixed tool call ID normalization for crossprovider handoffs (e.g., Codex to Antigravity Claude) ([#821](https://github.com/badlogic/pimono/issues/821)) | CHANGELOG.md |
| G-PI-CHANGELOG-1018 | Added | `pi.setLabel(entryId, label)` in ExtensionAPI for setting perentry labels from extensions ([#806](https://github.com/badlogic/pimono/issues/806)) | CHANGELOG.md |
| G-PI-CHANGELOG-1019 | Added | Export `keyHint`, `appKeyHint`, `editorKey`, `appKey`, `rawKeyHint` for extensions to format keybinding hints consistently ([#802](https://github.com/badlogic/pimono/pull/802) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1020 | Added | Exported `VERSION` from the package index and updated the customheader example. ([#798](https://github.com/badlogic/pimono/pull/798) by [@tallshort](https://github.com/tallshort)) | CHANGELOG.md |
| G-PI-CHANGELOG-1021 | Added | Added `showHardwareCursor` setting to control cursor visibility while still positioning it for IME support. ([#800](https://github.com/badlogic/pimono/pull/800) by [@ghoulr](https://github.com/ghoulr)) | CHANGELOG.md |
| G-PI-CHANGELOG-1022 | Added | Added Emacsstyle kill ring editing with yank and yankpop keybindings, plus legacy Alt+letter handling and Alt+D delete word forward support in the interactive editor. ([#810](https://github.com/badlogic/pimono/pull/810) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-1023 | Added | Added `ctx.compact()` and `ctx.getContextUsage()` to extension contexts for programmatic compaction and context usage checks. | CHANGELOG.md |
| G-PI-CHANGELOG-1024 | Added | Added documentation for delete word forward and kill ring keybindings in interactive mode. ([#810](https://github.com/badlogic/pimono/pull/810) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-1025 | Changed | Updated the default system prompt wording to clarify the pi harness and documentation scope. | CHANGELOG.md |
| G-PI-CHANGELOG-1026 | Changed | Simplified Codex system prompt handling to use the default system prompt directly for Codex instructions. | CHANGELOG.md |
| G-PI-CHANGELOG-1027 | Fixed | Fixed photon module failing to load in ESM context with "require is not defined" error ([#795](https://github.com/badlogic/pimono/pull/795) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1028 | Fixed | Fixed compaction UI not showing when extensions trigger compaction. | CHANGELOG.md |
| G-PI-CHANGELOG-1029 | Fixed | Fixed orphaned tool results after errored assistant messages causing Codex API errors. When an assistant message has `stopReason: "error"`, its tool calls are now excluded from pending tool tracking, preventing synthetic tool results from being generated for calls that will be dropped by providerspecific converters. ([#812](https://github.com/badlogic/pimono/issues/812)) | CHANGELOG.md |
| G-PI-CHANGELOG-1030 | Fixed | Fixed Bedrock Claude max_tokens handling to always exceed thinking budget tokens, preventing compaction failures. ([#797](https://github.com/badlogic/pimono/pull/797) by [@pjtf93](https://github.com/pjtf93)) | CHANGELOG.md |
| G-PI-CHANGELOG-1031 | Fixed | Fixed Claude Code tool name normalization to match the Claude Code tool list caseinsensitively and remove invalid mappings. | CHANGELOG.md |
| G-PI-CHANGELOG-1032 | Removed | Removed `piinternal://` path resolution from the read tool. | CHANGELOG.md |
| G-PI-CHANGELOG-1033 | Added | Added `quietStartup` setting to silence startup output (version header, loaded context info, model scope line). Changelog notifications are still shown. ([#777](https://github.com/badlogic/pimono/pull/777) by [@ribelo](https://github.com/ribelo)) | CHANGELOG.md |
| G-PI-CHANGELOG-1034 | Added | Added `editorPaddingX` setting for horizontal padding in input editor (03, default: 0) | CHANGELOG.md |
| G-PI-CHANGELOG-1035 | Added | Added `shellCommandPrefix` setting to prepend commands to every bash execution, enabling alias expansion in noninteractive shells (e.g., `"shellCommandPrefix": "shopt s expand_aliases"`) ([#790](https://github.com/badlogic/pimono/pull/790) by [@richardgill](https://github.com/richardgill)) | CHANGELOG.md |
| G-PI-CHANGELOG-1036 | Added | Added bashstyle argument slicing for prompt templates ([#770](https://github.com/badlogic/pimono/pull/770) by [@airtonix](https://github.com/airtonix)) | CHANGELOG.md |
| G-PI-CHANGELOG-1037 | Added | Extension commands can provide argument autocompletions via `getArgumentCompletions` in `pi.registerCommand()` ([#775](https://github.com/badlogic/pimono/pull/775) by [@ribelo](https://github.com/ribelo)) | CHANGELOG.md |
| G-PI-CHANGELOG-1038 | Added | Bash tool now displays the timeout value in the UI when a timeout is set ([#780](https://github.com/badlogic/pimono/pull/780) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1039 | Added | Export `getShellConfig` for extensions to detect user's shell environment ([#766](https://github.com/badlogic/pimono/pull/766) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1040 | Added | Added `thinkingText` and `selectedBg` to theme schema ([#763](https://github.com/badlogic/pimono/pull/763) by [@scutifer](https://github.com/scutifer)) | CHANGELOG.md |
| G-PI-CHANGELOG-1041 | Added | `navigateTree()` now supports `replaceInstructions` option to replace the default summarization prompt entirely, and `label` option to attach a label to the branch summary entry ([#787](https://github.com/badlogic/pimono/pull/787) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1042 | Fixed | Fixed crash during autocompaction when summarization fails (e.g., quota exceeded). Now displays error message instead of crashing ([#792](https://github.com/badlogic/pimono/issues/792)) | CHANGELOG.md |
| G-PI-CHANGELOG-1043 | Fixed | Fixed `session <UUID>` to search globally across projects if not found locally, with option to fork sessions from other projects ([#785](https://github.com/badlogic/pimono/pull/785) by [@ribelo](https://github.com/ribelo)) | CHANGELOG.md |
| G-PI-CHANGELOG-1044 | Fixed | Fixed standalone binary WASM loading on Linux ([#784](https://github.com/badlogic/pimono/issues/784)) | CHANGELOG.md |
| G-PI-CHANGELOG-1045 | Fixed | Fixed string numbers in tool arguments not being coerced to numbers during validation ([#786](https://github.com/badlogic/pimono/pull/786) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1046 | Fixed | Fixed `noextensions` flag not preventing extension discovery ([#776](https://github.com/badlogic/pimono/issues/776)) | CHANGELOG.md |
| G-PI-CHANGELOG-1047 | Fixed | Fixed extension messages rendering twice on startup when `pi.sendMessage({ display: true })` is called during `session_start` ([#765](https://github.com/badlogic/pimono/pull/765) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1048 | Fixed | Fixed `PI_CODING_AGENT_DIR` env var not expanding tilde (`~`) to home directory ([#778](https://github.com/badlogic/pimono/pull/778) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1049 | Fixed | Fixed session picker hint text overflow ([#764](https://github.com/badlogic/pimono/issues/764)) | CHANGELOG.md |
| G-PI-CHANGELOG-1050 | Fixed | Fixed Kitty keyboard protocol shifted symbol keys (e.g., `@`, `?`) not working in editor ([#779](https://github.com/badlogic/pimono/pull/779) by [@iamd3vil](https://github.com/iamd3vil)) | CHANGELOG.md |
| G-PI-CHANGELOG-1051 | Fixed | Fixed Bedrock tool call IDs causing API errors from invalid characters ([#781](https://github.com/badlogic/pimono/pull/781) by [@pjtf93](https://github.com/pjtf93)) | CHANGELOG.md |
| G-PI-CHANGELOG-1052 | Changed | Hardware cursor is now disabled by default for better terminal compatibility. Set `PI_HARDWARE_CURSOR=1` to enable (replaces `PI_NO_HARDWARE_CURSOR=1` which disabled it). | CHANGELOG.md |
| G-PI-CHANGELOG-1053 | Breaking Changes | Extensions using `Editor` directly must now pass `TUI` as the first constructor argument: `new Editor(tui, theme)`. The `tui` parameter is available in extension factory functions. ([#732](https://github.com/badlogic/pimono/issues/732)) | CHANGELOG.md |
| G-PI-CHANGELOG-1054 | Added | OpenAI Codex official support: Full compatibility with OpenAI's Codex CLI models (`gpt5.1`, `gpt5.2`, `gpt5.1codexmini`, `gpt5.2codex`). Features include static system prompt for OpenAI allowlisting, prompt caching via session ID, and reasoning signature retention across turns. Set `OPENAI_API_KEY` and use `provider openaicodex` or select a Codex model. ([#737](https://github.com/badlogic/pimono/pull/737)) | CHANGELOG.md |
| G-PI-CHANGELOG-1055 | Added | `piinternal://` URL scheme in read tool for accessing internal documentation. The model can read files from the codingagent package (README, docs, examples) to learn about extending pi. | CHANGELOG.md |
| G-PI-CHANGELOG-1056 | Added | New `input` event in extension system for intercepting, transforming, or handling user input before the agent processes it. Supports three result types: `continue` (pass through), `transform` (modify text/images), `handled` (respond without LLM). Handlers chain transforms and shortcircuit on handled. ([#761](https://github.com/badlogic/pimono/pull/761) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1057 | Added | Extension example: `inputtransform.ts` demonstrating input interception patterns (quick mode, instant commands, source routing) ([#761](https://github.com/badlogic/pimono/pull/761) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1058 | Added | Custom tool HTML export: extensions with `renderCall`/`renderResult` now render in `/share` and `/export` output with ANSItoHTML color conversion ([#702](https://github.com/badlogic/pimono/pull/702) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1059 | Added | Direct filter shortcuts in Tree mode: Ctrl+D (default), Ctrl+T (notools), Ctrl+U (useronly), Ctrl+L (labeledonly), Ctrl+A (all) ([#747](https://github.com/badlogic/pimono/pull/747) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-1060 | Changed | Skill commands (`/skill:name`) are now expanded in AgentSession instead of interactive mode. This enables skill commands in RPC and print modes, and allows the `input` event to intercept `/skill:name` before expansion. | CHANGELOG.md |
| G-PI-CHANGELOG-1061 | Fixed | Editor no longer corrupts terminal display when loading large prompts via `setEditorText`. Content now scrolls vertically with indicators showing lines above/below the viewport. ([#732](https://github.com/badlogic/pimono/issues/732)) | CHANGELOG.md |
| G-PI-CHANGELOG-1062 | Fixed | Piped stdin now works correctly: `echo foo | pi` is equivalent to `pi p foo`. When stdin is piped, print mode is automatically enabled since interactive mode requires a TTY ([#708](https://github.com/badlogic/pimono/issues/708)) | CHANGELOG.md |
| G-PI-CHANGELOG-1063 | Fixed | Session tree now preserves branch connectors and indentation when filters hide intermediate entries so descendants attach to the nearest visible ancestor and sibling branches align. Fixed in both TUI and HTML export ([#739](https://github.com/badlogic/pimono/pull/739) by [@wwinter](https://github.com/wwinter)) | CHANGELOG.md |
| G-PI-CHANGELOG-1064 | Fixed | Added `upstream connect`, `connection refused`, and `reset before headers` patterns to autoretry error detection ([#733](https://github.com/badlogic/pimono/issues/733)) | CHANGELOG.md |
| G-PI-CHANGELOG-1065 | Fixed | Multiline YAML frontmatter in skills and prompt templates now parses correctly. Centralized frontmatter parsing using the `yaml` library. ([#728](https://github.com/badlogic/pimono/pull/728) by [@richardgill](https://github.com/richardgill)) | CHANGELOG.md |
| G-PI-CHANGELOG-1066 | Fixed | `ctx.shutdown()` now waits for pending UI renders to complete before exiting, ensuring notifications and final output are visible ([#756](https://github.com/badlogic/pimono/issues/756)) | CHANGELOG.md |
| G-PI-CHANGELOG-1067 | Fixed | OpenAI Codex provider now retries on transient errors (429, 5xx, connection failures) with exponential backoff ([#733](https://github.com/badlogic/pimono/issues/733)) | CHANGELOG.md |
| G-PI-CHANGELOG-1068 | Fixed | Scoped models (`models` or `enabledModels`) now remember the last selected model across sessions instead of always starting with the first model in the scope ([#736](https://github.com/badlogic/pimono/pull/736) by [@ogulcancelik](https://github.com/ogulcancelik)) | CHANGELOG.md |
| G-PI-CHANGELOG-1069 | Fixed | Show `bun install` instead of `npm install` in update notification when running under Bun ([#714](https://github.com/badlogic/pimono/pull/714) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1070 | Fixed | `/skill` prompts now include the skill path ([#711](https://github.com/badlogic/pimono/pull/711) by [@jblwilliams](https://github.com/jblwilliams)) | CHANGELOG.md |
| G-PI-CHANGELOG-1071 | Fixed | Use configurable `expandTools` keybinding instead of hardcoded Ctrl+O ([#717](https://github.com/badlogic/pimono/pull/717) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1072 | Fixed | Compaction turn prefix summaries now merge correctly ([#738](https://github.com/badlogic/pimono/pull/738) by [@vsabavat](https://github.com/vsabavat)) | CHANGELOG.md |
| G-PI-CHANGELOG-1073 | Fixed | Avoid unsigned Gemini 3 tool calls ([#741](https://github.com/badlogic/pimono/pull/741) by [@roshanasingh4](https://github.com/roshanasingh4)) | CHANGELOG.md |
| G-PI-CHANGELOG-1074 | Fixed | Fixed signature support for nonAnthropic models in Amazon Bedrock provider ([#727](https://github.com/badlogic/pimono/pull/727) by [@unexge](https://github.com/unexge)) | CHANGELOG.md |
| G-PI-CHANGELOG-1075 | Fixed | Keyboard shortcuts (Ctrl+C, Ctrl+D, etc.) now work on nonLatin keyboard layouts (Russian, Ukrainian, Bulgarian, etc.) in terminals supporting Kitty keyboard protocol with alternate key reporting ([#718](https://github.com/badlogic/pimono/pull/718) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1076 | Added | Edit tool now uses fuzzy matching as fallback when exact match fails, tolerating trailing whitespace, smart quotes, Unicode dashes, and special spaces ([#713](https://github.com/badlogic/pimono/pull/713) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1077 | Added | Support `APPEND_SYSTEM.md` to append instructions to the system prompt ([#716](https://github.com/badlogic/pimono/pull/716) by [@tallshort](https://github.com/tallshort)) | CHANGELOG.md |
| G-PI-CHANGELOG-1078 | Added | Session picker search: Ctrl+R toggles sorting between fuzzy match (default) and most recent; supports quoted phrase matching and `re:` regex mode ([#731](https://github.com/badlogic/pimono/pull/731) by [@ogulcancelik](https://github.com/ogulcancelik)) | CHANGELOG.md |
| G-PI-CHANGELOG-1079 | Added | Export `getAgentDir` for extensions ([#749](https://github.com/badlogic/pimono/pull/749) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1080 | Added | Show loaded prompt templates on startup ([#743](https://github.com/badlogic/pimono/pull/743) by [@tallshort](https://github.com/tallshort)) | CHANGELOG.md |
| G-PI-CHANGELOG-1081 | Added | MiniMax China (`minimaxcn`) provider support ([#725](https://github.com/badlogic/pimono/pull/725) by [@tallshort](https://github.com/tallshort)) | CHANGELOG.md |
| G-PI-CHANGELOG-1082 | Added | `gpt5.2codex` models for GitHub Copilot and OpenCode Zen providers ([#734](https://github.com/badlogic/pimono/pull/734) by [@aadishv](https://github.com/aadishv)) | CHANGELOG.md |
| G-PI-CHANGELOG-1083 | Changed | Replaced `wasmvips` with `@silviaodwyer/photonnode` for image processing ([#710](https://github.com/badlogic/pimono/pull/710) by [@can1357](https://github.com/can1357)) | CHANGELOG.md |
| G-PI-CHANGELOG-1084 | Changed | Extension example: `planmode/` shortcut changed from Shift+P to Ctrl+Alt+P to avoid conflict with typing capital P ([#746](https://github.com/badlogic/pimono/pull/746) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-1085 | Changed | UI keybinding hints now respect configured keybindings across components ([#724](https://github.com/badlogic/pimono/pull/724) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1086 | Changed | CLI process title is now set to `pi` for easier process identification ([#742](https://github.com/badlogic/pimono/pull/742) by [@richardgill](https://github.com/richardgill)) | CHANGELOG.md |
| G-PI-CHANGELOG-1087 | Added | Exported `highlightCode` and `getLanguageFromPath` for extensions ([#703](https://github.com/badlogic/pimono/pull/703) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1088 | Added | `ctx.ui.custom()` now accepts `overlayOptions` for overlay positioning and sizing (anchor, margins, offsets, percentages, absolute positioning) ([#667](https://github.com/badlogic/pimono/pull/667) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1089 | Added | `ctx.ui.custom()` now accepts `onHandle` callback to receive the `OverlayHandle` for controlling overlay visibility ([#667](https://github.com/badlogic/pimono/pull/667) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1090 | Added | Extension example: `overlayqatests.ts` with 10 commands for testing overlay positioning, animation, and toggle scenarios ([#667](https://github.com/badlogic/pimono/pull/667) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1091 | Added | Extension example: `doomoverlay/`  DOOM game running as an overlay at 35 FPS (autodownloads WAD on first run) ([#667](https://github.com/badlogic/pimono/pull/667) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1092 | Fixed | Skip changelog display on fresh install (only show on upgrades) | CHANGELOG.md |
| G-PI-CHANGELOG-1093 | Changed | Light theme colors adjusted for WCAG AA compliance (4.5:1 contrast ratio against white backgrounds) | CHANGELOG.md |
| G-PI-CHANGELOG-1094 | Changed | Replaced `sharp` with `wasmvips` for image processing (resize, PNG conversion). Eliminates native build requirements that caused installation failures on some systems. ([#696](https://github.com/badlogic/pimono/issues/696)) | CHANGELOG.md |
| G-PI-CHANGELOG-1095 | Added | Extension example: `summarize.ts` for summarizing conversations using custom UI and an external model ([#684](https://github.com/badlogic/pimono/pull/684) by [@scutifer](https://github.com/scutifer)) | CHANGELOG.md |
| G-PI-CHANGELOG-1096 | Added | Extension example: `question.ts` enhanced with custom UI for asking user questions ([#693](https://github.com/badlogic/pimono/pull/693) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-1097 | Added | Extension example: `planmode/` enhanced with explicit step tracking and progress widget ([#694](https://github.com/badlogic/pimono/pull/694) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-1098 | Added | Extension example: `questionnaire.ts` for multiquestion input with tab bar navigation ([#695](https://github.com/badlogic/pimono/pull/695) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-1099 | Added | Experimental Vercel AI Gateway provider support: set `AI_GATEWAY_API_KEY` and use `provider vercelaigateway`. Token usage is currently reported incorrectly by Anthropic Messages compatible endpoint. ([#689](https://github.com/badlogic/pimono/pull/689) by [@timolins](https://github.com/timolins)) | CHANGELOG.md |
| G-PI-CHANGELOG-1100 | Fixed | Fix API key resolution after model switches by using provider argument ([#691](https://github.com/badlogic/pimono/pull/691) by [@joshp123](https://github.com/joshp123)) | CHANGELOG.md |
| G-PI-CHANGELOG-1101 | Fixed | Fixed z.ai thinking/reasoning: thinking toggle now correctly enables/disables thinking for z.ai models ([#688](https://github.com/badlogic/pimono/issues/688)) | CHANGELOG.md |
| G-PI-CHANGELOG-1102 | Fixed | Fixed extension loading in compiled Bun binary: extensions with local file imports now work correctly. Updated `@mariozechner/jiti` to v2.6.5 which bundles babel for Bun binary compatibility. ([#681](https://github.com/badlogic/pimono/issues/681)) | CHANGELOG.md |
| G-PI-CHANGELOG-1103 | Fixed | Fixed theme loading when installed via mise: use wrapper directory in release tarballs for compatibility with mise's `strip_components=1` extraction. ([#681](https://github.com/badlogic/pimono/issues/681)) | CHANGELOG.md |
| G-PI-CHANGELOG-1104 | Fixed | Extensions now load correctly in compiled Bun binary using `@mariozechner/jiti` fork with `virtualModules` support. Bundled packages (`@sinclair/typebox`, `@mariozechner/pitui`, `@mariozechner/piai`, `@mariozechner/picodingagent`) are accessible to extensions without filesystem node_modules. | CHANGELOG.md |
| G-PI-CHANGELOG-1105 | Changed | `/share` now outputs `buildwithpi.ai` session preview URLs instead of `pi.dev` | CHANGELOG.md |
| G-PI-CHANGELOG-1106 | Added | MiniMax provider support: set `MINIMAX_API_KEY` and use `minimax/MiniMaxM2.1` ([#656](https://github.com/badlogic/pimono/pull/656) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1107 | Added | `/scopedmodels`: Alt+Up/Down to reorder enabled models. Order is preserved when saving with Ctrl+S and determines Ctrl+P cycling order. ([#676](https://github.com/badlogic/pimono/pull/676) by [@thomasmhr](https://github.com/thomasmhr)) | CHANGELOG.md |
| G-PI-CHANGELOG-1108 | Added | Amazon Bedrock provider support (experimental, tested with Anthropic Claude models only) ([#494](https://github.com/badlogic/pimono/pull/494) by [@unexge](https://github.com/unexge)) | CHANGELOG.md |
| G-PI-CHANGELOG-1109 | Added | Extension example: `sandbox/` for OSlevel bash sandboxing using `@anthropicai/sandboxruntime` with perproject config ([#673](https://github.com/badlogic/pimono/pull/673) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-1110 | Added | Print mode JSON output now emits the session header as the first line. | CHANGELOG.md |
| G-PI-CHANGELOG-1111 | Breaking Changes | `pi.getAllTools()` now returns `ToolInfo[]` (with `name` and `description`) instead of `string[]`. Extensions that only need names can use `.map(t => t.name)`. ([#648](https://github.com/badlogic/pimono/pull/648) by [@carsonfarmer](https://github.com/carsonfarmer)) | CHANGELOG.md |
| G-PI-CHANGELOG-1112 | Added | Session naming: `/name <name>` command sets a display name shown in the session selector instead of the first message. Useful for distinguishing forked sessions. Extensions can use `pi.setSessionName()` and `pi.getSessionName()`. ([#650](https://github.com/badlogic/pimono/pull/650) by [@scutifer](https://github.com/scutifer)) | CHANGELOG.md |
| G-PI-CHANGELOG-1113 | Added | Extension example: `notify.ts` for desktop notifications via OSC 777 escape sequence ([#658](https://github.com/badlogic/pimono/pull/658) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-1114 | Added | Inline hint for queued messages showing the `Alt+Up` restore shortcut ([#657](https://github.com/badlogic/pimono/pull/657) by [@tmustier](https://github.com/tmustier)) | CHANGELOG.md |
| G-PI-CHANGELOG-1115 | Added | Pageup/down navigation in `/resume` session selector to jump by 5 items ([#662](https://github.com/badlogic/pimono/pull/662) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1116 | Added | Fuzzy search in `/settings` menu: type to filter settings by label ([#643](https://github.com/badlogic/pimono/pull/643) by [@ninlds](https://github.com/ninlds)) | CHANGELOG.md |
| G-PI-CHANGELOG-1117 | Fixed | Session selector now stays open when current folder has no sessions, allowing Tab to switch to "all" scope ([#661](https://github.com/badlogic/pimono/pull/661) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1118 | Fixed | Extensions using theme utilities like `getSettingsListTheme()` now work in dev mode with tsx | CHANGELOG.md |
| G-PI-CHANGELOG-1119 | Breaking Changes | Extension editor (`ctx.ui.editor()`) now uses Enter to submit and Shift+Enter for newlines, matching the main editor. Previously used Ctrl+Enter to submit. Extensions with hardcoded "ctrl+enter" hints need updating. ([#642](https://github.com/badlogic/pimono/pull/642) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1120 | Breaking Changes | Renamed `/branch` command to `/fork` ([#641](https://github.com/badlogic/pimono/issues/641)) | CHANGELOG.md |
| G-PI-CHANGELOG-1121 | Breaking Changes | RPC: `branch` → `fork`, `get_branch_messages` → `get_fork_messages` | CHANGELOG.md |
| G-PI-CHANGELOG-1122 | Breaking Changes | SDK: `branch()` → `fork()`, `getBranchMessages()` → `getForkMessages()` | CHANGELOG.md |
| G-PI-CHANGELOG-1123 | Breaking Changes | AgentSession: `branch()` → `fork()`, `getUserMessagesForBranching()` → `getUserMessagesForForking()` | CHANGELOG.md |
| G-PI-CHANGELOG-1124 | Breaking Changes | Extension events: `session_before_branch` → `session_before_fork`, `session_branch` → `session_fork` | CHANGELOG.md |
| G-PI-CHANGELOG-1125 | Breaking Changes | Settings: `doubleEscapeAction: "branch" | "tree"` → `"fork" | "tree"` | CHANGELOG.md |
| G-PI-CHANGELOG-1126 | Breaking Changes | `SessionManager.list()` and `SessionManager.listAll()` are now async, returning `Promise<SessionInfo[]>`. Callers must await them. ([#620](https://github.com/badlogic/pimono/pull/620) by [@tmustier](https://github.com/tmustier)) | CHANGELOG.md |
| G-PI-CHANGELOG-1127 | Added | `/resume` selector now toggles between currentfolder and all sessions with Tab, showing the session cwd in the All view and loading progress. ([#620](https://github.com/badlogic/pimono/pull/620) by [@tmustier](https://github.com/tmustier)) | CHANGELOG.md |
| G-PI-CHANGELOG-1128 | Added | `SessionManager.list()` and `SessionManager.listAll()` accept optional `onProgress` callback for progress updates | CHANGELOG.md |
| G-PI-CHANGELOG-1129 | Added | `SessionInfo.cwd` field containing the session's working directory (empty string for old sessions) | CHANGELOG.md |
| G-PI-CHANGELOG-1130 | Added | `SessionListProgress` type export for progress callbacks | CHANGELOG.md |
| G-PI-CHANGELOG-1131 | Added | `/scopedmodels` command to enable/disable models for Ctrl+P cycling. Changes are sessiononly by default; press Ctrl+S to persist to settings.json. ([#626](https://github.com/badlogic/pimono/pull/626) by [@CarlosGtrz](https://github.com/CarlosGtrz)) | CHANGELOG.md |
| G-PI-CHANGELOG-1132 | Added | `model_select` extension hook fires when model changes via `/model`, model cycling, or session restore with `source` field and `previousModel` ([#628](https://github.com/badlogic/pimono/pull/628) by [@marckrenn](https://github.com/marckrenn)) | CHANGELOG.md |
| G-PI-CHANGELOG-1133 | Added | `ctx.ui.setWorkingMessage()` extension API to customize the "Working..." message during streaming ([#625](https://github.com/badlogic/pimono/pull/625) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1134 | Added | Skill slash commands: loaded skills are registered as `/skill:name` commands for quick access. Toggle via `/settings` or `skills.enableSkillCommands` in settings.json. ([#630](https://github.com/badlogic/pimono/pull/630) by [@Dwsy](https://github.com/Dwsy)) | CHANGELOG.md |
| G-PI-CHANGELOG-1135 | Added | Slash command autocomplete now uses fuzzy matching (type `/skbra` to match `/skill:bravesearch`) | CHANGELOG.md |
| G-PI-CHANGELOG-1136 | Added | `/tree` branch summarization now offers three options: "No summary", "Summarize", and "Summarize with custom prompt". Custom prompts are appended as additional focus to the default summarization instructions. ([#642](https://github.com/badlogic/pimono/pull/642) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1137 | Fixed | Missing spacer between assistant message and text editor ([#655](https://github.com/badlogic/pimono/issues/655)) | CHANGELOG.md |
| G-PI-CHANGELOG-1138 | Fixed | Session picker respects custom keybindings when using `resume` ([#633](https://github.com/badlogic/pimono/pull/633) by [@aos](https://github.com/aos)) | CHANGELOG.md |
| G-PI-CHANGELOG-1139 | Fixed | Custom footer extensions now see model changes: `ctx.model` is now a getter that returns the current model instead of a snapshot from when the context was created ([#634](https://github.com/badlogic/pimono/pull/634) by [@ogulcancelik](https://github.com/ogulcancelik)) | CHANGELOG.md |
| G-PI-CHANGELOG-1140 | Fixed | Footer git branch not updating after external branch switches. Git uses atomic writes (temp file + rename), which changes the inode and breaks `fs.watch` on the file. Now watches the directory instead. | CHANGELOG.md |
| G-PI-CHANGELOG-1141 | Fixed | Extension loading errors are now displayed to the user instead of being silently ignored ([#639](https://github.com/badlogic/pimono/pull/639) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1142 | Fixed | Reduced flicker by only rerendering changed lines ([#617](https://github.com/badlogic/pimono/pull/617) by [@ogulcancelik](https://github.com/ogulcancelik)). No worries tho, there's still a little flicker in the VS Code Terminal. Praise the flicker. | CHANGELOG.md |
| G-PI-CHANGELOG-1143 | Fixed | Cursor position tracking when content shrinks with unchanged remaining lines | CHANGELOG.md |
| G-PI-CHANGELOG-1144 | Fixed | TUI renders with wrong dimensions after suspend/resume if terminal was resized while suspended ([#599](https://github.com/badlogic/pimono/issues/599)) | CHANGELOG.md |
| G-PI-CHANGELOG-1145 | Fixed | Pasted content containing Kitty key release patterns (e.g., `:3F` in MAC addresses) was incorrectly filtered out ([#623](https://github.com/badlogic/pimono/pull/623) by [@ogulcancelik](https://github.com/ogulcancelik)) | CHANGELOG.md |
| G-PI-CHANGELOG-1146 | Fixed | Bash output expanded hint now says "(ctrl+o to collapse)" ([#610](https://github.com/badlogic/pimono/pull/610) by [@tallshort](https://github.com/tallshort)) | CHANGELOG.md |
| G-PI-CHANGELOG-1147 | Fixed | Fixed UTF8 text corruption in remote bash execution (SSH, containers) by using streaming TextDecoder ([#608](https://github.com/badlogic/pimono/issues/608)) | CHANGELOG.md |
| G-PI-CHANGELOG-1148 | Changed | OpenAI Codex: updated to use bundled system prompt from upstream | CHANGELOG.md |
| G-PI-CHANGELOG-1149 | Added | `/model <search>` now prefilters the model selector or autoselects on exact match. Use `provider/model` syntax to disambiguate (e.g., `/model openai/gpt4`). ([#587](https://github.com/badlogic/pimono/pull/587) by [@zedrdave](https://github.com/zedrdave)) | CHANGELOG.md |
| G-PI-CHANGELOG-1150 | Added | `FooterDataProvider` for custom footers: `ctx.ui.setFooter()` now receives a third `footerData` parameter providing `getGitBranch()`, `getExtensionStatuses()`, and `onBranchChange()` for reactive updates ([#600](https://github.com/badlogic/pimono/pull/600) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1151 | Added | `Alt+Up` hotkey to restore queued steering/followup messages back into the editor without aborting the current run ([#604](https://github.com/badlogic/pimono/pull/604) by [@tmustier](https://github.com/tmustier)) | CHANGELOG.md |
| G-PI-CHANGELOG-1152 | Fixed | Fixed LM Studio compatibility for OpenAI Responses tool strict mapping in the ai provider ([#598](https://github.com/badlogic/pimono/pull/598) by [@gnattu](https://github.com/gnattu)) | CHANGELOG.md |
| G-PI-CHANGELOG-1153 | Fixed | Symlinked directories in `prompts/` folders are now followed when loading prompt templates ([#601](https://github.com/badlogic/pimono/pull/601) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1154 | Added | Added OpenCode Zen provider support. Set `OPENCODE_API_KEY` env var and use `opencode/<modelid>` (e.g., `opencode/claudeopus45`). | CHANGELOG.md |
| G-PI-CHANGELOG-1155 | Added | Anthropic OAuth support is back! Use `/login` to authenticate with your Claude Pro/Max subscription. | CHANGELOG.md |
| G-PI-CHANGELOG-1156 | Removed | Anthropic OAuth support (`/login`). Use API keys instead. | CHANGELOG.md |
| G-PI-CHANGELOG-1157 | Added | Documentation on component invalidation and theme changes in `docs/tui.md` | CHANGELOG.md |
| G-PI-CHANGELOG-1158 | Fixed | Components now properly rebuild their content on theme change (tool executions, assistant messages, bash executions, custom messages, branch/compaction summaries) | CHANGELOG.md |
| G-PI-CHANGELOG-1159 | Fixed | `setTheme()` now triggers a full rerender so previously rendered components update with the new theme colors | CHANGELOG.md |
| G-PI-CHANGELOG-1160 | Fixed | `macsystemtheme.ts` example now polls every 2 seconds and uses `osascript` for realtime macOS appearance detection | CHANGELOG.md |
| G-PI-CHANGELOG-1161 | Breaking Changes | `before_agent_start` event now receives `systemPrompt` in the event object and returns `systemPrompt` (full replacement) instead of `systemPromptAppend`. Extensions that were appending must now use `event.systemPrompt + extra` pattern. ([#575](https://github.com/badlogic/pimono/issues/575)) | CHANGELOG.md |
| G-PI-CHANGELOG-1162 | Breaking Changes | `discoverSkills()` now returns `{ skills: Skill[], warnings: SkillWarning[] }` instead of `Skill[]`. This allows callers to handle skill loading warnings. ([#577](https://github.com/badlogic/pimono/pull/577) by [@cv](https://github.com/cv)) | CHANGELOG.md |
| G-PI-CHANGELOG-1163 | Added | `ctx.ui.getAllThemes()`, `ctx.ui.getTheme(name)`, and `ctx.ui.setTheme(name | Theme)` methods for extensions to list, load, and switch themes at runtime ([#576](https://github.com/badlogic/pimono/pull/576)) | CHANGELOG.md |
| G-PI-CHANGELOG-1164 | Added | `notools` flag to disable all builtin tools, allowing extensiononly tool setups ([#557](https://github.com/badlogic/pimono/pull/557) by [@cv](https://github.com/cv)) | CHANGELOG.md |
| G-PI-CHANGELOG-1165 | Added | Pluggable operations for builtin tools enabling remote execution via SSH or other transports ([#564](https://github.com/badlogic/pimono/issues/564)). Interfaces: `ReadOperations`, `WriteOperations`, `EditOperations`, `BashOperations`, `LsOperations`, `GrepOperations`, `FindOperations` | CHANGELOG.md |
| G-PI-CHANGELOG-1166 | Added | `user_bash` event for intercepting user `!`/`!!` commands, allowing extensions to redirect to remote systems ([#528](https://github.com/badlogic/pimono/issues/528)) | CHANGELOG.md |
| G-PI-CHANGELOG-1167 | Added | `setActiveTools()` in ExtensionAPI for dynamic tool management | CHANGELOG.md |
| G-PI-CHANGELOG-1168 | Added | Builtin renderers used automatically for tool overrides without custom `renderCall`/`renderResult` | CHANGELOG.md |
| G-PI-CHANGELOG-1169 | Added | `ssh.ts` example: remote tool execution via `ssh user@host:/path` | CHANGELOG.md |
| G-PI-CHANGELOG-1170 | Added | `interactiveshell.ts` example: run interactive commands (vim, git rebase, htop) with full terminal access via `!i` prefix or autodetection | CHANGELOG.md |
| G-PI-CHANGELOG-1171 | Added | Wayland clipboard support for `/copy` command using wlcopy with xclip/xsel fallback ([#570](https://github.com/badlogic/pimono/pull/570) by [@OgulcanCelik](https://github.com/OgulcanCelik)) | CHANGELOG.md |
| G-PI-CHANGELOG-1172 | Added | Experimental: `ctx.ui.custom()` now accepts `{ overlay: true }` option for floating modal components that composite over existing content without clearing the screen ([#558](https://github.com/badlogic/pimono/pull/558) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1173 | Added | `AgentSession.skills` and `AgentSession.skillWarnings` properties to access loaded skills without rediscovery ([#577](https://github.com/badlogic/pimono/pull/577) by [@cv](https://github.com/cv)) | CHANGELOG.md |
| G-PI-CHANGELOG-1174 | Fixed | String `systemPrompt` in `createAgentSession()` now works as a full replacement instead of having context files and skills appended, matching documented behavior ([#543](https://github.com/badlogic/pimono/issues/543)) | CHANGELOG.md |
| G-PI-CHANGELOG-1175 | Fixed | Update notification for bun binary installs now shows release download URL instead of npm command ([#567](https://github.com/badlogic/pimono/pull/567) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-1176 | Fixed | ESC key now works during "Working..." state after autoretry ([#568](https://github.com/badlogic/pimono/pull/568) by [@tmustier](https://github.com/tmustier)) | CHANGELOG.md |
| G-PI-CHANGELOG-1177 | Fixed | Abort messages now show correct retry attempt count (e.g., "Aborted after 2 retry attempts") ([#568](https://github.com/badlogic/pimono/pull/568) by [@tmustier](https://github.com/tmustier)) | CHANGELOG.md |
| G-PI-CHANGELOG-1178 | Fixed | Fixed Antigravity provider returning 429 errors despite available quota ([#571](https://github.com/badlogic/pimono/pull/571) by [@benvargas](https://github.com/benvargas)) | CHANGELOG.md |
| G-PI-CHANGELOG-1179 | Fixed | Fixed malformed thinking text in Gemini/Antigravity responses where thinking content appeared as regular text or vice versa. Crossmodel conversations now properly convert thinking blocks to plain text. ([#561](https://github.com/badlogic/pimono/issues/561)) | CHANGELOG.md |
| G-PI-CHANGELOG-1180 | Fixed | `noskills` flag now correctly prevents skills from loading in interactive mode ([#577](https://github.com/badlogic/pimono/pull/577) by [@cv](https://github.com/cv)) | CHANGELOG.md |
| G-PI-CHANGELOG-1181 | Breaking Changes | `ctx.ui.custom()` factory signature changed from `(tui, theme, done)` to `(tui, theme, keybindings, done)` for keybinding access in custom components | CHANGELOG.md |
| G-PI-CHANGELOG-1182 | Breaking Changes | `LoadedExtension` type renamed to `Extension` | CHANGELOG.md |
| G-PI-CHANGELOG-1183 | Breaking Changes | `LoadExtensionsResult.setUIContext()` removed, replaced with `runtime: ExtensionRuntime` | CHANGELOG.md |
| G-PI-CHANGELOG-1184 | Breaking Changes | `ExtensionRunner` constructor now requires `runtime: ExtensionRuntime` as second parameter | CHANGELOG.md |
| G-PI-CHANGELOG-1185 | Breaking Changes | `ExtensionRunner.initialize()` signature changed from options object to positional params `(actions, contextActions, commandContextActions?, uiContext?)` | CHANGELOG.md |
| G-PI-CHANGELOG-1186 | Breaking Changes | `ExtensionRunner.getHasUI()` renamed to `hasUI()` | CHANGELOG.md |
| G-PI-CHANGELOG-1187 | Breaking Changes | OpenAI Codex model aliases removed (`gpt5`, `gpt5mini`, `gpt5nano`, `codexminilatest`). Use canonical IDs: `gpt5.1`, `gpt5.1codexmini`, `gpt5.2`, `gpt5.2codex`. ([#536](https://github.com/badlogic/pimono/pull/536) by [@ghoulr](https://github.com/ghoulr)) | CHANGELOG.md |
| G-PI-CHANGELOG-1188 | Added | `noextensions` flag to disable extension discovery while still allowing explicit `e` paths ([#524](https://github.com/badlogic/pimono/pull/524) by [@cv](https://github.com/cv)) | CHANGELOG.md |
| G-PI-CHANGELOG-1189 | Added | SDK: `InteractiveMode`, `runPrintMode()`, `runRpcMode()` exported for building custom run modes. See `docs/sdk.md`. | CHANGELOG.md |
| G-PI-CHANGELOG-1190 | Added | `PI_SKIP_VERSION_CHECK` environment variable to disable new version notifications at startup ([#549](https://github.com/badlogic/pimono/pull/549) by [@aos](https://github.com/aos)) | CHANGELOG.md |
| G-PI-CHANGELOG-1191 | Added | `thinkingBudgets` setting to customize token budgets per thinking level for tokenbased providers ([#529](https://github.com/badlogic/pimono/pull/529) by [@melihmucuk](https://github.com/melihmucuk)) | CHANGELOG.md |
| G-PI-CHANGELOG-1192 | Added | Extension UI dialogs (`ctx.ui.select()`, `ctx.ui.confirm()`, `ctx.ui.input()`) now support a `timeout` option with live countdown display ([#522](https://github.com/badlogic/pimono/pull/522) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1193 | Added | Extensions can now provide custom editor components via `ctx.ui.setEditorComponent()`. See `examples/extensions/modaleditor.ts` and `docs/tui.md` Pattern 7. | CHANGELOG.md |
| G-PI-CHANGELOG-1194 | Added | Extension factories can now be async, enabling dynamic imports and lazyloaded dependencies ([#513](https://github.com/badlogic/pimono/pull/513) by [@austinm911](https://github.com/austinm911)) | CHANGELOG.md |
| G-PI-CHANGELOG-1195 | Added | `ctx.shutdown()` is now available in extension contexts for requesting a graceful shutdown. In interactive mode, shutdown is deferred until the agent becomes idle (after processing all queued steering and followup messages). In RPC mode, shutdown is deferred until after completing the current command response. In print mode, shutdown is a noop as the process exits automatically when prompts complete. ([#542](https://github.com/badlogic/pimono/pull/542) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-1196 | Fixed | Default thinking level from settings now applies correctly when `enabledModels` is configured ([#540](https://github.com/badlogic/pimono/pull/540) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-1197 | Fixed | External edits to `settings.json` while pi is running are now preserved when pi saves settings ([#527](https://github.com/badlogic/pimono/pull/527) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-1198 | Fixed | Overflowbased compaction now skips if error came from a different model or was already handled by a previous compaction ([#535](https://github.com/badlogic/pimono/pull/535) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1199 | Fixed | OpenAI Codex context window reduced from 400k to 272k tokens to match Codex CLI defaults and prevent 400 errors ([#536](https://github.com/badlogic/pimono/pull/536) by [@ghoulr](https://github.com/ghoulr)) | CHANGELOG.md |
| G-PI-CHANGELOG-1200 | Fixed | Context overflow detection now recognizes `context_length_exceeded` errors. | CHANGELOG.md |
| G-PI-CHANGELOG-1201 | Fixed | Key presses no longer dropped when input is batched over SSH ([#538](https://github.com/badlogic/pimono/issues/538)) | CHANGELOG.md |
| G-PI-CHANGELOG-1202 | Fixed | Clipboard image support now works on Alpine Linux and other muslbased distros ([#533](https://github.com/badlogic/pimono/issues/533)) | CHANGELOG.md |
| G-PI-CHANGELOG-1203 | Added | Extension UI dialogs (`ctx.ui.select()`, `ctx.ui.confirm()`, `ctx.ui.input()`) now accept an optional `AbortSignal` to programmatically dismiss dialogs. Useful for implementing timeouts. See `examples/extensions/timedconfirm.ts`. ([#474](https://github.com/badlogic/pimono/issues/474)) | CHANGELOG.md |
| G-PI-CHANGELOG-1204 | Added | HTML export now shows bridge prompts in model change messages for Codex sessions ([#510](https://github.com/badlogic/pimono/pull/510) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1205 | Added | ExtensionAPI: `setModel()`, `getThinkingLevel()`, `setThinkingLevel()` methods for extensions to change model and thinking level at runtime ([#509](https://github.com/badlogic/pimono/issues/509)) | CHANGELOG.md |
| G-PI-CHANGELOG-1206 | Added | Exported truncation utilities for custom tools: `truncateHead`, `truncateTail`, `truncateLine`, `formatSize`, `DEFAULT_MAX_BYTES`, `DEFAULT_MAX_LINES`, `TruncationOptions`, `TruncationResult` | CHANGELOG.md |
| G-PI-CHANGELOG-1207 | Added | New example `truncatedtool.ts` demonstrating proper output truncation with custom rendering for extensions | CHANGELOG.md |
| G-PI-CHANGELOG-1208 | Added | New example `preset.ts` demonstrating preset configurations with model/thinking/tools switching ([#347](https://github.com/badlogic/pimono/issues/347)) | CHANGELOG.md |
| G-PI-CHANGELOG-1209 | Added | Documentation for output truncation best practices in `docs/extensions.md` | CHANGELOG.md |
| G-PI-CHANGELOG-1210 | Added | Exported all UI components for extensions: `ArminComponent`, `AssistantMessageComponent`, `BashExecutionComponent`, `BorderedLoader`, `BranchSummaryMessageComponent`, `CompactionSummaryMessageComponent`, `CustomEditor`, `CustomMessageComponent`, `DynamicBorder`, `ExtensionEditorComponent`, `ExtensionInputComponent`, `ExtensionSelectorComponent`, `FooterComponent`, `LoginDialogComponent`, `ModelSelectorComponent`, `OAuthSelectorComponent`, `SessionSelectorComponent`, `SettingsSelectorComponent`, `ShowImagesSelectorComponent`, `ThemeSelectorComponent`, `ThinkingSelectorComponent`, `ToolExecutionComponent`, `TreeSelectorComponent`, `UserMessageComponent`, `UserMessageSelectorComponent`, plus utilities `renderDiff`, `truncateToVisualLines` | CHANGELOG.md |
| G-PI-CHANGELOG-1211 | Added | `docs/tui.md`: Common Patterns section with copypaste code for SelectList, BorderedLoader, SettingsList, setStatus, setWidget, setFooter | CHANGELOG.md |
| G-PI-CHANGELOG-1212 | Added | `docs/tui.md`: Key Rules section documenting critical patterns for extension UI development | CHANGELOG.md |
| G-PI-CHANGELOG-1213 | Added | `docs/extensions.md`: Exhaustive example links for all ExtensionAPI methods and events | CHANGELOG.md |
| G-PI-CHANGELOG-1214 | Added | System prompt now references `docs/tui.md` for TUI component development | CHANGELOG.md |
| G-PI-CHANGELOG-1215 | Added | Session picker (`pi r`) and `session` flag now support searching/resuming by session ID (UUID prefix) ([#495](https://github.com/badlogic/pimono/issues/495) by [@arunsathiya](https://github.com/arunsathiya)) | CHANGELOG.md |
| G-PI-CHANGELOG-1216 | Added | Extensions can now replace the startup header with `ctx.ui.setHeader()`, see `examples/extensions/customheader.ts` ([#500](https://github.com/badlogic/pimono/pull/500) by [@tudoroancea](https://github.com/tudoroancea)) | CHANGELOG.md |
| G-PI-CHANGELOG-1217 | Changed | Startup help text: fixed misleading "ctrl+k to delete line" to "ctrl+k to delete to end" | CHANGELOG.md |
| G-PI-CHANGELOG-1218 | Changed | Startup help text and `/hotkeys`: added `!!` shortcut for running bash without adding output to context | CHANGELOG.md |
| G-PI-CHANGELOG-1219 | Fixed | Queued steering/followup messages no longer wipe unsent editor input ([#503](https://github.com/badlogic/pimono/pull/503) by [@tmustier](https://github.com/tmustier)) | CHANGELOG.md |
| G-PI-CHANGELOG-1220 | Fixed | OAuth token refresh failure no longer crashes app at startup, allowing user to `/login` to reauthenticate ([#498](https://github.com/badlogic/pimono/issues/498)) | CHANGELOG.md |
| G-PI-CHANGELOG-1221 | Added | Extensions can now replace the footer with `ctx.ui.setFooter()`, see `examples/extensions/customfooter.ts` ([#481](https://github.com/badlogic/pimono/issues/481)) | CHANGELOG.md |
| G-PI-CHANGELOG-1222 | Added | Session ID is now forwarded to LLM providers for sessionbased caching (used by OpenAI Codex for prompt caching). | CHANGELOG.md |
| G-PI-CHANGELOG-1223 | Added | Added `blockImages` setting to prevent images from being sent to LLM providers ([#492](https://github.com/badlogic/pimono/pull/492) by [@jsinge97](https://github.com/jsinge97)) | CHANGELOG.md |
| G-PI-CHANGELOG-1224 | Added | Extensions can now send user messages via `pi.sendUserMessage()` ([#483](https://github.com/badlogic/pimono/issues/483)) | CHANGELOG.md |
| G-PI-CHANGELOG-1225 | Fixed | Add `minimatch` as a direct dependency for explicit imports. | CHANGELOG.md |
| G-PI-CHANGELOG-1226 | Fixed | Status bar now shows correct git branch when running in a git worktree ([#490](https://github.com/badlogic/pimono/pull/490) by [@kcosr](https://github.com/kcosr)) | CHANGELOG.md |
| G-PI-CHANGELOG-1227 | Fixed | Interactive mode: Ctrl+V clipboard image paste now works on Wayland sessions by using `wlpaste` with `xclip` fallback ([#488](https://github.com/badlogic/pimono/pull/488) by [@ghoulr](https://github.com/ghoulr)) | CHANGELOG.md |
| G-PI-CHANGELOG-1228 | Fixed | Extension directories in `settings.json` now respect `package.json` manifests, matching global extension behavior ([#480](https://github.com/badlogic/pimono/pull/480) by [@prateekmedia](https://github.com/prateekmedia)) | CHANGELOG.md |
| G-PI-CHANGELOG-1229 | Fixed | Share viewer: deep links now scroll to the target message when opened via `/share` | CHANGELOG.md |
| G-PI-CHANGELOG-1230 | Fixed | Bash tool now handles spawn errors gracefully instead of crashing the agent (missing cwd, invalid shell path) ([#479](https://github.com/badlogic/pimono/pull/479) by [@robinwander](https://github.com/robinwander)) | CHANGELOG.md |
| G-PI-CHANGELOG-1231 | Fixed | Share viewer: copylink buttons now generate correct URLs when session is viewed via `/share` (iframe context) | CHANGELOG.md |
| G-PI-CHANGELOG-1232 | Added | Share viewer: copylink button on messages to share URLs that navigate directly to a specific message ([#477](https://github.com/badlogic/pimono/pull/477) by [@lockmeister](https://github.com/lockmeister)) | CHANGELOG.md |
| G-PI-CHANGELOG-1233 | Added | Extension example: add `clauderules` to load `.claude/rules/` entries into the system prompt ([#461](https://github.com/badlogic/pimono/pull/461) by [@vaayne](https://github.com/vaayne)) | CHANGELOG.md |
| G-PI-CHANGELOG-1234 | Added | Headless OAuth login: all providers now show paste input for manual URL/code entry, works over SSH without DISPLAY ([#428](https://github.com/badlogic/pimono/pull/428) by [@benvargas](https://github.com/benvargas), [#468](https://github.com/badlogic/pimono/pull/468) by [@crcatala](https://github.com/crcatala)) | CHANGELOG.md |
| G-PI-CHANGELOG-1235 | Changed | OAuth login UI now uses dedicated dialog component with consistent borders | CHANGELOG.md |
| G-PI-CHANGELOG-1236 | Changed | Assume truecolor support for all terminals except `dumb`, empty, or `linux` (fixes colors over SSH) | CHANGELOG.md |
| G-PI-CHANGELOG-1237 | Changed | OpenAI Codex cleanup: removed perthinkinglevel model variants, thinking level is now set separately and the provider clamps to what each model supports internally (initial implementation in [#472](https://github.com/badlogic/pimono/pull/472) by [@benvargas](https://github.com/benvargas)) | CHANGELOG.md |
| G-PI-CHANGELOG-1238 | Fixed | Messages submitted during compaction are queued and delivered after compaction completes, preserving steering and followup behavior. Extension commands execute immediately during compaction. ([#476](https://github.com/badlogic/pimono/pull/476) by [@tmustier](https://github.com/tmustier)) | CHANGELOG.md |
| G-PI-CHANGELOG-1239 | Fixed | Managed binaries (`fd`, `rg`) now stored in `~/.pi/agent/bin/` instead of `tools/`, eliminating false deprecation warnings ([#470](https://github.com/badlogic/pimono/pull/470) by [@mcinteerj](https://github.com/mcinteerj)) | CHANGELOG.md |
| G-PI-CHANGELOG-1240 | Fixed | Extensions defined in `settings.json` were not loaded ([#463](https://github.com/badlogic/pimono/pull/463) by [@melihmucuk](https://github.com/melihmucuk)) | CHANGELOG.md |
| G-PI-CHANGELOG-1241 | Fixed | OAuth refresh no longer logs users out when multiple pi instances are running ([#466](https://github.com/badlogic/pimono/pull/466) by [@Cursivez](https://github.com/Cursivez)) | CHANGELOG.md |
| G-PI-CHANGELOG-1242 | Fixed | Migration warnings now ignore `fd.exe` and `rg.exe` in `tools/` on Windows ([#458](https://github.com/badlogic/pimono/pull/458) by [@carlosgtrz](https://github.com/carlosgtrz)) | CHANGELOG.md |
| G-PI-CHANGELOG-1243 | Fixed | CI: add `examples/extensions/withdeps` to workspaces to fix typecheck ([#467](https://github.com/badlogic/pimono/pull/467) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1244 | Fixed | SDK: passing `extensions: []` now disables extension discovery as documented ([#465](https://github.com/badlogic/pimono/pull/465) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1245 | Added | Experimental: OpenAI Codex OAuth provider support: access Codex models via ChatGPT Plus/Pro subscription using `/login openaicodex` ([#451](https://github.com/badlogic/pimono/pull/451) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-1246 | [0.35.0] - 2026-01-05 | Before migrating, read: | CHANGELOG.md |
| G-PI-CHANGELOG-1247 | [0.35.0] - 2026-01-05 | [docs/extensions.md](docs/extensions.md)  Full API reference | CHANGELOG.md |
| G-PI-CHANGELOG-1248 | [0.35.0] - 2026-01-05 | [README.md](README.md)  Extensions section with examples | CHANGELOG.md |
| G-PI-CHANGELOG-1249 | [0.35.0] - 2026-01-05 | [examples/extensions/](examples/extensions/)  Working examples | CHANGELOG.md |
| G-PI-CHANGELOG-1250 | Extensions Migration | Automatic migration: | CHANGELOG.md |
| G-PI-CHANGELOG-1251 | Extensions Migration | `commands/` directories are automatically renamed to `prompts/` on startup (both `~/.pi/agent/commands/` and `.pi/commands/`) | CHANGELOG.md |
| G-PI-CHANGELOG-1252 | Extensions Migration | Manual migration required: | CHANGELOG.md |
| G-PI-CHANGELOG-1253 | Extensions Migration | Directory changes: | CHANGELOG.md |
| G-PI-CHANGELOG-1254 | Before | Extension discovery rules (in `extensions/` directories): | CHANGELOG.md |
| G-PI-CHANGELOG-1255 | Before | Type renames: | CHANGELOG.md |
| G-PI-CHANGELOG-1256 | Before | `HookAPI` → `ExtensionAPI` | CHANGELOG.md |
| G-PI-CHANGELOG-1257 | Before | `HookContext` → `ExtensionContext` | CHANGELOG.md |
| G-PI-CHANGELOG-1258 | Before | `HookCommandContext` → `ExtensionCommandContext` | CHANGELOG.md |
| G-PI-CHANGELOG-1259 | Before | `HookUIContext` → `ExtensionUIContext` | CHANGELOG.md |
| G-PI-CHANGELOG-1260 | Before | `CustomToolAPI` → `ExtensionAPI` (merged) | CHANGELOG.md |
| G-PI-CHANGELOG-1261 | Before | `CustomToolContext` → `ExtensionContext` (merged) | CHANGELOG.md |
| G-PI-CHANGELOG-1262 | Before | `CustomToolUIContext` → `ExtensionUIContext` | CHANGELOG.md |
| G-PI-CHANGELOG-1263 | Before | `CustomTool` → `ToolDefinition` | CHANGELOG.md |
| G-PI-CHANGELOG-1264 | Before | `CustomToolFactory` → `ExtensionFactory` | CHANGELOG.md |
| G-PI-CHANGELOG-1265 | Before | `HookMessage` → `CustomMessage` | CHANGELOG.md |
| G-PI-CHANGELOG-1266 | Before | Import changes: | CHANGELOG.md |
| G-PI-CHANGELOG-1267 | Before | Custom tools now have full context access. Tools registered via `pi.registerTool()` now receive the same `ctx` object that event handlers receive. Previously, custom tools had limited context. Now all extension code shares the same capabilities: | CHANGELOG.md |
| G-PI-CHANGELOG-1268 | Before | `pi.registerTool()`  Register tools the LLM can call | CHANGELOG.md |
| G-PI-CHANGELOG-1269 | Before | `pi.registerCommand()`  Register commands like `/mycommand` | CHANGELOG.md |
| G-PI-CHANGELOG-1270 | Before | `pi.registerShortcut()`  Register keyboard shortcuts (shown in `/hotkeys`) | CHANGELOG.md |
| G-PI-CHANGELOG-1271 | Before | `pi.registerFlag()`  Register CLI flags (shown in `help`) | CHANGELOG.md |
| G-PI-CHANGELOG-1272 | Before | `pi.registerMessageRenderer()`  Custom TUI rendering for message types | CHANGELOG.md |
| G-PI-CHANGELOG-1273 | Before | `pi.on()`  Subscribe to lifecycle events (tool_call, session_start, etc.) | CHANGELOG.md |
| G-PI-CHANGELOG-1274 | Before | `pi.sendMessage()`  Inject messages into the conversation | CHANGELOG.md |
| G-PI-CHANGELOG-1275 | Before | `pi.appendEntry()`  Persist custom data in session (survives restart/branch) | CHANGELOG.md |
| G-PI-CHANGELOG-1276 | Before | `pi.exec()`  Run shell commands | CHANGELOG.md |
| G-PI-CHANGELOG-1277 | Before | `pi.getActiveTools()` / `pi.setActiveTools()`  Dynamic tool enable/disable | CHANGELOG.md |
| G-PI-CHANGELOG-1278 | Before | `pi.getAllTools()`  List all available tools | CHANGELOG.md |
| G-PI-CHANGELOG-1279 | Before | `pi.events`  Event bus for crossextension communication | CHANGELOG.md |
| G-PI-CHANGELOG-1280 | Before | `ctx.ui.confirm()` / `select()` / `input()`  User prompts | CHANGELOG.md |
| G-PI-CHANGELOG-1281 | Before | `ctx.ui.notify()`  Toast notifications | CHANGELOG.md |
| G-PI-CHANGELOG-1282 | Before | `ctx.ui.setStatus()`  Persistent status in footer (multiple extensions can set their own) | CHANGELOG.md |
| G-PI-CHANGELOG-1283 | Before | `ctx.ui.setWidget()`  Widget display above editor | CHANGELOG.md |
| G-PI-CHANGELOG-1284 | Before | `ctx.ui.setTitle()`  Set terminal window title | CHANGELOG.md |
| G-PI-CHANGELOG-1285 | Before | `ctx.ui.custom()`  Full TUI component with keyboard handling | CHANGELOG.md |
| G-PI-CHANGELOG-1286 | Before | `ctx.ui.editor()`  Multiline text editor with external editor support | CHANGELOG.md |
| G-PI-CHANGELOG-1287 | Before | `ctx.sessionManager`  Read session entries, get branch history | CHANGELOG.md |
| G-PI-CHANGELOG-1288 | Before | Settings changes: | CHANGELOG.md |
| G-PI-CHANGELOG-1289 | Before | CLI changes: | CHANGELOG.md |
| G-PI-CHANGELOG-1290 | Prompt Templates Migration | Automatic migration: The `commands/` directory is automatically renamed to `prompts/` on startup (if `prompts/` doesn't exist). Works for both regular directories and symlinks. | CHANGELOG.md |
| G-PI-CHANGELOG-1291 | Prompt Templates Migration | Directory changes: | CHANGELOG.md |
| G-PI-CHANGELOG-1292 | Prompt Templates Migration | SDK type renames: | CHANGELOG.md |
| G-PI-CHANGELOG-1293 | Prompt Templates Migration | `FileSlashCommand` → `PromptTemplate` | CHANGELOG.md |
| G-PI-CHANGELOG-1294 | Prompt Templates Migration | `LoadSlashCommandsOptions` → `LoadPromptTemplatesOptions` | CHANGELOG.md |
| G-PI-CHANGELOG-1295 | Prompt Templates Migration | SDK function renames: | CHANGELOG.md |
| G-PI-CHANGELOG-1296 | Prompt Templates Migration | `discoverSlashCommands()` → `discoverPromptTemplates()` | CHANGELOG.md |
| G-PI-CHANGELOG-1297 | Prompt Templates Migration | `loadSlashCommands()` → `loadPromptTemplates()` | CHANGELOG.md |
| G-PI-CHANGELOG-1298 | Prompt Templates Migration | `expandSlashCommand()` → `expandPromptTemplate()` | CHANGELOG.md |
| G-PI-CHANGELOG-1299 | Prompt Templates Migration | `getCommandsDir()` → `getPromptsDir()` | CHANGELOG.md |
| G-PI-CHANGELOG-1300 | Prompt Templates Migration | SDK option renames: | CHANGELOG.md |
| G-PI-CHANGELOG-1301 | Prompt Templates Migration | `CreateAgentSessionOptions.slashCommands` → `.promptTemplates` | CHANGELOG.md |
| G-PI-CHANGELOG-1302 | Prompt Templates Migration | `AgentSession.fileCommands` → `.promptTemplates` | CHANGELOG.md |
| G-PI-CHANGELOG-1303 | Prompt Templates Migration | `PromptOptions.expandSlashCommands` → `.expandPromptTemplates` | CHANGELOG.md |
| G-PI-CHANGELOG-1304 | SDK Migration | Discovery functions: | CHANGELOG.md |
| G-PI-CHANGELOG-1305 | SDK Migration | `discoverAndLoadHooks()` → `discoverAndLoadExtensions()` | CHANGELOG.md |
| G-PI-CHANGELOG-1306 | SDK Migration | `discoverAndLoadCustomTools()` → merged into `discoverAndLoadExtensions()` | CHANGELOG.md |
| G-PI-CHANGELOG-1307 | SDK Migration | `loadHooks()` → `loadExtensions()` | CHANGELOG.md |
| G-PI-CHANGELOG-1308 | SDK Migration | `loadCustomTools()` → merged into `loadExtensions()` | CHANGELOG.md |
| G-PI-CHANGELOG-1309 | SDK Migration | Runner and wrapper: | CHANGELOG.md |
| G-PI-CHANGELOG-1310 | SDK Migration | `HookRunner` → `ExtensionRunner` | CHANGELOG.md |
| G-PI-CHANGELOG-1311 | SDK Migration | `wrapToolsWithHooks()` → `wrapToolsWithExtensions()` | CHANGELOG.md |
| G-PI-CHANGELOG-1312 | SDK Migration | `wrapToolWithHooks()` → `wrapToolWithExtensions()` | CHANGELOG.md |
| G-PI-CHANGELOG-1313 | SDK Migration | CreateAgentSessionOptions: | CHANGELOG.md |
| G-PI-CHANGELOG-1314 | SDK Migration | `.hooks` → removed (use `.additionalExtensionPaths` for paths) | CHANGELOG.md |
| G-PI-CHANGELOG-1315 | SDK Migration | `.additionalHookPaths` → `.additionalExtensionPaths` | CHANGELOG.md |
| G-PI-CHANGELOG-1316 | SDK Migration | `.preloadedHooks` → `.preloadedExtensions` | CHANGELOG.md |
| G-PI-CHANGELOG-1317 | SDK Migration | `.customTools` type changed: `Array<{ path?; tool: CustomTool }>` → `ToolDefinition[]` | CHANGELOG.md |
| G-PI-CHANGELOG-1318 | SDK Migration | `.additionalCustomToolPaths` → merged into `.additionalExtensionPaths` | CHANGELOG.md |
| G-PI-CHANGELOG-1319 | SDK Migration | `.slashCommands` → `.promptTemplates` | CHANGELOG.md |
| G-PI-CHANGELOG-1320 | SDK Migration | AgentSession: | CHANGELOG.md |
| G-PI-CHANGELOG-1321 | SDK Migration | `.hookRunner` → `.extensionRunner` | CHANGELOG.md |
| G-PI-CHANGELOG-1322 | SDK Migration | `.fileCommands` → `.promptTemplates` | CHANGELOG.md |
| G-PI-CHANGELOG-1323 | SDK Migration | `.sendHookMessage()` → `.sendCustomMessage()` | CHANGELOG.md |
| G-PI-CHANGELOG-1324 | Session Migration | Automatic. Session version bumped from 2 to 3. Existing sessions are migrated on first load: | CHANGELOG.md |
| G-PI-CHANGELOG-1325 | Session Migration | Message role `"hookMessage"` → `"custom"` | CHANGELOG.md |
| G-PI-CHANGELOG-1326 | Breaking Changes | Settings: `hooks` and `customTools` arrays replaced with single `extensions` array | CHANGELOG.md |
| G-PI-CHANGELOG-1327 | Breaking Changes | CLI: `hook` and `tool` flags replaced with `extension` / `e` | CHANGELOG.md |
| G-PI-CHANGELOG-1328 | Breaking Changes | Directories: `hooks/`, `tools/` → `extensions/`; `commands/` → `prompts/` | CHANGELOG.md |
| G-PI-CHANGELOG-1329 | Breaking Changes | Types: See type renames above | CHANGELOG.md |
| G-PI-CHANGELOG-1330 | Breaking Changes | SDK: See SDK migration above | CHANGELOG.md |
| G-PI-CHANGELOG-1331 | Changed | Extensions can have their own `package.json` with dependencies (resolved via jiti) | CHANGELOG.md |
| G-PI-CHANGELOG-1332 | Changed | Documentation: `docs/hooks.md` and `docs/customtools.md` merged into `docs/extensions.md` | CHANGELOG.md |
| G-PI-CHANGELOG-1333 | Changed | Examples: `examples/hooks/` and `examples/customtools/` merged into `examples/extensions/` | CHANGELOG.md |
| G-PI-CHANGELOG-1334 | Changed | README: Extensions section expanded with custom tools, commands, events, state persistence, shortcuts, flags, and UI examples | CHANGELOG.md |
| G-PI-CHANGELOG-1335 | Changed | SDK: `customTools` option now accepts `ToolDefinition[]` directly (simplified from `Array<{ path?, tool }>`) | CHANGELOG.md |
| G-PI-CHANGELOG-1336 | Changed | SDK: `extensions` option accepts `ExtensionFactory[]` for inline extensions | CHANGELOG.md |
| G-PI-CHANGELOG-1337 | Changed | SDK: `additionalExtensionPaths` replaces both `additionalHookPaths` and `additionalCustomToolPaths` | CHANGELOG.md |
| G-PI-CHANGELOG-1338 | Added | Hook API: `ctx.ui.setTitle(title)` allows hooks to set the terminal window/tab title ([#446](https://github.com/badlogic/pimono/pull/446) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1339 | Changed | Expanded keybinding documentation to list all 32 supported symbol keys with notes on ctrl+symbol behavior ([#450](https://github.com/badlogic/pimono/pull/450) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-1340 | Added | Hook API: `pi.getActiveTools()` and `pi.setActiveTools(toolNames)` for dynamically enabling/disabling tools from hooks | CHANGELOG.md |
| G-PI-CHANGELOG-1341 | Added | Hook API: `pi.getAllTools()` to enumerate all configured tools (builtin via tools or default, plus custom tools) | CHANGELOG.md |
| G-PI-CHANGELOG-1342 | Added | Hook API: `pi.registerFlag(name, options)` and `pi.getFlag(name)` for hooks to register custom CLI flags (parsed automatically) | CHANGELOG.md |
| G-PI-CHANGELOG-1343 | Added | Hook API: `pi.registerShortcut(shortcut, options)` for hooks to register custom keyboard shortcuts using `KeyId` (e.g., `Key.shift("p")`). Conflicts with builtin shortcuts are skipped, conflicts between hooks logged as warnings. | CHANGELOG.md |
| G-PI-CHANGELOG-1344 | Added | Hook API: `ctx.ui.setWidget(key, content)` for status displays above the editor. Accepts either a string array or a component factory function. | CHANGELOG.md |
| G-PI-CHANGELOG-1345 | Added | Hook API: `theme.strikethrough(text)` for strikethrough text styling | CHANGELOG.md |
| G-PI-CHANGELOG-1346 | Added | Hook API: `before_agent_start` handlers can now return `systemPromptAppend` to dynamically append text to the system prompt for that turn. Multiple hooks' appends are concatenated. | CHANGELOG.md |
| G-PI-CHANGELOG-1347 | Added | Hook API: `before_agent_start` handlers can now return multiple messages (all are injected, not just the first) | CHANGELOG.md |
| G-PI-CHANGELOG-1348 | Added | `/hotkeys` command now shows hookregistered shortcuts in a separate "Hooks" section | CHANGELOG.md |
| G-PI-CHANGELOG-1349 | Added | New example hook: `planmode.ts`  Claude Codestyle readonly exploration mode: | CHANGELOG.md |
| G-PI-CHANGELOG-1350 | Added | Toggle via `/plan` command, `Shift+P` shortcut, or `plan` CLI flag | CHANGELOG.md |
| G-PI-CHANGELOG-1351 | Added | Readonly tools: `read`, `bash`, `grep`, `find`, `ls` (no `edit`/`write`) | CHANGELOG.md |
| G-PI-CHANGELOG-1352 | Added | Bash commands restricted to nondestructive operations (blocks `rm`, `mv`, `git commit`, `npm install`, etc.) | CHANGELOG.md |
| G-PI-CHANGELOG-1353 | Added | Interactive prompt after each response: execute plan, stay in plan mode, or refine | CHANGELOG.md |
| G-PI-CHANGELOG-1354 | Added | Todo list widget showing progress with checkboxes and strikethrough for completed items | CHANGELOG.md |
| G-PI-CHANGELOG-1355 | Added | Each todo has a unique ID; agent marks items done by outputting `[DONE:id]` | CHANGELOG.md |
| G-PI-CHANGELOG-1356 | Added | Progress updates via `agent_end` hook (parses completed items from final message) | CHANGELOG.md |
| G-PI-CHANGELOG-1357 | Added | `/todos` command to view current plan progress | CHANGELOG.md |
| G-PI-CHANGELOG-1358 | Added | Shows `⏸ plan` indicator in footer when in plan mode, `📋 2/5` when executing | CHANGELOG.md |
| G-PI-CHANGELOG-1359 | Added | State persists across sessions (including todo progress) | CHANGELOG.md |
| G-PI-CHANGELOG-1360 | Added | New example hook: `tools.ts`  Interactive `/tools` command to enable/disable tools with session persistence | CHANGELOG.md |
| G-PI-CHANGELOG-1361 | Added | New example hook: `pirate.ts`  Demonstrates `systemPromptAppend` to make the agent speak like a pirate | CHANGELOG.md |
| G-PI-CHANGELOG-1362 | Added | Tool registry now contains all builtin tools (read, bash, edit, write, grep, find, ls) even when `tools` limits the initially active set. Hooks can enable any tool from the registry via `pi.setActiveTools()`. | CHANGELOG.md |
| G-PI-CHANGELOG-1363 | Added | System prompt now automatically rebuilds when tools change via `setActiveTools()`, updating tool descriptions and guidelines to match the new tool set | CHANGELOG.md |
| G-PI-CHANGELOG-1364 | Added | Hook errors now display full stack traces for easier debugging | CHANGELOG.md |
| G-PI-CHANGELOG-1365 | Added | Event bus (`pi.events`) for tool/hook communication: shared pub/sub between custom tools and hooks | CHANGELOG.md |
| G-PI-CHANGELOG-1366 | Added | Custom tools now have `pi.sendMessage()` to send messages directly to the agent session without needing the event bus | CHANGELOG.md |
| G-PI-CHANGELOG-1367 | Added | `sendMessage()` supports `deliverAs: "nextTurn"` to queue messages for the next user prompt | CHANGELOG.md |
| G-PI-CHANGELOG-1368 | Changed | Removed image placeholders after copy & paste, replaced with inserting image file paths directly. ([#442](https://github.com/badlogic/pimono/pull/442) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1369 | Fixed | Fixed potential text decoding issues in bash executor by using streaming TextDecoder instead of Buffer.toString() | CHANGELOG.md |
| G-PI-CHANGELOG-1370 | Fixed | External editor (CtrlG) now shows full pasted content instead of `[paste #N ...]` placeholders ([#444](https://github.com/badlogic/pimono/pull/444) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1371 | Breaking Changes | Key detection functions removed from `@mariozechner/pitui`: All `isXxx()` key detection functions (`isEnter()`, `isEscape()`, `isCtrlC()`, etc.) have been removed. Use `matchesKey(data, keyId)` instead (e.g., `matchesKey(data, "enter")`, `matchesKey(data, "ctrl+c")`). This affects hooks and custom tools that use `ctx.ui.custom()` with keyboard input handling. ([#405](https://github.com/badlogic/pimono/pull/405)) | CHANGELOG.md |
| G-PI-CHANGELOG-1372 | Added | Clipboard image paste support via `Ctrl+V`. Images are saved to a temp file and attached to the message. Works on macOS, Windows, and Linux (X11). ([#419](https://github.com/badlogic/pimono/issues/419)) | CHANGELOG.md |
| G-PI-CHANGELOG-1373 | Added | Configurable keybindings via `~/.pi/agent/keybindings.json`. All keyboard shortcuts (editor navigation, deletion, app actions like model cycling, etc.) can now be customized. Supports multiple bindings per action. ([#405](https://github.com/badlogic/pimono/pull/405) by [@hjanuschka](https://github.com/hjanuschka)) | CHANGELOG.md |
| G-PI-CHANGELOG-1374 | Added | `/quit` and `/exit` slash commands to gracefully exit the application. Unlike double Ctrl+C, these properly await hook and custom tool cleanup handlers before exiting. ([#426](https://github.com/badlogic/pimono/pull/426) by [@benvargas](https://github.com/benvargas)) | CHANGELOG.md |
| G-PI-CHANGELOG-1375 | Fixed | Subagent example README referenced incorrect filename `subagent.ts` instead of `index.ts` ([#427](https://github.com/badlogic/pimono/pull/427) by [@Whamp](https://github.com/Whamp)) | CHANGELOG.md |
| G-PI-CHANGELOG-1376 | Fixed | `listmodels` no longer shows Google Vertex AI models without explicit authentication configured | CHANGELOG.md |
| G-PI-CHANGELOG-1377 | Fixed | JPEG/GIF/WebP images not displaying in terminals using Kitty graphics protocol (Kitty, Ghostty, WezTerm). The protocol requires PNG format, so nonPNG images are now converted before display. | CHANGELOG.md |
| G-PI-CHANGELOG-1378 | Fixed | Version check URL typo preventing update notifications from working ([#423](https://github.com/badlogic/pimono/pull/423) by [@skuridin](https://github.com/skuridin)) | CHANGELOG.md |
| G-PI-CHANGELOG-1379 | Fixed | Large images exceeding Anthropic's 5MB limit now retry with progressive quality/size reduction ([#424](https://github.com/badlogic/pimono/pull/424) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1380 | Added | `$ARGUMENTS` syntax for custom slash commands as alternative to `$@` for all arguments joined. Aligns with patterns used by Claude, Codex, and OpenCode. Both syntaxes remain fully supported. ([#418](https://github.com/badlogic/pimono/pull/418) by [@skuridin](https://github.com/skuridin)) | CHANGELOG.md |
| G-PI-CHANGELOG-1381 | Changed | Slash commands and hook commands now work during streaming: Previously, using a slash command or hook command while the agent was streaming would crash with "Agent is already processing". Now: | CHANGELOG.md |
| G-PI-CHANGELOG-1382 | Changed | Hook commands execute immediately (they manage their own LLM interaction via `pi.sendMessage()`) | CHANGELOG.md |
| G-PI-CHANGELOG-1383 | Changed | Filebased slash commands are expanded and queued via steer/followUp | CHANGELOG.md |
| G-PI-CHANGELOG-1384 | Changed | `steer()` and `followUp()` now expand filebased slash commands and error on hook commands (hook commands cannot be queued) | CHANGELOG.md |
| G-PI-CHANGELOG-1385 | Changed | `prompt()` accepts new `streamingBehavior` option (`"steer"` or `"followUp"`) to specify queueing behavior during streaming | CHANGELOG.md |
| G-PI-CHANGELOG-1386 | Changed | RPC `prompt` command now accepts optional `streamingBehavior` field | CHANGELOG.md |
| G-PI-CHANGELOG-1387 | Fixed | Slash command argument substitution now processes positional arguments (`$1`, `$2`, etc.) before allarguments (`$@`, `$ARGUMENTS`) to prevent recursive substitution when argument values contain dollardigit patterns like `$100`. ([#418](https://github.com/badlogic/pimono/pull/418) by [@skuridin](https://github.com/skuridin)) | CHANGELOG.md |
| G-PI-CHANGELOG-1388 | Added | Shell commands without context contribution: use `!!command` to execute a bash command that is shown in the TUI and saved to session history but excluded from LLM context. Useful for running commands you don't want the AI to see. ([#414](https://github.com/badlogic/pimono/issues/414)) | CHANGELOG.md |
| G-PI-CHANGELOG-1389 | Fixed | Edit tool diff not displaying in TUI due to race condition between async preview computation and tool execution | CHANGELOG.md |
| G-PI-CHANGELOG-1390 | Breaking Changes | Queue API replaced with steer/followUp: The `queueMessage()` method has been split into two methods with different delivery semantics ([#403](https://github.com/badlogic/pimono/issues/403)): | CHANGELOG.md |
| G-PI-CHANGELOG-1391 | Breaking Changes | `steer(text)`: Interrupts the agent midrun (Enter while streaming). Delivered after current tool execution. | CHANGELOG.md |
| G-PI-CHANGELOG-1392 | Breaking Changes | `followUp(text)`: Waits until the agent finishes (Alt+Enter while streaming). Delivered only when agent stops. | CHANGELOG.md |
| G-PI-CHANGELOG-1393 | Breaking Changes | Settings renamed: `queueMode` setting renamed to `steeringMode`. Added new `followUpMode` setting. Old settings.json files are migrated automatically. | CHANGELOG.md |
| G-PI-CHANGELOG-1394 | Breaking Changes | AgentSession methods renamed: | CHANGELOG.md |
| G-PI-CHANGELOG-1395 | Breaking Changes | `queueMessage()` → `steer()` and `followUp()` | CHANGELOG.md |
| G-PI-CHANGELOG-1396 | Breaking Changes | `queueMode` getter → `steeringMode` and `followUpMode` getters | CHANGELOG.md |
| G-PI-CHANGELOG-1397 | Breaking Changes | `setQueueMode()` → `setSteeringMode()` and `setFollowUpMode()` | CHANGELOG.md |
| G-PI-CHANGELOG-1398 | Breaking Changes | `queuedMessageCount` → `pendingMessageCount` | CHANGELOG.md |
| G-PI-CHANGELOG-1399 | Breaking Changes | `getQueuedMessages()` → `getSteeringMessages()` and `getFollowUpMessages()` | CHANGELOG.md |
| G-PI-CHANGELOG-1400 | Breaking Changes | `clearQueue()` now returns `{ steering: string[], followUp: string[] }` | CHANGELOG.md |
| G-PI-CHANGELOG-1401 | Breaking Changes | `hasQueuedMessages()` → `hasPendingMessages()` | CHANGELOG.md |
| G-PI-CHANGELOG-1402 | Breaking Changes | Hook API signature changed: `pi.sendMessage()` second parameter changed from `triggerTurn?: boolean` to `options?: { triggerTurn?, deliverAs? }`. Use `deliverAs: "followUp"` for followup delivery. Affects both hooks and internal `sendHookMessage()` method. | CHANGELOG.md |
| G-PI-CHANGELOG-1403 | Breaking Changes | RPC API changes: | CHANGELOG.md |
| G-PI-CHANGELOG-1404 | Breaking Changes | `queue_message` command → `steer` and `follow_up` commands | CHANGELOG.md |
| G-PI-CHANGELOG-1405 | Breaking Changes | `set_queue_mode` command → `set_steering_mode` and `set_follow_up_mode` commands | CHANGELOG.md |
| G-PI-CHANGELOG-1406 | Breaking Changes | `RpcSessionState.queueMode` → `steeringMode` and `followUpMode` | CHANGELOG.md |
| G-PI-CHANGELOG-1407 | Breaking Changes | Settings UI: "Queue mode" setting split into "Steering mode" and "Followup mode" | CHANGELOG.md |
| G-PI-CHANGELOG-1408 | Added | Configurable doubleescape action: choose whether doubleescape with empty editor opens `/tree` (default) or `/branch`. Configure via `/settings` or `doubleEscapeAction` in settings.json ([#404](https://github.com/badlogic/pimono/issues/404)) | CHANGELOG.md |
| G-PI-CHANGELOG-1409 | Added | Vertex AI provider (`googlevertex`): access Gemini models via Google Cloud Vertex AI using Application Default Credentials ([#300](https://github.com/badlogic/pimono/pull/300) by [@defaultanton](https://github.com/defaultanton)) | CHANGELOG.md |
| G-PI-CHANGELOG-1410 | Added | Builtin provider overrides in `models.json`: override just `baseUrl` to route a builtin provider through a proxy while keeping all its models, or define `models` to fully replace the provider ([#406](https://github.com/badlogic/pimono/pull/406) by [@yevhen](https://github.com/yevhen)) | CHANGELOG.md |
| G-PI-CHANGELOG-1411 | Added | Automatic image resizing: images larger than 2000x2000 are resized for better model compatibility. Original dimensions are injected into the prompt. Controlled via `/settings` or `images.autoResize` in settings.json. ([#402](https://github.com/badlogic/pimono/pull/402) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1412 | Added | Alt+Enter keybind to queue followup messages while agent is streaming | CHANGELOG.md |
| G-PI-CHANGELOG-1413 | Added | `Theme` and `ThemeColor` types now exported for hooks using `ctx.ui.custom()` | CHANGELOG.md |
| G-PI-CHANGELOG-1414 | Added | Terminal window title now displays "pi  dirname" to identify which project session you're in ([#407](https://github.com/badlogic/pimono/pull/407) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-1415 | Changed | Editor component now uses word wrapping instead of characterlevel wrapping for better readability ([#382](https://github.com/badlogic/pimono/pull/382) by [@nickseelert](https://github.com/nickseelert)) | CHANGELOG.md |
| G-PI-CHANGELOG-1416 | Fixed | `/model` selector now opens instantly instead of waiting for OAuth token refresh. Token refresh is deferred until a model is actually used. | CHANGELOG.md |
| G-PI-CHANGELOG-1417 | Fixed | Shift+Space, Shift+Backspace, and Shift+Delete now work correctly in Kittyprotocol terminals (Kitty, WezTerm, etc.) instead of being silently ignored ([#411](https://github.com/badlogic/pimono/pull/411) by [@nathyong](https://github.com/nathyong)) | CHANGELOG.md |
| G-PI-CHANGELOG-1418 | Fixed | `AgentSession.prompt()` now throws if called while the agent is already streaming, preventing race conditions. Use `steer()` or `followUp()` to queue messages during streaming. | CHANGELOG.md |
| G-PI-CHANGELOG-1419 | Fixed | Ctrl+C now works like Escape in selector components, so mashing Ctrl+C will eventually close the program ([#400](https://github.com/badlogic/pimono/pull/400) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1420 | Fixed | Model selector no longer allows negative index when pressing arrow keys before models finish loading ([#398](https://github.com/badlogic/pimono/pull/398) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1421 | Fixed | Type guard functions (`isBashToolResult`, etc.) now exported at runtime, not just in type declarations ([#397](https://github.com/badlogic/pimono/issues/397)) | CHANGELOG.md |
| G-PI-CHANGELOG-1422 | Session Tree | Existing sessions are automatically migrated (v1 → v2) on first load. No manual action required. | CHANGELOG.md |
| G-PI-CHANGELOG-1423 | Hooks Migration | Type renames: | CHANGELOG.md |
| G-PI-CHANGELOG-1424 | Hooks Migration | `HookEventContext` → `HookContext` | CHANGELOG.md |
| G-PI-CHANGELOG-1425 | Hooks Migration | `HookCommandContext` is now a new interface extending `HookContext` with session control methods | CHANGELOG.md |
| G-PI-CHANGELOG-1426 | Hooks Migration | Event changes: | CHANGELOG.md |
| G-PI-CHANGELOG-1427 | Hooks Migration | The monolithic `session` event is now split into granular events: `session_start`, `session_before_switch`, `session_switch`, `session_before_branch`, `session_branch`, `session_before_compact`, `session_compact`, `session_shutdown` | CHANGELOG.md |
| G-PI-CHANGELOG-1428 | Hooks Migration | `session_before_switch` and `session_switch` events now include `reason: "new" | "resume"` to distinguish between `/new` and `/resume` | CHANGELOG.md |
| G-PI-CHANGELOG-1429 | Hooks Migration | New `session_before_tree` and `session_tree` events for `/tree` navigation (hook can provide custom branch summary) | CHANGELOG.md |
| G-PI-CHANGELOG-1430 | Hooks Migration | New `before_agent_start` event: inject messages before the agent loop starts | CHANGELOG.md |
| G-PI-CHANGELOG-1431 | Hooks Migration | New `context` event: modify messages nondestructively before each LLM call | CHANGELOG.md |
| G-PI-CHANGELOG-1432 | Hooks Migration | Session entries are no longer passed in events. Use `ctx.sessionManager.getEntries()` or `ctx.sessionManager.getBranch()` instead | CHANGELOG.md |
| G-PI-CHANGELOG-1433 | Hooks Migration | API changes: | CHANGELOG.md |
| G-PI-CHANGELOG-1434 | Hooks Migration | `pi.send(text, attachments?)` → `pi.sendMessage(message, triggerTurn?)` (creates `CustomMessageEntry`) | CHANGELOG.md |
| G-PI-CHANGELOG-1435 | Hooks Migration | New `pi.appendEntry(customType, data?)` for hook state persistence (not in LLM context) | CHANGELOG.md |
| G-PI-CHANGELOG-1436 | Hooks Migration | New `pi.registerCommand(name, options)` for custom slash commands (handler receives `HookCommandContext`) | CHANGELOG.md |
| G-PI-CHANGELOG-1437 | Hooks Migration | New `pi.registerMessageRenderer(customType, renderer)` for custom TUI rendering | CHANGELOG.md |
| G-PI-CHANGELOG-1438 | Hooks Migration | New `ctx.isIdle()`, `ctx.abort()`, `ctx.hasQueuedMessages()` for agent state (available in all events) | CHANGELOG.md |
| G-PI-CHANGELOG-1439 | Hooks Migration | New `ctx.ui.editor(title, prefill?)` for multiline text editing with Ctrl+G external editor support | CHANGELOG.md |
| G-PI-CHANGELOG-1440 | Hooks Migration | New `ctx.ui.custom(component)` for full TUI component rendering with keyboard focus | CHANGELOG.md |
| G-PI-CHANGELOG-1441 | Hooks Migration | New `ctx.ui.setStatus(key, text)` for persistent status text in footer (multiple hooks can set their own) | CHANGELOG.md |
| G-PI-CHANGELOG-1442 | Hooks Migration | New `ctx.ui.theme` getter for styling text with theme colors | CHANGELOG.md |
| G-PI-CHANGELOG-1443 | Hooks Migration | `ctx.exec()` moved to `pi.exec()` | CHANGELOG.md |
| G-PI-CHANGELOG-1444 | Hooks Migration | `ctx.sessionFile` → `ctx.sessionManager.getSessionFile()` | CHANGELOG.md |
| G-PI-CHANGELOG-1445 | Hooks Migration | New `ctx.modelRegistry` and `ctx.model` for API key resolution | CHANGELOG.md |
| G-PI-CHANGELOG-1446 | Hooks Migration | HookCommandContext (slash commands only): | CHANGELOG.md |
| G-PI-CHANGELOG-1447 | Hooks Migration | `ctx.waitForIdle()`  wait for agent to finish streaming | CHANGELOG.md |
| G-PI-CHANGELOG-1448 | Hooks Migration | `ctx.newSession(options?)`  create new sessions with optional setup callback | CHANGELOG.md |
| G-PI-CHANGELOG-1449 | Hooks Migration | `ctx.fork(entryId)  fork from a specific entry, creating a new session file | CHANGELOG.md |
| G-PI-CHANGELOG-1450 | Hooks Migration | `ctx.navigateTree(targetId, options?)`  navigate the session tree | CHANGELOG.md |
| G-PI-CHANGELOG-1451 | Hooks Migration | Removed: | CHANGELOG.md |
| G-PI-CHANGELOG-1452 | Hooks Migration | `hookTimeout` setting (hooks no longer have timeouts; use Ctrl+C to abort) | CHANGELOG.md |
| G-PI-CHANGELOG-1453 | Hooks Migration | `resolveApiKey` parameter (use `ctx.modelRegistry.getApiKey(model)`) | CHANGELOG.md |
| G-PI-CHANGELOG-1454 | Custom Tools Migration | Type renames: | CHANGELOG.md |
| G-PI-CHANGELOG-1455 | Custom Tools Migration | `CustomAgentTool` → `CustomTool` | CHANGELOG.md |
| G-PI-CHANGELOG-1456 | Custom Tools Migration | `ToolAPI` → `CustomToolAPI` | CHANGELOG.md |
| G-PI-CHANGELOG-1457 | Custom Tools Migration | `ToolContext` → `CustomToolContext` | CHANGELOG.md |
| G-PI-CHANGELOG-1458 | Custom Tools Migration | `ToolSessionEvent` → `CustomToolSessionEvent` | CHANGELOG.md |
| G-PI-CHANGELOG-1459 | Custom Tools Migration | Execute signature changed: | CHANGELOG.md |
| G-PI-CHANGELOG-1460 | Custom Tools Migration | `ctx.isIdle()`  check if agent is streaming | CHANGELOG.md |
| G-PI-CHANGELOG-1461 | Custom Tools Migration | `ctx.hasQueuedMessages()`  check if user has queued messages (skip interactive prompts) | CHANGELOG.md |
| G-PI-CHANGELOG-1462 | Custom Tools Migration | `ctx.abort()`  abort current operation (fireandforget) | CHANGELOG.md |
| G-PI-CHANGELOG-1463 | Custom Tools Migration | Session event changes: | CHANGELOG.md |
| G-PI-CHANGELOG-1464 | Custom Tools Migration | `CustomToolSessionEvent` now only has `reason` and `previousSessionFile` | CHANGELOG.md |
| G-PI-CHANGELOG-1465 | Custom Tools Migration | Session entries are no longer in the event. Use `ctx.sessionManager.getBranch()` or `ctx.sessionManager.getEntries()` to reconstruct state | CHANGELOG.md |
| G-PI-CHANGELOG-1466 | Custom Tools Migration | Reasons: `"start" | "switch" | "branch" | "tree" | "shutdown"` (no separate `"new"` reason; `/new` triggers `"switch"`) | CHANGELOG.md |
| G-PI-CHANGELOG-1467 | Custom Tools Migration | `dispose()` method removed. Use `onSession` with `reason: "shutdown"` for cleanup | CHANGELOG.md |
| G-PI-CHANGELOG-1468 | SDK Migration | Type changes: | CHANGELOG.md |
| G-PI-CHANGELOG-1469 | SDK Migration | `CustomAgentTool` → `CustomTool` | CHANGELOG.md |
| G-PI-CHANGELOG-1470 | SDK Migration | `AppMessage` → `AgentMessage` | CHANGELOG.md |
| G-PI-CHANGELOG-1471 | SDK Migration | `sessionFile` returns `string | undefined` (was `string | null`) | CHANGELOG.md |
| G-PI-CHANGELOG-1472 | SDK Migration | `model` returns `Model | undefined` (was `Model | null`) | CHANGELOG.md |
| G-PI-CHANGELOG-1473 | SDK Migration | `Attachment` type removed. Use `ImageContent` from `@mariozechner/piai` instead. Add images directly to message content arrays. | CHANGELOG.md |
| G-PI-CHANGELOG-1474 | SDK Migration | AgentSession API: | CHANGELOG.md |
| G-PI-CHANGELOG-1475 | SDK Migration | `branch(entryIndex: number)` → `branch(entryId: string)` | CHANGELOG.md |
| G-PI-CHANGELOG-1476 | SDK Migration | `getUserMessagesForBranching()` returns `{ entryId, text }` instead of `{ entryIndex, text }` | CHANGELOG.md |
| G-PI-CHANGELOG-1477 | SDK Migration | `reset()` → `newSession(options?)` where options has optional `parentSession` for lineage tracking | CHANGELOG.md |
| G-PI-CHANGELOG-1478 | SDK Migration | `newSession()` and `switchSession()` now return `Promise<boolean>` (false if cancelled by hook) | CHANGELOG.md |
| G-PI-CHANGELOG-1479 | SDK Migration | New `navigateTree(targetId, options?)` for inplace tree navigation | CHANGELOG.md |
| G-PI-CHANGELOG-1480 | SDK Migration | Hook integration: | CHANGELOG.md |
| G-PI-CHANGELOG-1481 | SDK Migration | New `sendHookMessage(message, triggerTurn?)` for hook message injection | CHANGELOG.md |
| G-PI-CHANGELOG-1482 | SDK Migration | SessionManager API: | CHANGELOG.md |
| G-PI-CHANGELOG-1483 | SDK Migration | Method renames: `saveXXX()` → `appendXXX()` (e.g., `appendMessage`, `appendCompaction`) | CHANGELOG.md |
| G-PI-CHANGELOG-1484 | SDK Migration | `branchInPlace()` → `branch()` | CHANGELOG.md |
| G-PI-CHANGELOG-1485 | SDK Migration | `reset()` → `newSession(options?)` with optional `parentSession` for lineage tracking | CHANGELOG.md |
| G-PI-CHANGELOG-1486 | SDK Migration | `createBranchedSessionFromEntries(entries, index)` → `createBranchedSession(leafId)` | CHANGELOG.md |
| G-PI-CHANGELOG-1487 | SDK Migration | `SessionHeader.branchedFrom` → `SessionHeader.parentSession` | CHANGELOG.md |
| G-PI-CHANGELOG-1488 | SDK Migration | `saveCompaction(entry)` → `appendCompaction(summary, firstKeptEntryId, tokensBefore, details?)` | CHANGELOG.md |
| G-PI-CHANGELOG-1489 | SDK Migration | `getEntries()` now excludes the session header (use `getHeader()` separately) | CHANGELOG.md |
| G-PI-CHANGELOG-1490 | SDK Migration | `getSessionFile()` returns `string | undefined` (undefined for inmemory sessions) | CHANGELOG.md |
| G-PI-CHANGELOG-1491 | SDK Migration | New tree methods: `getTree()`, `getBranch()`, `getLeafId()`, `getLeafEntry()`, `getEntry()`, `getChildren()`, `getLabel()` | CHANGELOG.md |
| G-PI-CHANGELOG-1492 | SDK Migration | New append methods: `appendCustomEntry()`, `appendCustomMessageEntry()`, `appendLabelChange()` | CHANGELOG.md |
| G-PI-CHANGELOG-1493 | SDK Migration | New branch methods: `branch(entryId)`, `branchWithSummary()` | CHANGELOG.md |
| G-PI-CHANGELOG-1494 | SDK Migration | ModelRegistry (new): | CHANGELOG.md |
| G-PI-CHANGELOG-1495 | SDK Migration | Renamed exports: | CHANGELOG.md |
| G-PI-CHANGELOG-1496 | SDK Migration | `messageTransformer` → `convertToLlm` | CHANGELOG.md |
| G-PI-CHANGELOG-1497 | SDK Migration | `SessionContext` alias `LoadedSession` removed | CHANGELOG.md |
| G-PI-CHANGELOG-1498 | RPC Migration | Session commands: | CHANGELOG.md |
| G-PI-CHANGELOG-1499 | RPC Migration | `reset` command → `new_session` command with optional `parentSession` field | CHANGELOG.md |
| G-PI-CHANGELOG-1500 | RPC Migration | Branching commands: | CHANGELOG.md |
| G-PI-CHANGELOG-1501 | RPC Migration | `branch` command: `entryIndex` → `entryId` | CHANGELOG.md |
| G-PI-CHANGELOG-1502 | RPC Migration | `get_branch_messages` response: `entryIndex` → `entryId` | CHANGELOG.md |
| G-PI-CHANGELOG-1503 | RPC Migration | Type changes: | CHANGELOG.md |
| G-PI-CHANGELOG-1504 | RPC Migration | Messages are now `AgentMessage` (was `AppMessage`) | CHANGELOG.md |
| G-PI-CHANGELOG-1505 | RPC Migration | `prompt` command: `attachments` field replaced with `images` field using `ImageContent` format | CHANGELOG.md |
| G-PI-CHANGELOG-1506 | RPC Migration | Compaction events: | CHANGELOG.md |
| G-PI-CHANGELOG-1507 | RPC Migration | `auto_compaction_start` now includes `reason` field (`"threshold"` or `"overflow"`) | CHANGELOG.md |
| G-PI-CHANGELOG-1508 | RPC Migration | `auto_compaction_end` now includes `willRetry` field | CHANGELOG.md |
| G-PI-CHANGELOG-1509 | RPC Migration | `compact` response includes full `CompactionResult` (`summary`, `firstKeptEntryId`, `tokensBefore`, `details`) | CHANGELOG.md |
| G-PI-CHANGELOG-1510 | Structured Compaction | Clear sections: Goal, Progress, Key Information, File Operations | CHANGELOG.md |
| G-PI-CHANGELOG-1511 | Structured Compaction | File tracking: `readFiles` and `modifiedFiles` arrays in `details`, accumulated across compactions | CHANGELOG.md |
| G-PI-CHANGELOG-1512 | Structured Compaction | Conversations are serialized to text before summarization to prevent the model from "continuing" them | CHANGELOG.md |
| G-PI-CHANGELOG-1513 | Interactive Mode | `/tree` command: | CHANGELOG.md |
| G-PI-CHANGELOG-1514 | Interactive Mode | Navigate the full session tree inplace | CHANGELOG.md |
| G-PI-CHANGELOG-1515 | Interactive Mode | Search by typing, page with ←/→ | CHANGELOG.md |
| G-PI-CHANGELOG-1516 | Interactive Mode | Filter modes (Ctrl+O): default → notools → useronly → labeledonly → all | CHANGELOG.md |
| G-PI-CHANGELOG-1517 | Interactive Mode | Press `l` to label entries as bookmarks | CHANGELOG.md |
| G-PI-CHANGELOG-1518 | Interactive Mode | Selecting a branch switches context and optionally injects a summary of the abandoned branch | CHANGELOG.md |
| G-PI-CHANGELOG-1519 | Interactive Mode | Entry labels: | CHANGELOG.md |
| G-PI-CHANGELOG-1520 | Interactive Mode | Bookmark any entry via `/tree` → select → `l` | CHANGELOG.md |
| G-PI-CHANGELOG-1521 | Interactive Mode | Labels appear in tree view and persist as `LabelEntry` | CHANGELOG.md |
| G-PI-CHANGELOG-1522 | Interactive Mode | Theme changes (breaking for custom themes): | CHANGELOG.md |
| G-PI-CHANGELOG-1523 | Interactive Mode | `selectedBg`: background for selected/highlighted items in tree selector and other components | CHANGELOG.md |
| G-PI-CHANGELOG-1524 | Interactive Mode | `customMessageBg`: background for hookinjected messages (`CustomMessageEntry`) | CHANGELOG.md |
| G-PI-CHANGELOG-1525 | Interactive Mode | `customMessageText`: text color for hook messages | CHANGELOG.md |
| G-PI-CHANGELOG-1526 | Interactive Mode | `customMessageLabel`: label color for hook messages (the `[customType]` prefix) | CHANGELOG.md |
| G-PI-CHANGELOG-1527 | Interactive Mode | Settings: | CHANGELOG.md |
| G-PI-CHANGELOG-1528 | Interactive Mode | `enabledModels`: allowlist models in `settings.json` (same format as `models` CLI) | CHANGELOG.md |
| G-PI-CHANGELOG-1529 | Added | `ctx.ui.setStatus(key, text)` for hooks to display persistent status text in the footer ([#385](https://github.com/badlogic/pimono/pull/385) by [@prateekmedia](https://github.com/prateekmedia)) | CHANGELOG.md |
| G-PI-CHANGELOG-1530 | Added | `ctx.ui.theme` getter for styling status text and other output with theme colors | CHANGELOG.md |
| G-PI-CHANGELOG-1531 | Added | `/share` command to upload session as a secret GitHub gist and get a shareable URL via pi.dev ([#380](https://github.com/badlogic/pimono/issues/380)) | CHANGELOG.md |
| G-PI-CHANGELOG-1532 | Added | HTML export now includes a tree visualization sidebar for navigating session branches ([#375](https://github.com/badlogic/pimono/issues/375)) | CHANGELOG.md |
| G-PI-CHANGELOG-1533 | Added | HTML export supports keyboard shortcuts: Ctrl+T to toggle thinking blocks, Ctrl+O to toggle tool outputs | CHANGELOG.md |
| G-PI-CHANGELOG-1534 | Added | HTML export supports themeconfigurable background colors via optional `export` section in theme JSON ([#387](https://github.com/badlogic/pimono/pull/387) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1535 | Added | HTML export syntax highlighting now uses theme colors and matches TUI rendering | CHANGELOG.md |
| G-PI-CHANGELOG-1536 | Added | Snake game example hook: Demonstrates `ui.custom()`, `registerCommand()`, and session persistence. See [examples/hooks/snake.ts](examples/hooks/snake.ts). | CHANGELOG.md |
| G-PI-CHANGELOG-1537 | Added | `thinkingText` theme token: Configurable color for thinking block text. ([#366](https://github.com/badlogic/pimono/pull/366) by [@paulbettner](https://github.com/paulbettner)) | CHANGELOG.md |
| G-PI-CHANGELOG-1538 | Changed | Entry IDs: Session entries now use short 8character hex IDs instead of full UUIDs | CHANGELOG.md |
| G-PI-CHANGELOG-1539 | Changed | API key priority: `ANTHROPIC_OAUTH_TOKEN` now takes precedence over `ANTHROPIC_API_KEY` | CHANGELOG.md |
| G-PI-CHANGELOG-1540 | Changed | HTML export template split into separate files (template.html, template.css, template.js) for easier maintenance | CHANGELOG.md |
| G-PI-CHANGELOG-1541 | Fixed | HTML export now properly sanitizes user messages containing HTML tags like `<style>` that could break DOM rendering | CHANGELOG.md |
| G-PI-CHANGELOG-1542 | Fixed | Crash when displaying bash output containing Unicode format characters like U+0600U+0604 ([#372](https://github.com/badlogic/pimono/pull/372) by [@HACKERC](https://github.com/HACKERC)) | CHANGELOG.md |
| G-PI-CHANGELOG-1543 | Fixed | Footer shows full session stats: Token usage and cost now include all messages, not just those after compaction. ([#322](https://github.com/badlogic/pimono/issues/322)) | CHANGELOG.md |
| G-PI-CHANGELOG-1544 | Fixed | Status messages spam chat log: Rapidly changing settings (e.g., thinking level via Shift+Tab) would add multiple status lines. Sequential status updates now coalesce into a single line. ([#365](https://github.com/badlogic/pimono/pull/365) by [@paulbettner](https://github.com/paulbettner)) | CHANGELOG.md |
| G-PI-CHANGELOG-1545 | Fixed | Toggling thinking blocks during streaming shows nothing: Pressing Ctrl+T while streaming would hide the current message until streaming completed. | CHANGELOG.md |
| G-PI-CHANGELOG-1546 | Fixed | Resuming session resets thinking level to off: Initial model and thinking level were not saved to session file, causing `resume`/`continue` to default to `off`. ([#342](https://github.com/badlogic/pimono/issues/342) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1547 | Fixed | Hook `tool_result` event ignores errors from custom tools: The `tool_result` hook event was never emitted when tools threw errors, and always had `isError: false` for successful executions. Now emits the event with correct `isError` value in both success and error cases. ([#374](https://github.com/badlogic/pimono/issues/374) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1548 | Fixed | Edit tool fails on Windows due to CRLF line endings: Files with CRLF line endings now match correctly when LLMs send LFonly text. Line endings are normalized before matching and restored to original style on write. ([#355](https://github.com/badlogic/pimono/issues/355) by [@PrathamDubey](https://github.com/PrathamDubey)) | CHANGELOG.md |
| G-PI-CHANGELOG-1549 | Fixed | Edit tool fails on files with UTF8 BOM: Files with UTF8 BOM marker could cause "text not found" errors since the LLM doesn't include the invisible BOM character. BOM is now stripped before matching and restored on write. ([#394](https://github.com/badlogic/pimono/pull/394) by [@prathamdby](https://github.com/prathamdby)) | CHANGELOG.md |
| G-PI-CHANGELOG-1550 | Fixed | Use bash instead of sh on Unix: Fixed shell commands using `/bin/sh` instead of `/bin/bash` on Unix systems. ([#328](https://github.com/badlogic/pimono/pull/328) by [@dnouri](https://github.com/dnouri)) | CHANGELOG.md |
| G-PI-CHANGELOG-1551 | Fixed | OAuth login URL clickable: Made OAuth login URLs clickable in terminal. ([#349](https://github.com/badlogic/pimono/pull/349) by [@Cursivez](https://github.com/Cursivez)) | CHANGELOG.md |
| G-PI-CHANGELOG-1552 | Fixed | Improved error messages: Better error messages when `apiKey` or `model` are missing. ([#346](https://github.com/badlogic/pimono/pull/346) by [@ronyrus](https://github.com/ronyrus)) | CHANGELOG.md |
| G-PI-CHANGELOG-1553 | Fixed | Session file validation: `findMostRecentSession()` now validates session headers before returning, preventing nonsession JSONL files from being loaded | CHANGELOG.md |
| G-PI-CHANGELOG-1554 | Fixed | Compaction error handling: `generateSummary()` and `generateTurnPrefixSummary()` now throw on LLM errors instead of returning empty strings | CHANGELOG.md |
| G-PI-CHANGELOG-1555 | Fixed | Compaction with branched sessions: Fixed compaction incorrectly including entries from abandoned branches, causing token overflow errors. Compaction now uses `sessionManager.getPath()` to work only on the current branch path, eliminating 80+ lines of duplicate entry collection logic between `prepareCompaction()` and `compact()` | CHANGELOG.md |
| G-PI-CHANGELOG-1556 | Fixed | enabledModels glob patterns: `models` and `enabledModels` now support glob patterns like `githubcopilot/` or `sonnet`. Previously, patterns were only matched literally or via substring search. ([#337](https://github.com/badlogic/pimono/issues/337)) | CHANGELOG.md |
| G-PI-CHANGELOG-1557 | Changed | Consolidated migrations: Moved auth migration from `AuthStorage.migrateLegacy()` to new `migrations.ts` module. | CHANGELOG.md |
| G-PI-CHANGELOG-1558 | Fixed | Sessions saved to wrong directory: In v0.30.0, sessions were being saved to `~/.pi/agent/` instead of `~/.pi/agent/sessions/<encodedcwd>/`, breaking `resume` and `/resume`. Misplaced sessions are automatically migrated on startup. ([#320](https://github.com/badlogic/pimono/issues/320) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1559 | Fixed | Custom system prompts missing context: When using a custom system prompt string, project context files (AGENTS.md), skills, date/time, and working directory were not appended. ([#321](https://github.com/badlogic/pimono/issues/321)) | CHANGELOG.md |
| G-PI-CHANGELOG-1560 | Breaking Changes | SessionManager API: The second parameter of `create()`, `continueRecent()`, and `list()` changed from `agentDir` to `sessionDir`. When provided, it specifies the session directory directly (no cwd encoding). When omitted, uses default (`~/.pi/agent/sessions/<encodedcwd>/`). `open()` no longer takes `agentDir`. ([#313](https://github.com/badlogic/pimono/pull/313)) | CHANGELOG.md |
| G-PI-CHANGELOG-1561 | Added | `sessiondir` flag: Use a custom directory for sessions instead of the default `~/.pi/agent/sessions/<encodedcwd>/`. Works with `c` (continue) and `r` (resume) flags. ([#313](https://github.com/badlogic/pimono/pull/313) by [@scutifer](https://github.com/scutifer)) | CHANGELOG.md |
| G-PI-CHANGELOG-1562 | Added | Reverse model cycling and model selector: Shift+Ctrl+P cycles models backward, Ctrl+L opens model selector (retaining text in editor). ([#315](https://github.com/badlogic/pimono/pull/315) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1563 | Added | Automatic custom system prompt loading: Pi now autoloads `SYSTEM.md` files to replace the default system prompt. Projectlocal `.pi/SYSTEM.md` takes precedence over global `~/.pi/agent/SYSTEM.md`. CLI `systemprompt` flag overrides both. ([#309](https://github.com/badlogic/pimono/issues/309)) | CHANGELOG.md |
| G-PI-CHANGELOG-1564 | Added | Unified `/settings` command: New settings menu consolidating thinking level, theme, queue mode, autocompact, show images, hide thinking, and collapse changelog. Replaces individual `/thinking`, `/queue`, `/theme`, `/autocompact`, and `/showimages` commands. ([#310](https://github.com/badlogic/pimono/issues/310)) | CHANGELOG.md |
| G-PI-CHANGELOG-1565 | Fixed | Custom tools/hooks with typebox subpath imports: Fixed jiti alias for `@sinclair/typebox` to point to package root instead of entry file, allowing imports like `@sinclair/typebox/compiler` to resolve correctly. ([#311](https://github.com/badlogic/pimono/issues/311) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-1566 | Breaking Changes | Renamed `/clear` to `/new`: The command to start a fresh session is now `/new`. Hook event reasons `before_clear`/`clear` are now `before_new`/`new`. Merry Christmas [@mitsuhiko](https://github.com/mitsuhiko)! ([#305](https://github.com/badlogic/pimono/pull/305)) | CHANGELOG.md |
| G-PI-CHANGELOG-1567 | Added | Autospace before pasted file paths: When pasting a file path (starting with `/`, `~`, or `.`) after a word character, a space is automatically prepended. ([#307](https://github.com/badlogic/pimono/pull/307) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1568 | Added | Word navigation in input fields: Added Ctrl+Left/Right and Alt+Left/Right for wordbyword cursor movement. ([#306](https://github.com/badlogic/pimono/pull/306) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-1569 | Added | Full Unicode input: Input fields now accept Unicode characters beyond ASCII. ([#306](https://github.com/badlogic/pimono/pull/306) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-1570 | Fixed | Readlinestyle Ctrl+W: Now skips trailing whitespace before deleting the preceding word, matching standard readline behavior. ([#306](https://github.com/badlogic/pimono/pull/306) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-1571 | Changed | Credential storage refactored: API keys and OAuth tokens are now stored in `~/.pi/agent/auth.json` instead of `oauth.json` and `settings.json`. Existing credentials are automatically migrated on first run. ([#296](https://github.com/badlogic/pimono/issues/296)) | CHANGELOG.md |
| G-PI-CHANGELOG-1572 | Changed | SDK API changes ([#296](https://github.com/badlogic/pimono/issues/296)): | CHANGELOG.md |
| G-PI-CHANGELOG-1573 | Changed | Added `AuthStorage` class for credential management (API keys and OAuth tokens) | CHANGELOG.md |
| G-PI-CHANGELOG-1574 | Changed | Added `ModelRegistry` class for model discovery and API key resolution | CHANGELOG.md |
| G-PI-CHANGELOG-1575 | Changed | Added `discoverAuthStorage()` and `discoverModels()` discovery functions | CHANGELOG.md |
| G-PI-CHANGELOG-1576 | Changed | `createAgentSession()` now accepts `authStorage` and `modelRegistry` options | CHANGELOG.md |
| G-PI-CHANGELOG-1577 | Changed | Removed `configureOAuthStorage()`, `defaultGetApiKey()`, `findModel()`, `discoverAvailableModels()` | CHANGELOG.md |
| G-PI-CHANGELOG-1578 | Changed | Removed `getApiKey` callback option (use `AuthStorage.setRuntimeApiKey()` for runtime overrides) | CHANGELOG.md |
| G-PI-CHANGELOG-1579 | Changed | Use `getModel()` from `@mariozechner/piai` for builtin models, `modelRegistry.find()` for custom models + builtin models | CHANGELOG.md |
| G-PI-CHANGELOG-1580 | Changed | See updated [SDK documentation](docs/sdk.md) and [README](README.md) | CHANGELOG.md |
| G-PI-CHANGELOG-1581 | Changed | Settings changes: Removed `apiKeys` from `settings.json`. Use `auth.json` instead. ([#296](https://github.com/badlogic/pimono/issues/296)) | CHANGELOG.md |
| G-PI-CHANGELOG-1582 | Fixed | Duplicate skill warnings for symlinks: Skills loaded via symlinks pointing to the same file are now silently deduplicated instead of showing name collision warnings. ([#304](https://github.com/badlogic/pimono/pull/304) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-1583 | Fixed | Model selector and listmodels with settings.json API keys: Models with API keys configured in settings.json (but not in environment variables) now properly appear in the /model selector and `listmodels` output. ([#295](https://github.com/badlogic/pimono/issues/295)) | CHANGELOG.md |
| G-PI-CHANGELOG-1584 | Fixed | API key priority: OAuth tokens now take priority over settings.json API keys. Previously, an API key in settings.json would trump OAuth, causing users logged in with a plan (unlimited tokens) to be billed via PAYG instead. | CHANGELOG.md |
| G-PI-CHANGELOG-1585 | Fixed | Thinking tag leakage: Fixed Claude mimicking literal `</thinking>` tags in responses. Unsigned thinking blocks (from aborted streams) are now converted to plain text without `<thinking>` tags. The TUI still displays them as thinking blocks. ([#302](https://github.com/badlogic/pimono/pull/302) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1586 | Added | Compaction hook improvements: The `before_compact` session event now includes: | CHANGELOG.md |
| G-PI-CHANGELOG-1587 | Added | `previousSummary`: Summary from the last compaction (if any), so hooks can preserve accumulated context | CHANGELOG.md |
| G-PI-CHANGELOG-1588 | Added | `messagesToKeep`: Messages that will be kept after the summary (recent turns), in addition to `messagesToSummarize` | CHANGELOG.md |
| G-PI-CHANGELOG-1589 | Added | `resolveApiKey`: Function to resolve API keys for any model (checks settings, OAuth, env vars) | CHANGELOG.md |
| G-PI-CHANGELOG-1590 | Added | Removed `apiKey` string in favor of `resolveApiKey` for more flexibility | CHANGELOG.md |
| G-PI-CHANGELOG-1591 | Added | SessionManager API cleanup: | CHANGELOG.md |
| G-PI-CHANGELOG-1592 | Added | Renamed `loadSessionFromEntries()` to `buildSessionContext()` (builds LLM context from entries, handling compaction) | CHANGELOG.md |
| G-PI-CHANGELOG-1593 | Added | Renamed `loadEntries()` to `getEntries()` (returns defensive copy of all session entries) | CHANGELOG.md |
| G-PI-CHANGELOG-1594 | Added | Added `buildSessionContext()` method to SessionManager | CHANGELOG.md |
| G-PI-CHANGELOG-1595 | Added | HTML export syntax highlighting: Code blocks in markdown and tool outputs (read, write) now have syntax highlighting using highlight.js with themeaware colors matching the TUI. | CHANGELOG.md |
| G-PI-CHANGELOG-1596 | Added | HTML export improvements: Render markdown serverside using marked (tables, headings, code blocks, etc.), honor user's chosen theme (light/dark), add image rendering for user messages, and style code blocks with TUIlike language markers. ([@scutifer](https://github.com/scutifer)) | CHANGELOG.md |
| G-PI-CHANGELOG-1597 | Fixed | Ghostty inline images in tmux: Fixed terminal detection for Ghostty when running inside tmux by checking `GHOSTTY_RESOURCES_DIR` env var. ([#299](https://github.com/badlogic/pimono/pull/299) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1598 | Fixed | Symlinked skill directories: Skills in symlinked directories (e.g., `~/.pi/agent/skills/myskills > /path/to/skills`) are now correctly discovered and loaded. | CHANGELOG.md |
| G-PI-CHANGELOG-1599 | Added | API keys in settings.json: Store API keys in `~/.pi/agent/settings.json` under the `apiKeys` field (e.g., `{ "apiKeys": { "anthropic": "sk..." } }`). Settings keys take priority over environment variables. ([#295](https://github.com/badlogic/pimono/issues/295)) | CHANGELOG.md |
| G-PI-CHANGELOG-1600 | Fixed | Allow startup without API keys: Interactive mode no longer throws when no API keys are configured. Users can now start the agent and use `/login` to authenticate. ([#288](https://github.com/badlogic/pimono/issues/288)) | CHANGELOG.md |
| G-PI-CHANGELOG-1601 | Fixed | `systemprompt` file path support: The `systemprompt` argument now correctly resolves file paths (like `appendsystemprompt` already did). ([#287](https://github.com/badlogic/pimono/pull/287) by [@scutifer](https://github.com/scutifer)) | CHANGELOG.md |
| G-PI-CHANGELOG-1602 | Added | Skip conversation restore on branch: Hooks can return `{ skipConversationRestore: true }` from `before_branch` to create the branched session file without restoring conversation messages. Useful for checkpoint hooks that restore files separately. ([#286](https://github.com/badlogic/pimono/pull/286) by [@nicobarray](https://github.com/nicobarray)) | CHANGELOG.md |
| G-PI-CHANGELOG-1603 | Fixed | Skill discovery performance: Skip `node_modules` directories when recursively scanning for skills. Fixes ~60ms startup delay when skill directories contain npm dependencies. | CHANGELOG.md |
| G-PI-CHANGELOG-1604 | Added | Startup timing instrumentation: Set `PI_TIMING=1` to see startup performance breakdown (interactive mode only). | CHANGELOG.md |
| G-PI-CHANGELOG-1605 | Breaking | Session hooks API redesign: Merged `branch` event into `session` event. `BranchEvent`, `BranchEventResult` types and `pi.on("branch", ...)` removed. Use `pi.on("session", ...)` with `reason: "before_branch" | "branch"` instead. `AgentSession.branch()` returns `{ cancelled }` instead of `{ skipped }`. `AgentSession.reset()` and `switchSession()` now return `boolean` (false if cancelled by hook). RPC commands `reset`, `switch_session`, and `branch` now include `cancelled` in response data. ([#278](https://github.com/badlogic/pimono/issues/278)) | CHANGELOG.md |
| G-PI-CHANGELOG-1606 | Added | Session lifecycle hooks: Added `before_` variants (`before_switch`, `before_clear`, `before_branch`) that fire before actions and can be cancelled with `{ cancel: true }`. Added `shutdown` reason for graceful exit handling. ([#278](https://github.com/badlogic/pimono/issues/278)) | CHANGELOG.md |
| G-PI-CHANGELOG-1607 | Fixed | File tab completion display: File paths no longer get cut off early. Folders now show trailing `/` and removed redundant "directory"/"file" labels to maximize horizontal space. ([#280](https://github.com/badlogic/pimono/issues/280)) | CHANGELOG.md |
| G-PI-CHANGELOG-1608 | Fixed | Bash tool visual line truncation: Fixed bash tool output in collapsed mode to use visual line counting (accounting for line wrapping) instead of logical line counting. Now consistent with bashexecution.ts behavior. Extracted shared `truncateToVisualLines` utility. ([#275](https://github.com/badlogic/pimono/issues/275)) | CHANGELOG.md |
| G-PI-CHANGELOG-1609 | Fixed | SDK tools respect cwd: Core tools (bash, read, edit, write, grep, find, ls) now properly use the `cwd` option from `createAgentSession()`. Added tool factory functions (`createBashTool`, `createReadTool`, etc.) for SDK users who specify custom `cwd` with explicit tools. ([#279](https://github.com/badlogic/pimono/issues/279)) | CHANGELOG.md |
| G-PI-CHANGELOG-1610 | Added | SDK for programmatic usage: New `createAgentSession()` factory with full control over model, tools, hooks, skills, session persistence, and settings. Philosophy: "omit to discover, provide to override". Includes 12 examples and comprehensive documentation. ([#272](https://github.com/badlogic/pimono/issues/272)) | CHANGELOG.md |
| G-PI-CHANGELOG-1611 | Added | Projectspecific settings: Settings now load from both `~/.pi/agent/settings.json` (global) and `<cwd>/.pi/settings.json` (project). Project settings override global with deep merge for nested objects. Project settings are readonly (for version control). ([#276](https://github.com/badlogic/pimono/pull/276)) | CHANGELOG.md |
| G-PI-CHANGELOG-1612 | Added | SettingsManager static factories: `SettingsManager.create(cwd?, agentDir?)` for filebased settings, `SettingsManager.inMemory(settings?)` for testing. Added `applyOverrides()` for programmatic overrides. | CHANGELOG.md |
| G-PI-CHANGELOG-1613 | Added | SessionManager static factories: `SessionManager.create()`, `SessionManager.open()`, `SessionManager.continueRecent()`, `SessionManager.inMemory()`, `SessionManager.list()` for flexible session management. | CHANGELOG.md |
| G-PI-CHANGELOG-1614 | Fixed | Syntax highlighting stderr spam: Fixed clihighlight logging errors to stderr when markdown contains malformed code fences (e.g., missing newlines around closing backticks). Now validates language identifiers before highlighting and falls back silently to plain text. ([#274](https://github.com/badlogic/pimono/issues/274)) | CHANGELOG.md |
| G-PI-CHANGELOG-1615 | Added | Gemini 3 preview models: Added `gemini3propreview` and `gemini3flashpreview` to the googlegeminicli provider. ([#264](https://github.com/badlogic/pimono/pull/264) by [@LukeFost](https://github.com/LukeFost)) | CHANGELOG.md |
| G-PI-CHANGELOG-1616 | Added | External editor support: Press `Ctrl+G` to edit your message in an external editor. Uses `$VISUAL` or `$EDITOR` environment variable. On successful save, the message is replaced; on cancel, the original is kept. ([#266](https://github.com/badlogic/pimono/pull/266) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1617 | Added | Process suspension: Press `Ctrl+Z` to suspend pi and return to the shell. Resume with `fg` as usual. ([#267](https://github.com/badlogic/pimono/pull/267) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1618 | Added | Configurable skills directories: Added granular control over skill sources with `enableCodexUser`, `enableClaudeUser`, `enableClaudeProject`, `enablePiUser`, `enablePiProject` toggles, plus `customDirectories` and `ignoredSkills` settings. ([#269](https://github.com/badlogic/pimono/pull/269) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1619 | Added | Skills CLI filtering: Added `skills <patterns>` flag for filtering skills with glob patterns. Also added `includeSkills` setting and glob pattern support for `ignoredSkills`. ([#268](https://github.com/badlogic/pimono/issues/268)) | CHANGELOG.md |
| G-PI-CHANGELOG-1620 | Fixed | Image shifting in tool output: Fixed an issue where images in tool output would shift down (due to accumulating spacers) each time the tool output was expanded or collapsed via Ctrl+O. | CHANGELOG.md |
| G-PI-CHANGELOG-1621 | Fixed | Gemini image reading broken: Fixed the `read` tool returning images causing flaky/broken responses with Gemini models. Images in tool results are now properly formatted per the Gemini API spec. | CHANGELOG.md |
| G-PI-CHANGELOG-1622 | Fixed | Tab completion for absolute paths: Fixed tab completion producing `//tmp` instead of `/tmp/`. Also fixed symlinks to directories (like `/tmp`) not getting a trailing slash, which prevented continuing to tab through subdirectories. | CHANGELOG.md |
| G-PI-CHANGELOG-1623 | Added | Interruptible tool execution: Queuing a message while tools are executing now interrupts the current tool batch. Remaining tools are skipped with an error result, and your queued message is processed immediately. Useful for redirecting the agent midtask. ([#259](https://github.com/badlogic/pimono/pull/259) by [@steipete](https://github.com/steipete)) | CHANGELOG.md |
| G-PI-CHANGELOG-1624 | Added | Google Gemini CLI OAuth provider: Access Gemini 2.0/2.5 models for free via Google Cloud Code Assist. Login with `/login` and select "Google Gemini CLI". Uses your Google account with rate limits. | CHANGELOG.md |
| G-PI-CHANGELOG-1625 | Added | Google Antigravity OAuth provider: Access Gemini 3, Claude (sonnet/opus thinking models), and GPTOSS models for free via Google's Antigravity sandbox. Login with `/login` and select "Antigravity". Uses your Google account with rate limits. | CHANGELOG.md |
| G-PI-CHANGELOG-1626 | Changed | Model selector respects models scope: The `/model` command now only shows models specified via `models` flag when that flag is used, instead of showing all available models. This prevents accidentally selecting models from unintended providers. ([#255](https://github.com/badlogic/pimono/issues/255)) | CHANGELOG.md |
| G-PI-CHANGELOG-1627 | Fixed | Connection errors not retried: Added "connection error" to the list of retryable errors so Anthropic connection drops trigger autoretry instead of silently failing. ([#252](https://github.com/badlogic/pimono/issues/252)) | CHANGELOG.md |
| G-PI-CHANGELOG-1628 | Fixed | Thinking level not clamped on model switch: Fixed TUI showing xhigh thinking level after switching to a model that doesn't support it. Thinking level is now automatically clamped to model capabilities. ([#253](https://github.com/badlogic/pimono/issues/253)) | CHANGELOG.md |
| G-PI-CHANGELOG-1629 | Fixed | Crossmodel thinking handoff: Fixed error when switching between models with different thinking signature formats (e.g., GPTOSS to Claude thinking models via Antigravity). Thinking blocks without signatures are now converted to text with `<thinking>` delimiters. | CHANGELOG.md |
| G-PI-CHANGELOG-1630 | Fixed | Input buffering in iTerm2: Fixed Ctrl+C, Ctrl+D, and other keys requiring multiple presses in iTerm2. The cell size query response parser was incorrectly holding back keyboard input. | CHANGELOG.md |
| G-PI-CHANGELOG-1631 | Fixed | Arrow keys and Enter in selector components: Fixed arrow keys and Enter not working in model selector, session selector, OAuth selector, and other selector components when Caps Lock or Num Lock is enabled. ([#243](https://github.com/badlogic/pimono/issues/243)) | CHANGELOG.md |
| G-PI-CHANGELOG-1632 | Fixed | Footer overflow on narrow terminals: Fixed footer path display exceeding terminal width when resizing to very narrow widths, causing rendering crashes. /arminsayshi | CHANGELOG.md |
| G-PI-CHANGELOG-1633 | Fixed | More Kitty keyboard protocol fixes: Fixed Backspace, Enter, Home, End, and Delete keys not working with Caps Lock enabled. The initial fix in 0.24.1 missed several key handlers that were still using raw byte detection. Now all key handlers use the helper functions that properly mask out lock key bits. ([#243](https://github.com/badlogic/pimono/issues/243)) | CHANGELOG.md |
| G-PI-CHANGELOG-1634 | Added | OAuth and model config exports: Scripts using `AgentSession` directly can now import `getAvailableModels`, `getApiKeyForModel`, `findModel`, `login`, `logout`, and `getOAuthProviders` from `@mariozechner/picodingagent` to reuse OAuth token storage and model resolution. ([#245](https://github.com/badlogic/pimono/issues/245)) | CHANGELOG.md |
| G-PI-CHANGELOG-1635 | Added | xhigh thinking level for gpt5.2 models: The thinking level selector and shift+tab cycling now show xhigh option for gpt5.2 and gpt5.2codex models (in addition to gpt5.1codexmax). ([#236](https://github.com/badlogic/pimono/pull/236) by [@theBucky](https://github.com/theBucky)) | CHANGELOG.md |
| G-PI-CHANGELOG-1636 | Fixed | Hooks wrap custom tools: Custom tools are now executed through the hook wrapper, so `tool_call`/`tool_result` hooks can observe, block, and modify custom tool executions (consistent with hook type docs). ([#248](https://github.com/badlogic/pimono/pull/248) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1637 | Fixed | Hook onUpdate callback forwarding: The `onUpdate` callback is now correctly forwarded through the hook wrapper, fixing custom tool progress updates. ([#238](https://github.com/badlogic/pimono/pull/238) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1638 | Fixed | Terminal cleanup on Ctrl+C in session selector: Fixed terminal not being properly restored when pressing Ctrl+C in the session selector. ([#247](https://github.com/badlogic/pimono/pull/247) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1639 | Fixed | OpenRouter models with colons in IDs: Fixed parsing of OpenRouter model IDs that contain colons (e.g., `openrouter:metallama/llama4scout:free`). ([#242](https://github.com/badlogic/pimono/pull/242) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1640 | Fixed | Global AGENTS.md loaded twice: Fixed global AGENTS.md being loaded twice when present in both `~/.pi/agent/` and the current directory. ([#239](https://github.com/badlogic/pimono/pull/239) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1641 | Fixed | Kitty keyboard protocol on Linux: Fixed keyboard input not working in Ghostty on Linux when Num Lock is enabled. The Kitty protocol includes Caps Lock and Num Lock state in modifier values, which broke key detection. Now correctly masks out lock key bits when matching keyboard shortcuts. ([#243](https://github.com/badlogic/pimono/issues/243)) | CHANGELOG.md |
| G-PI-CHANGELOG-1642 | Fixed | Emoji deletion and cursor movement: Backspace, Delete, and arrow keys now correctly handle multicodepoint characters like emojis. Previously, deleting an emoji would leave partial bytes, corrupting the editor state. ([#240](https://github.com/badlogic/pimono/issues/240)) | CHANGELOG.md |
| G-PI-CHANGELOG-1643 | Added | Subagent orchestration example: Added comprehensive custom tool example for spawning and orchestrating subagents with isolated context windows. Includes scout/planner/reviewer/worker agents and workflow commands for multiagent pipelines. ([#215](https://github.com/badlogic/pimono/pull/215) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1644 | Added | `getMarkdownTheme()` export: Custom tools can now import `getMarkdownTheme()` from `@mariozechner/picodingagent` to use the same markdown styling as the main UI. | CHANGELOG.md |
| G-PI-CHANGELOG-1645 | Added | `pi.exec()` signal and timeout support: Custom tools and hooks can now pass `{ signal, timeout }` options to `pi.exec()` for cancellation and timeout handling. The result includes a `killed` flag when the process was terminated. | CHANGELOG.md |
| G-PI-CHANGELOG-1646 | Added | Kitty keyboard protocol support: Shift+Enter, Alt+Enter, Shift+Tab, Ctrl+D, and all Ctrl+key combinations now work in Ghostty, Kitty, WezTerm, and other modern terminals. ([#225](https://github.com/badlogic/pimono/pull/225) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-1647 | Added | Dynamic API key refresh: OAuth tokens (GitHub Copilot, Anthropic OAuth) are now refreshed before each LLM call, preventing failures in longrunning agent loops where tokens expire midsession. ([#223](https://github.com/badlogic/pimono/pull/223) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-1648 | Added | `/hotkeys` command: Shows all keyboard shortcuts in a formatted table. | CHANGELOG.md |
| G-PI-CHANGELOG-1649 | Added | Markdown table borders: Tables now render with proper top and bottom borders. | CHANGELOG.md |
| G-PI-CHANGELOG-1650 | Changed | Subagent example improvements: Parallel mode now streams updates from all tasks. Chain mode shows all completed steps during streaming. Expanded view uses proper markdown rendering with syntax highlighting. Usage footer shows turn count. | CHANGELOG.md |
| G-PI-CHANGELOG-1651 | Changed | Skills standard compliance: Skills now adhere to the [Agent Skills standard](https://agentskills.io/specification). Validates name (must match parent directory, lowercase, max 64 chars), description (required, max 1024 chars), and frontmatter fields. Warns on violations but remains lenient. Prompt format changed to XML structure. Removed `{baseDir}` placeholder in favor of relative paths. ([#231](https://github.com/badlogic/pimono/issues/231)) | CHANGELOG.md |
| G-PI-CHANGELOG-1652 | Fixed | JSON mode stdout flush: Fixed race condition where `pi mode json` could exit before all output was written to stdout, causing consumers to miss final events. | CHANGELOG.md |
| G-PI-CHANGELOG-1653 | Fixed | Symlinked tools, hooks, and slash commands: Discovery now correctly follows symlinks when scanning for custom tools, hooks, and slash commands. ([#219](https://github.com/badlogic/pimono/pull/219), [#232](https://github.com/badlogic/pimono/pull/232) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-1654 | Breaking Changes | Custom tools now require `index.ts` entry point: Autodiscovered custom tools must be in a subdirectory with an `index.ts` file. The old pattern `~/.pi/agent/tools/mytool.ts` must become `~/.pi/agent/tools/mytool/index.ts`. This allows multifile tools to import helper modules. Explicit paths via `tool` or `settings.json` still work with any `.ts` file. | CHANGELOG.md |
| G-PI-CHANGELOG-1655 | Breaking Changes | Hook `tool_result` event restructured: The `ToolResultEvent` now exposes full tool result data instead of just text. ([#233](https://github.com/badlogic/pimono/pull/233)) | CHANGELOG.md |
| G-PI-CHANGELOG-1656 | Breaking Changes | Removed: `result: string` field | CHANGELOG.md |
| G-PI-CHANGELOG-1657 | Breaking Changes | Added: `content: (TextContent | ImageContent)[]`  full content array | CHANGELOG.md |
| G-PI-CHANGELOG-1658 | Breaking Changes | Added: `details: unknown`  toolspecific details (typed per tool via discriminated union on `toolName`) | CHANGELOG.md |
| G-PI-CHANGELOG-1659 | Breaking Changes | `ToolResultEventResult.result` renamed to `ToolResultEventResult.text` (removed), use `content` instead | CHANGELOG.md |
| G-PI-CHANGELOG-1660 | Breaking Changes | Hook handlers returning `{ result: "..." }` must change to `{ content: [{ type: "text", text: "..." }] }` | CHANGELOG.md |
| G-PI-CHANGELOG-1661 | Breaking Changes | Builtin tool details types exported: `BashToolDetails`, `ReadToolDetails`, `GrepToolDetails`, `FindToolDetails`, `LsToolDetails`, `TruncationResult` | CHANGELOG.md |
| G-PI-CHANGELOG-1662 | Breaking Changes | Type guards exported for narrowing: `isBashToolResult`, `isReadToolResult`, `isEditToolResult`, `isWriteToolResult`, `isGrepToolResult`, `isFindToolResult`, `isLsToolResult` | CHANGELOG.md |
| G-PI-CHANGELOG-1663 | Added | Syntax highlighting: Added syntax highlighting for markdown code blocks, read tool output, and write tool content. Uses clihighlight with themeaware color mapping and VS Codestyle syntax colors. ([#214](https://github.com/badlogic/pimono/pull/214) by [@svkozak](https://github.com/svkozak)) | CHANGELOG.md |
| G-PI-CHANGELOG-1664 | Added | Intraline diff highlighting: Edit tool now shows wordlevel changes with inverse highlighting when a single line is modified. Multiline changes show all removed lines first, then all added lines. | CHANGELOG.md |
| G-PI-CHANGELOG-1665 | Fixed | Gemini tool result format: Fixed tool result format for Gemini 3 Flash Preview which strictly requires `{ output: value }` for success and `{ error: value }` for errors. Previous format using `{ result, isError }` was rejected by newer Gemini models. ([#213](https://github.com/badlogic/pimono/issues/213), [#220](https://github.com/badlogic/pimono/pull/220)) | CHANGELOG.md |
| G-PI-CHANGELOG-1666 | Fixed | Google baseUrl configuration: Google provider now respects `baseUrl` configuration for custom endpoints or API proxies. ([#216](https://github.com/badlogic/pimono/issues/216), [#221](https://github.com/badlogic/pimono/pull/221) by [@theBucky](https://github.com/theBucky)) | CHANGELOG.md |
| G-PI-CHANGELOG-1667 | Fixed | Google provider FinishReason: Added handling for new `IMAGE_RECITATION` and `IMAGE_OTHER` finish reasons. Upgraded @google/genai to 1.34.0. | CHANGELOG.md |
| G-PI-CHANGELOG-1668 | Fixed | Check for compaction before submitting user prompt, not just after agent turn ends. This catches cases where user aborts midresponse and context is already near the limit. | CHANGELOG.md |
| G-PI-CHANGELOG-1669 | Changed | Improved system prompt documentation section with clearer pointers to specific doc files for custom models, themes, skills, hooks, custom tools, and RPC. | CHANGELOG.md |
| G-PI-CHANGELOG-1670 | Changed | Cleaned up documentation: | CHANGELOG.md |
| G-PI-CHANGELOG-1671 | Changed | `theme.md`: Added missing color tokens (`thinkingXhigh`, `bashMode`) | CHANGELOG.md |
| G-PI-CHANGELOG-1672 | Changed | `skills.md`: Rewrote with better framing and examples | CHANGELOG.md |
| G-PI-CHANGELOG-1673 | Changed | `hooks.md`: Fixed timeout/error handling docs, added import aliases section | CHANGELOG.md |
| G-PI-CHANGELOG-1674 | Changed | `customtools.md`: Added intro with use cases and comparison table | CHANGELOG.md |
| G-PI-CHANGELOG-1675 | Changed | `rpc.md`: Added missing `hook_error` event documentation | CHANGELOG.md |
| G-PI-CHANGELOG-1676 | Changed | `README.md`: Complete settings table, condensed philosophy section, standardized OAuth docs | CHANGELOG.md |
| G-PI-CHANGELOG-1677 | Changed | Hooks loader now supports same import aliases as custom tools (`@sinclair/typebox`, `@mariozechner/piai`, `@mariozechner/pitui`, `@mariozechner/picodingagent`). | CHANGELOG.md |
| G-PI-CHANGELOG-1678 | Breaking Changes | Hooks: `turn_end` event's `toolResults` type changed from `AppMessage[]` to `ToolResultMessage[]`. If you have hooks that handle `turn_end` events and explicitly type the results, update your type annotations. | CHANGELOG.md |
| G-PI-CHANGELOG-1679 | Fixed | Fixed Claude models via GitHub Copilot reanswering all previous prompts in multiturn conversations. The issue was that assistant message content was sent as an array instead of a string, which Copilot's Claude adapter misinterpreted. Also added missing `OpenaiIntent: conversationedits` header and fixed `XInitiator` logic to check for any assistant/tool message in history. ([#209](https://github.com/badlogic/pimono/issues/209)) | CHANGELOG.md |
| G-PI-CHANGELOG-1680 | Fixed | Detect image MIME type via file magic (read tool and `@file` attachments), not filename extension. | CHANGELOG.md |
| G-PI-CHANGELOG-1681 | Fixed | Fixed markdown tables overflowing terminal width. Tables now wrap cell contents to fit available width instead of breaking borders midrow. ([#206](https://github.com/badlogic/pimono/pull/206) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-1682 | Fixed | Fixed TUI performance regression caused by Box component lacking render caching. Builtin tools now use Text directly (like v0.22.5), and Box has proper caching for custom tool rendering. | CHANGELOG.md |
| G-PI-CHANGELOG-1683 | Fixed | Fixed custom tools failing to load from `~/.pi/agent/tools/` when pi is installed globally. Module imports (`@sinclair/typebox`, `@mariozechner/pitui`, `@mariozechner/piai`) are now resolved via aliases. | CHANGELOG.md |
| G-PI-CHANGELOG-1684 | Added | Custom tools: Extend pi with custom tools written in TypeScript. Tools can provide custom TUI rendering, interact with users via `pi.ui` (select, confirm, input, notify), and maintain state across sessions via `onSession` callback. See [docs/customtools.md](docs/customtools.md) and [examples/customtools/](examples/customtools/). ([#190](https://github.com/badlogic/pimono/issues/190)) | CHANGELOG.md |
| G-PI-CHANGELOG-1685 | Added | Hook and tool examples: Added `examples/hooks/` and `examples/customtools/` with working examples. Examples are now bundled in npm and binary releases. | CHANGELOG.md |
| G-PI-CHANGELOG-1686 | Breaking Changes | Hooks: Replaced `session_start` and `session_switch` events with unified `session` event. Use `event.reason` (`"start" | "switch" | "clear"`) to distinguish. Event now includes `entries` array for state reconstruction. | CHANGELOG.md |
| G-PI-CHANGELOG-1687 | Fixed | Fixed `session` flag not saving sessions in print mode (`p`). The session manager was never receiving events because no subscriber was attached. | CHANGELOG.md |
| G-PI-CHANGELOG-1688 | Added | `listmodels [search]` CLI flag to list available models with optional fuzzy search. Shows provider, model ID, context window, max output, thinking support, and image support. Only lists models with configured API keys. ([#203](https://github.com/badlogic/pimono/issues/203)) | CHANGELOG.md |
| G-PI-CHANGELOG-1689 | Fixed | Fixed tool execution showing green (success) background while still running. Now correctly shows gray (pending) background until the tool completes. | CHANGELOG.md |
| G-PI-CHANGELOG-1690 | Added | Streaming bash output: Bash tool now streams output in realtime during execution. The TUI displays live progress with the last 5 lines visible (expandable with ctrl+o). ([#44](https://github.com/badlogic/pimono/issues/44)) | CHANGELOG.md |
| G-PI-CHANGELOG-1691 | Changed | Tool output display: When collapsed, tool output now shows the last N lines instead of the first N lines, making streaming output more useful. | CHANGELOG.md |
| G-PI-CHANGELOG-1692 | Changed | Updated `@mariozechner/piai` with XInitiator header support for GitHub Copilot, ensuring agent calls are not deducted from quota. ([#200](https://github.com/badlogic/pimono/pull/200) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-1693 | Fixed | Fixed editor text being cleared during compaction. Text typed while compaction is running is now preserved. ([#179](https://github.com/badlogic/pimono/issues/179)) | CHANGELOG.md |
| G-PI-CHANGELOG-1694 | Fixed | Improved RGB to 256color mapping for terminals without truecolor support. Now correctly uses grayscale ramp for neutral colors and preserves semantic tints (green for success, red for error, blue for pending) instead of mapping everything to wrong cube colors. | CHANGELOG.md |
| G-PI-CHANGELOG-1695 | Fixed | `/think off` now actually disables thinking for all providers. Previously, providers like Gemini with "dynamic thinking" enabled by default would still use thinking even when turned off. ([#180](https://github.com/badlogic/pimono/pull/180) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-1696 | Changed | Updated `@mariozechner/piai` with interleaved thinking enabled by default for Anthropic Claude 4 models. | CHANGELOG.md |
| G-PI-CHANGELOG-1697 | Changed | Updated `@mariozechner/piai` with interleaved thinking support for Anthropic models. | CHANGELOG.md |
| G-PI-CHANGELOG-1698 | Added | GitHub Copilot support: Use GitHub Copilot models via OAuth login (`/login` > "GitHub Copilot"). Supports both github.com and GitHub Enterprise. Models are sourced from models.dev and include Claude, GPT, Gemini, Grok, and more. All models are automatically enabled after login. ([#191](https://github.com/badlogic/pimono/pull/191) by [@cau1k](https://github.com/cau1k)) | CHANGELOG.md |
| G-PI-CHANGELOG-1699 | Fixed | Model selector fuzzy search now matches against provider name (not just model ID) and supports spaceseparated tokens where all tokens must match | CHANGELOG.md |
| G-PI-CHANGELOG-1700 | Added | Inline image rendering: Terminals supporting Kitty graphics protocol (Kitty, Ghostty, WezTerm) or iTerm2 inline images now render images inline in tool output. Aspect ratio is preserved by querying terminal cell dimensions on startup. Toggle with `/showimages` command or `terminal.showImages` setting. Falls back to text placeholder on unsupported terminals or when disabled. ([#177](https://github.com/badlogic/pimono/pull/177) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1701 | Added | Gemini 3 Pro thinking levels: Thinking level selector now works with Gemini 3 Pro models. Minimal/low map to Google's LOW, medium/high map to Google's HIGH. ([#176](https://github.com/badlogic/pimono/pull/176) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-1702 | Fixed | Fixed read tool failing on macOS screenshot filenames due to Unicode Narrow NoBreak Space (U+202F) in timestamp. Added fallback to try macOS variant paths and consolidated duplicate expandPath functions into shared pathutils.ts. ([#181](https://github.com/badlogic/pimono/pull/181) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1703 | Fixed | Fixed double blank lines rendering after markdown code blocks ([#173](https://github.com/badlogic/pimono/pull/173) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-1704 | Added | Exported skills API: `loadSkillsFromDir`, `formatSkillsForPrompt`, and related types are now exported for use by other packages (e.g., mom). | CHANGELOG.md |
| G-PI-CHANGELOG-1705 | Breaking Changes | Pi skills now use `SKILL.md` convention: Pi skills must now be named `SKILL.md` inside a directory, matching Codex CLI format. Previously any `.md` file was treated as a skill. Migrate by renaming `~/.pi/agent/skills/foo.md` to `~/.pi/agent/skills/foo/SKILL.md`. | CHANGELOG.md |
| G-PI-CHANGELOG-1706 | Added | Display loaded skills on startup in interactive mode | CHANGELOG.md |
| G-PI-CHANGELOG-1707 | Fixed | Documentation: Added skills system documentation to README (setup, usage, CLI flags, settings) | CHANGELOG.md |
| G-PI-CHANGELOG-1708 | Added | Skills system: Autodiscover and load instruction files ondemand. Supports Claude Code (`~/.claude/skills//SKILL.md`), Codex CLI (`~/.codex/skills/`), and Pinative formats (`~/.pi/agent/skills/`, `.pi/skills/`). Skills are listed in system prompt with descriptions, agent loads them via read tool when needed. Supports `{baseDir}` placeholder. Disable with `noskills` or `skills.enabled: false` in settings. ([#169](https://github.com/badlogic/pimono/issues/169)) | CHANGELOG.md |
| G-PI-CHANGELOG-1709 | Added | Version flag: Added `version` / `v` flag to display the current version and exit. ([#170](https://github.com/badlogic/pimono/pull/170)) | CHANGELOG.md |
| G-PI-CHANGELOG-1710 | Added | Autoretry on transient errors: Automatically retries requests when providers return overloaded, rate limit, or server errors (429, 500, 502, 503, 504). Uses exponential backoff (2s, 4s, 8s). Shows retry status in TUI with option to cancel via Escape. Configurable in `settings.json` via `retry.enabled`, `retry.maxRetries`, `retry.baseDelayMs`. RPC mode emits `auto_retry_start` and `auto_retry_end` events. ([#157](https://github.com/badlogic/pimono/issues/157)) | CHANGELOG.md |
| G-PI-CHANGELOG-1711 | Added | HTML export line numbers: Read tool calls in HTML exports now display line number ranges (e.g., `file.txt:1020`) when offset/limit parameters are used, matching the TUI display format. Line numbers appear in yellow color for better visibility. ([#166](https://github.com/badlogic/pimono/issues/166)) | CHANGELOG.md |
| G-PI-CHANGELOG-1712 | Fixed | Branch selector now works with single message: Previously the branch selector would not open when there was only one user message. Now it correctly allows branching from any message, including the first one. This is needed for checkpoint hooks to restore state from before the first message. ([#163](https://github.com/badlogic/pimono/issues/163)) | CHANGELOG.md |
| G-PI-CHANGELOG-1713 | Fixed | Inmemory branching for `nosession` mode: Branching now works correctly in `nosession` mode without creating any session files. The conversation is truncated in memory. | CHANGELOG.md |
| G-PI-CHANGELOG-1714 | Fixed | Git branch indicator now works in subdirectories: The footer's git branch detection now walks up the directory hierarchy to find the git root, so it works when running pi from a subdirectory of a repository. ([#156](https://github.com/badlogic/pimono/issues/156)) | CHANGELOG.md |
| G-PI-CHANGELOG-1715 | Added | Mistral provider: Added support for Mistral AI models. Set `MISTRAL_API_KEY` environment variable to use. | CHANGELOG.md |
| G-PI-CHANGELOG-1716 | Fixed | Fixed print mode (`p`) not exiting after output when custom themes are present (theme watcher now properly stops in print mode) ([#161](https://github.com/badlogic/pimono/issues/161)) | CHANGELOG.md |
| G-PI-CHANGELOG-1717 | Added | Hooks system: TypeScript modules that extend agent behavior by subscribing to lifecycle events. Hooks can intercept tool calls, prompt for confirmation, modify results, and inject messages from external sources. Autodiscovered from `~/.pi/agent/hooks/.ts` and `.pi/hooks/.ts`. Thanks to [@nicobailon](https://github.com/nicobailon) for the collaboration on the design and implementation. ([#145](https://github.com/badlogic/pimono/issues/145), supersedes [#158](https://github.com/badlogic/pimono/pull/158)) | CHANGELOG.md |
| G-PI-CHANGELOG-1718 | Added | `pi.send()` API: Hooks can inject messages into the agent session from external sources (file watchers, webhooks, CI systems). If streaming, messages are queued; otherwise a new agent loop starts immediately. | CHANGELOG.md |
| G-PI-CHANGELOG-1719 | Added | `hook <path>` CLI flag: Load hook files directly for testing without modifying settings. | CHANGELOG.md |
| G-PI-CHANGELOG-1720 | Added | Hook events: `session_start`, `session_switch`, `agent_start`, `agent_end`, `turn_start`, `turn_end`, `tool_call` (can block), `tool_result` (can modify), `branch`. | CHANGELOG.md |
| G-PI-CHANGELOG-1721 | Added | Hook UI primitives: `ctx.ui.select()`, `ctx.ui.confirm()`, `ctx.ui.input()`, `ctx.ui.notify()` for interactive prompts from hooks. | CHANGELOG.md |
| G-PI-CHANGELOG-1722 | Added | Hooks documentation: Full API reference at `docs/hooks.md`, shipped with npm package. | CHANGELOG.md |
| G-PI-CHANGELOG-1723 | Changed | Simplified compaction flow: Removed proactive compaction (aborting midturn when threshold approached). Compaction now triggers in two cases only: (1) overflow error from LLM, which compacts and autoretries, or (2) threshold crossed after a successful turn, which compacts without retry. | CHANGELOG.md |
| G-PI-CHANGELOG-1724 | Changed | Compaction retry uses `Agent.continue()`: Autoretry after overflow now uses the new `continue()` API instead of resending the user message, preserving exact context state. | CHANGELOG.md |
| G-PI-CHANGELOG-1725 | Changed | Merged turn prefix summary: When a turn is split during compaction, the turn prefix summary is now merged into the main history summary instead of being stored separately. | CHANGELOG.md |
| G-PI-CHANGELOG-1726 | Added | `isCompacting` property on AgentSession: Check if autocompaction is currently running. | CHANGELOG.md |
| G-PI-CHANGELOG-1727 | Added | Session compaction indicator: When resuming a compacted session, displays "Session compacted N times" status message. | CHANGELOG.md |
| G-PI-CHANGELOG-1728 | Fixed | Block input during compaction: User input is now blocked while autocompaction is running to prevent race conditions. | CHANGELOG.md |
| G-PI-CHANGELOG-1729 | Fixed | Skip error messages in usage calculation: Context size estimation now skips both aborted and error messages, as neither have valid usage data. | CHANGELOG.md |
| G-PI-CHANGELOG-1730 | Breaking Changes | New RPC protocol: The RPC mode (`mode rpc`) has been completely redesigned with a new JSON protocol. The old protocol is no longer supported. See [`docs/rpc.md`](docs/rpc.md) for the new protocol documentation and [`test/rpcexample.ts`](test/rpcexample.ts) for a working example. Includes `RpcClient` TypeScript class for easy integration. ([#91](https://github.com/badlogic/pimono/issues/91)) | CHANGELOG.md |
| G-PI-CHANGELOG-1731 | Changed | README restructured: Reorganized documentation from 30+ flat sections into 10 logical groups. Converted verbose subsections to scannable tables. Consolidated philosophy sections. Reduced size by ~60% while preserving all information. | CHANGELOG.md |
| G-PI-CHANGELOG-1732 | Changed | Major code refactoring: Restructured codebase for better maintainability and separation of concerns. Moved files into organized directories (`core/`, `modes/`, `utils/`, `cli/`). Extracted `AgentSession` class as central session management abstraction. Split `main.ts` and `tuirenderer.ts` into focused modules. See `DEVELOPMENT.md` for the new code map. ([#153](https://github.com/badlogic/pimono/issues/153)) | CHANGELOG.md |
| G-PI-CHANGELOG-1733 | Added | `/debug` command now includes agent messages as JSONL in the output | CHANGELOG.md |
| G-PI-CHANGELOG-1734 | Fixed | Fix crash when bash command outputs binary data (e.g., `curl` downloading a video file) | CHANGELOG.md |
| G-PI-CHANGELOG-1735 | Fixed | Fix build errors with tsgo 7.0.0dev.20251208.1 by properly importing `ReasoningEffort` type | CHANGELOG.md |
| G-PI-CHANGELOG-1736 | Breaking Changes | Custom themes require new color tokens: Themes must now include `thinkingXhigh` and `bashMode` color tokens. The theme loader provides helpful error messages listing missing tokens. See builtin themes (dark.json, light.json) for reference values. | CHANGELOG.md |
| G-PI-CHANGELOG-1737 | Added | OpenAI compatibility overrides in models.json: Custom models using `openaicompletions` API can now specify a `compat` object to override provider quirks (`supportsStore`, `supportsDeveloperRole`, `supportsReasoningEffort`, `maxTokensField`). Useful for LiteLLM, custom proxies, and other nonstandard endpoints. ([#133](https://github.com/badlogic/pimono/issues/133), thanks @finkandreas for the initial idea and PR) | CHANGELOG.md |
| G-PI-CHANGELOG-1738 | Added | xhigh thinking level: Added `xhigh` thinking level for OpenAI codexmax models. Cycle through thinking levels with Shift+Tab; `xhigh` appears only when using a codexmax model. ([#143](https://github.com/badlogic/pimono/issues/143)) | CHANGELOG.md |
| G-PI-CHANGELOG-1739 | Added | Collapse changelog setting: Add `"collapseChangelog": true` to `~/.pi/agent/settings.json` to show a condensed "Updated to vX.Y.Z" message instead of the full changelog after updates. Use `/changelog` to view the full changelog. ([#148](https://github.com/badlogic/pimono/issues/148)) | CHANGELOG.md |
| G-PI-CHANGELOG-1740 | Added | Bash mode: Execute shell commands directly from the editor by prefixing with `!` (e.g., `!ls la`). Output streams in realtime, is added to the LLM context, and persists in session history. Supports multiline commands, cancellation (Escape), truncation for large outputs, and preview/expand toggle (Ctrl+O). Also available in RPC mode via `{"type":"bash","command":"..."}`. ([#112](https://github.com/badlogic/pimono/pull/112), original implementation by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-1741 | Changed | Tool output truncation: All tools now enforce consistent truncation limits with actionable notices for the LLM. ([#134](https://github.com/badlogic/pimono/issues/134)) | CHANGELOG.md |
| G-PI-CHANGELOG-1742 | Changed | Limits: 2000 lines OR 50KB (whichever hits first), never partial lines | CHANGELOG.md |
| G-PI-CHANGELOG-1743 | Changed | read: Shows `[Showing lines XY of Z. Use offset=N to continue]`. If first line exceeds 50KB, suggests bash command | CHANGELOG.md |
| G-PI-CHANGELOG-1744 | Changed | bash: Tail truncation with temp file. Shows `[Showing lines XY of Z. Full output: /tmp/...]` | CHANGELOG.md |
| G-PI-CHANGELOG-1745 | Changed | grep: Pretruncates match lines to 500 chars. Shows match limit and line truncation notices | CHANGELOG.md |
| G-PI-CHANGELOG-1746 | Changed | find/ls: Shows result/entry limit notices | CHANGELOG.md |
| G-PI-CHANGELOG-1747 | Changed | TUI displays truncation warnings in yellow at bottom of tool output (visible even when collapsed) | CHANGELOG.md |
| G-PI-CHANGELOG-1748 | Added | Flexible Windows shell configuration: The bash tool now supports multiple shell sources beyond Git Bash. Resolution order: (1) custom `shellPath` in settings.json, (2) Git Bash in standard locations, (3) any bash.exe on PATH. This enables Cygwin, MSYS2, and other bash environments. Configure with `~/.pi/agent/settings.json`: `{"shellPath": "C:\\cygwin64\\bin\\bash.exe"}`. | CHANGELOG.md |
| G-PI-CHANGELOG-1749 | Fixed | Windows binary detection: Fixed Bun compiled binary detection on Windows by checking for URLencoded `%7EBUN` in addition to `$bunfs` and `~BUN` in `import.meta.url`. This ensures the binary correctly locates supporting files (package.json, themes, etc.) next to the executable. | CHANGELOG.md |
| G-PI-CHANGELOG-1750 | Fixed | Editor crash with emojis/CJK characters: Fixed crash when pasting or typing text containing wide characters (emojis like ✅, CJK characters) that caused line width to exceed terminal width. The editor now uses graphemeaware text wrapping with proper visible width calculation. | CHANGELOG.md |
| G-PI-CHANGELOG-1751 | Added | DoubleEscape Branch Shortcut: Press Escape twice with an empty editor to quickly open the `/branch` selector for conversation branching. | CHANGELOG.md |
| G-PI-CHANGELOG-1752 | Changed | Faster startup: Version check now runs in parallel with TUI initialization instead of blocking startup for up to 1 second. Update notifications appear in chat when the check completes. | CHANGELOG.md |
| G-PI-CHANGELOG-1753 | Changed | Footer display: Token counts now use M suffix for millions (e.g., `10.2M` instead of `10184k`). Context display shortened from `61.3% of 200k` to `61.3%/200k`. | CHANGELOG.md |
| G-PI-CHANGELOG-1754 | Fixed | Multikey sequences in inputs: Inputs like model search now handle multikey sequences identically to the main prompt editor. ([#122](https://github.com/badlogic/pimono/pull/122) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-1755 | Fixed | Line wrapping escape codes: Fixed underline style bleeding into padding when wrapping long URLs. ANSI codes now attach to the correct content, and lineend resets only turn off underline (preserving background colors). ([#109](https://github.com/badlogic/pimono/issues/109)) | CHANGELOG.md |
| G-PI-CHANGELOG-1756 | Added | Fuzzy search models and sessions: Implemented a simple fuzzy search for models and sessions (e.g., `codexmax` now finds `gpt5.1codexmax`). ([#122](https://github.com/badlogic/pimono/pull/122) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-1757 | Added | Prompt History Navigation: Browse previously submitted prompts using Up/Down arrow keys when the editor is empty. Press Up to cycle through older prompts, Down to return to newer ones or clear the editor. Similar to shell history and Claude Code's prompt history feature. History is sessionscoped and stores up to 100 entries. ([#121](https://github.com/badlogic/pimono/pull/121) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-1758 | Added | `/resume` Command: Switch to a different session midconversation. Opens an interactive selector showing all available sessions. Equivalent to the `resume` CLI flag but can be used without restarting the agent. ([#117](https://github.com/badlogic/pimono/pull/117) by [@hewliyang](https://github.com/hewliyang)) | CHANGELOG.md |
| G-PI-CHANGELOG-1759 | Changed | Compaction UI: Simplified collapsed compaction indicator to show warningcolored text with token count instead of styled banner. Removed redundant success message after compaction. ([#108](https://github.com/badlogic/pimono/issues/108)) | CHANGELOG.md |
| G-PI-CHANGELOG-1760 | Fixed | Print mode error handling: `p` flag now outputs error messages and exits with code 1 when requests fail, instead of silently producing no output. | CHANGELOG.md |
| G-PI-CHANGELOG-1761 | Fixed | Branch selector crash: Fixed TUI crash when user messages contained Unicode characters (like `✔` or `›`) that caused line width to exceed terminal width. Now uses proper `truncateToWidth` instead of `substring`. | CHANGELOG.md |
| G-PI-CHANGELOG-1762 | Fixed | Bash output escape sequences: Fixed incomplete stripping of terminal escape sequences in bash tool output. `stripAnsi` misses some sequences like standalone String Terminator (`ESC \`), which could cause rendering issues when displaying captured TUI output. | CHANGELOG.md |
| G-PI-CHANGELOG-1763 | Fixed | Footer overflow crash: Fixed TUI crash when terminal width is too narrow for the footer stats line. The footer now truncates gracefully instead of overflowing. | CHANGELOG.md |
| G-PI-CHANGELOG-1764 | Added | `authHeader` option in models.json: Custom providers can set `"authHeader": true` to automatically add `Authorization: Bearer <apiKey>` header. Useful for providers that require explicit auth headers. ([#81](https://github.com/badlogic/pimono/issues/81)) | CHANGELOG.md |
| G-PI-CHANGELOG-1765 | Added | `appendsystemprompt` Flag: Append additional text or file contents to the system prompt. Supports both inline text and file paths. Complements `systemprompt` for layering custom instructions without replacing the base system prompt. ([#114](https://github.com/badlogic/pimono/pull/114) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-1766 | Added | Thinking Block Toggle: Added `Ctrl+T` shortcut to toggle visibility of LLM thinking blocks. When toggled off, shows a static "Thinking..." label instead of full content. Useful for reducing visual clutter during long conversations. ([#113](https://github.com/badlogic/pimono/pull/113) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-1767 | Added | Added `gpt5.1codexmax` model support | CHANGELOG.md |
| G-PI-CHANGELOG-1768 | Added | `/copy` Command: Copy the last agent message to clipboard. Works crossplatform (macOS, Windows, Linux). Useful for extracting text from rendered Markdown output. ([#105](https://github.com/badlogic/pimono/pull/105) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-1769 | [0.12.8] - 2025-12-04 | Fix: Use CTRL+O consistently for compaction expand shortcut (not CMD+O on Mac) | CHANGELOG.md |
| G-PI-CHANGELOG-1770 | Added | Context Compaction: Long sessions can now be compacted to reduce context usage while preserving recent conversation history. ([#92](https://github.com/badlogic/pimono/issues/92), [docs](https://github.com/badlogic/pimono/blob/main/packages/codingagent/README.md#contextcompaction)) | CHANGELOG.md |
| G-PI-CHANGELOG-1771 | Added | `/compact [instructions]`: Manually compact context with optional custom instructions for the summary | CHANGELOG.md |
| G-PI-CHANGELOG-1772 | Added | `/autocompact`: Toggle automatic compaction when context exceeds threshold | CHANGELOG.md |
| G-PI-CHANGELOG-1773 | Added | Compaction summarizes older messages while keeping recent messages (default 20k tokens) verbatim | CHANGELOG.md |
| G-PI-CHANGELOG-1774 | Added | Autocompaction triggers when context reaches `contextWindow  reserveTokens` (default 16k reserve) | CHANGELOG.md |
| G-PI-CHANGELOG-1775 | Added | Compacted sessions show a collapsible summary in the TUI (toggle with `o` key) | CHANGELOG.md |
| G-PI-CHANGELOG-1776 | Added | HTML exports include compaction summaries as collapsible sections | CHANGELOG.md |
| G-PI-CHANGELOG-1777 | Added | RPC mode supports `{"type":"compact"}` command and autocompaction (emits compaction events) | CHANGELOG.md |
| G-PI-CHANGELOG-1778 | Added | Branch Source Tracking: Branched sessions now store `branchedFrom` in the session header, containing the path to the original session file. Useful for tracing session lineage. | CHANGELOG.md |
| G-PI-CHANGELOG-1779 | Added | Forking/Rebranding Support: All branding (app name, config directory, environment variable names) is now configurable via `piConfig` in `package.json`. Forks can change `piConfig.name` and `piConfig.configDir` to rebrand the CLI without code changes. Affects CLI banner, help text, config paths, and error messages. ([#95](https://github.com/badlogic/pimono/pull/95)) | CHANGELOG.md |
| G-PI-CHANGELOG-1780 | Fixed | Bun Binary Detection: Fixed Bun compiled binary failing to start after Bun updated its virtual filesystem path format from `%7EBUN` to `$bunfs`. ([#95](https://github.com/badlogic/pimono/pull/95)) | CHANGELOG.md |
| G-PI-CHANGELOG-1781 | Added | RPC Termination Safeguard: When running as an RPC worker (stdin pipe detected), the CLI now exits immediately if the parent process terminates unexpectedly. Prevents orphaned RPC workers from persisting indefinitely and consuming system resources. | CHANGELOG.md |
| G-PI-CHANGELOG-1782 | Fixed | Rate limit handling: Anthropic rate limit errors now trigger automatic retry with exponential backoff (base 10s, max 5 retries). Previously these errors would abort the request immediately. | CHANGELOG.md |
| G-PI-CHANGELOG-1783 | Fixed | Usage tracking during retries: Retried requests now correctly accumulate token usage from all attempts, not just the final successful one. Fixes artificially low token counts when requests were retried. | CHANGELOG.md |
| G-PI-CHANGELOG-1784 | Changed | Removed support for gpt4.5preview and o3 models (not yet available) | CHANGELOG.md |
| G-PI-CHANGELOG-1785 | Added | Models: Added support for OpenAI's new models: | CHANGELOG.md |
| G-PI-CHANGELOG-1786 | Added | `gpt4.1` (128K context) | CHANGELOG.md |
| G-PI-CHANGELOG-1787 | Added | `gpt4.1mini` (128K context) | CHANGELOG.md |
| G-PI-CHANGELOG-1788 | Added | `gpt4.1nano` (128K context) | CHANGELOG.md |
| G-PI-CHANGELOG-1789 | Added | `o3` (200K context, reasoning model) | CHANGELOG.md |
| G-PI-CHANGELOG-1790 | Added | `o4mini` (200K context, reasoning model) | CHANGELOG.md |
| G-PI-CHANGELOG-1791 | Added | `p, print` Flag: Run in noninteractive batch mode. Processes input message or piped stdin without TUI, prints agent response directly to stdout. Ideal for scripting, piping, and CI/CD integration. Exits after first response. | CHANGELOG.md |
| G-PI-CHANGELOG-1792 | Added | `P, printstreaming` Flag: Like `p`, but streams response tokens as they arrive. Use `printstreaming nomarkdown` for raw unformatted output. | CHANGELOG.md |
| G-PI-CHANGELOG-1793 | Added | `printturn` Flag: Continue processing tool calls and agent turns until the agent naturally finishes or requires user input. Combine with `p` for complete multiturn conversations. | CHANGELOG.md |
| G-PI-CHANGELOG-1794 | Added | `nomarkdown` Flag: Output raw text without Markdown formatting. Useful when piping output to tools that expect plain text. | CHANGELOG.md |
| G-PI-CHANGELOG-1795 | Added | Streaming Print Mode: Added internal `printStreaming` option for streaming output in nonTUI mode. | CHANGELOG.md |
| G-PI-CHANGELOG-1796 | Added | RPC Mode `print` Command: Send `{"type":"print","content":"text"}` to get formatted print output via `print_output` events. | CHANGELOG.md |
| G-PI-CHANGELOG-1797 | Added | AutoSave in Print Mode: Print mode conversations are automatically saved to the session directory, allowing later resumption with `continue`. | CHANGELOG.md |
| G-PI-CHANGELOG-1798 | Added | Thinking level options: Added `thinkingoff`, `thinkingminimal`, `thinkinglow`, `thinkingmedium`, `thinkinghigh` flags for directly specifying thinking level without the selector UI. | CHANGELOG.md |
| G-PI-CHANGELOG-1799 | Changed | Simplified RPC Protocol: Replaced the `prompt` wrapper command with direct message objects. Send `{"role":"user","content":"text"}` instead of `{"type":"prompt","message":"text"}`. Better aligns with message format throughout the codebase. | CHANGELOG.md |
| G-PI-CHANGELOG-1800 | Changed | RPC Message Handling: Agent now processes raw message objects directly, with `timestamp` autopopulated if missing. | CHANGELOG.md |
| G-PI-CHANGELOG-1801 | Changed | Change Ctrl+I to Ctrl+P for model cycling shortcut to avoid collision with Tab key in some terminals | CHANGELOG.md |
| G-PI-CHANGELOG-1802 | Fixed | Absolute glob patterns (e.g., `/Users/foo//.ts`) are now handled correctly. Previously the leading `/` was being stripped, causing the pattern to be interpreted relative to the current directory. | CHANGELOG.md |
| G-PI-CHANGELOG-1803 | Fixed | Fix read path traversal vulnerability. Paths are now validated to prevent reading outside the working directory or its parents. The `read` tool can read from `cwd`, its ancestors (for config files), and all descendants. Symlinks are resolved before validation. | CHANGELOG.md |
| G-PI-CHANGELOG-1804 | Fixed | Fix `systemprompt <path>` allowing the path argument to be captured by the message collection, causing "file not found" errors. | CHANGELOG.md |
| G-PI-CHANGELOG-1805 | Fixed | Fixed fatal error "Cannot set properties of undefined (setting '0')" when editing empty files in the `edit` tool. | CHANGELOG.md |
| G-PI-CHANGELOG-1806 | Fixed | Simplified `edit` tool output: Shows only "Edited file.txt" for successful edits instead of verbose search/replace details. | CHANGELOG.md |
| G-PI-CHANGELOG-1807 | Fixed | Fixed fatal error in footer rendering when token counts contain NaN values due to missing usage data. | CHANGELOG.md |
| G-PI-CHANGELOG-1808 | Fixed | Fixed chat rendering crash when messages contain preformatted/styled text (e.g., thinking traces with gray italic styling). The markdown renderer now preserves existing ANSI escape codes when they appear before inline elements. | CHANGELOG.md |
| G-PI-CHANGELOG-1809 | Fixed | Fix file drop functionality for absolute paths | CHANGELOG.md |
| G-PI-CHANGELOG-1810 | Fixed | Fixed TUI crash when pasting content containing tab characters. Tabs are now converted to 4 spaces before insertion. | CHANGELOG.md |
| G-PI-CHANGELOG-1811 | Fixed | Fixed terminal corruption after exit when shell integration sequences (OSC 133) appeared in bash output. These sequences are now stripped along with other ANSI codes. | CHANGELOG.md |
| G-PI-CHANGELOG-1812 | Added | Added `fd` integration for file path autocompletion. Now uses `fd` for faster fuzzy file search | CHANGELOG.md |
| G-PI-CHANGELOG-1813 | Fixed | Fixed keyboard shortcuts Ctrl+A, Ctrl+E, Ctrl+K, Ctrl+U, Ctrl+W, and word navigation (Option+Arrow) not working in VS Code integrated terminal and some other terminal emulators | CHANGELOG.md |
| G-PI-CHANGELOG-1814 | Added | Filebased Slash Commands: Create custom reusable prompts as `.txt` files in `~/.pi/slashcommands/`. Files become `/filename` commands with firstline descriptions. Supports `{{selection}}` placeholder for referencing selected/attached content. | CHANGELOG.md |
| G-PI-CHANGELOG-1815 | Added | `/branch` Command: Create conversation branches from any previous user message. Opens a selector to pick a message, then creates a new session file starting from that point. Original message text is placed in the editor for modification. | CHANGELOG.md |
| G-PI-CHANGELOG-1816 | Added | Unified Content References: Both `@path` in messages and `file path` CLI arguments now use the same attachment system with consistent MIME type detection. | CHANGELOG.md |
| G-PI-CHANGELOG-1817 | Added | Drag & Drop Files: Drop files onto the terminal to attach them to your message. Supports multiple files and both text and image content. | CHANGELOG.md |
| G-PI-CHANGELOG-1818 | Changed | Model Selector with Search: The `/model` command now opens a searchable list. Type to filter models by name, use arrows to navigate, Enter to select. | CHANGELOG.md |
| G-PI-CHANGELOG-1819 | Changed | Improved File Autocomplete: File path completion after `@` now supports fuzzy matching and shows file/directory indicators. | CHANGELOG.md |
| G-PI-CHANGELOG-1820 | Changed | Session Selector with Search: The `resume` and `session` flags now open a searchable session list with fuzzy filtering. | CHANGELOG.md |
| G-PI-CHANGELOG-1821 | Changed | Attachment Display: Files added via `@path` are now shown as "Attached: filename" in the user message, separate from the prompt text. | CHANGELOG.md |
| G-PI-CHANGELOG-1822 | Changed | Tab Completion: Tab key now triggers file path autocompletion anywhere in the editor, not just after `@` symbol. | CHANGELOG.md |
| G-PI-CHANGELOG-1823 | Fixed | Fixed autocomplete zorder issue where dropdown could appear behind chat messages | CHANGELOG.md |
| G-PI-CHANGELOG-1824 | Fixed | Fixed cursor position when navigating through wrapped lines in the editor | CHANGELOG.md |
| G-PI-CHANGELOG-1825 | Fixed | Fixed attachment handling for continued sessions to preserve file references | CHANGELOG.md |
| G-PI-CHANGELOG-1826 | Changed | Show base64truncated indicator for large images in tool output | CHANGELOG.md |
| G-PI-CHANGELOG-1827 | Fixed | Fixed image dimensions not being read correctly from PNG/JPEG/GIF files | CHANGELOG.md |
| G-PI-CHANGELOG-1828 | Fixed | Fixed PDF images being incorrectly base64truncated in display | CHANGELOG.md |
| G-PI-CHANGELOG-1829 | Fixed | Allow reading files from ancestor directories (needed for monorepo configs) | CHANGELOG.md |
| G-PI-CHANGELOG-1830 | Added | Full multimodal support: attach images (PNG, JPEG, GIF, WebP) and PDFs to prompts using `@path` syntax or `file` flag | CHANGELOG.md |
| G-PI-CHANGELOG-1831 | Fixed | `@`references now handle special characters in file names (spaces, quotes, unicode) | CHANGELOG.md |
| G-PI-CHANGELOG-1832 | Fixed | Fixed cursor positioning issues with multibyte unicode characters in editor | CHANGELOG.md |
| G-PI-CHANGELOG-1833 | Fixed | Removed padding on first user message in TUI to improve visual consistency. | CHANGELOG.md |
| G-PI-CHANGELOG-1834 | Added | Added RPC mode (`rpc`) for programmatic integration. Accepts JSON commands on stdin, emits JSON events on stdout. See [RPC mode documentation](https://github.com/nicobailon/pimono/blob/main/packages/codingagent/README.md#rpcmode) for protocol details. | CHANGELOG.md |
| G-PI-CHANGELOG-1835 | Changed | Refactored internal architecture to support multiple frontends (TUI, RPC) with shared agent logic. | CHANGELOG.md |
| G-PI-CHANGELOG-1836 | Added | Added thinking level persistence. Default level stored in `~/.pi/settings.json`, restored on startup. Persession overrides saved in session files. | CHANGELOG.md |
| G-PI-CHANGELOG-1837 | Added | Added model cycling shortcut: `Ctrl+I` cycles through available models (or scoped models with `m` flag). | CHANGELOG.md |
| G-PI-CHANGELOG-1838 | Added | Added automatic retry with exponential backoff for transient API errors (network issues, 500s, overload). | CHANGELOG.md |
| G-PI-CHANGELOG-1839 | Added | Cumulative token usage now shown in footer (total tokens used across all messages in session). | CHANGELOG.md |
| G-PI-CHANGELOG-1840 | Added | Added `systemprompt` flag to override default system prompt with custom text or file contents. | CHANGELOG.md |
| G-PI-CHANGELOG-1841 | Added | Footer now shows estimated total cost in USD based on model pricing. | CHANGELOG.md |
| G-PI-CHANGELOG-1842 | Changed | Replaced `models` flag with `m/model` supporting multiple values. Specify models as `provider/model@thinking` (e.g., `anthropic/claudesonnet420250514@high`). Multiple `m` flags scope available models for the session. | CHANGELOG.md |
| G-PI-CHANGELOG-1843 | Changed | Thinking level border now persists visually after selector closes. | CHANGELOG.md |
| G-PI-CHANGELOG-1844 | Changed | Improved tool result display with collapsible output (default collapsed, expand with `Ctrl+O`). | CHANGELOG.md |
| G-PI-CHANGELOG-1845 | Added | Add custom model configuration via `~/.pi/models.json` | CHANGELOG.md |
| G-PI-CHANGELOG-1846 | Added | Interactive TUI with streaming responses | CHANGELOG.md |
| G-PI-CHANGELOG-1847 | Added | Conversation session management with `continue`, `resume`, and `session` flags | CHANGELOG.md |
| G-PI-CHANGELOG-1848 | Added | Multiline input support (Shift+Enter or Option+Enter for new lines) | CHANGELOG.md |
| G-PI-CHANGELOG-1849 | Added | Tool execution: `read`, `write`, `edit`, `bash`, `glob`, `grep`, `think` | CHANGELOG.md |
| G-PI-CHANGELOG-1850 | Added | Thinking mode support for Claude with visual indicator and `/thinking` selector | CHANGELOG.md |
| G-PI-CHANGELOG-1851 | Added | File path autocompletion with `@` prefix | CHANGELOG.md |
| G-PI-CHANGELOG-1852 | Added | Slash command autocompletion | CHANGELOG.md |
| G-PI-CHANGELOG-1853 | Added | `/export` command for HTML session export | CHANGELOG.md |
| G-PI-CHANGELOG-1854 | Added | `/model` command for runtime model switching | CHANGELOG.md |
| G-PI-CHANGELOG-1855 | Added | `/session` command for session statistics | CHANGELOG.md |
| G-PI-CHANGELOG-1856 | Added | Model provider support: Anthropic (Claude), OpenAI, Google (Gemini) | CHANGELOG.md |
| G-PI-CHANGELOG-1857 | Added | Git branch display in footer | CHANGELOG.md |
| G-PI-CHANGELOG-1858 | Added | Message queueing during streaming responses | CHANGELOG.md |
| G-PI-CHANGELOG-1859 | Added | OAuth integration for Gmail and Google Calendar access | CHANGELOG.md |
| G-PI-CHANGELOG-1860 | Added | HTML export with syntax highlighting and collapsible sections | CHANGELOG.md |
| G-PI-README-001 | Share your OSS coding agent sessions | [badlogicgames/pimono on Hugging Face](https://huggingface.co/datasets/badlogicgames/pimono) | README.md |
| G-PI-README-002 | Table of Contents | [Quick Start](#quickstart) | README.md |
| G-PI-README-003 | Table of Contents | [Providers & Models](#providersmodels) | README.md |
| G-PI-README-004 | Table of Contents | [Interactive Mode](#interactivemode) | README.md |
| G-PI-README-005 | Table of Contents | [Editor](#editor) | README.md |
| G-PI-README-006 | Table of Contents | [Commands](#commands) | README.md |
| G-PI-README-007 | Table of Contents | [Keyboard Shortcuts](#keyboardshortcuts) | README.md |
| G-PI-README-008 | Table of Contents | [Message Queue](#messagequeue) | README.md |
| G-PI-README-009 | Table of Contents | [Sessions](#sessions) | README.md |
| G-PI-README-010 | Table of Contents | [Branching](#branching) | README.md |
| G-PI-README-011 | Table of Contents | [Compaction](#compaction) | README.md |
| G-PI-README-012 | Table of Contents | [Settings](#settings) | README.md |
| G-PI-README-013 | Table of Contents | [Context Files](#contextfiles) | README.md |
| G-PI-README-014 | Table of Contents | [Customization](#customization) | README.md |
| G-PI-README-015 | Table of Contents | [Prompt Templates](#prompttemplates) | README.md |
| G-PI-README-016 | Table of Contents | [Skills](#skills) | README.md |
| G-PI-README-017 | Table of Contents | [Extensions](#extensions) | README.md |
| G-PI-README-018 | Table of Contents | [Themes](#themes) | README.md |
| G-PI-README-019 | Table of Contents | [Pi Packages](#pipackages) | README.md |
| G-PI-README-020 | Table of Contents | [Programmatic Usage](#programmaticusage) | README.md |
| G-PI-README-021 | Table of Contents | [Philosophy](#philosophy) | README.md |
| G-PI-README-022 | Table of Contents | [CLI Reference](#clireference) | README.md |
| G-PI-README-023 | Quick Start | Platform notes: [Windows](docs/windows.md) | [Termux (Android)](docs/termux.md) | [tmux](docs/tmux.md) | [Terminal setup](docs/terminalsetup.md) | [Shell aliases](docs/shellaliases.md) | README.md |
| G-PI-README-024 | Providers & Models | Subscriptions: | README.md |
| G-PI-README-025 | Providers & Models | Anthropic Claude Pro/Max | README.md |
| G-PI-README-026 | Providers & Models | OpenAI ChatGPT Plus/Pro (Codex) | README.md |
| G-PI-README-027 | Providers & Models | GitHub Copilot | README.md |
| G-PI-README-028 | Providers & Models | API keys: | README.md |
| G-PI-README-029 | Providers & Models | Anthropic | README.md |
| G-PI-README-030 | Providers & Models | OpenAI | README.md |
| G-PI-README-031 | Providers & Models | Azure OpenAI | README.md |
| G-PI-README-032 | Providers & Models | DeepSeek | README.md |
| G-PI-README-033 | Providers & Models | Google Gemini | README.md |
| G-PI-README-034 | Providers & Models | Google Vertex | README.md |
| G-PI-README-035 | Providers & Models | Amazon Bedrock | README.md |
| G-PI-README-036 | Providers & Models | Mistral | README.md |
| G-PI-README-037 | Providers & Models | Cerebras | README.md |
| G-PI-README-038 | Providers & Models | Cloudflare AI Gateway | README.md |
| G-PI-README-039 | Providers & Models | Cloudflare Workers AI | README.md |
| G-PI-README-040 | Providers & Models | OpenRouter | README.md |
| G-PI-README-041 | Providers & Models | Vercel AI Gateway | README.md |
| G-PI-README-042 | Providers & Models | OpenCode Zen | README.md |
| G-PI-README-043 | Providers & Models | OpenCode Go | README.md |
| G-PI-README-044 | Providers & Models | Hugging Face | README.md |
| G-PI-README-045 | Providers & Models | Fireworks | README.md |
| G-PI-README-046 | Providers & Models | Kimi For Coding | README.md |
| G-PI-README-047 | Providers & Models | MiniMax | README.md |
| G-PI-README-048 | Providers & Models | Xiaomi MiMo Token Plan | README.md |
| G-PI-README-049 | Providers & Models | Custom providers & models: Add providers via `~/.pi/agent/models.json` if they speak a supported API (OpenAI, Anthropic, Google). For custom APIs or OAuth, use extensions. See [docs/models.md](docs/models.md) and [docs/customprovider.md](docs/customprovider.md). | README.md |
| G-PI-README-050 | Interactive Mode | Startup header  Shows shortcuts (`/hotkeys` for all), loaded AGENTS.md files, prompt templates, skills, and extensions | README.md |
| G-PI-README-051 | Interactive Mode | Messages  Your messages, assistant responses, tool calls and results, notifications, errors, and extension UI | README.md |
| G-PI-README-052 | Interactive Mode | Editor  Where you type; border color indicates thinking level | README.md |
| G-PI-README-053 | Interactive Mode | Footer  Working directory, session name, total token/cache usage, cost, context usage, current model | README.md |
| G-PI-README-054 | Keyboard Shortcuts | Commonly used: | README.md |
| G-PI-README-055 | Message Queue | Enter queues a steering message, delivered after the current assistant turn finishes executing its tool calls | README.md |
| G-PI-README-056 | Message Queue | Alt+Enter queues a followup message, delivered only after the agent finishes all work | README.md |
| G-PI-README-057 | Message Queue | Escape aborts and restores queued messages to editor | README.md |
| G-PI-README-058 | Message Queue | Alt+Up retrieves queued messages back to editor | README.md |
| G-PI-README-059 | Branching | `/tree`  Navigate the session tree inplace. Select any previous point, continue from there, and switch between branches. All history preserved in a single file. | README.md |
| G-PI-README-060 | Branching | Search by typing, fold/unfold and jump between branches with Ctrl+←/Ctrl+→ or Alt+←/Alt+→, page with ←/→ | README.md |
| G-PI-README-061 | Branching | Filter modes (Ctrl+O): default → notools → useronly → labeledonly → all | README.md |
| G-PI-README-062 | Branching | Press Shift+L to label entries as bookmarks and Shift+T to toggle label timestamps | README.md |
| G-PI-README-063 | Branching | `/fork`  Create a new session file from a previous user message on the active branch. Opens a selector, copies the active path up to that point, and places the selected prompt in the editor for modification. | README.md |
| G-PI-README-064 | Branching | `/clone`  Duplicate the current active branch into a new session file at the current position. The new session keeps the full activepath history and opens with an empty editor. | README.md |
| G-PI-README-065 | Branching | `fork <path|id>`  Fork an existing session file or partial session UUID directly from the CLI. This copies the full source session into a new session file in the current project. | README.md |
| G-PI-README-066 | Compaction | Manual: `/compact` or `/compact <custom instructions>` | README.md |
| G-PI-README-067 | Compaction | Automatic: Enabled by default. Triggers on context overflow (recovers and retries) or when approaching the limit (proactive). Configure via `/settings` or `settings.json`. | README.md |
| G-PI-README-068 | Telemetry and update checks | Update check: fetches `https://pi.dev/api/latestversion` to check whether a newer Pi version exists. Disable it with `PI_SKIP_VERSION_CHECK=1`. Disabling update checks only turns off this check. | README.md |
| G-PI-README-069 | Telemetry and update checks | Install/update telemetry: after first install or a changelogdetected update, sends an anonymous version ping to `https://pi.dev/api/reportinstall`. Opt out by setting `enableInstallTelemetry` to `false` in `settings.json`, or by setting `PI_TELEMETRY=0`. This does not disable update checks; Pi may still contact `pi.dev` for the latest version unless update checks are disabled or offline mode is enabled. | README.md |
| G-PI-README-070 | Context Files | `~/.pi/agent/AGENTS.md` (global) | README.md |
| G-PI-README-071 | Context Files | Parent directories (walking up from cwd) | README.md |
| G-PI-README-072 | Context Files | Current directory | README.md |
| G-PI-README-073 | Extensions | What's possible: | README.md |
| G-PI-README-074 | Extensions | Custom tools (or replace builtin tools entirely) | README.md |
| G-PI-README-075 | Extensions | Subagents and plan mode | README.md |
| G-PI-README-076 | Extensions | Custom compaction and summarization | README.md |
| G-PI-README-077 | Extensions | Permission gates and path protection | README.md |
| G-PI-README-078 | Extensions | Custom editors and UI components | README.md |
| G-PI-README-079 | Extensions | Status lines, headers, footers | README.md |
| G-PI-README-080 | Extensions | Git checkpointing and autocommit | README.md |
| G-PI-README-081 | Extensions | SSH and sandbox execution | README.md |
| G-PI-README-082 | Extensions | MCP server integration | README.md |
| G-PI-README-083 | Extensions | Make pi look like Claude Code | README.md |
| G-PI-README-084 | Extensions | Games while waiting (yes, Doom runs) | README.md |
| G-PI-README-085 | Extensions | ...anything you can dream up | README.md |
| G-PI-README-086 | Philosophy | No MCP. Build CLI tools with READMEs (see [Skills](#skills)), or build an extension that adds MCP support. [Why?](https://mariozechner.at/posts/20251102whatifyoudontneedmcp/) | README.md |
| G-PI-README-087 | Philosophy | No subagents. There's many ways to do this. Spawn pi instances via tmux, or build your own with [extensions](#extensions), or install a package that does it your way. | README.md |
| G-PI-README-088 | Philosophy | No permission popups. Run in a container, or build your own confirmation flow with [extensions](#extensions) inline with your environment and security requirements. | README.md |
| G-PI-README-089 | Philosophy | No plan mode. Write plans to files, or build it with [extensions](#extensions), or install a package. | README.md |
| G-PI-README-090 | Philosophy | No builtin todos. They confuse models. Use a TODO.md file, or build your own with [extensions](#extensions). | README.md |
| G-PI-README-091 | Philosophy | No background bash. Use tmux. Full observability, direct interaction. | README.md |
| G-PI-README-092 | See Also | [@mariozechner/piai](https://www.npmjs.com/package/@mariozechner/piai): Core LLM toolkit | README.md |
| G-PI-README-093 | See Also | [@mariozechner/piagentcore](https://www.npmjs.com/package/@mariozechner/piagentcore): Agent framework | README.md |
| G-PI-README-094 | See Also | [@mariozechner/pitui](https://www.npmjs.com/package/@mariozechner/pitui): Terminal UI components | README.md |
| G-PI-CHANGELOG-001 | Fixed | Fixed `ProcessTerminal` to fall back to `COLUMNS` and `LINES` before defaulting to 80x24 dimensions ([#4004](https://github.com/badlogic/pimono/issues/4004)) | CHANGELOG.md |
| G-PI-CHANGELOG-002 | Fixed | Fixed editor rendering artifacts for Thai Sara Am and Lao AM vowel characters ([#3904](https://github.com/badlogic/pimono/issues/3904)) | CHANGELOG.md |
| G-PI-CHANGELOG-003 | Fixed | Fixed duplicate printable characters from Kitty keyboard protocol CSIu plus raw character input on layouts such as Italian ([#3780](https://github.com/badlogic/pimono/issues/3780)) | CHANGELOG.md |
| G-PI-CHANGELOG-004 | Fixed | Fixed CSIu Ctrl+letter decoding inside bracketed paste, so pasted modifiedkey escape sequences no longer become literal editor text ([#3623](https://github.com/badlogic/pimono/pull/3623) by [@Exrun94](https://github.com/Exrun94)) | CHANGELOG.md |
| G-PI-CHANGELOG-005 | Fixed | Kept OSC 9;4 terminal progress alive with periodic updates so Ghostty does not clear the indicator during longrunning agent work ([#3610](https://github.com/badlogic/pimono/issues/3610)) | CHANGELOG.md |
| G-PI-CHANGELOG-006 | Added | Added `setProgress(active: boolean)` to the `Terminal` interface for OSC 9;4 progress indicator support | CHANGELOG.md |
| G-PI-CHANGELOG-007 | Added | Added generic stacked autocomplete support for extension wrappers via `AutocompleteProvider.shouldTriggerFileCompletion?()` and `#` as a natural autocomplete trigger alongside `@` ([#2983](https://github.com/badlogic/pimono/issues/2983)) | CHANGELOG.md |
| G-PI-CHANGELOG-008 | Fixed | Fixed `@` autocomplete fuzzy search to follow symlinked directories and include symlinked paths in results ([#3507](https://github.com/badlogic/pimono/issues/3507)) | CHANGELOG.md |
| G-PI-CHANGELOG-009 | Added | Added `LoaderIndicatorOptions` and `Loader.setIndicator()` support for custom loader frames and animation intervals, allowing TUI consumers to use animated, static, or hidden loader indicators ([#3413](https://github.com/badlogic/pimono/issues/3413)) | CHANGELOG.md |
| G-PI-CHANGELOG-010 | Fixed | Fixed `@` autocomplete fuzzy search to stop matching against the full base path for plain queries, so worktree or cwd paths containing the query text no longer crowd out real results such as `@plan` suggestions ([#2778](https://github.com/badlogic/pimono/issues/2778)) | CHANGELOG.md |
| G-PI-CHANGELOG-011 | Fixed | Fixed xterm `modifyOtherKeys` printable input so shifted uppercase letters insert correctly in the editor and shifted letter bindings parse and match consistently ([#3436](https://github.com/badlogic/pimono/issues/3436)) | CHANGELOG.md |
| G-PI-CHANGELOG-012 | Added | Added OSC 8 hyperlink rendering for markdown links when the terminal advertises support. Introduces a public `hyperlink(text, url)` helper and a `setCapabilities()` test override in `packages/tui` ([#3248](https://github.com/badlogic/pimono/pull/3248) by [@ofa1](https://github.com/ofa1)). | CHANGELOG.md |
| G-PI-CHANGELOG-013 | Added | Added `argumentHint` to `SlashCommand` interface, displayed before the description in the autocomplete dropdown ([#2780](https://github.com/badlogic/pimono/pull/2780) by [@andresvi94](https://github.com/andresvi94)) | CHANGELOG.md |
| G-PI-CHANGELOG-014 | Changed | Tightened `detectCapabilities()` to default `hyperlinks: false` for unknown terminals and to force `hyperlinks: false` under tmux/screen (including nested sessions where the outer terminal would otherwise advertise OSC 8). Prevents markdown link URLs from disappearing on terminals that silently swallow OSC 8 sequences ([#3248](https://github.com/badlogic/pimono/pull/3248)). | CHANGELOG.md |
| G-PI-CHANGELOG-015 | Fixed | Fixed Zellij `Shift+Enter` regressions by reverting the Zellijspecific Kitty keyboard query bypass and restoring the previous keyboard negotiation behavior ([#3259](https://github.com/badlogic/pimono/issues/3259)) | CHANGELOG.md |
| G-PI-CHANGELOG-016 | Fixed | Fixed markdown strikethrough parsing to require strict doubletilde delimiters (`~~text~~`) with nonwhitespace boundaries, preventing accidental strikethrough from loose tilde usage. | CHANGELOG.md |
| G-PI-CHANGELOG-017 | Added | Added full helper support for Kitty `super`modified shortcuts, including combinations such as `super+k`, `super+enter`, and `ctrl+super+k` ([#2979](https://github.com/badlogic/pimono/issues/2979)) | CHANGELOG.md |
| G-PI-CHANGELOG-018 | Fixed | Fixed Ctrl+Alt letter key matching in tmux by falling through from legacy ESCprefixed handling to CSIu and xterm `modifyOtherKeys` parsing when the legacy form does not match ([#2989](https://github.com/badlogic/pimono/pull/2989) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-019 | Fixed | Fixed `Container.render()` stack overflow on long sessions by replacing `Array.push(...spread)` with a loopbased push, preventing `RangeError: Maximum call stack size exceeded` when child output exceeds the V8 call stack argument limit ([#2651](https://github.com/badlogic/pimono/issues/2651)) | CHANGELOG.md |
| G-PI-CHANGELOG-020 | Fixed | Fixed editor stickycolumn tracking around paste markers so vertical cursor navigation restores the column from before the cursor entered a paste marker instead of jumping inside or past pasted content ([#3092](https://github.com/badlogic/pimono/pull/3092) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-021 | Fixed | Fixed TUI test suite failures caused by render throttle scheduling: added `VirtualTerminal.waitForRender()` helper that waits for the 16ms throttled render pipeline to settle before asserting viewport state ([#3076](https://github.com/badlogic/pimono/pull/3076) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-022 | Fixed | Fixed render scheduling under heavy streaming output by coalescing `requestRender()` calls to a 16ms frame budget while preserving immediate `requestRender(true)` behavior. | CHANGELOG.md |
| G-PI-CHANGELOG-023 | Fixed | Fixed markdown H1 headings ending with inline code from leaking underline styling into trailing line padding | CHANGELOG.md |
| G-PI-CHANGELOG-024 | Fixed | Fixed slashcommand argument autocomplete to await async `getArgumentCompletions()` results and ignore invalid return values, preventing crashes when extension commands provide asynchronous completions ([#2719](https://github.com/badlogic/pimono/issues/2719)) | CHANGELOG.md |
| G-PI-CHANGELOG-025 | Fixed | Fixed noncapturing overlay padding from inflating scrollback and corrupting the viewport on terminal widen ([#2758](https://github.com/badlogic/pimono/pull/2758) by [@dotBeeps](https://github.com/dotBeeps)) | CHANGELOG.md |
| G-PI-CHANGELOG-026 | Fixed | Fixed TUI cell size response handling to consume only exact `CSI 6 ; height ; width t` replies, so bare `Escape` is no longer swallowed while waiting for terminal image metadata ([#2661](https://github.com/badlogic/pimono/issues/2661)) | CHANGELOG.md |
| G-PI-CHANGELOG-027 | Fixed | Fixed Kitty keyboard protocol keypad functional keys to normalize to logical digits, symbols, and navigation keys, so numpad input in terminals such as iTerm2 no longer inserts Private Use Area gibberish or gets ignored ([#2650](https://github.com/badlogic/pimono/issues/2650)) | CHANGELOG.md |
| G-PI-CHANGELOG-028 | Added | Added support for `PI_TUI_WRITE_LOG` directory paths, creating a unique log file (`tui<timestamp><pid>.log`) per instance for easier debugging of multiple pi sessions ([#2508](https://github.com/badlogic/pimono/pull/2508) by [@mrexodia](https://github.com/mrexodia)) | CHANGELOG.md |
| G-PI-CHANGELOG-029 | Fixed | Fixed blockquote text color breaking after inline links (and other inline elements) due to missing style restoration prefix | CHANGELOG.md |
| G-PI-CHANGELOG-030 | Fixed | Fixed slashcommand Tab completion from immediately chaining into argument autocomplete after completing the command name, restoring flows like `/model` that submit into a selector dialog ([#2577](https://github.com/badlogic/pimono/issues/2577)) | CHANGELOG.md |
| G-PI-CHANGELOG-031 | Fixed | Fixed stale content and incorrect viewport tracking after TUI content shrinks or transient components inflate the working area ([#2126](https://github.com/badlogic/pimono/pull/2126) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-032 | Fixed | Fixed `@` autocomplete to debounce editortriggered searches, cancel inflight `fd` lookups cleanly, and keep suggestions visible while results refresh ([#1278](https://github.com/badlogic/pimono/issues/1278)) | CHANGELOG.md |
| G-PI-CHANGELOG-033 | Fixed | Fixed `truncateToWidth()` to stream truncation for very large strings, keep contiguous prefixes, and always terminate truncated SGR styling safely ([#2447](https://github.com/badlogic/pimono/issues/2447)) | CHANGELOG.md |
| G-PI-CHANGELOG-034 | Fixed | Fixed markdown heading styling being lost after inline code spans within headings | CHANGELOG.md |
| G-PI-CHANGELOG-035 | Fixed | Fixed shared keybinding resolution to stop user overrides from evicting unrelated default shortcuts such as selector confirm and editor cursor keys ([#2455](https://github.com/badlogic/pimono/issues/2455)) | CHANGELOG.md |
| G-PI-CHANGELOG-036 | Fixed | Fixed Termux software keyboard height changes from forcing fullscreen redraws and replaying TUI history on every toggle ([#2467](https://github.com/badlogic/pimono/issues/2467)) | CHANGELOG.md |
| G-PI-CHANGELOG-037 | Breaking Changes | Replaced the editoronly keybinding store with a single global keybindings manager in `@mariozechner/pitui`. TUI keybinding ids are now namespaced: `cursorUp` > `tui.editor.cursorUp`, `cursorDown` > `tui.editor.cursorDown`, `cursorLeft` > `tui.editor.cursorLeft`, `cursorRight` > `tui.editor.cursorRight`, `cursorWordLeft` > `tui.editor.cursorWordLeft`, `cursorWordRight` > `tui.editor.cursorWordRight`, `cursorLineStart` > `tui.editor.cursorLineStart`, `cursorLineEnd` > `tui.editor.cursorLineEnd`, `jumpForward` > `tui.editor.jumpForward`, `jumpBackward` > `tui.editor.jumpBackward`, `pageUp` > `tui.editor.pageUp`, `pageDown` > `tui.editor.pageDown`, `deleteCharBackward` > `tui.editor.deleteCharBackward`, `deleteCharForward` > `tui.editor.deleteCharForward`, `deleteWordBackward` > `tui.editor.deleteWordBackward`, `deleteWordForward` > `tui.editor.deleteWordForward`, `deleteToLineStart` > `tui.editor.deleteToLineStart`, `deleteToLineEnd` > `tui.editor.deleteToLineEnd`, `yank` > `tui.editor.yank`, `yankPop` > `tui.editor.yankPop`, `undo` > `tui.editor.undo`, `newLine` > `tui.input.newLine`, `submit` > `tui.input.submit`, `tab` > `tui.input.tab`, `copy` > `tui.input.copy`, `selectUp` > `tui.select.up`, `selectDown` > `tui.select.down`, `selectPageUp` > `tui.select.pageUp`, `selectPageDown` > `tui.select.pageDown`, `selectConfirm` > `tui.select.confirm`, `selectCancel` > `tui.select.cancel`. `keybindings.json` stays backward compatible because each keybinding definition maps the new internal id back to the existing public config key. Apps extend `interface Keybindings` via declaration merging, create one manager with both TUI and app definitions, then install it with `setKeybindings(...)` ([#2391](https://github.com/badlogic/pimono/issues/2391)) | CHANGELOG.md |
| G-PI-CHANGELOG-038 | Fixed | Fixed userdefined keybindings to shadow conflicting default bindings across the shared registry, so applevel defaults no longer stay active when the same key is explicitly reassigned ([#2391](https://github.com/badlogic/pimono/issues/2391)) | CHANGELOG.md |
| G-PI-CHANGELOG-039 | Fixed | Fixed tmux xterm `modifyOtherKeys` matching for `Backspace`, `Escape`, and `Space`, and resolved raw `\x08` backspace ambiguity by treating Windows Terminal sessions differently from legacy terminals ([#2293](https://github.com/badlogic/pimono/issues/2293)) | CHANGELOG.md |
| G-PI-CHANGELOG-040 | Added | Added configurable `SelectList` primary column sizing via `SelectListLayoutOptions`, including custom primarylabel truncation hooks ([#2154](https://github.com/badlogic/pimono/pull/2154) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-041 | Fixed | Fixed stale scrollback remaining after fullscreen redraws such as session switches by clearing the screen before wiping scrollback ([#2155](https://github.com/badlogic/pimono/pull/2155) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-042 | Fixed | Fixed trailing blank lines after markdown block elements when they are followed immediately by the next block or end of document ([#2152](https://github.com/badlogic/pimono/pull/2152) by [@markusylisiurunen](https://github.com/markusylisiurunen)) | CHANGELOG.md |
| G-PI-CHANGELOG-043 | Fixed | Fixed Windows shell and path handling in autocomplete to properly handle drive letters and mixed path separators | CHANGELOG.md |
| G-PI-CHANGELOG-044 | Fixed | Fixed editor paste to preserve literal content instead of normalizing newlines, preventing content corruption for text with embedded escape sequences ([#2064](https://github.com/badlogic/pimono/issues/2064)) | CHANGELOG.md |
| G-PI-CHANGELOG-045 | Fixed | Fixed tab completion to preserve `./` prefix when completing relative paths ([#2087](https://github.com/badlogic/pimono/issues/2087)) | CHANGELOG.md |
| G-PI-CHANGELOG-046 | Fixed | Fixed `ctrl+backspace` being indistinguishable from plain `backspace` on Windows Terminal. `0x08` is now recognized as `ctrl+backspace` instead of `backspace`, making `ctrl+backspace` bindable on terminals where it produces a distinct byte ([#2139](https://github.com/badlogic/pimono/issues/2139)) | CHANGELOG.md |
| G-PI-CHANGELOG-047 | Added | Added paste marker atomic segment handling in editor, treating paste markers as indivisible units during word wrapping and cursor navigation ([#2111](https://github.com/badlogic/pimono/pull/2111) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-048 | Fixed | Fixed `Input` horizontal scrolling for wide Unicode text (CJK, fullwidth characters) to use visual column width and strict slice boundaries, preventing rendered line overflow and TUI crashes ([#1982](https://github.com/badlogic/pimono/issues/1982)) | CHANGELOG.md |
| G-PI-CHANGELOG-049 | Fixed | Fixed xterm `modifyOtherKeys` handling for `Tab` in `matchesKey()`, restoring `shift+tab` and other modified Tab bindings in tmux when `extendedkeysformat` is left at the default `xterm` | CHANGELOG.md |
| G-PI-CHANGELOG-050 | Fixed | Fixed editor scroll indicator rendering crash in narrow terminal widths ([#2103](https://github.com/badlogic/pimono/pull/2103) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-051 | Fixed | Fixed tab characters in editor `setText()` and input paths not being normalized to spaces ([#2027](https://github.com/badlogic/pimono/pull/2027) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-052 | Fixed | Fixed `wordWrapLine` overflow when wide characters (CJK, fullwidth) fall exactly at the wrap boundary ([#2082](https://github.com/badlogic/pimono/pull/2082) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-053 | Fixed | Fixed tab characters in `Input` paste not being normalized to spaces ([#1975](https://github.com/badlogic/pimono/pull/1975) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-054 | Added | Added `treeFoldOrUp` and `treeUnfoldOrDown` editor actions with default bindings for `Ctrl+←`/`Ctrl+→` and `Alt+←`/`Alt+→` ([#1724](https://github.com/badlogic/pimono/pull/1724) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-055 | Added | Added digit keys (`09`) to the keybinding system, including Kitty CSIu and xterm `modifyOtherKeys` support for bindings like `ctrl+1` ([#1905](https://github.com/badlogic/pimono/issues/1905)) | CHANGELOG.md |
| G-PI-CHANGELOG-056 | Fixed | Fixed autocomplete selection ignoring typed text: highlight now follows the first prefix match as the user types, and exact matches are always selected on Enter ([#1931](https://github.com/badlogic/pimono/pull/1931) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-057 | Fixed | Fixed xterm `modifyOtherKeys` parsing in `matchesKey()` and `parseKey()`, restoring Ctrlbased keybindings and modified Enter keys in tmux when `extendedkeysformat` is left at the default `xterm` ([#1872](https://github.com/badlogic/pimono/issues/1872)) | CHANGELOG.md |
| G-PI-CHANGELOG-058 | Fixed | Fixed slashcommand Tab completion to immediately open argument completions when available ([#1481](https://github.com/badlogic/pimono/pull/1481) by [@barapa](https://github.com/barapa)) | CHANGELOG.md |
| G-PI-CHANGELOG-059 | Added | Added noncapturing overlays via `OverlayOptions.nonCapturing` and new `OverlayHandle` methods: `focus()`, `unfocus()`, and `isFocused()` for programmatic overlay focus control ([#1916](https://github.com/badlogic/pimono/pull/1916) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-060 | Changed | Overlay compositing order now uses focus order so focused overlays render on top while preserving stack semantics for show/hide behavior ([#1916](https://github.com/badlogic/pimono/pull/1916) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-061 | Fixed | Fixed automatic focus restoration to skip noncapturing overlays and fixed `hideOverlay()` to only reassign focus when the popped overlay had focus ([#1916](https://github.com/badlogic/pimono/pull/1916) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-062 | Added | Added xterm modifyOtherKeys mode 2 fallback when Kitty keyboard protocol is not available, enabling modified enter keys (Shift+Enter, Ctrl+Enter) inside tmux ([#1872](https://github.com/badlogic/pimono/issues/1872)) | CHANGELOG.md |
| G-PI-CHANGELOG-063 | Added | Exported `decodeKittyPrintable()` from `keys.ts` for decoding Kitty CSIu sequences into printable characters | CHANGELOG.md |
| G-PI-CHANGELOG-064 | Fixed | Fixed `Input` component not accepting typed characters when Kitty keyboard protocol is active (e.g., VS Code 1.110+), causing model selector filter to ignore keystrokes ([#1857](https://github.com/badlogic/pimono/issues/1857)) | CHANGELOG.md |
| G-PI-CHANGELOG-065 | Fixed | Fixed editor/footer visibility drift during terminal resize by forcing full redraws when terminal width or height changes ([#1844](https://github.com/badlogic/pimono/pull/1844) by [@ghoulr](https://github.com/ghoulr)). | CHANGELOG.md |
| G-PI-CHANGELOG-066 | Fixed | Fixed markdown blockquote rendering to isolate blockquote styling from default text style, preventing style leakage. | CHANGELOG.md |
| G-PI-CHANGELOG-067 | Fixed | Fixed TUI width calculation for regional indicator symbols (e.g. partial flag sequences like `🇨` during streaming) to prevent wrap drift and stale character artifacts in differential rendering. | CHANGELOG.md |
| G-PI-CHANGELOG-068 | Fixed | Fixed Kitty CSIu handling to ignore unsupported modifiers so modifieronly events do not insert stray printable characters ([#1807](https://github.com/badlogic/pimono/issues/1807)) | CHANGELOG.md |
| G-PI-CHANGELOG-069 | Fixed | Fixed singleline paste performance by inserting pasted text atomically instead of characterbycharacter, preventing repeated `@` autocomplete scans during paste ([#1812](https://github.com/badlogic/pimono/issues/1812)) | CHANGELOG.md |
| G-PI-CHANGELOG-070 | Fixed | Fixed `visibleWidth()` to ignore generic OSC escape sequences (including OSC 133 semantic prompt markers), preventing width drift when terminals emit semantic zone markers ([#1805](https://github.com/badlogic/pimono/issues/1805)) | CHANGELOG.md |
| G-PI-CHANGELOG-071 | Fixed | Fixed markdown blockquotes dropping nested list content by rendering blockquote children as blocklevel tokens ([#1787](https://github.com/badlogic/pimono/issues/1787)) | CHANGELOG.md |
| G-PI-CHANGELOG-072 | Fixed | Fixed Windows VT input initialization in ESM by loading `koffi` via `createRequire`, restoring VT input mode while keeping `koffi` externalized from compiled binaries ([#1627](https://github.com/badlogic/pimono/pull/1627) by [@kaste](https://github.com/kaste)) | CHANGELOG.md |
| G-PI-CHANGELOG-073 | Fixed | Changed koffi import from toplevel to dynamic require in `enableWindowsVTInput()` to prevent bun from embedding all 18 platform `.node` files (~74MB) into every compiled binary. Koffi is only needed on Windows. | CHANGELOG.md |
| G-PI-CHANGELOG-074 | Added | Added terminal input listeners in `TUI` (`addInputListener` and `removeInputListener`) to let callers intercept, transform, or consume raw input before component handling. | CHANGELOG.md |
| G-PI-CHANGELOG-075 | Fixed | Fixed `@` autocomplete fuzzy matching to score against path segments and prefixes, reducing irrelevant matches for nested paths ([#1423](https://github.com/badlogic/pimono/issues/1423)) | CHANGELOG.md |
| G-PI-CHANGELOG-076 | Added | Added `pasteToEditor` to `EditorComponent` API for programmatic paste support ([#1351](https://github.com/badlogic/pimono/pull/1351) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-077 | Added | Added kill ring (ctrl+k/ctrl+y/alt+y) and undo (ctrl+z) support to the Input component ([#1373](https://github.com/badlogic/pimono/pull/1373) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-078 | Changed | Slash command menu now triggers on the first line even when other lines have content, allowing commands to be prepended to existing text ([#1227](https://github.com/badlogic/pimono/pull/1227) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-079 | Fixed | Fixed `/settings` crashing in narrow terminals by handling small widths in the settings list ([#1246](https://github.com/badlogic/pimono/pull/1246) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-080 | Fixed | Fixed input scrolling to avoid splitting emoji sequences ([#1228](https://github.com/badlogic/pimono/pull/1228) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-081 | Added | Added `Terminal.drainInput()` to drain stdin before exit (prevents Kitty key release events leaking over slow SSH) | CHANGELOG.md |
| G-PI-CHANGELOG-082 | Fixed | Fixed Kitty key release events leaking to parent shell over slow SSH connections by draining stdin for up to 1s ([#1204](https://github.com/badlogic/pimono/issues/1204)) | CHANGELOG.md |
| G-PI-CHANGELOG-083 | Fixed | Fixed legacy newline handling in the editor to preserve previous newline behavior | CHANGELOG.md |
| G-PI-CHANGELOG-084 | Fixed | Fixed @ autocomplete to include hidden paths | CHANGELOG.md |
| G-PI-CHANGELOG-085 | Fixed | Fixed submit fallback to honor configured keybindings | CHANGELOG.md |
| G-PI-CHANGELOG-086 | Added | Added `PI_DEBUG_REDRAW=1` env var for debugging full redraws (logs triggers to `~/.pi/agent/pidebug.log`) | CHANGELOG.md |
| G-PI-CHANGELOG-087 | Changed | Terminal height changes no longer trigger full redraws, reducing flicker on resize | CHANGELOG.md |
| G-PI-CHANGELOG-088 | Changed | `clearOnShrink` now defaults to `false` (use `PI_CLEAR_ON_SHRINK=1` or `setClearOnShrink(true)` to enable) | CHANGELOG.md |
| G-PI-CHANGELOG-089 | Fixed | Fixed emoji cursor positioning in Input component ([#1183](https://github.com/badlogic/pimono/pull/1183) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-090 | Fixed | Fixed unnecessary full redraws when appending many lines after content had previously shrunk (viewport check now uses actual previous content size instead of stale maximum) | CHANGELOG.md |
| G-PI-CHANGELOG-091 | Fixed | Fixed Ctrl+D exit closing the parent SSH session due to stdin buffer race condition ([#1185](https://github.com/badlogic/pimono/issues/1185)) | CHANGELOG.md |
| G-PI-CHANGELOG-092 | Added | Added sticky column tracking for vertical cursor navigation so the editor restores the preferred column when moving across short lines. ([#1120](https://github.com/badlogic/pimono/pull/1120) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-093 | Fixed | Fixed Kitty keyboard protocol base layout fallback so nonQWERTY layouts do not trigger wrong shortcuts ([#1096](https://github.com/badlogic/pimono/pull/1096) by [@rytswd](https://github.com/rytswd)) | CHANGELOG.md |
| G-PI-CHANGELOG-094 | Changed | Optimized `isImageLine()` with `startsWith` shortcircuit for faster image line detection | CHANGELOG.md |
| G-PI-CHANGELOG-095 | Fixed | Fixed empty rows appearing below footer when content shrinks (e.g., closing `/tree`, clearing multiline editor) ([#1095](https://github.com/badlogic/pimono/pull/1095) by [@marckrenn](https://github.com/marckrenn)) | CHANGELOG.md |
| G-PI-CHANGELOG-096 | Fixed | Fixed terminal cursor remaining hidden after exiting TUI via `stop()` when a render was pending ([#1099](https://github.com/badlogic/pimono/pull/1099) by [@haoqixu](https://github.com/haoqixu)) | CHANGELOG.md |
| G-PI-CHANGELOG-097 | Fixed | Fixed `isImageLine()` to check for image escape sequences anywhere in a line, not just at the start. This prevents TUI crashes when rendering lines containing image data. ([#1091](https://github.com/badlogic/pimono/pull/1091) by [@zedrdave](https://github.com/zedrdave)) | CHANGELOG.md |
| G-PI-CHANGELOG-098 | Added | Added Ctrl+B and Ctrl+F as alternative keybindings for cursor word left/right navigation ([#1053](https://github.com/badlogic/pimono/pull/1053) by [@ninlds](https://github.com/ninlds)) | CHANGELOG.md |
| G-PI-CHANGELOG-099 | Added | Added character jump navigation: Ctrl+] jumps forward to next character, Ctrl+Alt+] jumps backward ([#1074](https://github.com/badlogic/pimono/pull/1074) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-100 | Added | Editor now jumps to line start when pressing Up at first visual line, and line end when pressing Down at last visual line ([#1050](https://github.com/badlogic/pimono/pull/1050) by [@4h9fbZ](https://github.com/4h9fbZ)) | CHANGELOG.md |
| G-PI-CHANGELOG-101 | Changed | Optimized image line detection and box rendering cache for better performance ([#1084](https://github.com/badlogic/pimono/pull/1084) by [@can1357](https://github.com/can1357)) | CHANGELOG.md |
| G-PI-CHANGELOG-102 | Fixed | Fixed autocomplete for paths with spaces by supporting quoted path tokens ([#1077](https://github.com/badlogic/pimono/issues/1077)) | CHANGELOG.md |
| G-PI-CHANGELOG-103 | Fixed | Fixed quoted path completions to avoid duplicating closing quotes during autocomplete ([#1077](https://github.com/badlogic/pimono/issues/1077)) | CHANGELOG.md |
| G-PI-CHANGELOG-104 | Added | Added `autocompleteMaxVisible` option to `EditorOptions` with getter/setter methods for configurable autocomplete dropdown height ([#972](https://github.com/badlogic/pimono/pull/972) by [@masonc15](https://github.com/masonc15)) | CHANGELOG.md |
| G-PI-CHANGELOG-105 | Added | Added `alt+b` and `alt+f` as alternative keybindings for word navigation (`cursorWordLeft`, `cursorWordRight`) and `ctrl+d` for `deleteCharForward` ([#1043](https://github.com/badlogic/pimono/issues/1043) by [@jasonish](https://github.com/jasonish)) | CHANGELOG.md |
| G-PI-CHANGELOG-106 | Added | Editor autoapplies single suggestion when force file autocomplete triggers with exactly one match ([#993](https://github.com/badlogic/pimono/pull/993) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-107 | Changed | Improved `extractCursorPosition` performance: scans lines in reverse order, earlyouts when cursor is above viewport, and limits scan to bottom terminal height ([#1004](https://github.com/badlogic/pimono/pull/1004) by [@can1357](https://github.com/can1357)) | CHANGELOG.md |
| G-PI-CHANGELOG-108 | Changed | Autocomplete improvements: better handling of partial matches and edge cases ([#1024](https://github.com/badlogic/pimono/pull/1024) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-109 | Fixed | Fixed backslash input buffering causing delayed character display in editor and input components ([#1037](https://github.com/badlogic/pimono/pull/1037) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-110 | Fixed | Fixed markdown table rendering with proper row dividers and minimum column width ([#997](https://github.com/badlogic/pimono/pull/997) by [@tmustier](https://github.com/tmustier)) | CHANGELOG.md |
| G-PI-CHANGELOG-111 | Added | Added `fullRedraws` readonly property to TUI class for tracking full screen redraws | CHANGELOG.md |
| G-PI-CHANGELOG-112 | Added | Added `PI_TUI_WRITE_LOG` environment variable to capture raw ANSI output for debugging | CHANGELOG.md |
| G-PI-CHANGELOG-113 | Fixed | Fixed appended lines not being committed to scrollback, causing earlier content to be overwritten when viewport fills ([#954](https://github.com/badlogic/pimono/issues/954)) | CHANGELOG.md |
| G-PI-CHANGELOG-114 | Fixed | Slash command menu now only triggers when the editor input is otherwise empty ([#904](https://github.com/badlogic/pimono/issues/904)) | CHANGELOG.md |
| G-PI-CHANGELOG-115 | Fixed | Centeranchored overlays now stay vertically centered when resizing the terminal taller after a shrink ([#950](https://github.com/badlogic/pimono/pull/950) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-116 | Fixed | Fixed editor multiline insertion handling and lastAction tracking ([#945](https://github.com/badlogic/pimono/pull/945) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-117 | Fixed | Fixed editor word wrapping to reserve a cursor column ([#934](https://github.com/badlogic/pimono/pull/934) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-118 | Fixed | Fixed editor word wrapping to use singlepass backtracking for whitespace handling ([#924](https://github.com/badlogic/pimono/pull/924) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-119 | Fixed | Fixed Kitty image ID allocation and cleanup to prevent image ID collisions between modules | CHANGELOG.md |
| G-PI-CHANGELOG-120 | Added | `codeBlockIndent` property on `MarkdownTheme` to customize code block content indentation (default: 2 spaces) ([#855](https://github.com/badlogic/pimono/pull/855) by [@terrorobe](https://github.com/terrorobe)) | CHANGELOG.md |
| G-PI-CHANGELOG-121 | Added | Added Alt+Delete as hotkey for delete word forwards ([#878](https://github.com/badlogic/pimono/pull/878) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-122 | Changed | Fuzzy matching now scores consecutive matches higher and penalizes gaps more heavily for better relevance ([#860](https://github.com/badlogic/pimono/pull/860) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-123 | Fixed | Autolinked emails no longer display redundant `(mailto:...)` suffix in markdown output ([#888](https://github.com/badlogic/pimono/pull/888) by [@terrorobe](https://github.com/terrorobe)) | CHANGELOG.md |
| G-PI-CHANGELOG-124 | Fixed | Fixed viewport tracking and cursor positioning for overlays and content shrink scenarios | CHANGELOG.md |
| G-PI-CHANGELOG-125 | Fixed | Autocomplete now allows searches with `/` characters (e.g., `folder1/folder2`) ([#882](https://github.com/badlogic/pimono/pull/882) by [@richardgill](https://github.com/richardgill)) | CHANGELOG.md |
| G-PI-CHANGELOG-126 | Fixed | Directory completions for `@` file attachments no longer add trailing space, allowing continued autocomplete into subdirectories | CHANGELOG.md |
| G-PI-CHANGELOG-127 | Added | Added undo support to Editor with Ctrl+ hotkey. Undo coalesces consecutive word characters into one unit (fishstyle). ([#831](https://github.com/badlogic/pimono/pull/831) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-128 | Added | Added legacy terminal support for Ctrl+symbol keys (Ctrl+\, Ctrl+], Ctrl+) and their Ctrl+Alt variants. ([#831](https://github.com/badlogic/pimono/pull/831) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-129 | Added | Added `showHardwareCursor` getter and setter to control cursor visibility while keeping IME positioning active. ([#800](https://github.com/badlogic/pimono/pull/800) by [@ghoulr](https://github.com/ghoulr)) | CHANGELOG.md |
| G-PI-CHANGELOG-130 | Added | Added Emacsstyle kill ring editing with yank and yankpop keybindings. ([#810](https://github.com/badlogic/pimono/pull/810) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-131 | Added | Added legacy Alt+letter handling and Alt+D delete word forward support in the editor keymap. ([#810](https://github.com/badlogic/pimono/pull/810) by [@Perlence](https://github.com/Perlence)) | CHANGELOG.md |
| G-PI-CHANGELOG-132 | Added | `EditorOptions` with optional `paddingX` for horizontal content padding, plus `getPaddingX()`/`setPaddingX()` methods ([#791](https://github.com/badlogic/pimono/pull/791) by [@ferologics](https://github.com/ferologics)) | CHANGELOG.md |
| G-PI-CHANGELOG-133 | Changed | Hardware cursor is now disabled by default for better terminal compatibility. Set `PI_HARDWARE_CURSOR=1` to enable (replaces `PI_NO_HARDWARE_CURSOR=1` which disabled it). | CHANGELOG.md |
| G-PI-CHANGELOG-134 | Fixed | Decode Kitty CSIu printable sequences in the editor so shifted symbol keys (e.g., `@`, `?`) work in terminals that enable Kitty keyboard protocol ([#779](https://github.com/badlogic/pimono/pull/779) by [@iamd3vil](https://github.com/iamd3vil)) | CHANGELOG.md |
| G-PI-CHANGELOG-135 | Breaking Changes | `Editor` constructor now requires `TUI` as first parameter: `new Editor(tui, theme)`. This enables automatic vertical scrolling when content exceeds terminal height. ([#732](https://github.com/badlogic/pimono/issues/732)) | CHANGELOG.md |
| G-PI-CHANGELOG-136 | Added | Hardware cursor positioning for IME support in `Editor` and `Input` components. The terminal cursor now follows the text cursor position, enabling proper IME candidate window placement for CJK input. ([#719](https://github.com/badlogic/pimono/pull/719)) | CHANGELOG.md |
| G-PI-CHANGELOG-137 | Added | `Focusable` interface for components that need hardware cursor positioning. Implement `focused: boolean` and emit `CURSOR_MARKER` in render output when focused. | CHANGELOG.md |
| G-PI-CHANGELOG-138 | Added | `CURSOR_MARKER` constant and `isFocusable()` type guard exported from the package | CHANGELOG.md |
| G-PI-CHANGELOG-139 | Added | Editor now supports Page Up/Down keys (Fn+Up/Down on MacBook) for scrolling through large content ([#732](https://github.com/badlogic/pimono/issues/732)) | CHANGELOG.md |
| G-PI-CHANGELOG-140 | Added | Expanded keymap coverage for terminal compatibility: added support for Home/End keys in tmux, additional modifier combinations, and improved key sequence parsing ([#752](https://github.com/badlogic/pimono/pull/752) by [@richardgill](https://github.com/richardgill)) | CHANGELOG.md |
| G-PI-CHANGELOG-141 | Fixed | Editor no longer corrupts terminal display when text exceeds screen height. Content now scrolls vertically with indicators showing lines above/below the viewport. Max height is 30% of terminal (minimum 5 lines). ([#732](https://github.com/badlogic/pimono/issues/732)) | CHANGELOG.md |
| G-PI-CHANGELOG-142 | Fixed | `visibleWidth()` and `extractAnsiCode()` now handle APC escape sequences (`ESC _ ... BEL`), fixing width calculation and string slicing for strings containing cursor markers | CHANGELOG.md |
| G-PI-CHANGELOG-143 | Fixed | SelectList now handles multiline descriptions by replacing newlines with spaces ([#728](https://github.com/badlogic/pimono/pull/728) by [@richardgill](https://github.com/richardgill)) | CHANGELOG.md |
| G-PI-CHANGELOG-144 | Fixed | Keyboard shortcuts (Ctrl+C, Ctrl+D, etc.) now work on nonLatin keyboard layouts (Russian, Ukrainian, Bulgarian, etc.) in terminals supporting Kitty keyboard protocol with alternate key reporting ([#718](https://github.com/badlogic/pimono/pull/718) by [@dannote](https://github.com/dannote)) | CHANGELOG.md |
| G-PI-CHANGELOG-145 | Added | `OverlayOptions` API for overlay positioning and sizing with CSSlike values: `width`, `maxHeight`, `row`, `col` accept numbers (absolute) or percentage strings (e.g., `"50%"`). Also supports `minWidth`, `anchor`, `offsetX`, `offsetY`, `margin`. ([#667](https://github.com/badlogic/pimono/pull/667) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-146 | Added | `OverlayOptions.visible` callback for responsive overlays  receives terminal dimensions, return false to hide ([#667](https://github.com/badlogic/pimono/pull/667) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-147 | Added | `showOverlay()` now returns `OverlayHandle` with `hide()`, `setHidden(boolean)`, `isHidden()` for programmatic visibility control ([#667](https://github.com/badlogic/pimono/pull/667) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-148 | Added | New exported types: `OverlayAnchor`, `OverlayHandle`, `OverlayMargin`, `OverlayOptions`, `SizeValue` ([#667](https://github.com/badlogic/pimono/pull/667) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-149 | Added | `truncateToWidth()` now accepts optional `pad` parameter to pad result with spaces to exactly `maxWidth` ([#667](https://github.com/badlogic/pimono/pull/667) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-150 | Fixed | Overlay compositing crash when rendered lines exceed terminal width due to complex ANSI/OSC sequences (e.g., hyperlinks in subagent output) ([#667](https://github.com/badlogic/pimono/pull/667) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-151 | Added | `SettingsListOptions` with `enableSearch` for fuzzy filtering in `SettingsList` ([#643](https://github.com/badlogic/pimono/pull/643) by [@ninlds](https://github.com/ninlds)) | CHANGELOG.md |
| G-PI-CHANGELOG-152 | Added | `pageUp` and `pageDown` key support with `selectPageUp`/`selectPageDown` editor actions ([#662](https://github.com/badlogic/pimono/pull/662) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-153 | Fixed | Numbered list items showing "1." for all items when code blocks break list continuity ([#660](https://github.com/badlogic/pimono/pull/660) by [@ogulcancelik](https://github.com/ogulcancelik)) | CHANGELOG.md |
| G-PI-CHANGELOG-154 | Added | `fuzzyFilter()` and `fuzzyMatch()` utilities for fuzzy text matching | CHANGELOG.md |
| G-PI-CHANGELOG-155 | Added | Slash command autocomplete now uses fuzzy matching instead of prefix matching | CHANGELOG.md |
| G-PI-CHANGELOG-156 | Fixed | Cursor now moves to end of content on exit, preventing status line from being overwritten ([#629](https://github.com/badlogic/pimono/pull/629) by [@tallshort](https://github.com/tallshort)) | CHANGELOG.md |
| G-PI-CHANGELOG-157 | Fixed | Reset ANSI styles after each rendered line to prevent style leakage | CHANGELOG.md |
| G-PI-CHANGELOG-158 | Fixed | Reduced flicker by only rerendering changed lines ([#617](https://github.com/badlogic/pimono/pull/617) by [@ogulcancelik](https://github.com/ogulcancelik)) | CHANGELOG.md |
| G-PI-CHANGELOG-159 | Fixed | Cursor position tracking when content shrinks with unchanged remaining lines | CHANGELOG.md |
| G-PI-CHANGELOG-160 | Fixed | TUI renders with wrong dimensions after suspend/resume if terminal was resized while suspended ([#599](https://github.com/badlogic/pimono/issues/599)) | CHANGELOG.md |
| G-PI-CHANGELOG-161 | Fixed | Pasted content containing Kitty key release patterns (e.g., `:3F` in MAC addresses) was incorrectly filtered out ([#623](https://github.com/badlogic/pimono/pull/623) by [@ogulcancelik](https://github.com/ogulcancelik)) | CHANGELOG.md |
| G-PI-CHANGELOG-162 | Added | Experimental: Overlay compositing for `ctx.ui.custom()` with `{ overlay: true }` option ([#558](https://github.com/badlogic/pimono/pull/558) by [@nicobailon](https://github.com/nicobailon)) | CHANGELOG.md |
| G-PI-CHANGELOG-163 | Added | `EditorComponent` interface for custom editor implementations | CHANGELOG.md |
| G-PI-CHANGELOG-164 | Added | `StdinBuffer` class to split batched stdin into individual sequences (adapted from [OpenTUI](https://github.com/anomalyco/opentui), MIT license) | CHANGELOG.md |
| G-PI-CHANGELOG-165 | Fixed | Key presses no longer dropped when batched with other events over SSH ([#538](https://github.com/badlogic/pimono/pull/538)) | CHANGELOG.md |
| G-PI-CHANGELOG-166 | Added | `Component.wantsKeyRelease` property to optin to key release events (default false) | CHANGELOG.md |
| G-PI-CHANGELOG-167 | Fixed | TUI now filters out key release events by default, preventing doubleprocessing of keys in editors and other components | CHANGELOG.md |
| G-PI-CHANGELOG-168 | Fixed | `matchesKey()` now correctly matches Kitty protocol sequences for unmodified letter keys (needed for key release events) | CHANGELOG.md |
| G-PI-CHANGELOG-169 | Added | Kitty keyboard protocol flag 2 support for key release events. New exports: `isKeyRelease(data)`, `isKeyRepeat(data)`, `KeyEventType` type. Terminals supporting Kitty protocol (Kitty, Ghostty, WezTerm) now send proper keyup events. | CHANGELOG.md |
| G-PI-CHANGELOG-170 | Fixed | Crash when pasting text with trailing whitespace exceeding terminal width through Markdown rendering ([#457](https://github.com/badlogic/pimono/pull/457) by [@robinwander](https://github.com/robinwander)) | CHANGELOG.md |
| G-PI-CHANGELOG-171 | Added | Symbol key support in keybinding system: `SymbolKey` type with 32 symbol keys, `Key` constants (e.g., `Key.backtick`, `Key.comma`), updated `matchesKey()` and `parseKey()` to handle symbol input ([#450](https://github.com/badlogic/pimono/pull/450) by [@kaofelix](https://github.com/kaofelix)) | CHANGELOG.md |
| G-PI-CHANGELOG-172 | Added | `Editor.getExpandedText()` method that returns text with paste markers expanded to their actual content ([#444](https://github.com/badlogic/pimono/pull/444) by [@aliou](https://github.com/aliou)) | CHANGELOG.md |
| G-PI-CHANGELOG-173 | Breaking Changes | Key detection functions removed: All `isXxx()` key detection functions (`isEnter()`, `isEscape()`, `isCtrlC()`, etc.) have been removed. Use `matchesKey(data, keyId)` instead (e.g., `matchesKey(data, "enter")`, `matchesKey(data, "ctrl+c")`). This affects hooks and custom tools that use `ctx.ui.custom()` with keyboard input handling. ([#405](https://github.com/badlogic/pimono/pull/405)) | CHANGELOG.md |
| G-PI-CHANGELOG-174 | Added | `Editor.insertTextAtCursor(text)` method for programmatic text insertion ([#419](https://github.com/badlogic/pimono/issues/419)) | CHANGELOG.md |
| G-PI-CHANGELOG-175 | Added | `EditorKeybindingsManager` for configurable editor keybindings. Components now use `matchesKey()` and keybindings manager instead of individual `isXxx()` functions. ([#405](https://github.com/badlogic/pimono/pull/405) by [@hjanuschka](https://github.com/hjanuschka)) | CHANGELOG.md |
| G-PI-CHANGELOG-176 | Changed | Key detection refactored: consolidated `is()` functions into generic `matchesKey(data, keyId)` function that accepts key identifiers like `"ctrl+c"`, `"shift+enter"`, `"alt+left"`, etc. | CHANGELOG.md |
| G-PI-CHANGELOG-177 | Fixed | Slash command autocomplete now triggers for commands starting with `.`, ``, or `_` (e.g., `/.land`, `/foo`) ([#422](https://github.com/badlogic/pimono/issues/422)) | CHANGELOG.md |
| G-PI-CHANGELOG-178 | Changed | Editor component now uses word wrapping instead of characterlevel wrapping for better readability ([#382](https://github.com/badlogic/pimono/pull/382) by [@nickseelert](https://github.com/nickseelert)) | CHANGELOG.md |
| G-PI-CHANGELOG-179 | Fixed | Shift+Space, Shift+Backspace, and Shift+Delete now work correctly in Kittyprotocol terminals (Kitty, WezTerm, etc.) instead of being silently ignored ([#411](https://github.com/badlogic/pimono/pull/411) by [@nathyong](https://github.com/nathyong)) | CHANGELOG.md |
| G-PI-CHANGELOG-180 | Fixed | `visibleWidth()` now strips OSC 8 hyperlink sequences, fixing text wrapping for clickable links ([#396](https://github.com/badlogic/pimono/pull/396) by [@Cursivez](https://github.com/Cursivez)) | CHANGELOG.md |
| G-PI-CHANGELOG-181 | Added | `isShiftCtrlO()` key detection function for Shift+Ctrl+O (Kitty protocol) | CHANGELOG.md |
| G-PI-CHANGELOG-182 | Added | `isShiftCtrlD()` key detection function for Shift+Ctrl+D (Kitty protocol) | CHANGELOG.md |
| G-PI-CHANGELOG-183 | Added | `TUI.onDebug` callback for global debug key handling (Shift+Ctrl+D) | CHANGELOG.md |
| G-PI-CHANGELOG-184 | Added | `wrapTextWithAnsi()` utility now exported (wraps text to width, preserving ANSI codes) | CHANGELOG.md |
| G-PI-CHANGELOG-185 | Changed | README.md completely rewritten with accurate component documentation, theme interfaces, and examples | CHANGELOG.md |
| G-PI-CHANGELOG-186 | Changed | `visibleWidth()` reimplemented with graphemebased width calculation, 10x faster on Bun and ~15% faster on Node ([#369](https://github.com/badlogic/pimono/pull/369) by [@nathyong](https://github.com/nathyong)) | CHANGELOG.md |
| G-PI-CHANGELOG-187 | Fixed | Markdown component now renders HTML tags as plain text instead of silently dropping them ([#359](https://github.com/badlogic/pimono/issues/359)) | CHANGELOG.md |
| G-PI-CHANGELOG-188 | Fixed | Crash in `visibleWidth()` and grapheme iteration when encountering undefined code points ([#372](https://github.com/badlogic/pimono/pull/372) by [@HACKERC](https://github.com/HACKERC)) | CHANGELOG.md |
| G-PI-CHANGELOG-189 | Fixed | ZWJ emoji sequences (rainbow flag, family, etc.) now render with correct width instead of being split into multiple characters ([#369](https://github.com/badlogic/pimono/pull/369) by [@nathyong](https://github.com/nathyong)) | CHANGELOG.md |
| G-PI-CHANGELOG-190 | Added | Autospace before pasted file paths: When pasting a file path (starting with `/`, `~`, or `.`) and the cursor is after a word character, a space is automatically prepended for better readability. Useful when dragging screenshots from macOS. ([#307](https://github.com/badlogic/pimono/pull/307) by [@mitsuhiko](https://github.com/mitsuhiko)) | CHANGELOG.md |
| G-PI-CHANGELOG-191 | Added | Word navigation for Input component: Added Ctrl+Left/Right and Alt+Left/Right support for wordbyword cursor movement. ([#306](https://github.com/badlogic/pimono/pull/306) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-192 | Added | Full Unicode input: Input component now accepts Unicode characters beyond ASCII. ([#306](https://github.com/badlogic/pimono/pull/306) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-CHANGELOG-193 | Fixed | Readlinestyle Ctrl+W: Now skips trailing whitespace before deleting the preceding word, matching standard readline behavior. ([#306](https://github.com/badlogic/pimono/pull/306) by [@kim0](https://github.com/kim0)) | CHANGELOG.md |
| G-PI-README-001 | Features | Differential Rendering: Threestrategy rendering system that only updates what changed | README.md |
| G-PI-README-002 | Features | Synchronized Output: Uses CSI 2026 for atomic screen updates (no flicker) | README.md |
| G-PI-README-003 | Features | Bracketed Paste Mode: Handles large pastes correctly with markers for >10 line pastes | README.md |
| G-PI-README-004 | Features | Componentbased: Simple Component interface with render() method | README.md |
| G-PI-README-005 | Features | Theme Support: Components accept theme interfaces for customizable styling | README.md |
| G-PI-README-006 | Features | Builtin Components: Text, TruncatedText, Input, Editor, Markdown, Loader, SelectList, SettingsList, Spacer, Image, Box, Container | README.md |
| G-PI-README-007 | Features | Inline Images: Renders images in terminals that support Kitty or iTerm2 graphics protocols | README.md |
| G-PI-README-008 | Features | Autocomplete Support: File paths and slash commands | README.md |
| G-PI-README-009 | Overlays | Anchor values: `'center'`, `'topleft'`, `'topright'`, `'bottomleft'`, `'bottomright'`, `'topcenter'`, `'bottomcenter'`, `'leftcenter'`, `'rightcenter'` | README.md |
| G-PI-README-010 | Overlays | Resolution order: | README.md |
| G-PI-README-011 | Focusable Interface (IME Support) | Container components with embedded inputs: When a container component (dialog, selector, etc.) contains an `Input` or `Editor` child, the container must implement `Focusable` and propagate the focus state to the child: | README.md |
| G-PI-README-012 | Input | Key Bindings: | README.md |
| G-PI-README-013 | Input | `Enter`  Submit | README.md |
| G-PI-README-014 | Input | `Ctrl+A` / `Ctrl+E`  Line start/end | README.md |
| G-PI-README-015 | Input | `Ctrl+W` or `Alt+Backspace`  Delete word backwards | README.md |
| G-PI-README-016 | Input | `Ctrl+U`  Delete to start of line | README.md |
| G-PI-README-017 | Input | `Ctrl+K`  Delete to end of line | README.md |
| G-PI-README-018 | Input | `Ctrl+Left` / `Ctrl+Right`  Word navigation | README.md |
| G-PI-README-019 | Input | `Alt+Left` / `Alt+Right`  Word navigation | README.md |
| G-PI-README-020 | Input | Arrow keys, Backspace, Delete work as expected | README.md |
| G-PI-README-021 | Editor | Features: | README.md |
| G-PI-README-022 | Editor | Multiline editing with word wrap | README.md |
| G-PI-README-023 | Editor | Slash command autocomplete (type `/`) | README.md |
| G-PI-README-024 | Editor | File path autocomplete (press `Tab`) | README.md |
| G-PI-README-025 | Editor | Large paste handling (>10 lines creates `[paste #1 +50 lines]` marker) | README.md |
| G-PI-README-026 | Editor | Horizontal lines above/below editor | README.md |
| G-PI-README-027 | Editor | Fake cursor rendering (hidden real cursor) | README.md |
| G-PI-README-028 | Editor | Key Bindings: | README.md |
| G-PI-README-029 | Editor | `Enter`  Submit | README.md |
| G-PI-README-030 | Editor | `Shift+Enter`, `Ctrl+Enter`, or `Alt+Enter`  New line (terminaldependent, Alt+Enter most reliable) | README.md |
| G-PI-README-031 | Editor | `Tab`  Autocomplete | README.md |
| G-PI-README-032 | Editor | `Ctrl+K`  Delete to end of line | README.md |
| G-PI-README-033 | Editor | `Ctrl+U`  Delete to start of line | README.md |
| G-PI-README-034 | Editor | `Ctrl+W` or `Alt+Backspace`  Delete word backwards | README.md |
| G-PI-README-035 | Editor | `Alt+D` or `Alt+Delete`  Delete word forwards | README.md |
| G-PI-README-036 | Editor | `Ctrl+A` / `Ctrl+E`  Line start/end | README.md |
| G-PI-README-037 | Editor | `Ctrl+]`  Jump forward to character (awaits next keypress, then moves cursor to first occurrence) | README.md |
| G-PI-README-038 | Editor | `Ctrl+Alt+]`  Jump backward to character | README.md |
| G-PI-README-039 | Editor | Arrow keys, Backspace, Delete work as expected | README.md |
| G-PI-README-040 | Markdown | Features: | README.md |
| G-PI-README-041 | Markdown | Headings, bold, italic, code blocks, lists, links, blockquotes | README.md |
| G-PI-README-042 | Markdown | HTML tags rendered as plain text | README.md |
| G-PI-README-043 | Markdown | Optional syntax highlighting via `highlightCode` | README.md |
| G-PI-README-044 | Markdown | Padding support | README.md |
| G-PI-README-045 | Markdown | Render caching for performance | README.md |
| G-PI-README-046 | CancellableLoader | Properties: | README.md |
| G-PI-README-047 | CancellableLoader | `signal: AbortSignal`  Aborted when user presses Escape | README.md |
| G-PI-README-048 | CancellableLoader | `aborted: boolean`  Whether the loader was aborted | README.md |
| G-PI-README-049 | CancellableLoader | `onAbort?: () => void`  Callback when user presses Escape | README.md |
| G-PI-README-050 | SelectList | Controls: | README.md |
| G-PI-README-051 | SelectList | Arrow keys: Navigate | README.md |
| G-PI-README-052 | SelectList | Enter: Select | README.md |
| G-PI-README-053 | SelectList | Escape: Cancel | README.md |
| G-PI-README-054 | SettingsList | Controls: | README.md |
| G-PI-README-055 | SettingsList | Arrow keys: Navigate | README.md |
| G-PI-README-056 | SettingsList | Enter/Space: Activate (cycle value or open submenu) | README.md |
| G-PI-README-057 | SettingsList | Escape: Cancel | README.md |
| G-PI-README-058 | CombinedAutocompleteProvider | Features: | README.md |
| G-PI-README-059 | CombinedAutocompleteProvider | Type `/` to see slash commands | README.md |
| G-PI-README-060 | CombinedAutocompleteProvider | Press `Tab` for file path completion | README.md |
| G-PI-README-061 | CombinedAutocompleteProvider | Works with `~/`, `./`, `../`, and `@` prefix | README.md |
| G-PI-README-062 | CombinedAutocompleteProvider | Filters to attachable files for `@` prefix | README.md |
| G-PI-README-063 | Key Detection | Key identifiers (use `Key.` for autocomplete, or string literals): | README.md |
| G-PI-README-064 | Key Detection | Basic keys: `Key.enter`, `Key.escape`, `Key.tab`, `Key.space`, `Key.backspace`, `Key.delete`, `Key.home`, `Key.end` | README.md |
| G-PI-README-065 | Key Detection | Arrow keys: `Key.up`, `Key.down`, `Key.left`, `Key.right` | README.md |
| G-PI-README-066 | Key Detection | With modifiers: `Key.ctrl("c")`, `Key.shift("tab")`, `Key.alt("left")`, `Key.ctrlShift("p")` | README.md |
| G-PI-README-067 | Key Detection | String format also works: `"enter"`, `"ctrl+c"`, `"shift+tab"`, `"ctrl+shift+p"` | README.md |
| G-PI-README-068 | Terminal Interface | Builtin implementations: | README.md |
| G-PI-README-069 | Terminal Interface | `ProcessTerminal`  Uses `process.stdin/stdout` | README.md |
| G-PI-README-070 | Terminal Interface | `VirtualTerminal`  For testing (uses `@xterm/headless`) | README.md |
| G-PI-README-071 | ANSI Code Considerations | `visibleWidth()` ignores ANSI codes when calculating width | README.md |
| G-PI-README-072 | ANSI Code Considerations | `truncateToWidth()` preserves ANSI codes and properly closes them when truncating | README.md |
| G-PI-README-073 | Example | Markdown messages with custom background colors | README.md |
| G-PI-README-074 | Example | Loading spinner during responses | README.md |
| G-PI-README-075 | Example | Editor with autocomplete and slash commands | README.md |
| G-PI-README-076 | Example | Spacers between messages | README.md |
| G-PI-CHANGELOG-001 | Breaking Changes | Migrated the web UI's TypeBoxbased tool definitions and runtime dependency from `@sinclair/typebox` 0.34.x to `typebox` 1.x. Install and import from `typebox` instead of `@sinclair/typebox` when embedding or extending `@mariozechner/piwebui` with shared TypeBox schemas ([#3112](https://github.com/badlogic/pimono/issues/3112)) | CHANGELOG.md |
| G-PI-CHANGELOG-002 | Fixed | Render SVG artifact previews through a blobbacked image instead of injecting untrusted SVG markup into the page DOM ([#3552](https://github.com/badlogic/pimono/issues/3552)) | CHANGELOG.md |
| G-PI-CHANGELOG-003 | Added | Exported `CustomProviderDialog` from `@mariozechner/piwebui` ([#2267](https://github.com/badlogic/pimono/issues/2267)) | CHANGELOG.md |
| G-PI-CHANGELOG-004 | Added | `onModelSelect` callback on `AgentInterface` and `ChatPanel.setAgent` config | CHANGELOG.md |
| G-PI-CHANGELOG-005 | Added | `allowedProviders` filter on `ModelSelector.open()` to restrict visible models | CHANGELOG.md |
| G-PI-CHANGELOG-006 | Added | `onClose` callback on `SettingsDialog.open()` | CHANGELOG.md |
| G-PI-CHANGELOG-007 | Added | `state_change` event emitted by Agent on `setModel()` and `setThinkingLevel()` | CHANGELOG.md |
| G-PI-CHANGELOG-008 | Added | Subsequencebased fuzzy search in model selector (replaces substring matching) | CHANGELOG.md |
| G-PI-CHANGELOG-009 | Added | `openaicodex` and `githubcopilot` to `shouldUseProxyForProvider` | CHANGELOG.md |
| G-PI-CHANGELOG-010 | Changed | Anthropic test model updated from `claude35haiku20241022` to `claudehaiku45` | CHANGELOG.md |
| G-PI-CHANGELOG-011 | Fixed | `AgentInterface` clears streaming container on `message_end` to prevent duplicate tool rendering | CHANGELOG.md |
| G-PI-CHANGELOG-012 | Fixed | Build `@mariozechner/piwebui` with `tsc` instead of `tsgo` so Lit decoratorbased state updates rerender correctly. | CHANGELOG.md |
| G-PI-CHANGELOG-013 | Fixed | Made model selector search caseinsensitive by normalizing query tokens, fixing autocapitalized mobile input filtering ([#1443](https://github.com/badlogic/pimono/issues/1443)) | CHANGELOG.md |
| G-PI-CHANGELOG-014 | Added | Exported `CustomProviderCard`, `ProviderKeyInput`, `AbortedMessage`, and `ToolMessageDebugView` components for custom UIs ([#1015](https://github.com/badlogic/pimono/issues/1015)) | CHANGELOG.md |
| G-PI-CHANGELOG-015 | Changed | Updated tsgo to 7.0.0dev.20260120.1 for decorator support ([#873](https://github.com/badlogic/pimono/issues/873)) | CHANGELOG.md |
| G-PI-CHANGELOG-016 | Breaking Changes | Agent class moved to `@mariozechner/piagentcore`: The `Agent` class, `AgentState`, and related types are no longer exported from this package. Import them from `@mariozechner/piagentcore` instead. | CHANGELOG.md |
| G-PI-CHANGELOG-017 | Breaking Changes | Transport abstraction removed: `ProviderTransport`, `AppTransport`, `AgentTransport` interface, and related types have been removed. The `Agent` class now uses `streamFn` for custom streaming. | CHANGELOG.md |
| G-PI-CHANGELOG-018 | Breaking Changes | `AppMessage` renamed to `AgentMessage`: Now imported from `@mariozechner/piagentcore`. Custom message types use declaration merging on `CustomAgentMessages` interface. | CHANGELOG.md |
| G-PI-CHANGELOG-019 | Breaking Changes | `UserMessageWithAttachments` is now a custom message type: Has `role: "userwithattachments"` instead of `role: "user"`. Use `isUserMessageWithAttachments()` type guard. | CHANGELOG.md |
| G-PI-CHANGELOG-020 | Breaking Changes | `CustomMessages` interface removed: Use declaration merging on `CustomAgentMessages` from `@mariozechner/piagentcore` instead. | CHANGELOG.md |
| G-PI-CHANGELOG-021 | Breaking Changes | `agent.appendMessage()` removed: Use `agent.queueMessage()` instead. | CHANGELOG.md |
| G-PI-CHANGELOG-022 | Breaking Changes | Agent event types changed: `AgentInterface` now handles new event types from `@mariozechner/piagentcore`: `message_start`, `message_end`, `message_update`, `turn_start`, `turn_end`, `agent_start`, `agent_end`. | CHANGELOG.md |
| G-PI-CHANGELOG-023 | Added | `defaultConvertToLlm`: Default message transformer that handles `UserMessageWithAttachments` and `ArtifactMessage`. Apps can extend this for custom message types. | CHANGELOG.md |
| G-PI-CHANGELOG-024 | Added | `convertAttachments`: Utility to convert `Attachment[]` to LLM content blocks (images and extracted document text). | CHANGELOG.md |
| G-PI-CHANGELOG-025 | Added | `isUserMessageWithAttachments` / `isArtifactMessage`: Type guard functions for custom message types. | CHANGELOG.md |
| G-PI-CHANGELOG-026 | Added | `createStreamFn`: Creates a stream function with CORS proxy support. Reads proxy settings on each call for dynamic configuration. | CHANGELOG.md |
| G-PI-CHANGELOG-027 | Added | Default `streamFn` and `getApiKey`: `AgentInterface` now sets sensible defaults if not provided: | CHANGELOG.md |
| G-PI-CHANGELOG-028 | Added | `streamFn`: Uses `createStreamFn` with proxy settings from storage | CHANGELOG.md |
| G-PI-CHANGELOG-029 | Added | `getApiKey`: Reads from `providerKeys` storage | CHANGELOG.md |
| G-PI-CHANGELOG-030 | Added | Proxy utilities exported: `applyProxyIfNeeded`, `shouldUseProxyForProvider`, `isCorsError`, `createStreamFn` | CHANGELOG.md |
| G-PI-CHANGELOG-031 | Removed | `Agent` class (moved to `@mariozechner/piagentcore`) | CHANGELOG.md |
| G-PI-CHANGELOG-032 | Removed | `ProviderTransport` class | CHANGELOG.md |
| G-PI-CHANGELOG-033 | Removed | `AppTransport` class | CHANGELOG.md |
| G-PI-CHANGELOG-034 | Removed | `AgentTransport` interface | CHANGELOG.md |
| G-PI-CHANGELOG-035 | Removed | `AgentRunConfig` type | CHANGELOG.md |
| G-PI-CHANGELOG-036 | Removed | `ProxyAssistantMessageEvent` type | CHANGELOG.md |
| G-PI-CHANGELOG-037 | Removed | `testsessions.ts` example file | CHANGELOG.md |
| G-PI-CHANGELOG-038 | Migration Guide | Before (0.30.x): | CHANGELOG.md |
| G-PI-CHANGELOG-039 | Migration Guide | After: | CHANGELOG.md |
| G-PI-CHANGELOG-040 | Migration Guide | Custom message types: | CHANGELOG.md |
| G-PI-README-001 | Features | Chat UI: Complete interface with message history, streaming, and tool execution | README.md |
| G-PI-README-002 | Features | Tools: JavaScript REPL, document extraction, and artifacts (HTML, SVG, Markdown, etc.) | README.md |
| G-PI-README-003 | Features | Attachments: PDF, DOCX, XLSX, PPTX, images with preview and text extraction | README.md |
| G-PI-README-004 | Features | Artifacts: Interactive HTML, SVG, Markdown with sandboxed execution | README.md |
| G-PI-README-005 | Features | Storage: IndexedDBbacked storage for sessions, API keys, and settings | README.md |
| G-PI-README-006 | Features | CORS Proxy: Automatic proxy handling for browser environments | README.md |
| G-PI-README-007 | Features | Custom Providers: Support for Ollama, LM Studio, vLLM, and OpenAIcompatible APIs | README.md |
| G-PI-README-008 | AgentInterface | `session`: Agent instance | README.md |
| G-PI-README-009 | AgentInterface | `enableAttachments`: Show attachment button (default: true) | README.md |
| G-PI-README-010 | AgentInterface | `enableModelSelector`: Show model selector (default: true) | README.md |
| G-PI-README-011 | AgentInterface | `enableThinkingSelector`: Show thinking level selector (default: true) | README.md |
| G-PI-README-012 | AgentInterface | `showThemeToggle`: Show theme toggle (default: false) | README.md |
| G-PI-README-013 | Examples | [example/](./example)  Complete web app with sessions, artifacts, custom messages | README.md |
| G-PI-README-014 | Examples | [sitegeist](https://sitegeist.ai)  Browser extension using piwebui | README.md |
| G-PI-README-015 | Known Issues | PersistentStorageDialog: Currently broken | README.md |
| G-PI-README-001 | What's Included | ChatPanel  The main chat interface component | README.md |
| G-PI-README-002 | What's Included | System Prompt  Custom configuration for the AI assistant | README.md |
| G-PI-README-003 | What's Included | Tools  JavaScript REPL and artifacts tool | README.md |
| G-PI-README-004 | API Keys | Anthropic: Get a key from [console.anthropic.com](https://console.anthropic.com/) | README.md |
| G-PI-README-005 | API Keys | OpenAI: Get a key from [platform.openai.com](https://platform.openai.com/) | README.md |
| G-PI-README-006 | API Keys | Google: Get a key from [makersuite.google.com](https://makersuite.google.com/) | README.md |
| G-PI-README-007 | Learn More | [Pi Web UI Documentation](../README.md) | README.md |
| G-PI-README-008 | Learn More | [Pi AI Documentation](../../ai/README.md) | README.md |
| G-PI-README-009 | Learn More | [Mini Lit Documentation](https://github.com/badlogic/minilit) | README.md |
| G-PI-PACKAGES-001 | Table of Contents | [Install and Manage](#installandmanage) | packages.md |
| G-PI-PACKAGES-002 | Table of Contents | [Package Sources](#packagesources) | packages.md |
| G-PI-PACKAGES-003 | Table of Contents | [Creating a Pi Package](#creatingapipackage) | packages.md |
| G-PI-PACKAGES-004 | Table of Contents | [Package Structure](#packagestructure) | packages.md |
| G-PI-PACKAGES-005 | Table of Contents | [Dependencies](#dependencies) | packages.md |
| G-PI-PACKAGES-006 | Table of Contents | [Package Filtering](#packagefiltering) | packages.md |
| G-PI-PACKAGES-007 | Table of Contents | [Enable and Disable Resources](#enableanddisableresources) | packages.md |
| G-PI-PACKAGES-008 | Table of Contents | [Scope and Deduplication](#scopeanddeduplication) | packages.md |
| G-PI-PACKAGES-009 | npm | Versioned specs are pinned and skipped by package updates (`pi update`, `pi update extensions`). | packages.md |
| G-PI-PACKAGES-010 | npm | Global installs use `npm install g`. | packages.md |
| G-PI-PACKAGES-011 | npm | Project installs go under `.pi/npm/`. | packages.md |
| G-PI-PACKAGES-012 | npm | Set `npmCommand` in `settings.json` to pin npm package lookup and install operations to a specific wrapper command such as `mise` or `asdf`. | packages.md |
| G-PI-PACKAGES-013 | git | Without `git:` prefix, only protocol URLs are accepted (`https://`, `http://`, `ssh://`, `git://`). | packages.md |
| G-PI-PACKAGES-014 | git | With `git:` prefix, shorthand formats are accepted, including `github.com/user/repo` and `git@github.com:user/repo`. | packages.md |
| G-PI-PACKAGES-015 | git | HTTPS and SSH URLs are both supported. | packages.md |
| G-PI-PACKAGES-016 | git | SSH URLs use your configured SSH keys automatically (respects `~/.ssh/config`). | packages.md |
| G-PI-PACKAGES-017 | git | For noninteractive runs (for example CI), you can set `GIT_TERMINAL_PROMPT=0` to disable credential prompts and set `GIT_SSH_COMMAND` (for example `ssh o BatchMode=yes o ConnectTimeout=5`) to fail fast. | packages.md |
| G-PI-PACKAGES-018 | git | Refs pin the package and skip package updates (`pi update`, `pi update extensions`). | packages.md |
| G-PI-PACKAGES-019 | git | Cloned to `~/.pi/agent/git/<host>/<path>` (global) or `.pi/git/<host>/<path>` (project). | packages.md |
| G-PI-PACKAGES-020 | git | Runs `npm install` after clone or pull if `package.json` exists. | packages.md |
| G-PI-PACKAGES-021 | git | SSH examples: | packages.md |
| G-PI-PACKAGES-022 | Gallery Metadata | video: MP4 only. On desktop, autoplays on hover. Clicking opens a fullscreen player. | packages.md |
| G-PI-PACKAGES-023 | Gallery Metadata | image: PNG, JPEG, GIF, or WebP. Displayed as a static preview. | packages.md |
| G-PI-PACKAGES-024 | Convention Directories | `extensions/` loads `.ts` and `.js` files | packages.md |
| G-PI-PACKAGES-025 | Convention Directories | `skills/` recursively finds `SKILL.md` folders and loads toplevel `.md` files as skills | packages.md |
| G-PI-PACKAGES-026 | Convention Directories | `prompts/` loads `.md` files | packages.md |
| G-PI-PACKAGES-027 | Convention Directories | `themes/` loads `.json` files | packages.md |
| G-PI-PACKAGES-028 | Package Filtering | Omit a key to load all of that type. | packages.md |
| G-PI-PACKAGES-029 | Package Filtering | Use `[]` to load none of that type. | packages.md |
| G-PI-PACKAGES-030 | Package Filtering | `!pattern` excludes matches. | packages.md |
| G-PI-PACKAGES-031 | Package Filtering | `+path` forceincludes an exact path. | packages.md |
| G-PI-PACKAGES-032 | Package Filtering | `path` forceexcludes an exact path. | packages.md |
| G-PI-PACKAGES-033 | Package Filtering | Filters layer on top of the manifest. They narrow down what is already allowed. | packages.md |
| G-PI-PACKAGES-034 | Scope and Deduplication | npm: package name | packages.md |
| G-PI-PACKAGES-035 | Scope and Deduplication | git: repository URL without ref | packages.md |
| G-PI-PACKAGES-036 | Scope and Deduplication | local: resolved absolute path | packages.md |
| G-PI-COMPACTION-001 | Compaction & Branch Summarization | Source files ([pimono](https://github.com/badlogic/pimono)): | compaction.md |
| G-PI-COMPACTION-002 | Compaction & Branch Summarization | [`packages/codingagent/src/core/compaction/compaction.ts`](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/compaction/compaction.ts)  Autocompaction logic | compaction.md |
| G-PI-COMPACTION-003 | Compaction & Branch Summarization | [`packages/codingagent/src/core/compaction/branchsummarization.ts`](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/compaction/branchsummarization.ts)  Branch summarization | compaction.md |
| G-PI-COMPACTION-004 | Compaction & Branch Summarization | [`packages/codingagent/src/core/compaction/utils.ts`](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/compaction/utils.ts)  Shared utilities (file tracking, serialization) | compaction.md |
| G-PI-COMPACTION-005 | Compaction & Branch Summarization | [`packages/codingagent/src/core/sessionmanager.ts`](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/sessionmanager.ts)  Entry types (`CompactionEntry`, `BranchSummaryEntry`) | compaction.md |
| G-PI-COMPACTION-006 | Compaction & Branch Summarization | [`packages/codingagent/src/core/extensions/types.ts`](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/extensions/types.ts)  Extension event types | compaction.md |
| G-PI-COMPACTION-007 | Cut Point Rules | User messages | compaction.md |
| G-PI-COMPACTION-008 | Cut Point Rules | Assistant messages | compaction.md |
| G-PI-COMPACTION-009 | Cut Point Rules | BashExecution messages | compaction.md |
| G-PI-COMPACTION-010 | Cut Point Rules | Custom messages (custom_message, branch_summary) | compaction.md |
| G-PI-COMPACTION-011 | Cumulative File Tracking | Tool calls in the messages being summarized | compaction.md |
| G-PI-COMPACTION-012 | Cumulative File Tracking | Previous compaction or branch summary `details` (if any) | compaction.md |
| G-PI-COMPACTION-013 | Constraints & Preferences | [Requirements mentioned by user] | compaction.md |
| G-PI-COMPACTION-014 | Done | [x] [Completed tasks] | compaction.md |
| G-PI-COMPACTION-015 | In Progress | [Current work] | compaction.md |
| G-PI-COMPACTION-016 | Blocked | [Issues, if any] | compaction.md |
| G-PI-COMPACTION-017 | Key Decisions | [Decision]: [Rationale] | compaction.md |
| G-PI-COMPACTION-018 | Critical Context | [Data needed to continue] | compaction.md |
| G-PI-CUSTOM-PROVIDER-001 | Custom Providers | Proxies  Route requests through corporate proxies or API gateways | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-002 | Custom Providers | Custom endpoints  Use selfhosted or private model deployments | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-003 | Custom Providers | OAuth/SSO  Add authentication flows for enterprise providers | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-004 | Custom Providers | Custom APIs  Implement streaming for nonstandard LLM APIs | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-005 | Example Extensions | [`examples/extensions/customprovideranthropic/`](../examples/extensions/customprovideranthropic/) | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-006 | Example Extensions | [`examples/extensions/customprovidergitlabduo/`](../examples/extensions/customprovidergitlabduo/) | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-007 | Table of Contents | [Example Extensions](#exampleextensions) | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-008 | Table of Contents | [Quick Reference](#quickreference) | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-009 | Table of Contents | [Override Existing Provider](#overrideexistingprovider) | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-010 | Table of Contents | [Register New Provider](#registernewprovider) | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-011 | Table of Contents | [Unregister Provider](#unregisterprovider) | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-012 | Table of Contents | [OAuth Support](#oauthsupport) | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-013 | Table of Contents | [Custom Streaming API](#customstreamingapi) | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-014 | Table of Contents | [Testing Your Implementation](#testingyourimplementation) | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-015 | Table of Contents | [Config Reference](#configreference) | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-016 | Table of Contents | [Model Definition Reference](#modeldefinitionreference) | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-017 | Custom Streaming API | Reference implementations: | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-018 | Custom Streaming API | [anthropic.ts](https://github.com/badlogic/pimono/blob/main/packages/ai/src/providers/anthropic.ts)  Anthropic Messages API | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-019 | Custom Streaming API | [mistral.ts](https://github.com/badlogic/pimono/blob/main/packages/ai/src/providers/mistral.ts)  Mistral Conversations API | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-020 | Custom Streaming API | [openaicompletions.ts](https://github.com/badlogic/pimono/blob/main/packages/ai/src/providers/openaicompletions.ts)  OpenAI Chat Completions | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-021 | Custom Streaming API | [openairesponses.ts](https://github.com/badlogic/pimono/blob/main/packages/ai/src/providers/openairesponses.ts)  OpenAI Responses API | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-022 | Custom Streaming API | [google.ts](https://github.com/badlogic/pimono/blob/main/packages/ai/src/providers/google.ts)  Google Generative AI | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-023 | Custom Streaming API | [amazonbedrock.ts](https://github.com/badlogic/pimono/blob/main/packages/ai/src/providers/amazonbedrock.ts)  AWS Bedrock | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-024 | Event Types | `{ type: "text_start", contentIndex, partial }`  Text block started | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-025 | Event Types | `{ type: "text_delta", contentIndex, delta, partial }`  Text chunk | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-026 | Event Types | `{ type: "text_end", contentIndex, content, partial }`  Text block ended | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-027 | Event Types | `{ type: "thinking_start", contentIndex, partial }`  Thinking started | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-028 | Event Types | `{ type: "thinking_delta", contentIndex, delta, partial }`  Thinking chunk | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-029 | Event Types | `{ type: "thinking_end", contentIndex, content, partial }`  Thinking ended | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-030 | Event Types | `{ type: "toolcall_start", contentIndex, partial }`  Tool call started | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-031 | Event Types | `{ type: "toolcall_delta", contentIndex, delta, partial }`  Tool call JSON chunk | custom-provider.md |
| G-PI-CUSTOM-PROVIDER-032 | Event Types | `{ type: "toolcall_end", contentIndex, toolCall, partial }`  Tool call ended | custom-provider.md |
| G-PI-DEVELOPMENT-001 | Path Resolution | Always use `src/config.ts` for package assets: | development.md |
| G-PI-DEVELOPMENT-002 | Debug Command | Rendered TUI lines with ANSI codes | development.md |
| G-PI-DEVELOPMENT-003 | Debug Command | Last messages sent to the LLM | development.md |
| G-PI-EXTENSIONS-001 | Extensions | Key capabilities: | extensions.md |
| G-PI-EXTENSIONS-002 | Extensions | Custom tools  Register tools the LLM can call via `pi.registerTool()` | extensions.md |
| G-PI-EXTENSIONS-003 | Extensions | Event interception  Block or modify tool calls, inject context, customize compaction | extensions.md |
| G-PI-EXTENSIONS-004 | Extensions | User interaction  Prompt users via `ctx.ui` (select, confirm, input, notify) | extensions.md |
| G-PI-EXTENSIONS-005 | Extensions | Custom UI components  Full TUI components with keyboard input via `ctx.ui.custom()` for complex interactions | extensions.md |
| G-PI-EXTENSIONS-006 | Extensions | Custom commands  Register commands like `/mycommand` via `pi.registerCommand()` | extensions.md |
| G-PI-EXTENSIONS-007 | Extensions | Session persistence  Store state that survives restarts via `pi.appendEntry()` | extensions.md |
| G-PI-EXTENSIONS-008 | Extensions | Custom rendering  Control how tool calls/results and messages appear in TUI | extensions.md |
| G-PI-EXTENSIONS-009 | Extensions | Example use cases: | extensions.md |
| G-PI-EXTENSIONS-010 | Extensions | Permission gates (confirm before `rm rf`, `sudo`, etc.) | extensions.md |
| G-PI-EXTENSIONS-011 | Extensions | Git checkpointing (stash at each turn, restore on branch) | extensions.md |
| G-PI-EXTENSIONS-012 | Extensions | Path protection (block writes to `.env`, `node_modules/`) | extensions.md |
| G-PI-EXTENSIONS-013 | Extensions | Custom compaction (summarize conversation your way) | extensions.md |
| G-PI-EXTENSIONS-014 | Extensions | Conversation summaries (see `summarize.ts` example) | extensions.md |
| G-PI-EXTENSIONS-015 | Extensions | Interactive tools (questions, wizards, custom dialogs) | extensions.md |
| G-PI-EXTENSIONS-016 | Extensions | Stateful tools (todo lists, connection pools) | extensions.md |
| G-PI-EXTENSIONS-017 | Extensions | External integrations (file watchers, webhooks, CI triggers) | extensions.md |
| G-PI-EXTENSIONS-018 | Extensions | Games while you wait (see `snake.ts` example) | extensions.md |
| G-PI-EXTENSIONS-019 | Table of Contents | [Quick Start](#quickstart) | extensions.md |
| G-PI-EXTENSIONS-020 | Table of Contents | [Extension Locations](#extensionlocations) | extensions.md |
| G-PI-EXTENSIONS-021 | Table of Contents | [Available Imports](#availableimports) | extensions.md |
| G-PI-EXTENSIONS-022 | Table of Contents | [Writing an Extension](#writinganextension) | extensions.md |
| G-PI-EXTENSIONS-023 | Table of Contents | [Extension Styles](#extensionstyles) | extensions.md |
| G-PI-EXTENSIONS-024 | Table of Contents | [Events](#events) | extensions.md |
| G-PI-EXTENSIONS-025 | Table of Contents | [Lifecycle Overview](#lifecycleoverview) | extensions.md |
| G-PI-EXTENSIONS-026 | Table of Contents | [Resource Events](#resourceevents) | extensions.md |
| G-PI-EXTENSIONS-027 | Table of Contents | [Session Events](#sessionevents) | extensions.md |
| G-PI-EXTENSIONS-028 | Table of Contents | [Agent Events](#agentevents) | extensions.md |
| G-PI-EXTENSIONS-029 | Table of Contents | [Model Events](#modelevents) | extensions.md |
| G-PI-EXTENSIONS-030 | Table of Contents | [Tool Events](#toolevents) | extensions.md |
| G-PI-EXTENSIONS-031 | Table of Contents | [ExtensionContext](#extensioncontext) | extensions.md |
| G-PI-EXTENSIONS-032 | Table of Contents | [ExtensionCommandContext](#extensioncommandcontext) | extensions.md |
| G-PI-EXTENSIONS-033 | Table of Contents | [ExtensionAPI Methods](#extensionapimethods) | extensions.md |
| G-PI-EXTENSIONS-034 | Table of Contents | [State Management](#statemanagement) | extensions.md |
| G-PI-EXTENSIONS-035 | Table of Contents | [Custom Tools](#customtools) | extensions.md |
| G-PI-EXTENSIONS-036 | Table of Contents | [Custom UI](#customui) | extensions.md |
| G-PI-EXTENSIONS-037 | Table of Contents | [Error Handling](#errorhandling) | extensions.md |
| G-PI-EXTENSIONS-038 | Table of Contents | [Mode Behavior](#modebehavior) | extensions.md |
| G-PI-EXTENSIONS-039 | Table of Contents | [Examples Reference](#examplesreference) | extensions.md |
| G-PI-EXTENSIONS-040 | Extension Styles | Single file  simplest, for small extensions: | extensions.md |
| G-PI-EXTENSIONS-041 | Extension Styles | Directory with index.ts  for multifile extensions: | extensions.md |
| G-PI-EXTENSIONS-042 | Extension Styles | Package with dependencies  for extensions that need npm packages: | extensions.md |
| G-PI-EXTENSIONS-043 | message_start / message_update / message_end | `message_start` and `message_end` fire for user, assistant, and toolResult messages. | extensions.md |
| G-PI-EXTENSIONS-044 | message_start / message_update / message_end | `message_update` fires for assistant streaming updates. | extensions.md |
| G-PI-EXTENSIONS-045 | message_start / message_update / message_end | `message_end` handlers can return `{ message }` to replace the finalized message. The replacement must keep the same `role`. | extensions.md |
| G-PI-EXTENSIONS-046 | tool_execution_start / tool_execution_update / tool_execution_end | `tool_execution_start` is emitted in assistant source order during the preflight phase | extensions.md |
| G-PI-EXTENSIONS-047 | tool_execution_start / tool_execution_update / tool_execution_end | `tool_execution_update` events may interleave across tools | extensions.md |
| G-PI-EXTENSIONS-048 | tool_execution_start / tool_execution_update / tool_execution_end | `tool_execution_end` is emitted in tool completion order after each tool is finalized | extensions.md |
| G-PI-EXTENSIONS-049 | tool_execution_start / tool_execution_update / tool_execution_end | final `toolResult` message events are still emitted later in assistant source order | extensions.md |
| G-PI-EXTENSIONS-050 | tool_call | Mutations to `event.input` affect the actual tool execution | extensions.md |
| G-PI-EXTENSIONS-051 | tool_call | Later `tool_call` handlers see mutations made by earlier handlers | extensions.md |
| G-PI-EXTENSIONS-052 | tool_call | No revalidation is performed after your mutation | extensions.md |
| G-PI-EXTENSIONS-053 | tool_call | Return values from `tool_call` only control blocking via `{ block: true, reason?: string }` | extensions.md |
| G-PI-EXTENSIONS-054 | tool_result | Handlers run in extension load order | extensions.md |
| G-PI-EXTENSIONS-055 | tool_result | Each handler sees the latest result after previous handler changes | extensions.md |
| G-PI-EXTENSIONS-056 | tool_result | Handlers can return partial patches (`content`, `details`, or `isError`); omitted fields keep their current values | extensions.md |
| G-PI-EXTENSIONS-057 | input | Processing order: | extensions.md |
| G-PI-EXTENSIONS-058 | input | Results: | extensions.md |
| G-PI-EXTENSIONS-059 | input | `continue`  pass through unchanged (default if handler returns nothing) | extensions.md |
| G-PI-EXTENSIONS-060 | input | `transform`  modify text/images, then continue to expansion | extensions.md |
| G-PI-EXTENSIONS-061 | input | `handled`  skip agent entirely (first handler to return this wins) | extensions.md |
| G-PI-EXTENSIONS-062 | ctx.signal | `fetch(..., { signal: ctx.signal })` | extensions.md |
| G-PI-EXTENSIONS-063 | ctx.signal | model calls that accept `signal` | extensions.md |
| G-PI-EXTENSIONS-064 | ctx.signal | file or process helpers that accept `AbortSignal` | extensions.md |
| G-PI-EXTENSIONS-065 | ctx.shutdown() | Interactive mode: Deferred until the agent becomes idle (after processing all queued steering and followup messages). | extensions.md |
| G-PI-EXTENSIONS-066 | ctx.shutdown() | RPC mode: Deferred until the next idle state (after completing the current command response, when waiting for the next command). | extensions.md |
| G-PI-EXTENSIONS-067 | ctx.shutdown() | Print mode: Noop. The process exits automatically when all prompts are processed. | extensions.md |
| G-PI-EXTENSIONS-068 | ctx.getSystemPrompt() | During `before_agent_start`, this reflects chained systemprompt changes made so far for the current turn. | extensions.md |
| G-PI-EXTENSIONS-069 | ctx.getSystemPrompt() | It does not include later `context` message mutations. | extensions.md |
| G-PI-EXTENSIONS-070 | ctx.getSystemPrompt() | It does not include `before_provider_request` payload rewrites. | extensions.md |
| G-PI-EXTENSIONS-071 | ctx.getSystemPrompt() | If laterloaded extensions run after yours, they can still change what is ultimately sent. | extensions.md |
| G-PI-EXTENSIONS-072 | ctx.newSession(options?) | `parentSession`: parent session file to record in the new session header | extensions.md |
| G-PI-EXTENSIONS-073 | ctx.newSession(options?) | `setup`: mutate the new session's `SessionManager` before `withSession` runs | extensions.md |
| G-PI-EXTENSIONS-074 | ctx.newSession(options?) | `withSession`: run postswitch work against a fresh replacementsession context. Do not use captured old `pi` / command `ctx`; see [Session replacement lifecycle and footguns](#sessionreplacementlifecycleandfootguns). | extensions.md |
| G-PI-EXTENSIONS-075 | ctx.fork(entryId, options?) | `position`: `"before"` (default) forks before the selected user message, restoring that prompt into the editor | extensions.md |
| G-PI-EXTENSIONS-076 | ctx.fork(entryId, options?) | `position`: `"at"` duplicates the active path through the selected entry without restoring editor text | extensions.md |
| G-PI-EXTENSIONS-077 | ctx.fork(entryId, options?) | `withSession`: run postswitch work against a fresh replacementsession context. Do not use captured old `pi` / command `ctx`; see [Session replacement lifecycle and footguns](#sessionreplacementlifecycleandfootguns). | extensions.md |
| G-PI-EXTENSIONS-078 | ctx.navigateTree(targetId, options?) | `summarize`: Whether to generate a summary of the abandoned branch | extensions.md |
| G-PI-EXTENSIONS-079 | ctx.navigateTree(targetId, options?) | `customInstructions`: Custom instructions for the summarizer | extensions.md |
| G-PI-EXTENSIONS-080 | ctx.navigateTree(targetId, options?) | `replaceInstructions`: If true, `customInstructions` replaces the default prompt instead of being appended | extensions.md |
| G-PI-EXTENSIONS-081 | ctx.navigateTree(targetId, options?) | `label`: Label to attach to the branch summary entry (or target entry if not summarizing) | extensions.md |
| G-PI-EXTENSIONS-082 | ctx.switchSession(sessionPath, options?) | `withSession`: run postswitch work against a fresh replacementsession context. Do not use captured old `pi` / command `ctx`; see [Session replacement lifecycle and footguns](#sessionreplacementlifecycleandfootguns). | extensions.md |
| G-PI-EXTENSIONS-083 | Session replacement lifecycle and footguns | `withSession` runs only after the old session has emitted `session_shutdown`, the old runtime has been torn down, the replacement session has been rebound, and the new extension instance has already received `session_start`. | extensions.md |
| G-PI-EXTENSIONS-084 | Session replacement lifecycle and footguns | The callback still executes in the original closure, not inside the new extension instance. That means your old extension instance may already have run its shutdown cleanup before `withSession` starts. | extensions.md |
| G-PI-EXTENSIONS-085 | Session replacement lifecycle and footguns | Captured old `pi` / old command `ctx` sessionbound objects are stale after replacement and will throw if used. Use only the `ctx` passed to `withSession` for sessionbound work. | extensions.md |
| G-PI-EXTENSIONS-086 | Session replacement lifecycle and footguns | Previously extracted raw objects are still your responsibility. For example, if you capture `const sm = ctx.sessionManager` before replacement, `sm` is still the old `SessionManager` object. Do not reuse it after replacement. | extensions.md |
| G-PI-EXTENSIONS-087 | Session replacement lifecycle and footguns | Code in `withSession` should assume any state invalidated by your `session_shutdown` handler is already gone. Only capture plain data that survives shutdown cleanly, such as strings, ids, and serialized config. | extensions.md |
| G-PI-EXTENSIONS-088 | ctx.reload() | `await ctx.reload()` emits `session_shutdown` for the current extension runtime | extensions.md |
| G-PI-EXTENSIONS-089 | ctx.reload() | It then reloads resources and emits `session_start` with `reason: "reload"` and `resources_discover` with reason `"reload"` | extensions.md |
| G-PI-EXTENSIONS-090 | ctx.reload() | The currently running command handler still continues in the old call frame | extensions.md |
| G-PI-EXTENSIONS-091 | ctx.reload() | Code after `await ctx.reload()` still runs from the prereload version | extensions.md |
| G-PI-EXTENSIONS-092 | ctx.reload() | Code after `await ctx.reload()` must not assume old inmemory extension state is still valid | extensions.md |
| G-PI-EXTENSIONS-093 | ctx.reload() | After the handler returns, future commands/events/tool calls use the new extension version | extensions.md |
| G-PI-EXTENSIONS-094 | pi.registerTool(definition) | Important: `promptGuidelines` bullets are appended flat to the `Guidelines` section with no tool name prefix. Each guideline must name the tool it refers to — avoid "Use this tool when..." because the LLM cannot tell which tool "this" means. Write "Use my_tool when..." instead. | extensions.md |
| G-PI-EXTENSIONS-095 | pi.sendMessage(message, options?) | Options: | extensions.md |
| G-PI-EXTENSIONS-096 | pi.sendMessage(message, options?) | `deliverAs`  Delivery mode: | extensions.md |
| G-PI-EXTENSIONS-097 | pi.sendMessage(message, options?) | `"steer"` (default)  Queues the message while streaming. Delivered after the current assistant turn finishes executing its tool calls, before the next LLM call. | extensions.md |
| G-PI-EXTENSIONS-098 | pi.sendMessage(message, options?) | `"followUp"`  Waits for agent to finish. Delivered only when agent has no more tool calls. | extensions.md |
| G-PI-EXTENSIONS-099 | pi.sendMessage(message, options?) | `"nextTurn"`  Queued for next user prompt. Does not interrupt or trigger anything. | extensions.md |
| G-PI-EXTENSIONS-100 | pi.sendMessage(message, options?) | `triggerTurn: true`  If agent is idle, trigger an LLM response immediately. Only applies to `"steer"` and `"followUp"` modes (ignored for `"nextTurn"`). | extensions.md |
| G-PI-EXTENSIONS-101 | pi.sendUserMessage(content, options?) | Options: | extensions.md |
| G-PI-EXTENSIONS-102 | pi.sendUserMessage(content, options?) | `deliverAs`  Required when agent is streaming: | extensions.md |
| G-PI-EXTENSIONS-103 | pi.sendUserMessage(content, options?) | `"steer"`  Queues the message for delivery after the current assistant turn finishes executing its tool calls | extensions.md |
| G-PI-EXTENSIONS-104 | pi.sendUserMessage(content, options?) | `"followUp"`  Waits for agent to finish all tools | extensions.md |
| G-PI-EXTENSIONS-105 | pi.getActiveTools() / pi.getAllTools() / pi.setActiveTools(names) | `builtin` for builtin tools | extensions.md |
| G-PI-EXTENSIONS-106 | pi.getActiveTools() / pi.getAllTools() / pi.setActiveTools(names) | `sdk` for tools passed via `createAgentSession({ customTools })` | extensions.md |
| G-PI-EXTENSIONS-107 | pi.getActiveTools() / pi.getAllTools() / pi.setActiveTools(names) | extension source metadata for tools registered by extensions | extensions.md |
| G-PI-EXTENSIONS-108 | pi.registerProvider(name, config) | Config options: | extensions.md |
| G-PI-EXTENSIONS-109 | pi.registerProvider(name, config) | `name`  Display name for the provider in UI such as `/login`. | extensions.md |
| G-PI-EXTENSIONS-110 | pi.registerProvider(name, config) | `baseUrl`  API endpoint URL. Required when defining models. | extensions.md |
| G-PI-EXTENSIONS-111 | pi.registerProvider(name, config) | `apiKey`  API key or environment variable name. Required when defining models (unless `oauth` provided). | extensions.md |
| G-PI-EXTENSIONS-112 | pi.registerProvider(name, config) | `api`  API type: `"anthropicmessages"`, `"openaicompletions"`, `"openairesponses"`, etc. | extensions.md |
| G-PI-EXTENSIONS-113 | pi.registerProvider(name, config) | `headers`  Custom headers to include in requests. | extensions.md |
| G-PI-EXTENSIONS-114 | pi.registerProvider(name, config) | `authHeader`  If true, adds `Authorization: Bearer` header automatically. | extensions.md |
| G-PI-EXTENSIONS-115 | pi.registerProvider(name, config) | `models`  Array of model definitions. If provided, replaces all existing models for this provider. Model definitions can set `baseUrl` to override the provider endpoint for that model. | extensions.md |
| G-PI-EXTENSIONS-116 | pi.registerProvider(name, config) | `oauth`  OAuth provider config for `/login` support. When provided, the provider appears in the login menu. | extensions.md |
| G-PI-EXTENSIONS-117 | pi.registerProvider(name, config) | `streamSimple`  Custom streaming implementation for nonstandard APIs. | extensions.md |
| G-PI-EXTENSIONS-118 | Custom Tools | Important: `promptGuidelines` bullets are appended flat to the `Guidelines` section with no tool name prefix or grouping. Each guideline must name the tool it refers to — avoid "Use this tool when..." because the LLM cannot tell which tool "this" means. Write "Use my_tool when..." instead. | extensions.md |
| G-PI-EXTENSIONS-119 | Tool Definition | Signaling errors: To mark a tool execution as failed (sets `isError: true` on the result and reports it to the LLM), throw an error from `execute`. Returning a value never sets the error flag regardless of what properties you include in the return object. | extensions.md |
| G-PI-EXTENSIONS-120 | Tool Definition | Early termination: Return `terminate: true` from `execute()` to hint that the automatic followup LLM call should be skipped after the current tool batch. This only takes effect when every finalized tool result in that batch is terminating. See [examples/extensions/structuredoutput.ts](../examples/extensions/structuredoutput.ts) for a minimal example where the agent ends on a final structuredoutput tool call. | extensions.md |
| G-PI-EXTENSIONS-121 | Tool Definition | Important: Use `StringEnum` from `@mariozechner/piai` for string enums. `Type.Union`/`Type.Literal` doesn't work with Google's API. | extensions.md |
| G-PI-EXTENSIONS-122 | Tool Definition | Argument preparation: `prepareArguments(args)` is optional. If defined, it runs before schema validation and before `execute()`. Use it to mimic an older accepted input shape when pi resumes an older session whose stored tool call arguments no longer match the current schema. Return the object you want validated against `parameters`. Keep the public schema strict. Do not add deprecated compatibility fields to `parameters` just to keep old resumed sessions working. | extensions.md |
| G-PI-EXTENSIONS-123 | No built-in tools, only extension tools | Rendering: Builtin renderer inheritance is resolved per slot. Execution override and rendering override are independent. If your override omits `renderCall`, the builtin `renderCall` is used. If your override omits `renderResult`, the builtin `renderResult` is used. If your override omits both, the builtin renderer is used automatically (syntax highlighting, diffs, etc.). This lets you wrap builtin tools for logging or access control without reimplementing the UI. | extensions.md |
| G-PI-EXTENSIONS-124 | No built-in tools, only extension tools | Prompt metadata: `promptSnippet` and `promptGuidelines` are not inherited from the builtin tool. If your override should keep those prompt instructions, define them on the override explicitly. | extensions.md |
| G-PI-EXTENSIONS-125 | No built-in tools, only extension tools | Your implementation must match the exact result shape, including the `details` type. The UI and session logic depend on these shapes for rendering and state tracking. | extensions.md |
| G-PI-EXTENSIONS-126 | No built-in tools, only extension tools | [read.ts](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/tools/read.ts)  `ReadToolDetails` | extensions.md |
| G-PI-EXTENSIONS-127 | No built-in tools, only extension tools | [bash.ts](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/tools/bash.ts)  `BashToolDetails` | extensions.md |
| G-PI-EXTENSIONS-128 | No built-in tools, only extension tools | [edit.ts](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/tools/edit.ts) | extensions.md |
| G-PI-EXTENSIONS-129 | No built-in tools, only extension tools | [write.ts](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/tools/write.ts) | extensions.md |
| G-PI-EXTENSIONS-130 | No built-in tools, only extension tools | [grep.ts](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/tools/grep.ts)  `GrepToolDetails` | extensions.md |
| G-PI-EXTENSIONS-131 | No built-in tools, only extension tools | [find.ts](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/tools/find.ts)  `FindToolDetails` | extensions.md |
| G-PI-EXTENSIONS-132 | No built-in tools, only extension tools | [ls.ts](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/tools/ls.ts)  `LsToolDetails` | extensions.md |
| G-PI-EXTENSIONS-133 | Remote Execution | Operations interfaces: `ReadOperations`, `WriteOperations`, `EditOperations`, `BashOperations`, `LsOperations`, `GrepOperations`, `FindOperations` | extensions.md |
| G-PI-EXTENSIONS-134 | Output Truncation | Tools MUST truncate their output to avoid overwhelming the LLM context. Large outputs can cause: | extensions.md |
| G-PI-EXTENSIONS-135 | Output Truncation | Context overflow errors (prompt too long) | extensions.md |
| G-PI-EXTENSIONS-136 | Output Truncation | Compaction failures | extensions.md |
| G-PI-EXTENSIONS-137 | Output Truncation | Degraded model performance | extensions.md |
| G-PI-EXTENSIONS-138 | Output Truncation | Key points: | extensions.md |
| G-PI-EXTENSIONS-139 | Output Truncation | Use `truncateHead` for content where the beginning matters (search results, file reads) | extensions.md |
| G-PI-EXTENSIONS-140 | Output Truncation | Use `truncateTail` for content where the end matters (logs, command output) | extensions.md |
| G-PI-EXTENSIONS-141 | Output Truncation | Always inform the LLM when output is truncated and where to find the full version | extensions.md |
| G-PI-EXTENSIONS-142 | Output Truncation | Document the truncation limits in your tool's description | extensions.md |
| G-PI-EXTENSIONS-143 | Custom Rendering | `args`  the current tool call arguments | extensions.md |
| G-PI-EXTENSIONS-144 | Custom Rendering | `state`  shared rowlocal state across `renderCall` and `renderResult` | extensions.md |
| G-PI-EXTENSIONS-145 | Custom Rendering | `lastComponent`  the previously returned component for that slot, if any | extensions.md |
| G-PI-EXTENSIONS-146 | Custom Rendering | `invalidate()`  request a rerender of this tool row | extensions.md |
| G-PI-EXTENSIONS-147 | Custom Rendering | `toolCallId`, `cwd`, `executionStarted`, `argsComplete`, `isPartial`, `expanded`, `showImages`, `isError` | extensions.md |
| G-PI-EXTENSIONS-148 | Keybinding Hints | `keyHint(keybinding, description)`  Formats a configured keybinding id such as `"app.tools.expand"` or `"tui.select.confirm"` | extensions.md |
| G-PI-EXTENSIONS-149 | Keybinding Hints | `keyText(keybinding)`  Returns the raw configured key text for a keybinding id | extensions.md |
| G-PI-EXTENSIONS-150 | Keybinding Hints | `rawKeyHint(key, description)`  Format a raw key string | extensions.md |
| G-PI-EXTENSIONS-151 | Keybinding Hints | Codingagent ids use the `app.` namespace, for example `app.tools.expand`, `app.editor.external`, `app.session.rename` | extensions.md |
| G-PI-EXTENSIONS-152 | Keybinding Hints | Shared TUI ids use the `tui.` namespace, for example `tui.select.confirm`, `tui.select.cancel`, `tui.input.tab` | extensions.md |
| G-PI-EXTENSIONS-153 | Best Practices | Use `Text` with padding `(0, 0)`. The default Box handles padding. | extensions.md |
| G-PI-EXTENSIONS-154 | Best Practices | Use `\n` for multiline content. | extensions.md |
| G-PI-EXTENSIONS-155 | Best Practices | Handle `isPartial` for streaming progress. | extensions.md |
| G-PI-EXTENSIONS-156 | Best Practices | Support `expanded` for detail on demand. | extensions.md |
| G-PI-EXTENSIONS-157 | Best Practices | Keep default view compact. | extensions.md |
| G-PI-EXTENSIONS-158 | Best Practices | Read `context.args` in `renderResult` instead of copying args into `context.state`. | extensions.md |
| G-PI-EXTENSIONS-159 | Best Practices | Use `context.state` only for data that must be shared across call and result slots. | extensions.md |
| G-PI-EXTENSIONS-160 | Best Practices | Reuse `context.lastComponent` when the same component instance can be updated in place. | extensions.md |
| G-PI-EXTENSIONS-161 | Best Practices | Use `renderShell: "self"` only when the default boxed shell gets in the way. In selfshell mode the tool is responsible for its own framing, padding, and background. | extensions.md |
| G-PI-EXTENSIONS-162 | Fallback | `renderCall`: Shows the tool name | extensions.md |
| G-PI-EXTENSIONS-163 | Fallback | `renderResult`: Shows raw text from `content` | extensions.md |
| G-PI-EXTENSIONS-164 | Custom UI | For custom components, see [tui.md](tui.md) which has copypaste patterns for: | extensions.md |
| G-PI-EXTENSIONS-165 | Custom UI | Selection dialogs (SelectList) | extensions.md |
| G-PI-EXTENSIONS-166 | Custom UI | Async operations with cancel (BorderedLoader) | extensions.md |
| G-PI-EXTENSIONS-167 | Custom UI | Settings toggles (SettingsList) | extensions.md |
| G-PI-EXTENSIONS-168 | Custom UI | Status indicators (setStatus) | extensions.md |
| G-PI-EXTENSIONS-169 | Custom UI | Working message, visibility, and indicator during streaming (`setWorkingMessage`, `setWorkingVisible`, `setWorkingIndicator`) | extensions.md |
| G-PI-EXTENSIONS-170 | Custom UI | Widgets above/below editor (setWidget) | extensions.md |
| G-PI-EXTENSIONS-171 | Custom UI | Autocomplete providers layered on top of builtin slash/path completion (addAutocompleteProvider) | extensions.md |
| G-PI-EXTENSIONS-172 | Custom UI | Custom footers (setFooter) | extensions.md |
| G-PI-EXTENSIONS-173 | Timed Dialogs with Countdown | Return values on timeout: | extensions.md |
| G-PI-EXTENSIONS-174 | Timed Dialogs with Countdown | `select()` returns `undefined` | extensions.md |
| G-PI-EXTENSIONS-175 | Timed Dialogs with Countdown | `confirm()` returns `false` | extensions.md |
| G-PI-EXTENSIONS-176 | Timed Dialogs with Countdown | `input()` returns `undefined` | extensions.md |
| G-PI-EXTENSIONS-177 | Autocomplete Providers | inspect the text before the cursor | extensions.md |
| G-PI-EXTENSIONS-178 | Autocomplete Providers | return your own suggestions when your extensionspecific syntax matches | extensions.md |
| G-PI-EXTENSIONS-179 | Autocomplete Providers | otherwise delegate to `current.getSuggestions(...)` | extensions.md |
| G-PI-EXTENSIONS-180 | Autocomplete Providers | delegate `applyCompletion(...)` unless you need custom insertion behavior | extensions.md |
| G-PI-EXTENSIONS-181 | Custom Components | `tui`  TUI instance (for screen dimensions, focus management) | extensions.md |
| G-PI-EXTENSIONS-182 | Custom Components | `theme`  Current theme for styling | extensions.md |
| G-PI-EXTENSIONS-183 | Custom Components | `keybindings`  App keybinding manager (for checking shortcuts) | extensions.md |
| G-PI-EXTENSIONS-184 | Custom Components | `done(value)`  Call to close component and return value | extensions.md |
| G-PI-EXTENSIONS-185 | Custom Editor | Key points: | extensions.md |
| G-PI-EXTENSIONS-186 | Custom Editor | Extend `CustomEditor` (not base `Editor`) to get app keybindings (escape to abort, ctrl+d, model switching) | extensions.md |
| G-PI-EXTENSIONS-187 | Custom Editor | Call `super.handleInput(data)` for keys you don't handle | extensions.md |
| G-PI-EXTENSIONS-188 | Custom Editor | Factory receives `theme` and `keybindings` from the app | extensions.md |
| G-PI-EXTENSIONS-189 | Custom Editor | Use `ctx.ui.getEditorComponent()` before `setEditorComponent()` to wrap the previously configured custom editor | extensions.md |
| G-PI-EXTENSIONS-190 | Custom Editor | Pass `undefined` to restore default: `ctx.ui.setEditorComponent(undefined)` | extensions.md |
| G-PI-EXTENSIONS-191 | Error Handling | Extension errors are logged, agent continues | extensions.md |
| G-PI-EXTENSIONS-192 | Error Handling | `tool_call` errors block the tool (failsafe) | extensions.md |
| G-PI-EXTENSIONS-193 | Error Handling | Tool `execute` errors must be signaled by throwing; the thrown error is caught, reported to the LLM with `isError: true`, and execution continues | extensions.md |
| G-PI-INDEX-001 | Start here | [Quickstart](quickstart.md)  install, authenticate, and run a first session. | index.md |
| G-PI-INDEX-002 | Start here | [Using Pi](usage.md)  interactive mode, slash commands, context files, and CLI reference. | index.md |
| G-PI-INDEX-003 | Start here | [Providers](providers.md)  subscription and APIkey setup for builtin providers. | index.md |
| G-PI-INDEX-004 | Start here | [Settings](settings.md)  global and project settings. | index.md |
| G-PI-INDEX-005 | Start here | [Keybindings](keybindings.md)  default shortcuts and custom keybindings. | index.md |
| G-PI-INDEX-006 | Start here | [Sessions](sessions.md)  session management, branching, and tree navigation. | index.md |
| G-PI-INDEX-007 | Start here | [Compaction](compaction.md)  context compaction and branch summarization. | index.md |
| G-PI-INDEX-008 | Customization | [Extensions](extensions.md)  TypeScript modules for tools, commands, events, and custom UI. | index.md |
| G-PI-INDEX-009 | Customization | [Skills](skills.md)  Agent Skills for reusable ondemand capabilities. | index.md |
| G-PI-INDEX-010 | Customization | [Prompt templates](prompttemplates.md)  reusable prompts that expand from slash commands. | index.md |
| G-PI-INDEX-011 | Customization | [Themes](themes.md)  builtin and custom terminal themes. | index.md |
| G-PI-INDEX-012 | Customization | [Pi packages](packages.md)  bundle and share extensions, skills, prompts, and themes. | index.md |
| G-PI-INDEX-013 | Customization | [Custom models](models.md)  add model entries for supported provider APIs. | index.md |
| G-PI-INDEX-014 | Customization | [Custom providers](customprovider.md)  implement custom APIs and OAuth flows. | index.md |
| G-PI-INDEX-015 | Programmatic usage | [SDK](sdk.md)  embed pi in Node.js applications. | index.md |
| G-PI-INDEX-016 | Programmatic usage | [RPC mode](rpc.md)  integrate over stdin/stdout JSONL. | index.md |
| G-PI-INDEX-017 | Programmatic usage | [JSON event stream mode](json.md)  print mode with structured events. | index.md |
| G-PI-INDEX-018 | Programmatic usage | [TUI components](tui.md)  build custom terminal UI for extensions. | index.md |
| G-PI-INDEX-019 | Reference | [Session format](sessionformat.md)  JSONL session file format, entry types, and SessionManager API. | index.md |
| G-PI-INDEX-020 | Platform setup | [Windows](windows.md) | index.md |
| G-PI-INDEX-021 | Platform setup | [Termux on Android](termux.md) | index.md |
| G-PI-INDEX-022 | Platform setup | [tmux](tmux.md) | index.md |
| G-PI-INDEX-023 | Platform setup | [Terminal setup](terminalsetup.md) | index.md |
| G-PI-INDEX-024 | Platform setup | [Shell aliases](shellaliases.md) | index.md |
| G-PI-INDEX-025 | Development | [Development](development.md)  local setup, project structure, and debugging. | index.md |
| G-PI-JSON-001 | Message Types | `UserMessage` (line 134) | json.md |
| G-PI-JSON-002 | Message Types | `AssistantMessage` (line 140) | json.md |
| G-PI-JSON-003 | Message Types | `ToolResultMessage` (line 152) | json.md |
| G-PI-JSON-004 | Message Types | `BashExecutionMessage` (line 29) | json.md |
| G-PI-JSON-005 | Message Types | `CustomMessage` (line 46) | json.md |
| G-PI-JSON-006 | Message Types | `BranchSummaryMessage` (line 55) | json.md |
| G-PI-JSON-007 | Message Types | `CompactionSummaryMessage` (line 62) | json.md |
| G-PI-KEYBINDINGS-001 | Key Format | Letters: `az` | keybindings.md |
| G-PI-KEYBINDINGS-002 | Key Format | Digits: `09` | keybindings.md |
| G-PI-KEYBINDINGS-003 | Key Format | Special: `escape`, `esc`, `enter`, `return`, `tab`, `space`, `backspace`, `delete`, `insert`, `clear`, `home`, `end`, `pageUp`, `pageDown`, `up`, `down`, `left`, `right` | keybindings.md |
| G-PI-KEYBINDINGS-004 | Key Format | Function: `f1``f12` | keybindings.md |
| G-PI-KEYBINDINGS-005 | Key Format | Symbols: `` ` ``, ``, `=`, `[`, `]`, `\`, `;`, `'`, `,`, `.`, `/`, `!`, `@`, `#`, `$`, `%`, `^`, `&`, ``, `(`, `)`, `_`, `+`, `|`, `~`, `{`, `}`, `:`, `<`, `>`, `?` | keybindings.md |
| G-PI-MODELS-001 | Table of Contents | [Minimal Example](#minimalexample) | models.md |
| G-PI-MODELS-002 | Table of Contents | [Full Example](#fullexample) | models.md |
| G-PI-MODELS-003 | Table of Contents | [Supported APIs](#supportedapis) | models.md |
| G-PI-MODELS-004 | Table of Contents | [Provider Configuration](#providerconfiguration) | models.md |
| G-PI-MODELS-005 | Table of Contents | [Model Configuration](#modelconfiguration) | models.md |
| G-PI-MODELS-006 | Table of Contents | [Overriding Builtin Providers](#overridingbuiltinproviders) | models.md |
| G-PI-MODELS-007 | Table of Contents | [Permodel Overrides](#permodeloverrides) | models.md |
| G-PI-MODELS-008 | Table of Contents | [Anthropic Messages Compatibility](#anthropicmessagescompatibility) | models.md |
| G-PI-MODELS-009 | Table of Contents | [OpenAI Compatibility](#openaicompatibility) | models.md |
| G-PI-MODELS-010 | Value Resolution | Shell command: `"!command"` executes and uses stdout | models.md |
| G-PI-MODELS-011 | Value Resolution | Environment variable: Uses the value of the named variable | models.md |
| G-PI-MODELS-012 | Value Resolution | Literal value: Used directly | models.md |
| G-PI-MODELS-013 | Model Configuration | `/model` and `listmodels` list entries by model `id`. | models.md |
| G-PI-MODELS-014 | Model Configuration | The configured `name` is used for model matching and detail/status text. | models.md |
| G-PI-MODELS-015 | Overriding Built-in Providers | Builtin models are kept. | models.md |
| G-PI-MODELS-016 | Overriding Built-in Providers | Custom models are upserted by `id` within the provider. | models.md |
| G-PI-MODELS-017 | Overriding Built-in Providers | If a custom model `id` matches a builtin model `id`, the custom model replaces that builtin model. | models.md |
| G-PI-MODELS-018 | Overriding Built-in Providers | If a custom model `id` is new, it is added alongside builtin models. | models.md |
| G-PI-MODELS-019 | Per-model Overrides | `modelOverrides` are applied to builtin provider models. | models.md |
| G-PI-MODELS-020 | Per-model Overrides | Unknown model IDs are ignored. | models.md |
| G-PI-MODELS-021 | Per-model Overrides | You can combine providerlevel `baseUrl`/`headers` with `modelOverrides`. | models.md |
| G-PI-MODELS-022 | Per-model Overrides | If `models` is also defined for a provider, custom models are merged after builtin overrides. A custom model with the same `id` replaces the overridden builtin model entry. | models.md |
| G-PI-MODELS-023 | OpenAI Compatibility | Providerlevel `compat` applies defaults to all models under that provider. | models.md |
| G-PI-MODELS-024 | OpenAI Compatibility | Modellevel `compat` overrides providerlevel values for that model. | models.md |
| G-PI-PROMPT-TEMPLATES-001 | Locations | Global: `~/.pi/agent/prompts/.md` | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-002 | Locations | Project: `.pi/prompts/.md` | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-003 | Locations | Packages: `prompts/` directories or `pi.prompts` entries in `package.json` | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-004 | Locations | Settings: `prompts` array with files or directories | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-005 | Locations | CLI: `prompttemplate <path>` (repeatable) | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-006 | Format | Bugs and logic errors | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-007 | Format | Security issues | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-008 | Format | Error handling gaps | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-009 | Format | The filename becomes the command name. `review.md` becomes `/review`. | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-010 | Format | `description` is optional. If missing, the first nonempty line is used. | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-011 | Format | `argumenthint` is optional. When set, the hint is displayed before the description in the autocomplete dropdown. | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-012 | Arguments | `$1`, `$2`, ... positional args | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-013 | Arguments | `$@` or `$ARGUMENTS` for all args joined | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-014 | Arguments | `${@:N}` for args from the Nth position (1indexed) | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-015 | Arguments | `${@:N:L}` for `L` args starting at N | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-016 | Loading Rules | Template discovery in `prompts/` is nonrecursive. | prompt-templates.md |
| G-PI-PROMPT-TEMPLATES-017 | Loading Rules | If you want templates in subdirectories, add them explicitly via `prompts` settings or a package manifest. | prompt-templates.md |
| G-PI-PROVIDERS-001 | Table of Contents | [Subscriptions](#subscriptions) | providers.md |
| G-PI-PROVIDERS-002 | Table of Contents | [API Keys](#apikeys) | providers.md |
| G-PI-PROVIDERS-003 | Table of Contents | [Auth File](#authfile) | providers.md |
| G-PI-PROVIDERS-004 | Table of Contents | [Cloud Providers](#cloudproviders) | providers.md |
| G-PI-PROVIDERS-005 | Table of Contents | [Custom Providers](#customproviders) | providers.md |
| G-PI-PROVIDERS-006 | Table of Contents | [Resolution Order](#resolutionorder) | providers.md |
| G-PI-PROVIDERS-007 | Subscriptions | ChatGPT Plus/Pro (Codex) | providers.md |
| G-PI-PROVIDERS-008 | Subscriptions | Claude Pro/Max | providers.md |
| G-PI-PROVIDERS-009 | Subscriptions | GitHub Copilot | providers.md |
| G-PI-PROVIDERS-010 | OpenAI Codex | Requires ChatGPT Plus or Pro subscription | providers.md |
| G-PI-PROVIDERS-011 | OpenAI Codex | Officially endorsed by OpenAI: [Codex for OSS](https://developers.openai.com/community/codexfoross) | providers.md |
| G-PI-PROVIDERS-012 | GitHub Copilot | Press Enter for github.com, or enter your GitHub Enterprise Server domain | providers.md |
| G-PI-PROVIDERS-013 | GitHub Copilot | If you get "model not supported", enable it in VS Code: Copilot Chat → model selector → select model → "Enable" | providers.md |
| G-PI-PROVIDERS-014 | Key Resolution | Shell command: `"!command"` executes and uses stdout (cached for process lifetime) | providers.md |
| G-PI-PROVIDERS-015 | Key Resolution | Environment variable: Uses the value of the named variable | providers.md |
| G-PI-PROVIDERS-016 | Key Resolution | Literal value: Used directly | providers.md |
| G-PI-PROVIDERS-017 | Custom Providers | Via models.json: Add Ollama, LM Studio, vLLM, or any provider that speaks a supported API (OpenAI Completions, OpenAI Responses, Anthropic Messages, Google Generative AI). See [models.md](models.md). | providers.md |
| G-PI-PROVIDERS-018 | Custom Providers | Via extensions: For providers that need custom API implementations or OAuth flows, create an extension. See [customprovider.md](customprovider.md) and [examples/extensions/customprovidergitlabduo](../examples/extensions/customprovidergitlabduo/). | providers.md |
| G-PI-QUICKSTART-001 | First session | `read`  read files | quickstart.md |
| G-PI-QUICKSTART-002 | First session | `write`  create or overwrite files | quickstart.md |
| G-PI-QUICKSTART-003 | First session | `edit`  patch files | quickstart.md |
| G-PI-QUICKSTART-004 | First session | `bash`  run shell commands | quickstart.md |
| G-PI-QUICKSTART-005 | Project Instructions | Run `npm run check` after code changes. | quickstart.md |
| G-PI-QUICKSTART-006 | Project Instructions | Do not run production migrations locally. | quickstart.md |
| G-PI-QUICKSTART-007 | Project Instructions | Keep responses concise. | quickstart.md |
| G-PI-QUICKSTART-008 | Project Instructions | `~/.pi/agent/AGENTS.md` for global instructions | quickstart.md |
| G-PI-QUICKSTART-009 | Project Instructions | `AGENTS.md` or `CLAUDE.md` from parent directories and the current directory | quickstart.md |
| G-PI-QUICKSTART-010 | Next steps | [Using Pi](usage.md)  interactive mode, slash commands, sessions, context files, and CLI reference. | quickstart.md |
| G-PI-QUICKSTART-011 | Next steps | [Providers](providers.md)  authentication and model setup. | quickstart.md |
| G-PI-QUICKSTART-012 | Next steps | [Settings](settings.md)  global and project configuration. | quickstart.md |
| G-PI-QUICKSTART-013 | Next steps | [Keybindings](keybindings.md)  shortcuts and customization. | quickstart.md |
| G-PI-QUICKSTART-014 | Next steps | [Pi Packages](packages.md)  install shared extensions, skills, prompts, and themes. | quickstart.md |
| G-PI-RPC-001 | RPC Mode | Note for Node.js/TypeScript users: If you're building a Node.js application, consider using `AgentSession` directly from `@mariozechner/picodingagent` instead of spawning a subprocess. See [`src/core/agentsession.ts`](../src/core/agentsession.ts) for the API. For a subprocessbased TypeScript client, see [`src/modes/rpc/rpcclient.ts`](../src/modes/rpc/rpcclient.ts). | rpc.md |
| G-PI-RPC-002 | Starting RPC Mode | `provider <name>`: Set the LLM provider (anthropic, openai, google, etc.) | rpc.md |
| G-PI-RPC-003 | Starting RPC Mode | `model <pattern>`: Model pattern or ID (supports `provider/id` and optional `:<thinking>`) | rpc.md |
| G-PI-RPC-004 | Starting RPC Mode | `nosession`: Disable session persistence | rpc.md |
| G-PI-RPC-005 | Starting RPC Mode | `sessiondir <path>`: Custom session storage directory | rpc.md |
| G-PI-RPC-006 | Protocol Overview | Commands: JSON objects sent to stdin, one per line | rpc.md |
| G-PI-RPC-007 | Protocol Overview | Responses: JSON objects with `type: "response"` indicating command success/failure | rpc.md |
| G-PI-RPC-008 | Protocol Overview | Events: Agent events streamed to stdout as JSON lines | rpc.md |
| G-PI-RPC-009 | Framing | Split records on `\n` only | rpc.md |
| G-PI-RPC-010 | Framing | Accept optional `\r\n` input by stripping a trailing `\r` | rpc.md |
| G-PI-RPC-011 | Framing | Do not use generic line readers that treat Unicode separators as newlines | rpc.md |
| G-PI-RPC-012 | prompt | During streaming: If the agent is already streaming, you must specify `streamingBehavior` to queue the message: | rpc.md |
| G-PI-RPC-013 | prompt | `"steer"`: Queue the message while the agent is running. It is delivered after the current assistant turn finishes executing its tool calls, before the next LLM call. | rpc.md |
| G-PI-RPC-014 | prompt | `"followUp"`: Wait until the agent finishes. Message is delivered only when agent stops. | rpc.md |
| G-PI-RPC-015 | prompt | Extension commands: If the message is an extension command (e.g., `/mycommand`), it executes immediately even during streaming. Extension commands manage their own LLM interaction via `pi.sendMessage()`. | rpc.md |
| G-PI-RPC-016 | prompt | Input expansion: Skill commands (`/skill:name`) and prompt templates (`/template`) are expanded before sending/queueing. | rpc.md |
| G-PI-RPC-017 | set_steering_mode | `"all"`: Deliver all steering messages after the current assistant turn finishes executing its tool calls | rpc.md |
| G-PI-RPC-018 | set_steering_mode | `"oneatatime"`: Deliver one steering message per completed assistant turn (default) | rpc.md |
| G-PI-RPC-019 | set_follow_up_mode | `"all"`: Deliver all followup messages when agent finishes | rpc.md |
| G-PI-RPC-020 | set_follow_up_mode | `"oneatatime"`: Deliver one followup message per agent completion (default) | rpc.md |
| G-PI-RPC-021 | bash | How bash results reach the LLM: | rpc.md |
| G-PI-RPC-022 | get_commands | `name`: Command name (invoke with `/name`) | rpc.md |
| G-PI-RPC-023 | get_commands | `description`: Humanreadable description (optional for extension commands) | rpc.md |
| G-PI-RPC-024 | get_commands | `source`: What kind of command: | rpc.md |
| G-PI-RPC-025 | get_commands | `"extension"`: Registered via `pi.registerCommand()` in an extension | rpc.md |
| G-PI-RPC-026 | get_commands | `"prompt"`: Loaded from a prompt template `.md` file | rpc.md |
| G-PI-RPC-027 | get_commands | `"skill"`: Loaded from a skill directory (name is prefixed with `skill:`) | rpc.md |
| G-PI-RPC-028 | get_commands | `location`: Where it was loaded from (optional, not present for extensions): | rpc.md |
| G-PI-RPC-029 | get_commands | `"user"`: Userlevel (`~/.pi/agent/`) | rpc.md |
| G-PI-RPC-030 | get_commands | `"project"`: Projectlevel (`./.pi/agent/`) | rpc.md |
| G-PI-RPC-031 | get_commands | `"path"`: Explicit path via CLI or settings | rpc.md |
| G-PI-RPC-032 | get_commands | `path`: Absolute file path to the command source (optional) | rpc.md |
| G-PI-RPC-033 | get_commands | Note: Builtin TUI commands (`/settings`, `/hotkeys`, etc.) are not included. They are handled only in interactive mode and would not execute if sent via `prompt`. | rpc.md |
| G-PI-RPC-034 | Extension UI Protocol | Dialog methods (`select`, `confirm`, `input`, `editor`): emit an `extension_ui_request` on stdout and block until the client sends back an `extension_ui_response` on stdin with the matching `id`. | rpc.md |
| G-PI-RPC-035 | Extension UI Protocol | Fireandforget methods (`notify`, `setStatus`, `setWidget`, `setTitle`, `set_editor_text`): emit an `extension_ui_request` on stdout but do not expect a response. The client can display the information or ignore it. | rpc.md |
| G-PI-RPC-036 | Extension UI Protocol | `custom()` returns `undefined` | rpc.md |
| G-PI-RPC-037 | Extension UI Protocol | `setWorkingMessage()`, `setWorkingIndicator()`, `setFooter()`, `setHeader()`, `setEditorComponent()`, `setToolsExpanded()` are noops | rpc.md |
| G-PI-RPC-038 | Extension UI Protocol | `getEditorText()` returns `""` | rpc.md |
| G-PI-RPC-039 | Extension UI Protocol | `getToolsExpanded()` returns `false` | rpc.md |
| G-PI-RPC-040 | Extension UI Protocol | `pasteToEditor()` delegates to `setEditorText()` (no paste/collapse handling) | rpc.md |
| G-PI-RPC-041 | Extension UI Protocol | `getAllThemes()` returns `[]` | rpc.md |
| G-PI-RPC-042 | Extension UI Protocol | `getTheme()` returns `undefined` | rpc.md |
| G-PI-RPC-043 | Extension UI Protocol | `setTheme()` returns `{ success: false, error: "..." }` | rpc.md |
| G-PI-RPC-044 | Types | [`packages/ai/src/types.ts`](../../ai/src/types.ts)  `Model`, `UserMessage`, `AssistantMessage`, `ToolResultMessage` | rpc.md |
| G-PI-RPC-045 | Types | [`packages/agent/src/types.ts`](../../agent/src/types.ts)  `AgentMessage`, `AgentEvent` | rpc.md |
| G-PI-RPC-046 | Types | [`src/core/messages.ts`](../src/core/messages.ts)  `BashExecutionMessage` | rpc.md |
| G-PI-RPC-047 | Types | [`src/modes/rpc/rpctypes.ts`](../src/modes/rpc/rpctypes.ts)  RPC command/response types, extension UI request/response types | rpc.md |
| G-PI-SDK-001 | SDK | Example use cases: | sdk.md |
| G-PI-SDK-002 | SDK | Build a custom UI (web, desktop, mobile) | sdk.md |
| G-PI-SDK-003 | SDK | Integrate agent capabilities into existing applications | sdk.md |
| G-PI-SDK-004 | SDK | Create automated pipelines with agent reasoning | sdk.md |
| G-PI-SDK-005 | SDK | Build custom tools that spawn subagents | sdk.md |
| G-PI-SDK-006 | SDK | Test agent behavior programmatically | sdk.md |
| G-PI-SDK-007 | createAgentSessionRuntime() and AgentSessionRuntime | `newSession()` | sdk.md |
| G-PI-SDK-008 | createAgentSessionRuntime() and AgentSessionRuntime | `switchSession()` | sdk.md |
| G-PI-SDK-009 | createAgentSessionRuntime() and AgentSessionRuntime | `fork()` | sdk.md |
| G-PI-SDK-010 | createAgentSessionRuntime() and AgentSessionRuntime | clone flows via `fork(entryId, { position: "at" })` | sdk.md |
| G-PI-SDK-011 | createAgentSessionRuntime() and AgentSessionRuntime | `importFromJsonl()` | sdk.md |
| G-PI-SDK-012 | createAgentSessionRuntime() and AgentSessionRuntime | `runtime.session` changes after those operations | sdk.md |
| G-PI-SDK-013 | createAgentSessionRuntime() and AgentSessionRuntime | event subscriptions are attached to a specific `AgentSession`, so resubscribe after replacement | sdk.md |
| G-PI-SDK-014 | createAgentSessionRuntime() and AgentSessionRuntime | if you use extensions, call `runtime.session.bindExtensions(...)` again for the new session | sdk.md |
| G-PI-SDK-015 | createAgentSessionRuntime() and AgentSessionRuntime | creation returns diagnostics on `runtime.diagnostics` | sdk.md |
| G-PI-SDK-016 | createAgentSessionRuntime() and AgentSessionRuntime | if runtime creation or replacement fails, the method throws and the caller decides how to handle it | sdk.md |
| G-PI-SDK-017 | Prompting and Message Queueing | `true` when the prompt was accepted, queued, or handled immediately | sdk.md |
| G-PI-SDK-018 | Prompting and Message Queueing | `false` when prompt preflight rejected before acceptance | sdk.md |
| G-PI-SDK-019 | Prompting and Message Queueing | Behavior: | sdk.md |
| G-PI-SDK-020 | Prompting and Message Queueing | Extension commands (e.g., `/mycommand`): Execute immediately, even during streaming. They manage their own LLM interaction via `pi.sendMessage()`. | sdk.md |
| G-PI-SDK-021 | Prompting and Message Queueing | Filebased prompt templates (from `.md` files): Expanded to their content before sending or queueing. | sdk.md |
| G-PI-SDK-022 | Prompting and Message Queueing | During streaming without `streamingBehavior`: Throws an error. Use `steer()` or `followUp()` directly, or specify the option. | sdk.md |
| G-PI-SDK-023 | Prompting and Message Queueing | `preflightResult(true)`: Means the prompt was accepted, queued, or handled immediately. | sdk.md |
| G-PI-SDK-024 | Prompting and Message Queueing | `preflightResult(false)`: Means preflight rejected before acceptance. | sdk.md |
| G-PI-SDK-025 | Directories | Project extensions (`.pi/extensions/`) | sdk.md |
| G-PI-SDK-026 | Directories | Project skills: | sdk.md |
| G-PI-SDK-027 | Directories | `.pi/skills/` | sdk.md |
| G-PI-SDK-028 | Directories | `.agents/skills/` in `cwd` and ancestor directories (up to git repo root, or filesystem root when not in a repo) | sdk.md |
| G-PI-SDK-029 | Directories | Project prompts (`.pi/prompts/`) | sdk.md |
| G-PI-SDK-030 | Directories | Context files (`AGENTS.md` walking up from cwd) | sdk.md |
| G-PI-SDK-031 | Directories | Session directory naming | sdk.md |
| G-PI-SDK-032 | Directories | Global extensions (`extensions/`) | sdk.md |
| G-PI-SDK-033 | Directories | Global skills: | sdk.md |
| G-PI-SDK-034 | Directories | `skills/` under `agentDir` (for example `~/.pi/agent/skills/`) | sdk.md |
| G-PI-SDK-035 | Directories | `~/.agents/skills/` | sdk.md |
| G-PI-SDK-036 | Directories | Global prompts (`prompts/`) | sdk.md |
| G-PI-SDK-037 | Directories | Global context file (`AGENTS.md`) | sdk.md |
| G-PI-SDK-038 | Directories | Settings (`settings.json`) | sdk.md |
| G-PI-SDK-039 | Directories | Custom models (`models.json`) | sdk.md |
| G-PI-SDK-040 | Directories | Credentials (`auth.json`) | sdk.md |
| G-PI-SDK-041 | Directories | Sessions (`sessions/`) | sdk.md |
| G-PI-SDK-042 | Tools with Custom cwd | Important: The prebuilt tool instances (`readTool`, `bashTool`, etc.) use `process.cwd()` for path resolution. When you specify a custom `cwd` AND provide explicit `tools`, you must use the tool factory functions to ensure paths resolve correctly: | sdk.md |
| G-PI-SDK-043 | Tools with Custom cwd | When you don't need factories: | sdk.md |
| G-PI-SDK-044 | Tools with Custom cwd | If you omit `tools`, pi automatically creates them with the correct `cwd` | sdk.md |
| G-PI-SDK-045 | Tools with Custom cwd | If you use `process.cwd()` as your `cwd`, the prebuilt instances work fine | sdk.md |
| G-PI-SDK-046 | Tools with Custom cwd | When you must use factories: | sdk.md |
| G-PI-SDK-047 | Tools with Custom cwd | When you specify both `cwd` (different from `process.cwd()`) AND `tools` | sdk.md |
| G-PI-SDK-048 | Extensions | Event Bus: Extensions can communicate via `pi.events`. Pass a shared `eventBus` to `DefaultResourceLoader` if you need to emit or listen from outside: | sdk.md |
| G-PI-SDK-049 | Session Management | SessionManager tree API: | sdk.md |
| G-PI-SDK-050 | Settings Management | Static factories: | sdk.md |
| G-PI-SDK-051 | Settings Management | `SettingsManager.create(cwd?, agentDir?)`  Load from files | sdk.md |
| G-PI-SDK-052 | Settings Management | `SettingsManager.inMemory(settings?)`  No file I/O | sdk.md |
| G-PI-SDK-053 | Settings Management | Projectspecific settings: | sdk.md |
| G-PI-SDK-054 | Settings Management | Persistence and error handling semantics: | sdk.md |
| G-PI-SDK-055 | Settings Management | Settings getters/setters are synchronous for inmemory state. | sdk.md |
| G-PI-SDK-056 | Settings Management | Setters enqueue persistence writes asynchronously. | sdk.md |
| G-PI-SDK-057 | Settings Management | Call `await settingsManager.flush()` when you need a durability boundary (for example, before process exit or before asserting file contents in tests). | sdk.md |
| G-PI-SDK-058 | Settings Management | `SettingsManager` does not print settings I/O errors. Use `settingsManager.drainErrors()` and report them in your app layer. | sdk.md |
| G-PI-SDK-059 | RPC Mode Alternative | You want type safety | sdk.md |
| G-PI-SDK-060 | RPC Mode Alternative | You're in the same Node.js process | sdk.md |
| G-PI-SDK-061 | RPC Mode Alternative | You need direct access to agent state | sdk.md |
| G-PI-SDK-062 | RPC Mode Alternative | You want to customize tools/extensions programmatically | sdk.md |
| G-PI-SDK-063 | RPC Mode Alternative | You're integrating from another language | sdk.md |
| G-PI-SDK-064 | RPC Mode Alternative | You want process isolation | sdk.md |
| G-PI-SDK-065 | RPC Mode Alternative | You're building a languageagnostic client | sdk.md |
| G-PI-SESSION-FORMAT-001 | Session Version | Version 1: Linear entry sequence (legacy, automigrated on load) | session-format.md |
| G-PI-SESSION-FORMAT-002 | Session Version | Version 2: Tree structure with `id`/`parentId` linking | session-format.md |
| G-PI-SESSION-FORMAT-003 | Session Version | Version 3: Renamed `hookMessage` role to `custom` (extensions unification) | session-format.md |
| G-PI-SESSION-FORMAT-004 | Source Files | [`packages/codingagent/src/core/sessionmanager.ts`](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/sessionmanager.ts)  Session entry types and SessionManager | session-format.md |
| G-PI-SESSION-FORMAT-005 | Source Files | [`packages/codingagent/src/core/messages.ts`](https://github.com/badlogic/pimono/blob/main/packages/codingagent/src/core/messages.ts)  Extended message types (BashExecutionMessage, CustomMessage, etc.) | session-format.md |
| G-PI-SESSION-FORMAT-006 | Source Files | [`packages/ai/src/types.ts`](https://github.com/badlogic/pimono/blob/main/packages/ai/src/types.ts)  Base message types (UserMessage, AssistantMessage, ToolResultMessage) | session-format.md |
| G-PI-SESSION-FORMAT-007 | Source Files | [`packages/agent/src/types.ts`](https://github.com/badlogic/pimono/blob/main/packages/agent/src/types.ts)  AgentMessage union type | session-format.md |
| G-PI-SESSION-FORMAT-008 | CompactionEntry | `details`: Implementationspecific data (e.g., `{ readFiles: string[], modifiedFiles: string[] }` for default, or custom data for extensions) | session-format.md |
| G-PI-SESSION-FORMAT-009 | CompactionEntry | `fromHook`: `true` if generated by an extension, `false`/`undefined` if pigenerated (legacy field name) | session-format.md |
| G-PI-SESSION-FORMAT-010 | BranchSummaryEntry | `details`: File tracking data (`{ readFiles: string[], modifiedFiles: string[] }`) for default, or custom data for extensions | session-format.md |
| G-PI-SESSION-FORMAT-011 | BranchSummaryEntry | `fromHook`: `true` if generated by an extension, `false`/`undefined` if pigenerated (legacy field name) | session-format.md |
| G-PI-SESSION-FORMAT-012 | CustomMessageEntry | `content`: String or `(TextContent | ImageContent)[]` (same as UserMessage) | session-format.md |
| G-PI-SESSION-FORMAT-013 | CustomMessageEntry | `display`: `true` = show in TUI with distinct styling, `false` = hidden | session-format.md |
| G-PI-SESSION-FORMAT-014 | CustomMessageEntry | `details`: Optional extensionspecific metadata (not sent to LLM) | session-format.md |
| G-PI-SESSION-FORMAT-015 | Tree Structure | First entry has `parentId: null` | session-format.md |
| G-PI-SESSION-FORMAT-016 | Tree Structure | Each subsequent entry points to its parent via `parentId` | session-format.md |
| G-PI-SESSION-FORMAT-017 | Tree Structure | Branching creates new children from an earlier entry | session-format.md |
| G-PI-SESSION-FORMAT-018 | Tree Structure | The "leaf" is the current position in the tree | session-format.md |
| G-PI-SESSION-FORMAT-019 | Context Building | Emits the summary first | session-format.md |
| G-PI-SESSION-FORMAT-020 | Context Building | Then messages from `firstKeptEntryId` to compaction | session-format.md |
| G-PI-SESSION-FORMAT-021 | Context Building | Then messages after compaction | session-format.md |
| G-PI-SESSION-FORMAT-022 | Static Creation Methods | `SessionManager.create(cwd, sessionDir?)`  New session | session-format.md |
| G-PI-SESSION-FORMAT-023 | Static Creation Methods | `SessionManager.open(path, sessionDir?)`  Open existing session file | session-format.md |
| G-PI-SESSION-FORMAT-024 | Static Creation Methods | `SessionManager.continueRecent(cwd, sessionDir?)`  Continue most recent or create new | session-format.md |
| G-PI-SESSION-FORMAT-025 | Static Creation Methods | `SessionManager.inMemory(cwd?)`  No file persistence | session-format.md |
| G-PI-SESSION-FORMAT-026 | Static Creation Methods | `SessionManager.forkFrom(sourcePath, targetCwd, sessionDir?)`  Fork session from another project | session-format.md |
| G-PI-SESSION-FORMAT-027 | Static Listing Methods | `SessionManager.list(cwd, sessionDir?, onProgress?)`  List sessions for a directory | session-format.md |
| G-PI-SESSION-FORMAT-028 | Static Listing Methods | `SessionManager.listAll(onProgress?)`  List all sessions across all projects | session-format.md |
| G-PI-SESSION-FORMAT-029 | Instance Methods - Session Management | `newSession(options?)`  Start a new session (options: `{ parentSession?: string }`) | session-format.md |
| G-PI-SESSION-FORMAT-030 | Instance Methods - Session Management | `setSessionFile(path)`  Switch to a different session file | session-format.md |
| G-PI-SESSION-FORMAT-031 | Instance Methods - Session Management | `createBranchedSession(leafId)`  Extract branch to new session file | session-format.md |
| G-PI-SESSION-FORMAT-032 | Instance Methods - Appending (all return entry ID) | `appendMessage(message)`  Add message | session-format.md |
| G-PI-SESSION-FORMAT-033 | Instance Methods - Appending (all return entry ID) | `appendThinkingLevelChange(level)`  Record thinking change | session-format.md |
| G-PI-SESSION-FORMAT-034 | Instance Methods - Appending (all return entry ID) | `appendModelChange(provider, modelId)`  Record model change | session-format.md |
| G-PI-SESSION-FORMAT-035 | Instance Methods - Appending (all return entry ID) | `appendCompaction(summary, firstKeptEntryId, tokensBefore, details?, fromHook?)`  Add compaction | session-format.md |
| G-PI-SESSION-FORMAT-036 | Instance Methods - Appending (all return entry ID) | `appendCustomEntry(customType, data?)`  Extension state (not in context) | session-format.md |
| G-PI-SESSION-FORMAT-037 | Instance Methods - Appending (all return entry ID) | `appendSessionInfo(name)`  Set session display name | session-format.md |
| G-PI-SESSION-FORMAT-038 | Instance Methods - Appending (all return entry ID) | `appendCustomMessageEntry(customType, content, display, details?)`  Extension message (in context) | session-format.md |
| G-PI-SESSION-FORMAT-039 | Instance Methods - Appending (all return entry ID) | `appendLabelChange(targetId, label)`  Set/clear label | session-format.md |
| G-PI-SESSION-FORMAT-040 | Instance Methods - Tree Navigation | `getLeafId()`  Current position | session-format.md |
| G-PI-SESSION-FORMAT-041 | Instance Methods - Tree Navigation | `getLeafEntry()`  Get current leaf entry | session-format.md |
| G-PI-SESSION-FORMAT-042 | Instance Methods - Tree Navigation | `getEntry(id)`  Get entry by ID | session-format.md |
| G-PI-SESSION-FORMAT-043 | Instance Methods - Tree Navigation | `getBranch(fromId?)`  Walk from entry to root | session-format.md |
| G-PI-SESSION-FORMAT-044 | Instance Methods - Tree Navigation | `getTree()`  Get full tree structure | session-format.md |
| G-PI-SESSION-FORMAT-045 | Instance Methods - Tree Navigation | `getChildren(parentId)`  Get direct children | session-format.md |
| G-PI-SESSION-FORMAT-046 | Instance Methods - Tree Navigation | `getLabel(id)`  Get label for entry | session-format.md |
| G-PI-SESSION-FORMAT-047 | Instance Methods - Tree Navigation | `branch(entryId)`  Move leaf to earlier entry | session-format.md |
| G-PI-SESSION-FORMAT-048 | Instance Methods - Tree Navigation | `resetLeaf()`  Reset leaf to null (before any entries) | session-format.md |
| G-PI-SESSION-FORMAT-049 | Instance Methods - Tree Navigation | `branchWithSummary(entryId, summary, details?, fromHook?)`  Branch with context summary | session-format.md |
| G-PI-SESSION-FORMAT-050 | Instance Methods - Context & Info | `buildSessionContext()`  Get messages, thinkingLevel, and model for LLM | session-format.md |
| G-PI-SESSION-FORMAT-051 | Instance Methods - Context & Info | `getEntries()`  All entries (excluding header) | session-format.md |
| G-PI-SESSION-FORMAT-052 | Instance Methods - Context & Info | `getHeader()`  Session header metadata | session-format.md |
| G-PI-SESSION-FORMAT-053 | Instance Methods - Context & Info | `getSessionName()`  Get display name from latest session_info entry | session-format.md |
| G-PI-SESSION-FORMAT-054 | Instance Methods - Context & Info | `getCwd()`  Working directory | session-format.md |
| G-PI-SESSION-FORMAT-055 | Instance Methods - Context & Info | `getSessionDir()`  Session storage directory | session-format.md |
| G-PI-SESSION-FORMAT-056 | Instance Methods - Context & Info | `getSessionId()`  Session UUID | session-format.md |
| G-PI-SESSION-FORMAT-057 | Instance Methods - Context & Info | `getSessionFile()`  Session file path (undefined for inmemory) | session-format.md |
| G-PI-SESSION-FORMAT-058 | Instance Methods - Context & Info | `isPersisted()`  Whether session is saved to disk | session-format.md |
| G-PI-SESSIONS-001 | Resuming and Deleting Sessions | search by typing | sessions.md |
| G-PI-SESSIONS-002 | Resuming and Deleting Sessions | toggle path display with Ctrl+P | sessions.md |
| G-PI-SESSIONS-003 | Resuming and Deleting Sessions | toggle sort mode with Ctrl+S | sessions.md |
| G-PI-SESSIONS-004 | Resuming and Deleting Sessions | filter to named sessions with Ctrl+N | sessions.md |
| G-PI-SESSIONS-005 | Resuming and Deleting Sessions | rename with Ctrl+R | sessions.md |
| G-PI-SESSIONS-006 | Resuming and Deleting Sessions | delete with Ctrl+D, then confirm | sessions.md |
| G-PI-SKILLS-001 | Table of Contents | [Locations](#locations) | skills.md |
| G-PI-SKILLS-002 | Table of Contents | [How Skills Work](#howskillswork) | skills.md |
| G-PI-SKILLS-003 | Table of Contents | [Skill Commands](#skillcommands) | skills.md |
| G-PI-SKILLS-004 | Table of Contents | [Skill Structure](#skillstructure) | skills.md |
| G-PI-SKILLS-005 | Table of Contents | [Frontmatter](#frontmatter) | skills.md |
| G-PI-SKILLS-006 | Table of Contents | [Validation](#validation) | skills.md |
| G-PI-SKILLS-007 | Table of Contents | [Example](#example) | skills.md |
| G-PI-SKILLS-008 | Table of Contents | [Skill Repositories](#skillrepositories) | skills.md |
| G-PI-SKILLS-009 | Locations | Global: | skills.md |
| G-PI-SKILLS-010 | Locations | `~/.pi/agent/skills/` | skills.md |
| G-PI-SKILLS-011 | Locations | `~/.agents/skills/` | skills.md |
| G-PI-SKILLS-012 | Locations | Project: | skills.md |
| G-PI-SKILLS-013 | Locations | `.pi/skills/` | skills.md |
| G-PI-SKILLS-014 | Locations | `.agents/skills/` in `cwd` and ancestor directories (up to git repo root, or filesystem root when not in a repo) | skills.md |
| G-PI-SKILLS-015 | Locations | Packages: `skills/` directories or `pi.skills` entries in `package.json` | skills.md |
| G-PI-SKILLS-016 | Locations | Settings: `skills` array with files or directories | skills.md |
| G-PI-SKILLS-017 | Locations | CLI: `skill <path>` (repeatable, additive even with `noskills`) | skills.md |
| G-PI-SKILLS-018 | Locations | In `~/.pi/agent/skills/` and `.pi/skills/`, direct root `.md` files are discovered as individual skills | skills.md |
| G-PI-SKILLS-019 | Locations | In all skill locations, directories containing `SKILL.md` are discovered recursively | skills.md |
| G-PI-SKILLS-020 | Locations | In `~/.agents/skills/` and project `.agents/skills/`, root `.md` files are ignored | skills.md |
| G-PI-SKILLS-021 | Name Rules | 164 characters | skills.md |
| G-PI-SKILLS-022 | Name Rules | Lowercase letters, numbers, hyphens only | skills.md |
| G-PI-SKILLS-023 | Name Rules | No leading/trailing hyphens | skills.md |
| G-PI-SKILLS-024 | Name Rules | No consecutive hyphens | skills.md |
| G-PI-SKILLS-025 | Name Rules | Must match parent directory name | skills.md |
| G-PI-SKILLS-026 | Validation | Name doesn't match parent directory | skills.md |
| G-PI-SKILLS-027 | Validation | Name exceeds 64 characters or contains invalid characters | skills.md |
| G-PI-SKILLS-028 | Validation | Name starts/ends with hyphen or has consecutive hyphens | skills.md |
| G-PI-SKILLS-029 | Validation | Description exceeds 1024 characters | skills.md |
| G-PI-SKILLS-030 | Validation | Exception: Skills with missing description are not loaded. | skills.md |
| G-PI-SKILLS-031 | Example | SKILL.md: | skills.md |
| G-PI-SKILLS-032 | Skill Repositories | [Anthropic Skills](https://github.com/anthropics/skills)  Document processing (docx, pdf, pptx, xlsx), web development | skills.md |
| G-PI-SKILLS-033 | Skill Repositories | [Pi Skills](https://github.com/badlogic/piskills)  Web search, browser automation, Google APIs, transcription | skills.md |
| G-PI-TERMINAL-SETUP-001 | VS Code (Integrated Terminal) | macOS: `~/Library/Application Support/Code/User/keybindings.json` | terminal-setup.md |
| G-PI-TERMINAL-SETUP-002 | VS Code (Integrated Terminal) | Linux: `~/.config/Code/User/keybindings.json` | terminal-setup.md |
| G-PI-TERMINAL-SETUP-003 | VS Code (Integrated Terminal) | Windows: `%APPDATA%\\Code\\User\\keybindings.json` | terminal-setup.md |
| G-PI-TERMINAL-SETUP-004 | Windows Terminal | `Shift+Enter` inserts a new line. | terminal-setup.md |
| G-PI-TERMINAL-SETUP-005 | Windows Terminal | Windows Terminal binds `Alt+Enter` to fullscreen by default. That prevents pi from receiving `Alt+Enter` for followup queueing. | terminal-setup.md |
| G-PI-TERMINAL-SETUP-006 | Windows Terminal | Remapping `Alt+Enter` to `sendInput` forwards the real key chord to pi instead. | terminal-setup.md |
| G-PI-TERMINAL-SETUP-007 | xfce4-terminal, terminator | [Kitty](https://sw.kovidgoyal.net/kitty/) | terminal-setup.md |
| G-PI-TERMINAL-SETUP-008 | xfce4-terminal, terminator | [Ghostty](https://ghostty.org/) | terminal-setup.md |
| G-PI-TERMINAL-SETUP-009 | xfce4-terminal, terminator | [WezTerm](https://wezfurlong.org/wezterm/) | terminal-setup.md |
| G-PI-TERMINAL-SETUP-010 | xfce4-terminal, terminator | [iTerm2](https://iterm2.com/) | terminal-setup.md |
| G-PI-TERMINAL-SETUP-011 | xfce4-terminal, terminator | [Alacritty](https://github.com/alacritty/alacritty) (requires compilation with Kitty protocol support) | terminal-setup.md |
| G-PI-TERMUX-001 | Location | OS: Android (Termux terminal emulator) | termux.md |
| G-PI-TERMUX-002 | Location | Home: `/data/data/com.termux/files/home` | termux.md |
| G-PI-TERMUX-003 | Location | Prefix: `/data/data/com.termux/files/usr` | termux.md |
| G-PI-TERMUX-004 | Location | Shared storage: `/storage/emulated/0` (Downloads, Documents, etc.) | termux.md |
| G-PI-TERMUX-005 | Notes | Termux:API app must be installed for `termux` commands | termux.md |
| G-PI-TERMUX-006 | Notes | Use `pkg install termuxapi` for the commandline tools | termux.md |
| G-PI-TERMUX-007 | Notes | Storage permission needed for `/storage/emulated/0` access | termux.md |
| G-PI-TERMUX-008 | Limitations | No image clipboard: Termux clipboard API only supports text | termux.md |
| G-PI-TERMUX-009 | Limitations | No native binaries: Some optional native dependencies (like the clipboard module) are unavailable on Android ARM64 and are skipped during installation | termux.md |
| G-PI-TERMUX-010 | Limitations | Storage access: To access files in `/storage/emulated/0` (Downloads, etc.), run `termuxsetupstorage` once to grant permissions | termux.md |
| G-PI-THEMES-001 | Table of Contents | [Locations](#locations) | themes.md |
| G-PI-THEMES-002 | Table of Contents | [Selecting a Theme](#selectingatheme) | themes.md |
| G-PI-THEMES-003 | Table of Contents | [Creating a Custom Theme](#creatingacustomtheme) | themes.md |
| G-PI-THEMES-004 | Table of Contents | [Theme Format](#themeformat) | themes.md |
| G-PI-THEMES-005 | Table of Contents | [Color Tokens](#colortokens) | themes.md |
| G-PI-THEMES-006 | Table of Contents | [Color Values](#colorvalues) | themes.md |
| G-PI-THEMES-007 | Table of Contents | [Tips](#tips) | themes.md |
| G-PI-THEMES-008 | Locations | Builtin: `dark`, `light` | themes.md |
| G-PI-THEMES-009 | Locations | Global: `~/.pi/agent/themes/.json` | themes.md |
| G-PI-THEMES-010 | Locations | Project: `.pi/themes/.json` | themes.md |
| G-PI-THEMES-011 | Locations | Packages: `themes/` directories or `pi.themes` entries in `package.json` | themes.md |
| G-PI-THEMES-012 | Locations | Settings: `themes` array with files or directories | themes.md |
| G-PI-THEMES-013 | Locations | CLI: `theme <path>` (repeatable) | themes.md |
| G-PI-THEMES-014 | Creating a Custom Theme | Hot reload: When you edit the currently active custom theme file, pi reloads it automatically for immediate visual feedback. | themes.md |
| G-PI-THEMES-015 | Theme Format | `name` is required and must be unique. | themes.md |
| G-PI-THEMES-016 | Theme Format | `vars` is optional. Define reusable colors here, then reference them in `colors`. | themes.md |
| G-PI-THEMES-017 | Theme Format | `colors` must define all 51 required tokens. | themes.md |
| G-PI-THEMES-018 | 256-Color Palette | `015`: Basic ANSI colors (terminaldependent) | themes.md |
| G-PI-THEMES-019 | 256-Color Palette | `16231`: 6×6×6 RGB cube (`16 + 36×R + 6×G + B` where R,G,B are 05) | themes.md |
| G-PI-THEMES-020 | 256-Color Palette | `232255`: Grayscale ramp | themes.md |
| G-PI-THEMES-021 | Tips | Dark terminals: Use bright, saturated colors with higher contrast. | themes.md |
| G-PI-THEMES-022 | Tips | Light terminals: Use darker, muted colors with lower contrast. | themes.md |
| G-PI-THEMES-023 | Tips | Color harmony: Start with a base palette (Nord, Gruvbox, Tokyo Night), define it in `vars`, and reference consistently. | themes.md |
| G-PI-THEMES-024 | Tips | Testing: Check your theme with different message types, tool states, markdown content, and long wrapped text. | themes.md |
| G-PI-THEMES-025 | Tips | VS Code: Set `terminal.integrated.minimumContrastRatio` to `1` for accurate colors. | themes.md |
| G-PI-THEMES-026 | Examples | [dark.json](../src/modes/interactive/theme/dark.json) | themes.md |
| G-PI-THEMES-027 | Examples | [light.json](../src/modes/interactive/theme/light.json) | themes.md |
| G-PI-TMUX-001 | Why `csi-u` Is Recommended | `Ctrl+C` → `\x1b[27;5;99~` | tmux.md |
| G-PI-TMUX-002 | Why `csi-u` Is Recommended | `Ctrl+D` → `\x1b[27;5;100~` | tmux.md |
| G-PI-TMUX-003 | Why `csi-u` Is Recommended | `Ctrl+Enter` → `\x1b[27;5;13~` | tmux.md |
| G-PI-TMUX-004 | Why `csi-u` Is Recommended | `Ctrl+C` → `\x1b[99;5u` | tmux.md |
| G-PI-TMUX-005 | Why `csi-u` Is Recommended | `Ctrl+D` → `\x1b[100;5u` | tmux.md |
| G-PI-TMUX-006 | Why `csi-u` Is Recommended | `Ctrl+Enter` → `\x1b[13;5u` | tmux.md |
| G-PI-TMUX-007 | Requirements | tmux 3.2 or later (run `tmux V` to check) | tmux.md |
| G-PI-TMUX-008 | Requirements | A terminal emulator that supports extended keys (Ghostty, Kitty, iTerm2, WezTerm, Windows Terminal) | tmux.md |
| G-PI-TUI-001 | TUI Components | Source: [`@mariozechner/pitui`](https://github.com/badlogic/pimono/tree/main/packages/tui) | tui.md |
| G-PI-TUI-002 | Using Components | In extensions via `ctx.ui.custom()`: | tui.md |
| G-PI-TUI-003 | Using Components | In custom tools via `pi.ui.custom()`: | tui.md |
| G-PI-TUI-004 | Keyboard Input | Key identifiers (use `Key.` for autocomplete, or string literals): | tui.md |
| G-PI-TUI-005 | Keyboard Input | Basic keys: `Key.enter`, `Key.escape`, `Key.tab`, `Key.space`, `Key.backspace`, `Key.delete`, `Key.home`, `Key.end` | tui.md |
| G-PI-TUI-006 | Keyboard Input | Arrow keys: `Key.up`, `Key.down`, `Key.left`, `Key.right` | tui.md |
| G-PI-TUI-007 | Keyboard Input | With modifiers: `Key.ctrl("c")`, `Key.shift("tab")`, `Key.alt("left")`, `Key.ctrlShift("p")` | tui.md |
| G-PI-TUI-008 | Keyboard Input | String format also works: `"enter"`, `"ctrl+c"`, `"shift+tab"`, `"ctrl+shift+p"` | tui.md |
| G-PI-TUI-009 | Line Width | Critical: Each line from `render()` must not exceed the `width` parameter. | tui.md |
| G-PI-TUI-010 | Line Width | `visibleWidth(str)`  Get display width (ignores ANSI codes) | tui.md |
| G-PI-TUI-011 | Line Width | `truncateToWidth(str, width, ellipsis?)`  Truncate with optional ellipsis | tui.md |
| G-PI-TUI-012 | Line Width | `wrapTextWithAnsi(str, width)`  Word wrap preserving ANSI codes | tui.md |
| G-PI-TUI-013 | Theming | In `renderCall`/`renderResult`, use the `theme` parameter: | tui.md |
| G-PI-TUI-014 | Theming | Foreground colors (`theme.fg(color, text)`): | tui.md |
| G-PI-TUI-015 | Theming | Background colors (`theme.bg(color, text)`): | tui.md |
| G-PI-TUI-016 | Theming | For Markdown, use `getMarkdownTheme()`: | tui.md |
| G-PI-TUI-017 | Theming | For custom components, define your own theme interface: | tui.md |
| G-PI-TUI-018 | The Problem | Wrong approach (theme colors won't update): | tui.md |
| G-PI-TUI-019 | Pattern 1: Selection Dialog (SelectList) | Examples: [preset.ts](../examples/extensions/preset.ts), [tools.ts](../examples/extensions/tools.ts) | tui.md |
| G-PI-TUI-020 | Pattern 2: Async Operation with Cancel (BorderedLoader) | Examples: [qna.ts](../examples/extensions/qna.ts), [handoff.ts](../examples/extensions/handoff.ts) | tui.md |
| G-PI-TUI-021 | Pattern 3: Settings/Toggles (SettingsList) | Examples: [tools.ts](../examples/extensions/tools.ts) | tui.md |
| G-PI-TUI-022 | Pattern 4: Persistent Status Indicator | Examples: [statusline.ts](../examples/extensions/statusline.ts), [planmode.ts](../examples/extensions/planmode.ts), [preset.ts](../examples/extensions/preset.ts) | tui.md |
| G-PI-TUI-023 | Pattern 4b: Working Indicator Customization | Examples: [workingindicator.ts](../examples/extensions/workingindicator.ts) | tui.md |
| G-PI-TUI-024 | Pattern 5: Widgets Above/Below Editor | Examples: [planmode.ts](../examples/extensions/planmode.ts) | tui.md |
| G-PI-TUI-025 | Pattern 6: Custom Footer | Examples: [customfooter.ts](../examples/extensions/customfooter.ts) | tui.md |
| G-PI-TUI-026 | Pattern 7: Custom Editor (vim mode, etc.) | Key points: | tui.md |
| G-PI-TUI-027 | Pattern 7: Custom Editor (vim mode, etc.) | Extend `CustomEditor` (not base `Editor`) to get app keybindings (escape to abort, ctrl+d to exit, model switching, etc.) | tui.md |
| G-PI-TUI-028 | Pattern 7: Custom Editor (vim mode, etc.) | Call `super.handleInput(data)` for keys you don't handle | tui.md |
| G-PI-TUI-029 | Pattern 7: Custom Editor (vim mode, etc.) | Factory pattern: `setEditorComponent` receives a factory function that gets `tui`, `theme`, and `keybindings` | tui.md |
| G-PI-TUI-030 | Pattern 7: Custom Editor (vim mode, etc.) | Pass `undefined` to restore the default editor: `ctx.ui.setEditorComponent(undefined)` | tui.md |
| G-PI-TUI-031 | Pattern 7: Custom Editor (vim mode, etc.) | Examples: [modaleditor.ts](../examples/extensions/modaleditor.ts) | tui.md |
| G-PI-TUI-032 | Examples | Selection UI: [examples/extensions/preset.ts](../examples/extensions/preset.ts)  SelectList with DynamicBorder framing | tui.md |
| G-PI-TUI-033 | Examples | Async with cancel: [examples/extensions/qna.ts](../examples/extensions/qna.ts)  BorderedLoader for LLM calls | tui.md |
| G-PI-TUI-034 | Examples | Settings toggles: [examples/extensions/tools.ts](../examples/extensions/tools.ts)  SettingsList for tool enable/disable | tui.md |
| G-PI-TUI-035 | Examples | Status indicators: [examples/extensions/planmode.ts](../examples/extensions/planmode.ts)  setStatus and setWidget | tui.md |
| G-PI-TUI-036 | Examples | Working indicator: [examples/extensions/workingindicator.ts](../examples/extensions/workingindicator.ts)  setWorkingIndicator | tui.md |
| G-PI-TUI-037 | Examples | Custom footer: [examples/extensions/customfooter.ts](../examples/extensions/customfooter.ts)  setFooter with stats | tui.md |
| G-PI-TUI-038 | Examples | Custom editor: [examples/extensions/modaleditor.ts](../examples/extensions/modaleditor.ts)  Vimlike modal editing | tui.md |
| G-PI-TUI-039 | Examples | Snake game: [examples/extensions/snake.ts](../examples/extensions/snake.ts)  Full game with keyboard input, game loop | tui.md |
| G-PI-TUI-040 | Examples | Custom tool rendering: [examples/extensions/todo.ts](../examples/extensions/todo.ts)  renderCall and renderResult | tui.md |
| G-PI-USAGE-001 | Interactive Mode | Startup header  shortcuts, loaded context files, prompt templates, skills, and extensions | usage.md |
| G-PI-USAGE-002 | Interactive Mode | Messages  user messages, assistant responses, tool calls, tool results, notifications, errors, and extension UI | usage.md |
| G-PI-USAGE-003 | Interactive Mode | Editor  where you type; border color indicates the current thinking level | usage.md |
| G-PI-USAGE-004 | Interactive Mode | Footer  working directory, session name, token/cache usage, cost, context usage, and current model | usage.md |
| G-PI-USAGE-005 | Message Queue | Enter queues a steering message, delivered after the current assistant turn finishes executing its tool calls. | usage.md |
| G-PI-USAGE-006 | Message Queue | Alt+Enter queues a followup message, delivered after the agent finishes all work. | usage.md |
| G-PI-USAGE-007 | Message Queue | Escape aborts and restores queued messages to the editor. | usage.md |
| G-PI-USAGE-008 | Message Queue | Alt+Up retrieves queued messages back to the editor. | usage.md |
| G-PI-USAGE-009 | Sessions | `/session` shows the current session file and ID. | usage.md |
| G-PI-USAGE-010 | Sessions | `/tree` navigates the infile session tree and can summarize abandoned branches. | usage.md |
| G-PI-USAGE-011 | Sessions | `/fork` creates a new session from an earlier user message. | usage.md |
| G-PI-USAGE-012 | Sessions | `/clone` duplicates the current active branch into a new session file. | usage.md |
| G-PI-USAGE-013 | Sessions | `/compact` summarizes older messages to free context. | usage.md |
| G-PI-USAGE-014 | Context Files | `~/.pi/agent/AGENTS.md` for global instructions | usage.md |
| G-PI-USAGE-015 | Context Files | parent directories, walking up from the current working directory | usage.md |
| G-PI-USAGE-016 | Context Files | the current directory | usage.md |
| G-PI-USAGE-017 | System Prompt Files | `.pi/SYSTEM.md` for a project | usage.md |
| G-PI-USAGE-018 | System Prompt Files | `~/.pi/agent/SYSTEM.md` globally | usage.md |
| G-PI-README-001 | [extensions/](extensions/) | Lifecycle event handlers (tool interception, safety gates, context modifications) | README.md |
| G-PI-README-002 | [extensions/](extensions/) | Custom tools (todo lists, questions, subagents, output truncation) | README.md |
| G-PI-README-003 | [extensions/](extensions/) | Commands and keyboard shortcuts | README.md |
| G-PI-README-004 | [extensions/](extensions/) | Custom UI (footers, headers, editors, overlays) | README.md |
| G-PI-README-005 | [extensions/](extensions/) | Git integration (checkpoints, autocommit) | README.md |
| G-PI-README-006 | [extensions/](extensions/) | System prompt modifications and custom compaction | README.md |
| G-PI-README-007 | [extensions/](extensions/) | External integrations (SSH, file watchers, system theme sync) | README.md |
| G-PI-README-008 | [extensions/](extensions/) | Custom providers (Anthropic with custom streaming, GitLab Duo) | README.md |
| G-PI-README-009 | Documentation | [SDK Reference](sdk/README.md) | README.md |
| G-PI-README-010 | Documentation | [Extensions Documentation](../docs/extensions.md) | README.md |
| G-PI-README-011 | Documentation | [Skills Documentation](../docs/skills.md) | README.md |
| G-PI-README-001 | Coding agent suite tests | Use `test/suite/harness.ts` | README.md |
| G-PI-README-002 | Coding agent suite tests | Use the faux provider from `packages/ai/src/providers/faux.ts` | README.md |
| G-PI-README-003 | Coding agent suite tests | Do not use real provider APIs, real API keys, network calls, or paid tokens | README.md |
| G-PI-README-004 | Coding agent suite tests | Keep these tests CIsafe and deterministic | README.md |
| G-PI-README-005 | Coding agent suite tests | Do not use or extend the legacy `test/testharness.ts` path unless a missing capability forces it | README.md |
| G-PI-README-006 | Coding agent suite tests | Put broad lifecycle and characterization tests directly under `test/suite/` | README.md |
| G-PI-README-007 | Coding agent suite tests | Put issuespecific regression tests under `test/suite/regressions/` | README.md |
| G-PI-README-008 | Coding agent suite tests | Name regression tests as `<issuenumber><shortslug>.test.ts` | README.md |
| G-PI-README-009 | Coding agent suite tests | Example: `test/suite/regressions/2023queuedslashcommandfollowup.test.ts` | README.md |
| G-PI-README-001 | Key Patterns | Use StringEnum for string parameters (required for Google API compatibility): | README.md |
| G-PI-README-002 | Key Patterns | State persistence via details: | README.md |
| G-PI-README-001 | How It Works | `width: "90%"`  90% of terminal width | README.md |
| G-PI-README-002 | How It Works | `maxHeight: "80%"`  Maximum 80% of terminal height | README.md |
| G-PI-README-003 | How It Works | `anchor: "center"`  Centered in terminal | README.md |
| G-PI-README-004 | Credits | [id Software](https://github.com/idSoftware/DOOM) for the original DOOM | README.md |
| G-PI-README-005 | Credits | [doomgeneric](https://github.com/ozkl/doomgeneric) for the portable DOOM implementation | README.md |
| G-PI-README-006 | Credits | [pidoom](https://github.com/badlogic/pidoom) for the original pi integration | README.md |
| G-PI-README-001 | Features | Readonly tools: Restricts available tools to read, bash, grep, find, ls, question | README.md |
| G-PI-README-002 | Features | Bash allowlist: Only readonly bash commands are allowed | README.md |
| G-PI-README-003 | Features | Plan extraction: Extracts numbered steps from `Plan:` sections | README.md |
| G-PI-README-004 | Features | Progress tracking: Widget shows completion status during execution | README.md |
| G-PI-README-005 | Features | [DONE:n] markers: Explicit step completion tracking | README.md |
| G-PI-README-006 | Features | Session persistence: State survives session resume | README.md |
| G-PI-README-007 | Commands | `/plan`  Toggle plan mode | README.md |
| G-PI-README-008 | Commands | `/todos`  Show current plan progress | README.md |
| G-PI-README-009 | Commands | `Ctrl+Alt+P`  Toggle plan mode (shortcut) | README.md |
| G-PI-README-010 | Plan Mode (Read-Only) | Only readonly tools available | README.md |
| G-PI-README-011 | Plan Mode (Read-Only) | Bash commands filtered through allowlist | README.md |
| G-PI-README-012 | Plan Mode (Read-Only) | Agent creates a plan without making changes | README.md |
| G-PI-README-013 | Execution Mode | Full tool access restored | README.md |
| G-PI-README-014 | Execution Mode | Agent executes steps in order | README.md |
| G-PI-README-015 | Execution Mode | `[DONE:n]` markers track completion | README.md |
| G-PI-README-016 | Execution Mode | Widget shows progress | README.md |
| G-PI-README-017 | Command Allowlist | File inspection: `cat`, `head`, `tail`, `less`, `more` | README.md |
| G-PI-README-018 | Command Allowlist | Search: `grep`, `find`, `rg`, `fd` | README.md |
| G-PI-README-019 | Command Allowlist | Directory: `ls`, `pwd`, `tree` | README.md |
| G-PI-README-020 | Command Allowlist | Git read: `git status`, `git log`, `git diff`, `git branch` | README.md |
| G-PI-README-021 | Command Allowlist | Package info: `npm list`, `npm outdated`, `yarn info` | README.md |
| G-PI-README-022 | Command Allowlist | System info: `uname`, `whoami`, `date`, `uptime` | README.md |
| G-PI-README-023 | Command Allowlist | File modification: `rm`, `mv`, `cp`, `mkdir`, `touch` | README.md |
| G-PI-README-024 | Command Allowlist | Git write: `git add`, `git commit`, `git push` | README.md |
| G-PI-README-025 | Command Allowlist | Package install: `npm install`, `yarn add`, `pip install` | README.md |
| G-PI-README-026 | Command Allowlist | System: `sudo`, `kill`, `reboot` | README.md |
| G-PI-README-027 | Command Allowlist | Editors: `vim`, `nano`, `code` | README.md |
| G-PI-README-001 | Features | Isolated context: Each subagent runs in a separate `pi` process | README.md |
| G-PI-README-002 | Features | Streaming output: See tool calls and progress as they happen | README.md |
| G-PI-README-003 | Features | Parallel streaming: All parallel tasks stream updates simultaneously | README.md |
| G-PI-README-004 | Features | Markdown rendering: Final output rendered with proper formatting (expanded view) | README.md |
| G-PI-README-005 | Features | Usage tracking: Shows turns, tokens, cost, and context usage per agent | README.md |
| G-PI-README-006 | Features | Abort support: Ctrl+C propagates to kill subagent processes | README.md |
| G-PI-README-007 | Security Model | Projectlocal agents (`.pi/agents/.md`) are repocontrolled prompts that can instruct the model to read files, run bash commands, etc. | README.md |
| G-PI-README-008 | Security Model | Default behavior: Only loads userlevel agents from `~/.pi/agent/agents`. | README.md |
| G-PI-README-009 | Output Display | Collapsed view (default): | README.md |
| G-PI-README-010 | Output Display | Status icon (✓/✗/⏳) and agent name | README.md |
| G-PI-README-011 | Output Display | Last 510 items (tool calls and text) | README.md |
| G-PI-README-012 | Output Display | Usage stats: `3 turns ↑input ↓output RcacheRead WcacheWrite $cost ctx:contextTokens model` | README.md |
| G-PI-README-013 | Output Display | Expanded view (Ctrl+O): | README.md |
| G-PI-README-014 | Output Display | Full task text | README.md |
| G-PI-README-015 | Output Display | All tool calls with formatted arguments | README.md |
| G-PI-README-016 | Output Display | Final output rendered as Markdown | README.md |
| G-PI-README-017 | Output Display | Pertask usage (for chain/parallel) | README.md |
| G-PI-README-018 | Output Display | Parallel mode streaming: | README.md |
| G-PI-README-019 | Output Display | Shows all tasks with live status (⏳ running, ✓ done, ✗ failed) | README.md |
| G-PI-README-020 | Output Display | Updates as each task makes progress | README.md |
| G-PI-README-021 | Output Display | Shows "2/3 done, 1 running" status | README.md |
| G-PI-README-022 | Output Display | Tool call formatting (mimics builtin tools): | README.md |
| G-PI-README-023 | Output Display | `$ command` for bash | README.md |
| G-PI-README-024 | Output Display | `read ~/path:110` for read | README.md |
| G-PI-README-025 | Output Display | `grep /pattern/ in ~/path` for grep | README.md |
| G-PI-README-026 | Agent Definitions | Locations: | README.md |
| G-PI-README-027 | Agent Definitions | `~/.pi/agent/agents/.md`  Userlevel (always loaded) | README.md |
| G-PI-README-028 | Agent Definitions | `.pi/agents/.md`  Projectlevel (only with `agentScope: "project"` or `"both"`) | README.md |
| G-PI-README-029 | Error Handling | Exit code != 0: Tool returns error with stderr/output | README.md |
| G-PI-README-030 | Error Handling | stopReason "error": LLM error propagated with error message | README.md |
| G-PI-README-031 | Error Handling | stopReason "aborted": User abort (Ctrl+C) kills subprocess, throws error | README.md |
| G-PI-README-032 | Error Handling | Chain mode: Stops at first failing step, reports which step failed | README.md |
| G-PI-README-033 | Limitations | Output truncated to last 10 items in collapsed view (expand to see all) | README.md |
| G-PI-README-034 | Limitations | Agents discovered fresh on each invocation (allows editing midsession) | README.md |
| G-PI-README-035 | Limitations | Parallel mode limited to 8 tasks, 4 concurrent | README.md |
| G-PI-PLANNER-001 | General | Context/findings from a scout agent | planner.md |
| G-PI-PLANNER-002 | General | Original query or requirements | planner.md |
| G-PI-PLANNER-003 | Files to Modify | `path/to/file.ts`  what changes | planner.md |
| G-PI-PLANNER-004 | Files to Modify | `path/to/other.ts`  what changes | planner.md |
| G-PI-PLANNER-005 | New Files (if any) | `path/to/new.ts`  purpose | planner.md |
| G-PI-REVIEWER-001 | Files Reviewed | `path/to/file.ts` (lines XY) | reviewer.md |
| G-PI-REVIEWER-002 | Critical (must fix) | `file.ts:42`  Issue description | reviewer.md |
| G-PI-REVIEWER-003 | Warnings (should fix) | `file.ts:100`  Issue description | reviewer.md |
| G-PI-REVIEWER-004 | Suggestions (consider) | `file.ts:150`  Improvement idea | reviewer.md |
| G-PI-SCOUT-001 | General | Quick: Targeted lookups, key files only | scout.md |
| G-PI-SCOUT-002 | General | Medium: Follow imports, read critical sections | scout.md |
| G-PI-SCOUT-003 | General | Thorough: Trace all dependencies, check tests/types | scout.md |
| G-PI-WORKER-001 | Files Changed | `path/to/file.ts`  what changed | worker.md |
| G-PI-WORKER-002 | Notes (if any) | Exact file paths changed | worker.md |
| G-PI-WORKER-003 | Notes (if any) | Key functions/types touched (short list) | worker.md |
| G-PI-CL-001 | Process | packages/ai/CHANGELOG.md | cl.md |
| G-PI-CL-002 | Process | packages/tui/CHANGELOG.md | cl.md |
| G-PI-CL-003 | Process | packages/codingagent/CHANGELOG.md | cl.md |
| G-PI-CL-004 | Process | Skip: changelog updates, doconly changes, release housekeeping | cl.md |
| G-PI-CL-005 | Process | Skip: changes to generated model catalogs (for example `packages/ai/src/models.generated.ts`) unless accompanied by an intentional productfacing change in nongenerated source/docs. | cl.md |
| G-PI-CL-006 | Process | Determine which package(s) the commit affects (use `git show <hash> stat`) | cl.md |
| G-PI-CL-007 | Process | Verify a changelog entry exists in the affected package(s) | cl.md |
| G-PI-CL-008 | Process | For external contributions (PRs), verify format: `Description ([#N](url) by [@user](url))` | cl.md |
| G-PI-CL-009 | Process | Insert a `### New Features` section at the start of `## [Unreleased]` in `packages/codingagent/CHANGELOG.md`. | cl.md |
| G-PI-CL-010 | Process | Propose the top new features to the user for confirmation before writing them. | cl.md |
| G-PI-CL-011 | Process | Link to relevant docs and sections whenever possible. | cl.md |
| G-PI-CL-012 | Process | List commits with missing entries | cl.md |
| G-PI-CL-013 | Process | List entries that need crosspackage duplication | cl.md |
| G-PI-CL-014 | Process | Add any missing entries directly | cl.md |
| G-PI-CL-015 | Changelog Format Reference | `### Breaking Changes`  API changes requiring migration | cl.md |
| G-PI-CL-016 | Changelog Format Reference | `### Added`  New features | cl.md |
| G-PI-CL-017 | Changelog Format Reference | `### Changed`  Changes to existing functionality | cl.md |
| G-PI-CL-018 | Changelog Format Reference | `### Fixed`  Bug fixes | cl.md |
| G-PI-CL-019 | Changelog Format Reference | `### Removed`  Removed features | cl.md |
| G-PI-CL-020 | Changelog Format Reference | Internal: `Fixed foo ([#123](https://github.com/badlogic/pimono/issues/123))` | cl.md |
| G-PI-CL-021 | Changelog Format Reference | External: `Added bar ([#456](https://github.com/badlogic/pimono/pull/456) by [@user](https://github.com/user))` | cl.md |
| G-PI-IS-001 | General | Ignore any root cause analysis in the issue (likely wrong) | is.md |
| G-PI-IS-002 | General | Read all related code files in full (no truncation) | is.md |
| G-PI-IS-003 | General | Trace the code path and identify the actual root cause | is.md |
| G-PI-IS-004 | General | Propose a fix | is.md |
| G-PI-IS-005 | General | Do not trust implementation proposals in the issue without verification | is.md |
| G-PI-IS-006 | General | Read all related code files in full (no truncation) | is.md |
| G-PI-IS-007 | General | Propose the most concise implementation approach | is.md |
| G-PI-IS-008 | General | List affected files and changes needed | is.md |
| G-PI-PR-001 | General | Entry uses correct section (`### Breaking Changes`, `### Added`, `### Fixed`, etc.) | pr.md |
| G-PI-PR-002 | General | External contributions include PR link and author: `Fixed foo ([#123](https://github.com/badlogic/pimono/pull/123) by [@user](https://github.com/user))` | pr.md |
| G-PI-PR-003 | General | Breaking changes are in `### Breaking Changes`, not just `### Fixed` | pr.md |
| G-PI-PR-004 | General | Good: solid choices or improvements | pr.md |
| G-PI-PR-005 | General | Bad: concrete issues, regressions, missing tests, or risks | pr.md |
| G-PI-PR-006 | General | Ugly: subtle or high impact problems | pr.md |
| G-PI-WR-001 | General | If the conversation already mentions a GitHub issue or PR, use that existing context. | wr.md |
| G-PI-WR-002 | General | If the work came from `/is` or `/pr`, assume the issue or PR context is already known from the conversation and from the analysis work already done. | wr.md |
| G-PI-WR-003 | General | If there is no GitHub issue or PR in the conversation history, treat this as nonGitHub work. | wr.md |
| G-PI-WR-004 | General | Never stage unrelated files. | wr.md |
| G-PI-WR-005 | General | Never use `git add .` or `git add A`. | wr.md |
| G-PI-WR-006 | General | Run required checks before committing if code changed. | wr.md |
| G-PI-WR-007 | General | Do not open a PR unless I explicitly ask. | wr.md |
| G-PI-WR-008 | General | If this is not GitHub issue or PR work, do not post a GitHub comment. | wr.md |
| G-PI-WR-009 | General | If a final issue or PR comment was already posted in this session, do not post another one unless I explicitly ask. | wr.md |
