# AXiomEngine: 100+ Atomic Feature & Capability List

Below is an exhaustive, atomic-level enumeration of 120 distinct features, capabilities, and functions currently present (or explicitly modeled) within the AXiomEngine ecosystem.

### PI (Personal Intelligence) & CLI Interactions
1. `PI.interact()`: Infinite CLI `while True:` loop capturing user keyboard input.
2. Direct raw chat delegation bypassing backend queues.
3. Keyword interception: `plan` command triggers Archon sub-routing.
4. Auto-tag injection: Injects `["personal", "delegation"]` contexts to `plan` commands.
5. Graceful shutdown handler trapping `KeyboardInterrupt`.
6. `user_prompt.py`: Utility for blocking user CLI input with timeouts.
7. Terminal-native formatting for PI agent responses.
8. `rich_tui.py`: Styled command-line chat application.
9. Interactive Markdown rendering within the terminal interface.
10. `TUI` custom color schemes for differing agent personas.

### Archon (Architect Agent) & Agent Daemons
11. `Archon.plan_task()`: Autonomous decomposition of high-level user delegation into atomic sub-tasks.
12. `agent_daemon.py`: Background daemon executing an infinite `while True:` listening loop.
13. `AgentDaemon.handle_task()`: Consumes `Stitch` envelopes targeted for specific agents.
14. Per-task dynamic model overriding (allows an agent to switch models mid-execution).
15. `think=True` detection: Enables Qwen/DeepSeek reasoning traces for complex tasks.
16. Async LLM execution bypassing the HTTP router for reduced latency.
17. Real-time metric calculation: Computes Token/Second throughput post-execution.
18. `SyncState` initialization per-task.
19. `task:{id}:status` Redis key updates (`running`, `completed`, `failed`).
20. `task:{id}:thinking` Redis key updates (storing pure reasoning traces separately).
21. Native error handling and traceback capture pushed to `task:{id}:error`.
22. `intent_mapper.py`: Analyzes incoming roadmap/specs to map required agents.
23. `generate_task_payloads()`: Formats JSON outputs into Stitch payloads.

### Ollama Integration & VGPU Manager (`ollama_controller.py`)
24. `OllamaController.is_alive()`: HTTP health check to `localhost:11434`.
25. `OllamaController.version()`: Parses the installed Ollama daemon version.
26. `OllamaController.list_models()`: Fetches all locally installed model tags.
27. `OllamaController.list_running()`: Queries VRAM for currently active/loaded models.
28. `OllamaController.show()`: Retrieves full metadata (parameters, license, system prompt).
29. `OllamaController.get_capabilities()`: Parses `['completion', 'vision', 'tools', 'thinking']`.
30. `OllamaController.get_context_length()`: Dynamically extracts max context window limits.
31. `OllamaController.pull()`: Streaming block download of external registry models.
32. `OllamaController.push()`: Pushes local modifications to registries.
33. `OllamaController.copy()`: Duplicates/aliases models locally.
34. `OllamaController.delete()`: Uninstalls models from disk.
35. `OllamaController.create()`: Compiles a new model dynamically from raw Modelfile content.
36. `OllamaController.load_model()`: Pre-loads models into VRAM without triggering generation.
37. `OllamaController.unload_model()`: Exploits `keep_alive=0` to force immediate VRAM eviction.
38. `OllamaController.switch_model()`: Atomic operation unloads Model A and loads Model B.
39. `OllamaController.ensure_model_loaded()`: Safety check preventing inference failures on unloaded models.
40. `OllamaController.chat()`: Standard multi-turn generation endpoint.
41. Streaming chunk generator yielding raw JSON dicts as they process.
42. `chat_simple()`: Helper stripping JSON envelopes and returning raw string responses.
43. `generate()`: Raw completion endpoint bypassing template logic.
44. `embed()`: High-performance vector embedding generation.
45. Context truncation flag (`truncate=True`) preventing OOM on massive documents.
46. `openai_chat()`: `/v1/chat/completions` compatibility bridge.
47. `get_vram_usage()`: Iterates loaded models to calculate exact total MiB usage.
48. `recommended_context()`: Mathematical scaling down of context limits based on VRAM thresholds (24GB vs 48GB).
49. `vgpu_manager.py`: Abstraction layer mapping hardware (`P40` vs `3070`).
50. `switch_mode.sh`: Hardware execution toggling script.

### MCP (Model Context Protocol) Bridge (`mcp_bridge.py`)
51. `MCPBridge.register_tool()`: Dynamic tool registration mechanism.
52. Automatic `inspect` parsing of Python function signatures.
53. Automatic translation of Python types (`int`, `str`, `list`) to JSON Schema (`integer`, `string`, `array`).
54. Extraction of Python docstrings to populate LLM tool `description` fields.
55. Dynamic generation of `required` parameter lists for strict parsing.
56. `MCPBridge.execute_tool()`: Safe wrapper around native python function execution.
57. Exception trapping during execution returning string-formatted stack traces to the LLM.
58. Daemon loop explicitly listening to `Stitch` for `mcp_bridge` targeted envelopes.
59. `action="get_schemas"` handler providing Archon the full JSON schema of available tools.
60. `action="execute"` handler parsing JSON arguments and invoking the tool.
61. Emitting `mcp_response` role objects back into the Valkey cache.
62. `read_workspace_file()`: Native registered tool for secure file reads.
63. Directory traversal security checks preventing reads outside the `Projects/` root.
64. `list_workspace_dir()`: Native tool for `ls` equivalent actions.
65. `get_system_time()`: Native tool for temporal context.

