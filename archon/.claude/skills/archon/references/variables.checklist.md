# Active ARCHON-REFERENCES Checklist: variables.md

- [ ] G-ARCHON-REFERENCES-VARIABLES-001: Command files (`.archon/commands/.md`) — all variables except `$nodeId.output` (Section: Where Variables Are Substituted)
- [ ] G-ARCHON-REFERENCES-VARIABLES-002: Inline `prompt:` fields — in DAG prompt nodes and loop node prompts (Section: Where Variables Are Substituted)
- [ ] G-ARCHON-REFERENCES-VARIABLES-003: `bash:` scripts in DAG nodes — `$nodeId.output` references are automatically shellquoted (singlequoted with `'` escaped) (Section: Where Variables Are Substituted)
- [ ] G-ARCHON-REFERENCES-VARIABLES-004: `script:` bodies in DAG nodes — same substitution as bash, but `$nodeId.output` values are NOT shellquoted. For TypeScript/bun scripts, assign directly (`const data = $nodeId.output;`) — JSON is valid JS expression syntax. Avoid `String.raw\`$nodeId.output\`` — it silently breaks when the output contains a backtick (common in AIgenerated markdown and `output_format` payloads). (Section: Where Variables Are Substituted)
