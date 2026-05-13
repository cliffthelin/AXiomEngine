// RULE-START: R-PDD-ATLAS-001
# R-PDD-ATLAS-001: AI Atlas Code Engineering
// RULE-END: R-PDD-ATLAS-001
## Purpose
Define governance for the multi-agent orchestration performed by `@wizdear/atlas-code`.

## Rules
1. **Orchestration Authority**: `Atlas Code` is authorized to manage the end-to-end engineering pipeline (Discovery to Review).
2. **Context Integrity**: All `Atlas Code` operations MUST use the AXiomEngine Router (`http://localhost:9001/v1`) for LLM inference to ensure PDD compliance and auditability.
3. **Sandbox Enforcement**: Code generated or executed by `Atlas Code` sub-agents MUST run within the AXiomEngine Sandbox (Phase 4).
4. **Human Review**: Critical implementation phases (Design and Review) SHOULD trigger a notification on the Governance Dashboard for human oversight.
5. **VGPU Quotas**: `Atlas Code` swarms share the `Swarm` VGPU quota managed by `vgpu_manager.py`.

## Configuration
- Endpoint: `http://localhost:9001/v1`
- Provider: `OpenAI-Compatible`
- Model: `nemotron` or `qwen3.6`
