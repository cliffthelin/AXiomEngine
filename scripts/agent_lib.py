import json
import httpx
from typing import List, Dict, Any, Optional
try:
    from scripts.toon import TOON
except ImportError:
    try:
        from toon import TOON
    except ImportError:
        TOON = None
try:
    from scripts.vgpu_manager import VGPUManager
except ImportError:
    try:
        from vgpu_manager import VGPUManager
    except ImportError:
        VGPUManager = None

class AXiomEngineClient:
    """Base client for all AXiomEngine agents to interact with the PDD Router."""
    
    def __init__(self, 
                 name: str, 
                 router_url: str = "http://127.0.0.1:9001",
                 session_id: str = "default_session"):
        self.name = name
        self.router_url = router_url
        self.session_id = session_id
        self.client = httpx.Client(timeout=120.0)

    def chat(self, 
             prompt: str, 
             model: str = "nemotron", 
             tags: List[str] = None,
             stream: bool = False,
             vram_mib: int = 8192) -> Dict[str, Any]:
        """Send a prompt through the PDD-governed router."""
        mgr = VGPUManager() if VGPUManager else None
        reserved = False
        
        if mgr and vram_mib > 0:
            if not mgr.reserve(self.name, vram_mib):
                raise Exception(f"VGPU Reservation Failed: Not enough VRAM for {vram_mib}MiB")
            reserved = True
            
        try:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "tags": tags or [],
                "stream": stream
            }
            headers = {
                "X-Session-Id": self.session_id,
                "X-Agent-Name": self.name
            }
            
            response = self.client.post(
                f"{self.router_url}/v1/chat/completions",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        finally:
            if reserved and mgr:
                mgr.release(self.name)

    def get_audit(self, limit: int = 5):
        """Retrieve recent audit logs for this agent."""
        r = self.client.get(f"{self.router_url}/admin/audit?limit={limit}")
        return r.json()

    def switch_mode(self, mode: str):
        """Request a system mode switch (e.g. from 1 to 2)."""
        r = self.client.post(f"{self.router_url}/admin/mode/{mode}")
        return r.json()

try:
    from .agent_types import AgentMessage, AgentLoopEvent, AgentState, AgentLoopConfig, THINKING_BUDGETS
except ImportError:
    try:
        from agent_types import AgentMessage, AgentLoopEvent, AgentState, AgentLoopConfig, THINKING_BUDGETS
    except ImportError:
        from scripts.agent_types import AgentMessage, AgentLoopEvent, AgentState, AgentLoopConfig, THINKING_BUDGETS

class Agent:
    """
    High-level Agent class mirroring @mariozechner/pi-agent-core.
    Manages the agent loop, state, and queues.
    """
    def __init__(self, state: AgentState = None):
        self.state = state or AgentState()
        self.config = AgentLoopConfig()
        self.steering_queue = []
        self.follow_up_queue = []
        self._abort_signal = False

    def steer(self, message: AgentMessage):
        self.steering_queue.append(message)

    def follow_up(self, message: AgentMessage):
        self.follow_up_queue.append(message)

    async def prompt(self, text: str) -> AsyncGenerator[AgentLoopEvent, None]:
        from scripts.session_manager import SessionManager
        sm = SessionManager(self.state.session_id)
        user_msg = AgentMessage(role="user", content=text)
        sm.save_message(user_msg)
        
        self.config.steering_queue.append(text)
        async for event in self.agent_loop():
            yield event

    async def agent_loop(self):
        """
        The core async generator for the agent's operation.
        """
        from scripts.pi_ai import stream as ai_stream
        from jsonschema import validate, ValidationError
        from scripts.extension_manager import get_manager
        from scripts.session_manager import SessionManager
        sm = SessionManager(self.state.session_id)
        mgr = get_manager()
        
        self.state.is_streaming = True
        yield AgentLoopEvent(type="agent_start")
        await mgr.api.emit("agent_start", {}, {"state": self.state})
        
        while True:
            # Update state with latest branch
            self.state.messages = sm.get_active_branch()
            
            yield AgentLoopEvent(type="turn_start")
            await mgr.api.emit("turn_start", {}, {"state": self.state})
            
            # --- CHECK COMPACTION ---
            if self.config.compaction_enabled:
                total_tokens = sum(len(m.content) for m in self.state.messages) // 4
                if total_tokens > self.config.reserve_tokens:
                    yield AgentLoopEvent(type="system_status", content="Auto-compacting session...")
                    from scripts.compaction_manager import CompactionManager
                    from scripts.pi_ai import stream as ai_stream
                    cm = CompactionManager(ai_stream)
                    await cm.compact_session(self.state, self.state.model)
                    yield AgentLoopEvent(type="system_status", content="Session compacted.")

            # --- TRANSFORM CONTEXT ---
            # (Optional: call self.transform_context)
            
            # --- REAL LLM CALL VIA PI-AI ---
            assistant_msg = AgentMessage(role="assistant", content="")
            yield AgentLoopEvent(type="message_start", message=assistant_msg)
            
            context = {
                "systemPrompt": self.state.system_prompt,
                "messages": [m.dict() for m in self.state.messages],
                "tools": [t.dict() for t in self.state.tools]
            }
            
            async for ai_event in ai_stream(self.state.model, context, {"sessionId": self.state.session_id, "thinking": True}):
                if ai_event.type == "text_delta":
                    assistant_msg.content += ai_event.delta
                    yield AgentLoopEvent(type="message_update", delta=ai_event.delta)
                elif ai_event.type == "thinking_delta":
                    # Store thinking in metadata for handoffs
                    if "thinking" not in assistant_msg.metadata:
                        assistant_msg.metadata["thinking"] = ""
                    assistant_msg.metadata["thinking"] += ai_event.delta
                    yield AgentLoopEvent(type="thinking_update", thinking=ai_event.delta)
                elif ai_event.type == "toolcall_delta":
                    # Accumulate tool calls
                    if not assistant_msg.tool_calls: assistant_msg.tool_calls = []
                    for tc in ai_event.content:
                        # Simple merge logic for partial tool calls
                        idx = tc.get("index", 0)
                        while len(assistant_msg.tool_calls) <= idx:
                            assistant_msg.tool_calls.append({"id": "", "name": "", "arguments": ""})
                        
                        entry = assistant_msg.tool_calls[idx]
                        if "id" in tc: entry["id"] = tc["id"]
                        if "function" in tc:
                            if "name" in tc["function"]: entry["name"] = tc["function"]["name"]
                            if "arguments" in tc["function"]: entry["arguments"] += tc["function"]["arguments"]
                        
                        yield AgentLoopEvent(type="tool_execution_update", tool_call_id=entry["id"], delta=tc.get("function", {}).get("arguments", ""))

                elif ai_event.type == "error":
                    yield AgentLoopEvent(type="error", error=ai_event.content)
            
            yield AgentLoopEvent(type="message_end", message=assistant_msg)
            self.state.messages.append(assistant_msg)
            
            # --- TOOL EXECUTION ---
            if assistant_msg.tool_calls:
                for tc in assistant_msg.tool_calls:
                    tool_name = tc["name"]
                    tool_id = tc["id"]
                    
                    try:
                        args = json.loads(tc["arguments"])
                    except:
                        args = {}

                    yield AgentLoopEvent(type="tool_execution_start", tool_call_id=tool_id, tool_name=tool_name, args=args)
                    
                    # 1. Validate
                    tool_def = next((t for t in self.state.tools if t.name == tool_name), None)
                    if tool_def:
                        try:
                            validate(instance=args, schema=tool_def.parameters)
                        except ValidationError as e:
                            # Validation failed - return error to LLM
                            res_msg = AgentMessage(role="toolResult", content=f"Validation Error: {e.message}", tool_call_id=tool_id, metadata={"isError": True})
                            self.state.messages.append(res_msg)
                            continue

                    # 2. Before Hook
                    # (Simplified: check if tool exists in a registry)
                    
                    # 3. Execute
                    # (Simulation)
                    await asyncio.sleep(0.5)
                    result = f"Result of {tool_name}"
                    
                    yield AgentLoopEvent(type="tool_execution_end", tool_call_id=tool_id, result=result)
                    
                    # 4. After Hook & Store
                    res_msg = AgentMessage(role="toolResult", content=result, tool_call_id=tool_id)
                    self.state.messages.append(res_msg)
            
            yield AgentLoopEvent(type="turn_end")

            # --- CHECK QUEUES & TERMINATION ---
            if self.steering_queue:
                self.state.messages.extend(self.steering_queue)
                self.steering_queue = []
                continue
                
            if not assistant_msg.tool_calls and not self.follow_up_queue:
                break
                
            if self.follow_up_queue:
                self.state.messages.extend(self.follow_up_queue)
                self.follow_up_queue = []
                continue

        yield AgentLoopEvent(type="agent_end")
        self.state.is_streaming = False

class AsyncAXiomEngineClient:
    """Asynchronous client for AXiomEngine agents."""
    
    def __init__(self, 
                 name: str = "Agent", 
                 router_url: str = "http://127.0.0.1:9001",
                 session_id: str = "default_session"):
        self.name = name
        self.router_url = router_url
        self.session_id = session_id
        self.agent = Agent()

    async def chat(self, 
                 prompt: str, 
                 model: str = "nemotron", 
                 tags: List[str] = None,
                 stream: bool = False,
                 vram_mib: int = 8192) -> Dict[str, Any]:
        """Send a prompt through the PDD-governed router asynchronously."""
        # Legacy support for simple chat
        events = []
        async for event in self.agent.prompt(prompt):
            events.append(event)
        
        # Format back to OpenAI style for compatibility
        return {
            "choices": [{"message": {"content": self.agent.state.messages[-1].content}}]
        }

        mgr = VGPUManager() if VGPUManager else None
        reserved = False
        
        if mgr and vram_mib > 0:
            if not mgr.reserve(self.name, vram_mib):
                raise Exception(f"VGPU Reservation Failed: Not enough VRAM for {vram_mib}MiB")
            reserved = True
            
        try:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "tags": tags or [],
                "stream": stream
            }
            headers = {
                "X-Session-Id": self.session_id,
                "X-Agent-Name": self.name
            }
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.router_url}/v1/chat/completions",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
        finally:
            if reserved and mgr:
                mgr.release(self.name)
