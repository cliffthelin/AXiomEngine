# Purpose and Scope

This document defines how prompts must be authored, chained, and executed through failure-resistant pipelines. 

### R-PDD-EXEC-001
Prompts as Versioned Artifacts Prompts that influence production behavior must be stored as Markdown, code-reviewed, versioned, and explicitly referenced. Ad-hoc chats are forbidden for production changes. 

### R-PDD-EXEC-002
Role-Separated Prompt Chaining Prompt chaining must never rely on implicit memory. Each prompt in a chain must be independently correct. Prompts must adopt strict, separate roles:
- Planning Prompts: Analyze problems and produce plans. Cannot modify code.
- Execution Prompts: Generate code using explicit scope and the plan. Must halt if intent is missing.
- Review Prompts: Evaluate output against intent for drift. Cannot introduce new behavior. 

### R-PDD-EXEC-003
Stop-the-Line Pipelines Pipelines must enforce strict gates. If a prompt omits required intent, expands its scope, or violates deterministic review criteria, the workflow must halt immediately. Outputs are only promoted deliberately.