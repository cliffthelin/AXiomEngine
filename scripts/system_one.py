#!/usr/bin/env python3
"""
AXIOMENGINE SYSTEM ONE DECISION LAYER

A small, self-hosted "System One" primitive set — Choice and Score — for
structured decisions that are currently either a hand-rolled heuristic or a
full free-text LLM call doing something much simpler than open-ended chat.
It is deliberately NOT a drop-in client for any third-party hosted decision
API: it runs entirely over AXiomEngine's own governed router
(`AXiomEngineClient.chat`), using the models already declared in
`model_registry` (see scripts/00_install_base.sh). No new external service,
package, or model weight is introduced.

Two primitives, matching the shape most "fast decision" call sites need:

  - choice(state, question, options) -> which option, with a calibrated-ish
    confidence distribution over all options.
  - score(state, question) -> a single 0..1 float for "how well does X match
    Y" style questions.

Both ask the model for strict JSON and degrade to a low-confidence uniform
answer (never an exception) if the model's output can't be parsed — callers
that gate on confidence can fall back to their existing heuristic or escalate
to a human, exactly like every other best-effort subsystem in this repo.
"""
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

from agent_lib import AXiomEngineClient

DEFAULT_MODEL = "qwen3.6:35b"  # same fast reasoning model Governor already uses


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model output")
    return json.loads(match.group(0))


class SystemOneClient(AXiomEngineClient):
    """Fast structured-decision primitives layered on the governed router."""

    def __init__(self, name: str = "SystemOne", session_id: str = "system_one_session"):
        super().__init__(name=name, session_id=session_id)

    def choice(self, state: str, question: str, options: List[str], model: str = DEFAULT_MODEL) -> Dict[str, Any]:
        """Classify `state` against `question` into exactly one of `options`.
        Returns {options, probabilities, best, confidence, degraded}."""
        prompt = (
            "You are a fast structured-decision engine, not a conversational assistant. "
            "Respond with ONLY a JSON object, no prose, no markdown fences.\n\n"
            f"CONTEXT: {state}\n"
            f"QUESTION: {question}\n"
            f"OPTIONS (in this exact order): {json.dumps(options)}\n\n"
            'Respond as: {"probabilities": [p0, p1, ...]} where each p aligns '
            "positionally with OPTIONS and the values sum to 1.0."
        )

        try:
            response = self.chat(prompt, model=model, tags=["system_one", "choice"], vram_mib=0)
            content = response["choices"][0]["message"]["content"]
            parsed = _extract_json(content)
            probs = [float(p) for p in parsed["probabilities"]]
            if len(probs) != len(options):
                raise ValueError("probability count does not match option count")
            total = sum(probs) or 1.0
            probs = [p / total for p in probs]
            best_idx = probs.index(max(probs))
            return {
                "options": options,
                "probabilities": probs,
                "best": options[best_idx],
                "confidence": probs[best_idx],
                "degraded": False,
            }
        except Exception as e:
            print(f"SystemOneClient.choice: degraded to uniform distribution ({e})")
            uniform = 1.0 / len(options)
            return {
                "options": options,
                "probabilities": [uniform] * len(options),
                "best": options[0],
                "confidence": uniform,
                "degraded": True,
            }

    def score(self, state: str, question: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
        """Score `state` against `question` on a 0..1 scale.
        Returns {score, degraded}."""
        prompt = (
            "You are a fast structured-decision engine, not a conversational assistant. "
            "Respond with ONLY a JSON object, no prose, no markdown fences.\n\n"
            f"CONTEXT: {state}\n"
            f"QUESTION: {question}\n\n"
            'Respond as: {"score": <float between 0.0 and 1.0>}'
        )

        try:
            response = self.chat(prompt, model=model, tags=["system_one", "score"], vram_mib=0)
            content = response["choices"][0]["message"]["content"]
            parsed = _extract_json(content)
            value = max(0.0, min(1.0, float(parsed["score"])))
            return {"score": value, "degraded": False}
        except Exception as e:
            print(f"SystemOneClient.score: degraded to neutral score ({e})")
            return {"score": 0.5, "degraded": True}


if __name__ == "__main__":
    client = SystemOneClient()
    result = client.choice(
        state="Governance rejection reason: 'no rule covers concurrent VRAM reservation caps for third-party extensions'",
        question="Is this rejection reason a governance coverage gap, or a violation of an existing rule?",
        options=["coverage_gap", "policy_violation"],
    )
    print(json.dumps(result, indent=2))