### API & Central Router (`router/main.py`)
66. Asynchronous Uvicorn/FastAPI server lifecycle management.
67. `asyncpg` connection pooling for Postgres connectivity.
68. `select_backend()`: Dynamic routing based on model names (e.g. `nemotron` -> Split GPU).
69. `prompt_hash()`: Cryptographic SHA256 hashing of JSON prompts for immutability.
70. `get_pdd_rules()`: Database query fetching active governance rules based on scope.
71. `inject_pdd_context()`: Prepending Postgres rule strings directly into the LLM system prompt.
72. `audit_log()`: SQL Insertion of invocation metadata (`tokens_in`, `tokens_out`, `latency`).
73. `GET /health`: Core infrastructure check (DB and Cache connectivity).
74. `GET /admin/audit`: Fetches the last 50 execution logs.
75. `GET /admin/test-results`: Deserializes JSON test outputs from Valkey.
76. `POST /admin/run-tests`: Subprocess spawner for integration harnesses.
77. `GET /admin/kg-stats`: Disk parser for `knowledge_graph.json` analytics.
78. `GET /admin/dashboard`: Serves the HTML Audit dashboard.
79. `GET /admin/settings`: Serves the HTML Configuration dashboard.
80. `GET /admin/proposals`: Fetches pending PDD modification requests.
81. `POST /admin/proposals/{pid}/{action}`: Dynamic SQL engine updating/deleting/inserting governance rules.
82. Dashboard Metric: Total Invocations calculator.
83. Dashboard Metric: Average Latency calculator.
84. Dashboard Metric: Token Burn Rate calculator.
85. Dashboard Interaction: Pure Vanilla JS Chart.js real-time line graphs.

### CLI, Valkey Cache, and Stitch Bus
86. `Stitch.client`: Valkey/Redis client instantiation.
87. `Stitch.send_task()`: JSON serialization and list-pushing (LPUSH) into queues.
88. `Stitch.get_task()`: Blocking list-pop (BRPOP) for task consumption.
89. `SyncState.set()`: Key-value caching for global state sync.
90. `ResponseStateCache`: In-memory LRU cache for minimizing redundant LLM queries.
91. `ResponseStateCache.prune_expired()`: Garbage collection of stale sessions.

### Security, Graph, and Extensibility Scripts
92. `workspace_sec_scan.py`: Regex-based scanner for `.env`, `AWS_KEY`, and secrets.
93. `git_worker.sh`: Automated bash script wrapping `git commit`.
94. `git_metadata.py`: Extracts exact AXiomEngine state to append to commit messages.
95. `knowledge_graph.py`: Manages an in-memory graph array of nodes and edges.
96. `KnowledgeGraph.add_node()`: Prevents duplicate entity insertion.
97. `KnowledgeGraph.populate_from_ast()`: Mass-ingests Python code structures into the graph.
98. `kg_pruner.py`: Analyzes edge weights and purges disconnected nodes.
99. `ast_indexer.py`: Uses Python's `ast` module to index functions, classes, and async methods.
100. `smart_fetch.py`: Translates natural language intent into precise AST lookups.
101. `search_context.py`: Compiles search results into token-optimized strings for prompt injection.
102. `behavior_monitor.py`: Daemon polling task outputs for deviations against strict rules.
103. `governor.py`: Drafts JSON proposals recommending new PDD rules based on failure analysis.
104. `propose_rule.py`: CLI wrapper for manually pushing PDD proposals into Postgres.
105. `sis_loop.py`: The Self-Improvement System loop constantly analyzing agent efficiency.
106. `archon_tester.py`: Integration harness validating end-to-end task flows.
107. `test_concurrency.py`: Load testing framework spawning simultaneous mock-agent requests.
108. `benchmark.py`: Pure latency and token-per-second measuring tool.
109. `full_system_test.py`: Top-level validation script wrapping all underlying testing suites.
110. `atlas_bridge.py`: Stub interface designed to map internal concepts to external APIs.
111. `keychain.py`: Secure local storage wrapper (`.agent_keychain.json`).
112. `settings_registry.py`: Centralized fallback dictionary for system configurations.
113. `00_install_base.sh`: System bootstrapper compiling ValKey, Postgres, and Python environments.
114. `01_start_router.sh`: Daemonizes the Uvicorn web server.
115. `02_index_context.py`: Embeds project data into vectors.
116. `03_heartbeat.py`: Health-check pinger validating agent daemon life.
117. `status.sh`: Shell wrapper querying systemctl for service states.
118. `qemu_launcher.sh`: Virtualization script for isolated agent execution environments.
119. `test_70b_load.sh`: Specialized script stress-testing Split GPU VRAM limits.
120. `toon.py`: Advanced object orienting / networking logic (in development).
