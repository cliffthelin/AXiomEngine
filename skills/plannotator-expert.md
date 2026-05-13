---
name: plannotator-expert
description: Specialized instructions for performing visual plan reviews and annotations using the Plannotator tool. Use this skill when the user requests a visual feedback loop or when complex architectural changes need manual approval.
---

# Plannotator Expert Skill

When this skill is active, the agent should prioritize using the visual annotation interface for any multi-step plan.

## Instructions
1.  **Gating**: Always trigger `/plannotator-review` before executing a complex multi-file edit.
2.  **Context**: Use the `read` tool to extract context from the codebase and present it visually in the Plannotator UI.
3.  **Feedback**: Monitor for the `plan_created` event and wait for the `plan_approved` signal before proceeding.

## Shortcuts
- `/review`: Shortcut for `/plannotator-review`
- `/annotate`: Shortcut for `/plannotator-annotate`
