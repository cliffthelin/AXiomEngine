# Purpose and Scope

This document defines the foundational operating model for Policy-Driven Development (PDD) and how AI context must be assembled in this repository. 

## Definitions
- Context Assembling: The dynamic process by which AI tools (like GitHub Copilot) gather signals to generate responses.
- Retrieval-Augmented Generation (RAG): AI searching the repository for relevant content based on similarity and explicit references, not directory structures. 

### R-PDD-CORE-001
AI Does Not Infer Intent AI tools do not reason about "intent" unless it is explicitly retrievable; they generate probabilistically based on the context they are given at that exact moment. 

### R-PDD-CORE-002
Folder Structure is Not Authority Folder structure (e.g., /docs or /rules) does not signal authority to an AI. From the AI's perspective, a folder name is just a string. Authority must be explicitly declared and retrieved, not inferred from placement. 

### R-PDD-CORE-003
The Developer is a Context Orchestrator Developers are responsible for explicitly shaping AI context. Governing Markdown must be kept open, or explicitly referenced in AI Policys to force retrieval and make omission reviewable. If intent is not retrieved, it does not exist to the AI. 

### R-PDD-CORE-004
Missing Intent Leads to Silent Failure Context loss is a system failure, not a human error. Without explicit intent, AI will produce output that is behaviorally plausible but prompt-incorrect (e.g., passing tests while removing historical constraints).