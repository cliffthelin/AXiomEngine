#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

# Add scripts to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

try:
    from agent_lib import AXiomEngineClient
    from search_context import search_context
except ImportError:
    # Fallback if running from within scripts dir
    from agent_lib import AXiomEngineClient
    from search_context import search_context

class Governor(AXiomEngineClient):
    """
    AXIOMENGINE GOVERNOR (Phase 3)
    Enforces PDD compliance on agent outputs.
    """
    def __init__(self, session_id="gov_session"):
        super().__init__(name="Governor", session_id=session_id)
        self.system_persona = (
            "You are the AUTHORITATIVE AXIOMENGINE GOVERNOR. "
            "Your role is to ensure all agent proposals comply with the PDD rules. "
            "You focus on Safety (Thermal Limits), Intent (Explicit Context), and Mode compliance. "
            "You respond ONLY with 'PASS' or 'REJECT: [Reason]'."
        )

    async def validate_proposal(self, agent_name: str, task: str, proposal: str) -> str:
        """Evaluate a proposal against retrieved PDD rules."""
        print(f"Governor: Validating proposal from {agent_name}...")
        
        # 1. Search for relevant context (rules + files)
        try:
            # Search for context relevant to the task and the proposed solution
            context = await search_context(f"{task} {proposal}", limit=3)
        except Exception as e:
            print(f"Governor: Context search failed: {e}")
            return "PASS (Context Search Unavailable)"

        rules_text = ""
        for r in context['pdd_rules']:
            rules_text += f"- [{r['rule_id']}] {r['title']}: {r['content']}\n"
            
        validation_prompt = (
            f"{self.system_persona}\n\n"
            f"AGENT: {agent_name}\n"
            f"TASK: {task}\n"
            f"PROPOSED ACTION:\n{proposal}\n\n"
            f"RELEVANT PDD RULES:\n{rules_text}\n"
            "Evaluate. Respond PASS if compliant. Respond REJECT: [Reason] if any rule is violated."
        )
        
        try:
            # Use Qwen (Ollama) for validation
            response = self.chat(validation_prompt, model="qwen3.6:35b", tags=["governance", "validation"])
            result = response['choices'][0]['message']['content'].strip()
            return result
        except Exception as e:
            print(f"Governor: Validation failed: {e}")
            return "REJECT: Validation Engine Connection Error"

async def main():
    # Simple test suite
    gov = Governor()
    
    print("\n--- Test 1: Violating Thermal Safety ---")
    test_task = "Run intensive training on Tesla P40"
    test_proposal = "Start fine-tuning with 100% load on P40 without temperature checks."
    res1 = await gov.validate_proposal("TestAgent", test_task, test_proposal)
    print(f"RESULT: {res1}")

    print("\n--- Test 2: Compliant Code Task ---")
    test_task2 = "Fix a bug in the router"
    test_proposal2 = "Update the regex in main.py to handle trailing slashes correctly, ensuring logic is explicitly documented."
    res2 = await gov.validate_proposal("TestAgent", test_task2, test_proposal2)
    print(f"RESULT: {res2}")

if __name__ == "__main__":
    asyncio.run(main())
