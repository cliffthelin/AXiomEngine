#!/usr/bin/env python3
import asyncio
from typing import List, Dict, Any, Optional, Callable, AsyncGenerator
from scripts.agent_lib import Agent as CoreAgentSession, AgentLoopEvent
from scripts.session_manager import SessionManager
from scripts.auth_manager import get_auth_manager
from scripts.pi_ai import registry

class AgentSession:
    def __init__(self, core_session: CoreAgentSession):
        self._core = core_session
        self.listeners: List[Callable[[AgentLoopEvent], None]] = []

    @property
    def state(self): return self._core.state
    
    @property
    def session_id(self): return self._core.state.session_id

    async def prompt(self, text: str) -> AsyncGenerator[AgentLoopEvent, None]:
        async for event in self._core.prompt(text):
            for l in self.listeners: l(event)
            yield event

    def subscribe(self, listener: Callable[[AgentLoopEvent], None]):
        self.listeners.append(listener)
        return lambda: self.listeners.remove(listener)

    async def set_model(self, provider: str, model_id: str):
        full_id = f"{provider}/{model_id}"
        self._core.state.model = full_id

    async def abort(self):
        self._core.state.is_streaming = False

class AgentSessionRuntime:
    def __init__(self, cwd: str = "."):
        self.cwd = cwd
        self.session: Optional[AgentSession] = None

    async def new_session(self):
        sm = SessionManager()
        from scripts.agent_lib import Agent as CoreSession
        core = CoreSession()
        core.state.session_id = sm.session_id
        self.session = AgentSession(core)
        return self.session

    async def continue_session(self):
        sm = SessionManager()
        sessions = sm.list_sessions()
        if sessions:
            from scripts.agent_lib import Agent as CoreSession
            core = CoreSession()
            core.state.session_id = sessions[0]["id"]
            self.session = AgentSession(core)
            return self.session
        return await self.new_session()

async def create_agent_session(options: Dict[str, Any] = None) -> AgentSession:
    runtime = AgentSessionRuntime()
    return await runtime.continue_session()
