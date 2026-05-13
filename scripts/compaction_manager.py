#!/usr/bin/env python3
import json
import uuid
from typing import List, Dict, Any, Tuple
from scripts.agent_types import AgentMessage, CompactionEntry, CompactionDetails, AgentState

class CompactionManager:
    def __init__(self, pi_ai_stream):
        self.ai_stream = pi_ai_stream

    def serialize_conversation(self, messages: List[AgentMessage]) -> str:
        """
        Serializes messages to the PI standard format for summarization.
        Truncates tool results to 2000 chars.
        """
        lines = []
        for m in messages:
            role_label = f"[{m.role.capitalize()}]"
            content = m.content
            
            # Truncate tool results
            if m.role == "toolResult" and len(content) > 2000:
                content = content[:2000] + f"\n... (truncated {len(content)-2000} chars)"
            
            # Add thinking if present
            thinking = m.metadata.get("thinking")
            if thinking:
                lines.append(f"[Assistant thinking]: {thinking}")
            
            # Add tool calls if present
            if m.tool_calls:
                tc_str = "; ".join([f"{tc['name']}({tc['arguments']})" for tc in m.tool_calls])
                lines.append(f"[Assistant tool calls]: {tc_str}")
                
            lines.append(f"{role_label}: {content}")
        
        return "\n".join(lines)

    async def generate_summary(self, model_id: str, conversation_text: str, previous_summary: str = None) -> str:
        """
        Calls the LLM to generate the structured PI summary.
        """
        from scripts.pi_ai import complete
        
        prompt = "Summarize the following coding session history into the PI structured format. "
        if previous_summary:
            prompt += f"Integrate this previous summary: \n{previous_summary}\n\n"
        
        prompt += f"Conversation to summarize:\n{conversation_text}"
        
        context = {
            "systemPrompt": "You are a session summarizer. Use the PI structured format (Goal, Constraints, Progress, Decisions, Next Steps, Critical Context).",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = await complete(model_id, context)
        return response["content"]

    def extract_file_ops(self, messages: List[AgentMessage]) -> Tuple[List[str], List[str]]:
        """
        Extracts read and modified files from tool calls.
        """
        read = set()
        mod = set()
        for m in messages:
            if m.tool_calls:
                for tc in m.tool_calls:
                    args = json.loads(tc["arguments"])
                    path = args.get("path")
                    if not path: continue
                    
                    if tc["name"] in ["read", "ls", "grep"]:
                        read.add(path)
                    elif tc["name"] in ["write", "edit", "patch", "sed"]:
                        mod.add(path)
        return list(read), list(mod)

    async def compact_session(self, state: AgentState, model_id: str, keep_recent: int = 20000) -> CompactionEntry:
        """
        Main compaction logic.
        """
        # 1. Find cut point (Simplified: assume 1 char = 0.25 tokens)
        total_len = sum(len(m.content) for m in state.messages)
        # For this demo, we'll just summarize the first half if context is "large"
        mid = len(state.messages) // 2
        messages_to_sum = state.messages[:mid]
        kept_messages = state.messages[mid:]
        
        conv_text = self.serialize_conversation(messages_to_sum)
        read, mod = self.extract_file_ops(messages_to_sum)
        
        summary = await self.generate_summary(model_id, conv_text)
        
        entry = CompactionEntry(
            id=str(uuid.uuid4()),
            parent_id="root", # Simplified
            summary=summary,
            first_kept_entry_id="entry_id_0", # Placeholder
            tokens_before=total_len // 4,
            details=CompactionDetails(read_files=read, modified_files=mod)
        )
        
        # Update state: Replace messages with summary entry + kept messages
        # Note: In real PI, the summary is an entry in the JSONL tree.
        # Here we'll just update the message list.
        summary_msg = AgentMessage(role="system", content=f"SESSION SUMMARY:\n{summary}")
        state.messages = [summary_msg] + kept_messages
        
        return entry
